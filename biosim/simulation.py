# -*- coding: utf-8 -*-

__author__ = 'Astrid Sedal, Mikal Breiteig'
__email__ = 'astrised@nmbu.no, mibreite@nmbu.no'


from biosim.animals import Herbivore, Carnivore
from biosim import landscape as Landscape
from biosim.island import CreateIsland as island
from biosim.visualization import Visualization

import pandas as pd
import os
import subprocess
import random
import matplotlib.pyplot as plt
import numpy as np

_FFMPEG_BINARY = "ffmpeg"
_CONVERT_BINARY = "magick"

_DEFAULT_GRAPHICS_DIR = os.path.join("..", "data")
_DEFAULT_GRAPHICS_NAME = "dv"

_DEFAULT_MOVIE_FORMAT = "mp4"


class BioSim:
    def __init__(self,
                 island_map,
                 ini_pop,
                 seed,
                 ymax_animals=None,
                 cmax_animals=None,
                 hist_specs=None,
                 img_name=_DEFAULT_GRAPHICS_NAME,
                 img_fmt='png',
                 img_dir=None,
                 img_base=None
                 ):
        """
        Parameters
        ----------
        island_map: multilinestring specifying island geography
        ini_pop : List of dictionaries specifying initial population
        seed: Integer used as random number seed
        ymax_animals: Number specifying y-axis limit for graph showing animal numbers.
        cmax_animals: Dict specifying color- code limits for animal densities.
        hist_specs: Dict specifying settings in histogram
        img_name: Graphics name
        img_fmt: String wih fle type for figure, e.g. 'png'
        img_dir: path
        img_base: where to store pictures and make movies from
        """

        random.seed(seed)

        self._year = 0
        self._final_year = None

        self._step = 0
        self.hist_specs = hist_specs
        self.inserted_map = island_map
        self.island = island(island_map, ini_pop)

        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals

        if img_dir is not None:
            self.img_base = os.path.join(img_dir, img_name)
        else:
            self.img_base = None

        self.img_fmt = img_fmt
        self._img_ctr = 0

        self.visualization = Visualization()
        self.visualization.graphics_setup(kart_rgb=self.plot_island_map(island_map))

    def set_animal_parameters(self, species, params):
        """
        Sets parameter for animals
        Parameters
        ----------
        species: object
        params: dict

        Returns
        -------

        """
        if species == 'Herbivore':
            Herbivore.set_parameters(params)
        elif species == 'Carnviore':
            Carnivore.set_parameters(params)

    def set_landscape_parameters(self, landscape, params):
        if landscape == 'W':
            Landscape.Water.cell_parameter(params)
        elif landscape == 'D':
            Landscape.Desert.cell_parameter(params)
        if landscape == 'H':
            Landscape.Highland.cell_parameter(params)
        elif landscape == 'L':
            Landscape.Lowland.cell_parameter(params)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Simulates number of years using the simulate_one_year method from island.py
        Parameters
        ----------
        num_years: int
        vis_years: int
        img_years: int

        Returns
        -------
        """
        if img_years is None:
            img_years = vis_years

        self._final_year = self._year + num_years

        while self._year < self._final_year:
            self.island.simulate_one_year()

        # for year in range(num_years):

            if self._year % vis_years == 0:
                self.visualization._changing_text.set_text('Year:' + str(self._year))
                self.visualization.update_graphics(vis_years, self.create_population_heatmap(),
                                                   self.island.num_animals_per_species)
                self.visualization.update_histogram_fitness(self.island.fitness_list()[0],
                                                            self.island.fitness_list()[1],
                                                            self.hist_specs)
                self.visualization.update_histogram_age(self.island.age_list()[0],
                                                        self.island.age_list()[1],
                                                        self.hist_specs)
                self.visualization.update_histogram_weight(self.island.weight_list()[0],
                                                           self.island.weight_list()[1],
                                                           self.hist_specs)
            if self._year % img_years == 0:
                self.save_graphics()

            self._year += 1

    def add_population(self, population):
        """
        Adds population to Rossumøya.

        Parameters
        ----------
        population: dict
        """

        self.island.add_population(population)

    @property
    def year(self):
        return self.island.year

    @property
    def num_animals(self):
        return self.island.num_animals

    @property
    def num_animals_per_species(self):
        return self.island.num_animals_per_species

    @property
    def animal_distribution(self):
        dict_for_df = {'Row': [], 'Col': [], 'Herbivore': [], 'Carnivore': []}
        for pos, cell in self.island.map.items():
            row, col = pos
            dict_for_df['Row'].append(row)
            dict_for_df['Col'].append(col)
            dict_for_df['Herbivore'].append(cell.num_herbivores)
            dict_for_df['Carnivore'].append(cell.num_carnivores)
        df_sim = pd.DataFrame.from_dict(dict_for_df)
        return df_sim

    def length_of_map(self):
        """
        Finds the length and width of the map
        Returns
        -------
        lenx_map: int
        leny_map: int
        """

        lines = self.inserted_map.strip()
        lines = lines.split('\n')
        lenx_map = len(lines[0])
        leny_map = len(lines)
        return lenx_map, leny_map

    def plot_island_map(self, island_map):
        """
        Plots the map of Rossumøya.
        Parameters
        ----------
        island_map

        Returns
        -------
        kart_rgb
        """
        #
        # island_string = island_map
        # string_map = textwrap.dedent(island_string)
        # string_map.replace('\n', ' ')

        #                   R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        kart_rgb = [[rgb_value[column] for column in row]
                    for row in island_map.splitlines()]
        return kart_rgb

    def create_population_heatmap(self):
        """
        Uses DataFrame and return values to plot in the heatmaps.

        Returns
        -------
        herb_array : object
        carn_array : object
        """
        x_len, y_len = self.length_of_map()

        df = self.animal_distribution
        df.set_index(['Row', 'Col'], inplace=True)
        herb_array = np.asarray(df['Herbivore']).reshape(y_len, x_len)
        carn_array = np.asarray(df['Carnivore']).reshape(y_len, x_len)

        return herb_array, carn_array

    def make_movie(self, movie_fmt):
        """
        Method will create an mp4 or a gif from saved images.

        Parameters
        ----------
        movie_fmt
            Must have a ffmpeg
        """

        if self.img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt == "mp4":
            try:
                subprocess.check_call([_FFMPEG_BINARY,
                                       "-framerate", "5", "-i",
                                       "{}_%05d.png".format(self.img_base),
                                       "-y",
                                       "-profile:v", "baseline",
                                       "-level", "3.0",
                                       "-pix_fmt", "yuv420p",
                                       "{}.{}".format(self.img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError("ERROR: ffmpeg failed with: {)". format(err))
        elif movie_fmt == "gif":
            try:
                subprocess.check_call([_CONVERT_BINARY,
                                       "-delay", "1",
                                       "-loop", "0",
                                       "{}.{]".format(self.img_base),
                                       "{].{}".format(self.img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError("ERROR: converted failed with: {}".format(err))
        else:
            raise ValueError("Uknown movie format: " + movie_fmt)

    def save_graphics(self):
        """
        Method will save figure with given filename.

        """

        if self.img_base is None:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self.img_base,
                                                     num=self._img_ctr,
                                                     type=self.img_fmt))
        self._img_ctr += 1


