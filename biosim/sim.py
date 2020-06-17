# -*- coding: utf-8 -*-


from biosim import island as island
from biosim import landscape as Landscape
from biosim.animals import Animals, Herbivore, Carnivore
from biosim.visualization import Visualization

import os
import pandas as pd
import matplotlib.pyplot as plt
import textwrap
import random
import subprocess
import numpy as np

_FFMPEG_BINARY = "ffmpeg"
_CONVERT_BINARY = "magick"

_DEFAULT_GRAPHICS_DIR = os.path.join("..", "data")
_DEFAULT_GRAPHICS_NAME = "dv"

_DEFAULT_MOVIE_FORMAT = "mp4"


class BioSim:

    density_heatmap ={'Herbivore': 200,
                      'Carnivore': 50}

    def __init__(self,
                 island_map,
                 ini_pop,
                 seed,
                 hist_specs=None,
                 ymax_animals=None,
                 cmax_animals=None,
                 img_dir=None,
                 img_base=None,
                 img_name=_DEFAULT_GRAPHICS_NAME,
                 img_fmt='png'):

        random.seed(seed)

        self.last_year_simulated = 0
        self.island_map = island_map
        self.ini_pop = ini_pop
        self.hist_specs = hist_specs
        self.island = island.CreateIsland(geography_island_string=island_map,
                                          initial_population=ini_pop)
        self.object = self.island.make_map(geography_island_string=island_map)
        self.herbivore_list = [self.island.num_animals_per_species['Herbivore']]
        self.carnivore_list = [self.island.num_animals_per_species['Carnivore']]
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.hist_specs = hist_specs

        if img_dir is not None:
            self.img_base = os.path.join(img_dir, img_name)
        else:
            self.img_base = None

        self.img_fmt = img_fmt
        self._img_ctr = 0

        self.num_years = None

        self.herbivore_line = None
        self.carnivore_line = None

        self.grid = None  # Trenger?
        self._fig = None
        self._map = None
        self._map_axis = None
        self._pop_ax = None
        self._pop_axis = None
        self._herb_heat_ax = None
        self._herb_heat_axis = None
        self._carn_heat_ax = None
        self._carn_heat_axis = None

        self._fit_ax = None
        self._fit_axis = None
        self._age_ax = None
        self._age_axis = None
        self._weight_ax = None
        self._weight_axis = None


    def set_animal_parameters(self, species, params):
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
        if img_years is None:
            img_years = vis_years

        self.set_up_graphics()
        self.plot_island_map()
        self.num_years = num_years

        for _ in range(num_years):
            new_island_population = self.island.simulate_one_year()
            self.herbivore_list.append(new_island_population['Herbivore'])
            self.carnivore_list.append(new_island_population['Carnivore'])

            if self._age_axis is not None:
                self.up_hist(num_years)

            self._fig.suptitle(f"Year:{self.num_years}")

            if num_years % vis_years == 0:
                self.update_graphics()

            if num_years % img_years == 0:
                self.save_graphics()

            self.last_year_simulated += 1

    def add_population(self, population):
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

    def set_up_graphics(self):
        if self._fig is None:
            self._fig = plt.figure(figsize=(12, 6))
            self._fig.suptitle("Rossumøya", fontweight="bold")

        # if self._fit_ax is None:
        #     self.update_plot_hist(fit_list=self.fitness_list)

        if self._map is None:
            self.plot_island_map()
            self._map.set_title("Landscape of Rossumøya")

        if self._pop_ax is None:
            self._pop_ax = self._fig.add_subplot(4, 3, 3)
            if self.ymax_animals is not None:
                self._pop_ax.set_ylim(0, self.ymax_animals)

            self._pop_ax.set_title("Ecosystem on Rossumøya", y=0.98)

        if self._herb_heat_ax is None:
            self._herb_heat_ax = self._fig.add_subplot(3, 2, 3)
            self._herb_heat_ax.set_title("Herbivore movement on Rossumøya", y=0.98)

        if self._carn_heat_ax is None:
            self._carn_heat_ax = self._fig.add_subplot(3, 2, 4)

            self._carn_heat_ax.set_title("Carnivore movement on Rossumøya")

        if self._fit_axis is None:
            self._fit_ax = self._fig.add_subplot(4, 4, 14)

        if self._age_axis is None:
            self._age_ax = self._fig.add_subplot(4, 4, 15)

        if self._weight_axis is None:
            self._weight_ax = self._fig.add_subplot(4, 4, 16)



    def plot_island_map(self):

        island_string = self.island_map
        string_map = textwrap.dedent(island_string)
        string_map.replace('\n', ' ')

        #                   R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        kart_rgb = [[rgb_value[column] for column in row]
                    for row in string_map.splitlines()]

        self._map = self._fig.add_subplot(3, 2, 1)

        self._map.imshow(kart_rgb)
        self._map.set_xticks(np.arange(0, len(kart_rgb[0]), 2))  # sets the location
        self._map.set_xticklabels(np.arange(1, 1 + len(kart_rgb[0]), 2))  # sets the displayed txt
        self._map.set_yticks(np.arange(0, len(kart_rgb), 2))
        self._map.set_yticklabels(np.arange(1, 1 + len(kart_rgb), 2))

        axlg = self._fig.add_axes([0.03, 0.525, 0.05, 0.35])  # llx, lly, w, h
        axlg.axis('off')
        for ix, name in enumerate(('Water', 'Lowland',
                                   'Highland', 'Desert')):
            axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                         edgecolor='none',
                                         facecolor=rgb_value[name[0]]))
            axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

    def plot_population_graph(self):

        if self.carnivore_line is None:
            carn_line = self._pop_ax.plot(np.arange(0, self.num_years),
                                          np.full(self.num_years, np.nan))
            self.carnivore_line = carn_line[0]
        else:
            x_data, y_data = self.carnivore_line.get_data()
            xnew = np.arange(x_data[-1] + 1, self.num_years)
            ynew = np.full(xnew.shape, np.nan)
            self.carnivore_line.set_data(np.hstack((x_data, xnew)),
                                         np.hstack((y_data, ynew)))

        if self.herbivore_line is None:
            herb_line = self._pop_ax.plot(np.arange(0, self.num_years),
                                          np.full(self.num_years, np.nan))
            self.herbivore_line = herb_line[0]
        else:
            x_data, y_data = self.herbivore_line.get_data()
            xnew = np.arange(x_data[-1] + 1, self.num_years)
            ynew = np.full(xnew.shape, np.nan)
            self.herbivore_line.set_data(np.hstack((x_data, xnew)),
                                         np.hstack((y_data, ynew)))

        if self.herbivore_line is None:
            herb_line = self._pop_ax.plot(np.arange(0, self.num_years), np.full(self.num_years, np.nan))
            self.herbivore_line = herb_line[0]
        else:
            x_data, y_data = self.herbivore_line.get_data()
            xnew = np.arange(x_data[-1] + 1, self.num_years)
            ynew = np.full(xnew.shape, np.nan)
            self.herbivore_line.set_data((np.hstack((x_data, xnew)), np.hstack((y_data, ynew))))

        if self._pop_axis is None:
            self._pop_ax.plot([i for i in range(len(self.herbivore_list))],
                              self.herbivore_list, 'b-')
            self._pop_ax.plot([i for i in range(len(self.carnivore_list))],
                              self.carnivore_list, 'g-')
            self._pop_ax.legend(['Herbivores', 'Carnivores'], loc='upper left')

    def update_population_graph(self, population):
        # Bruker get_data først, deretter set_data'
        ydata = self.carnivore_line.get_data()
        ydata[self.num_years] = population
        self.carnivore_line.set_data(ydata)
        #self.carnivore_line.lege

        ydata = self.herbivore_line.get_data()
        ydata[self.num_years] = population
        self.carnivore_line.set_data(ydata)

    def update_heatmap(self):
        df = self.animal_distribution

        herbivore_array = df.pivot_table(columns='Col', index='Row', values='Herbivore')
        carnivore_array = df.pivot_table(columns='Col', index='Row', values='Carnivore')

        if self.cmax_animals is None:
            self.cmax_animals = self.density_heatmap

        if self._herb_heat_axis is not None:
            self._herb_heat_axis.set_data(herbivore_array)
        else:
            self._herb_heat_axis = self._herb_heat_ax.imshow(herbivore_array,
                                                             cmap='BuGn',
                                                             interpolation='nearest',
                                                             vmax=self.cmax_animals['Herbivore'])
            plt.colorbar(self._herb_heat_axis, ax=self._herb_heat_ax)



        if self._carn_heat_axis is None:
            self._carn_heat_axis = self._carn_heat_ax.imshow(carnivore_array,
                                                             cmap='OrRd',
                                                             interpolation='nearest',
                                                             vmax=self.cmax_animals['Carnivore'])
            plt.colorbar(self._carn_heat_axis, ax=self._carn_heat_ax)
        else:
            self._carn_heat_axis.set_data(carnivore_array)

    def up_hist(self, num_years):
        fit_bins = (int(self.hist_specs["fitness"]["max"]/self.hist_specs["fitness"]["delta"]))
        self._fit_ax.clear()
        self._fit_ax.hist(self.island.fitness_list()[0], bins=fit_bins,
                          histtype="step", color="g", range=(0,self.hist_specs["fitness"]["max"]))
        self._fit_ax.hist(self.island.fitness_list()[1], bins=fit_bins,
                          histtype="step", color="r", range=(0,self.hist_specs["fitness"]["max"]))
        self._fit_ax.title.set_text("Histogram of fitness")

        age_bins = (int(self.hist_specs["age"]["max"]/self.hist_specs["age"]["delta"]))
        self._age_ax.clear()

        self._age_ax.hist(self.island.age_list()[0], bins=age_bins,
                          histtype="step", color="g", range=(0, self.hist_specs["age"]["max"]))
        self._age_ax.hist(self.island.age_list()[1], bins=age_bins,
                          histtype="step", color="r", range=(0, self.hist_specs["age"]["max"]))
        self._age_ax.title.set_text("Histogram of age")

        weight_bins = (int(self.hist_specs["weight"]["max"] / self.hist_specs["weight"]["delta"]))
        self._weight_ax.clear()
        self._weight_ax.hist(self.island.weight_list()[0], bins=weight_bins,
                          histtype="step", color="g", range=(0, self.hist_specs["weight"]["max"]))
        self._weight_ax.hist(self.island.weight_list()[1], bins=weight_bins,
                          histtype="step", color="r", range=(0, self.hist_specs["weight"]["max"]))
        self._weight_ax.title.set_text("Histogram of weight")

        self._map.set_title(f"Year:{num_years}")





    def update_graphics(self):
        # fig = plt.figure()
        # ax = fig.add_subplot(1, 1, 1)
        # ax.set_xlim(0, n_steps)
        # ax.set_ylim(0, 1)
        # line = ax.plot(np.arrange(n_steps), np.full(n_steps, np.nan), 'b-'[0])

        self.plot_population_graph()
        self.update_heatmap()
        plt.pause(0.1)
        self._fig.suptitle("ÅR: {}".format(self.num_years))

    def save_graphics(self):
        if self.img_base is None:
            return

        plt.savefig(f"{self.img_base}_{self._img_ctr:05d}.{self.img_fmt}")
        self._img_ctr += 1

    def make_movie(self, movie_fmt):
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
                raise RuntimeError( "ERROR: ffmpeg failed with: {)". format(err))
        elif movie_fmt == "gif":
            try:
                subprocess.check_call([_CONVERT_BINARY,
                                       "-delay", "1",
                                       "-loop", "0",
                                       "{}.{]".format(self.img_base),
                                       "{].{}".format(self.img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError("ERROR: converted failed: " + movie_fmt)
        else:
            raise ValueError("Uknown movie format: " + movie_fmt)

if __name__ == '__main__':
    plt.ion()
    default_map = """WWWWWWWWWWWWWWWWWWWWW\nWWWWWWWWHWWWWLLLLLLLW\nWHHHHHLLLLWWLLLLLLLWW\nWHHHHHHHHHWWLLLLLLWWW\nWHHHHHLLLLLLLLLLLLWWW\nWHHHHHLLLDDLLLHLLLWWW\nWHHLLLLLDDDLLLHHHHWWW\nWWHHHHLLLDDLLLHWWWWWW\nWHHHLLLLLDDLLLLLLLWWW\nWHHHHLLLLDDLLLLWWWWWW\nWWHHHHLLLLLLLLWWWWWWW\nWWWHHHHLLLLLLLWWWWWWW\nWWWWWWWWWWWWWWWWWWWWW"""

    ini_herbs = [{'loc': (10, 10),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(150)]}]
    ini_carns = [{'loc': (10, 10),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(40)]}]

    sim = BioSim(island_map=default_map, ini_pop=ini_herbs,
                 seed=123456,
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                                'age': {'max': 60.0, 'delta': 2},
                                'weight': {'max': 60, 'delta': 2}},)

    sim.set_animal_parameters('Herbivore', {'zeta': 3.2, 'xi': 1.8})
    sim.set_animal_parameters('Carnivore', {'a_half': 70, 'phi_age': 0.5,
                                            'omega': 0.3, 'F': 65,
                                            'DeltaPhiMax': 9.})
    sim.set_landscape_parameters('L', {'f_max': 700})

    sim.simulate(num_years=100, vis_years=1, img_years=2000)
    sim.add_population(population=ini_carns)
    sim.simulate(num_years=300, vis_years=1, img_years=2000)
    sim.make_movie(movie_fmt="mp4")
