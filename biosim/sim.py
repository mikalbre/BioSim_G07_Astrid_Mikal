# -*- coding: utf-8 -*-

import random
import subprocess
import numpy as np
from biosim import island as island
from biosim import landscape as Landscape
from biosim import animals

import pandas as pd
import matplotlib.pyplot as plt


class BioSim:

    def __init__(self,
                 island_map,
                 ini_pop,
                 seed,
                 ymax_animals=None,
                 cmax_animals=None,
                 img_base=None,
                 img_fmt='png'):

        random.seed(seed)

        self.last_year_simulated = 0
        self.island_map = island_map
        self.ini_pop = ini_pop
        self.island = island.CreateIsland(geography_island_string=island_map,
                                          initial_population=ini_pop)
        self.herbivore_list = [self.island.num_animals_per_species['Herbivore']]
        self.carnivore_list = [self.island.num_animals_per_species['Carnivore']]
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals

        self.img_base = img_base
        self.img_fmt = img_fmt
        self._img_ctr = 0

        self._fig = None
        self._map_ax = None
        self._map_axis = None
        self._pop_ax = None
        self._pop_axis = None
        self._herb_heat_ax = None
        self._herb_heat_axis = None
        self._carn_heat_ax = None
        self._carn_heat_axis = None

    def set_animal_parameters(self, species, params):
        if species == 'Herbivore':
            animals.Herbivore.set_parameters(params)
        elif species == 'Carnviore':
            animals.Carnivore.set_parameters(params)

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

        for _ in range(num_years):
            new_island_population = self.island.simulate_one_year()
            self.herbivore_list.append(new_island_population['Herbivore'])
            self.carnivore_list.append(new_island_population['Carnivore'])

            if num_years % vis_years == 0:
                self.update_graphics()

            if num_years% img_years == 0:
                self.save_graphics()

            self.last_year_simulated += 1

    def add_population(self, population):
        self.island.add_population(population)

    @property
    def year(self):
        return self.last_year_simulated

    @property
    def num_animals(self):
        return self.herbivore_list[-1] + self.carnivore_list[-1]

    @property
    def num_animals_per_species(self):
        animal_dict = {'Herbivore': self.island.num_animals_per_species['Herbivore'],
                       'Carnivore': self.island.num_animals_per_species['Carnviore']}

        return animal_dict

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

    def make_movie(self, movie_fmt):
        pass

    def set_up_graphics(self):

        if self._fig is None:
            self._fig = plt.figure(figsize=(12, 6))

        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(2, 2, 1)
            self._map_axis = None

        if self._pop_ax is None:
            self._pop_ax = self._fig.add_subplot(2, 2, 2)
            if self.ymax_animals is not None:
                self._pop_ax.set_ylim(0, self.ymax_animals)

        if self._herb_heat_ax is None:
            self._herb_heat_ax = self._fig.add_subplot(2, 2, 3)

        if self._carn_heat_ax is None:
            self._carn_heat_ax = self._fig.add_subplot(2, 2, 4)

    def plot_island_map(self):
        kart = """WWW\nWLW\nWWW"""

        #                   R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        kart_rgb = [[rgb_value[column] for column in row]
                    for row in kart.splitlines()]

        fig = plt.figure()

        axim = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
        axim.imshow(kart_rgb)
        axim.set_xticks(range(len(kart_rgb[0])))
        axim.set_xticklabels(range(1, 1 + len(kart_rgb[0])))
        axim.set_yticks(range(len(kart_rgb)))
        axim.set_yticklabels(range(1, 1 + len(kart_rgb)))

        axlg = fig.add_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
        axlg.axis('off')
        for ix, name in enumerate(('Water', 'Lowland',
                                   'Highland', 'Desert')):
            axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                         edgecolor='none',
                                         facecolor=rgb_value[name[0]]))
            axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

    def plot_population_graph(self):
        if self._pop_axis is None:
            self._pop_ax.plot([i for i in range(len(self.herbivore_list))], self.herbivore_list, 'g-')
            self._pop_ax.plot([i for i in range(len(self.carnivore_list))], self.carnivore_list,
                              'b-')
            self._pop_ax.legend(['Herbivores', 'Carnivores'], loc='upper left')

            # p_ax.plot([i for i in range(len(self.herbivore_list))], self.herbivore_list, 'g-') np.arrange(nonenan

            # set_y
            # antall herbivores og carn
            # to linjer, herb og carn, get_y(data)

    def plot_heatmap(self):
        df = self.animal_distribution

        herbivore_array = df.pivot_table(columns='Col', index='Row', values='Herbivore')
        carnivore_array = df.pivot_table(columns='Col', index='Row', values='Carnivore')

        if self.cmax_animals is None:
            self.cmax_animals = 100

        if self._herb_heat_axis is None:
            self._herb_heat_axis = self._herb_heat_ax.imshow(herbivore_array,
                                                             cmap='BuGn',
                                                             interpolation='nearest',
                                                             vmax=self.cmax_animals)
            plt.colorbar(self._herb_heat_axis, ax=self._herb_heat_ax)
        else:
            self._herb_heat_axis.set_data(herbivore_array)

        if self._carn_heat_axis is None:
            self._carn_heat_axis = self._carn_heat_ax.imshow(carnivore_array,
                                                             cmap='OrRd',
                                                             interpolation='nearest',
                                                             vmax=self.cmax_animals)
            plt.colorbar(self._carn_heat_axis, ax=self._carn_heat_ax)
        else:
            self._carn_heat_axis.set_data(carnivore_array)

    def update_graphics(self):
        # fig = plt.figure()
        # ax = fig.add_subplot(1, 1, 1)
        # ax.set_xlim(0, n_steps)
        # ax.set_ylim(0, 1)
        # line = ax.plot(np.arrange(n_steps), np.full(n_steps, np.nan), 'b-'[0])

        self.plot_population_graph()
        self.plot_heatmap()
        plt.pause(0.001)

    def save_graphics(self):
        pass

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
                 )

    sim.set_animal_parameters('Herbivore', {'zeta': 3.2, 'xi': 1.8})
    sim.set_animal_parameters('Carnivore', {'a_half': 70, 'phi_age': 0.5,
                                            'omega': 0.3, 'F': 65,
                                            'DeltaPhiMax': 9.})
    sim.set_landscape_parameters('L', {'f_max': 700})
    # print(sim.heat_map_herbivore())
    sim.simulate(num_years=100, vis_years=1, img_years=2000)
    sim.add_population(population=ini_carns)
    sim.simulate(num_years=100, vis_years=1, img_years=2000)


