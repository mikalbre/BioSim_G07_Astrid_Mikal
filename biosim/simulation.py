# -*- coding: utf-8 -*-

import random
import subprocess
import numpy as np
from biosim import island as island
from biosim import landscape as Landscape
from biosim.animals import Animals, Herbivore, Carnivore

import pandas as pd
import matplotlib.pyplot as plt
import textwrap


class BioSim:

    density_heatmap ={'Herbivore': 200,
                      'Carnivore': 50}

    def __init__(self,
                 island_map,
                 ini_pop,
                 seed,
                 ymax_animals=None,
                 cmax_animals=None,
                 img_base=None,
                 img_fmt='png'):

        self.seed = seed
        # random.seed(seed)

        self.last_year_simulated = 0
        self.island_map = island_map
        self.ini_pop = ini_pop
        self.island = island.CreateIsland(geography_island_string=island_map,
                                          initial_population=ini_pop)
        self.object = self.island.make_map(geography_island_string=island_map)
        self.herbivore_list = [self.island.num_animals_per_species['Herbivore']]
        self.carnivore_list = [self.island.num_animals_per_species['Carnivore']]
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals

        self.img_base = img_base
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
        self.weight_ax = None
        self.weight_axis = None


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
        self.num_years = num_years  # ??

        for _ in range(num_years):
            random.seed(self.seed)
            new_island_population = self.island.simulate_one_year()
            self.herbivore_list.append(new_island_population['Herbivore'])
            self.carnivore_list.append(new_island_population['Carnivore'])

            if self._age_ax is not None:
                self.upda(num_years)

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

    def make_movie(self, movie_fmt):
        pass

    # @property
    # def fitness_list(self):
    #     herb_lt = [Animals.get_fitness() for cell in np.asarray(self.island.map.values()).flatten()
    #                for herbs in cell.present_herbivores]
    #     carn_lt = [Animals.phi for cell in np.asarray(self.object).flatten()
    #                for Animals in cell.num_carnivores]
    #     return {"Herbivore": herb_lt, {"Carnivore"}: carn_lt}
    #
    # @property
    # def age_list(self):
    #     herb_lt = [Animals.get_age() for cell in np.asarray(self.object).flatten()
    #                for Animals in cell.num_herbivores]
    #     carn_lt = [Animals.age for cell in np.asarray(self.object).flatten()
    #                for Animals in cell.num_carnivores]
    #     return {"Herbivore": herb_lt, {"Carnivore"}: carn_lt}
    #
    # @property
    # def weight_list(self):
    #     herb_lt = [Animals.get_weight() for cell in np.asarray(self.object).flatten()
    #                for Animals in cell.num_herbivores]
    #     carn_lt = [Animals.get_weight() for cell in np.asarray(self.object).flatten()
    #                for Animals in cell.num_carnivores]
    #     return {"Herbivore": herb_lt, {"Carnivore"}: carn_lt}

    # def update_plot_hist(self, fit_list=None):
    #     self._fit_ax = self._fig.add_subplot(6, 3, 16)
    #     self._fit_ax.title.set_text("Hist FIT")
    #     self._fit_ax.hist(self.fitness_list()["Herbivore"], bins=10, histtype="step")
    #
    # def update_hist(self):
    #     pass

    def set_up_graphics(self):
        if self._fig is None:
            self._fig = plt.figure(figsize=(16, 9))
            self._fig.suptitle("Rossumøya", fontweight="bold")

        # if self._fit_ax is None:
        #     self.update_plot_hist(fit_list=self.fitness_list)

        if self._map is None:  # MAP
            self.plot_island_map()
            self._map.set_title("Landscape of Rossumøya")

        if self._pop_ax is None:
            self._pop_ax = self._fig.add_subplot(3, 2, 2)
            if self.ymax_animals is not None:
                self._pop_ax.set_ylim(0, self.ymax_animals)

            self._pop_ax.set_title("Ecosystem on Rossumøya", y=0.98)

        if self._herb_heat_ax is None:
            self._herb_heat_ax = self._fig.add_subplot(3, 2, 3)
            self._herb_heat_ax.set_title("Herbivore movement on Rossumøya", y=0.98)

        if self._carn_heat_ax is None:
            self._carn_heat_ax = self._fig.add_subplot(3, 2, 4)

            self._carn_heat_ax.set_title("Carnivore movement on Rossumøya")

        # if self._fit_axis is None:
        #
        #     # self._fit_ax = Visualization.update_histogram_fitness()
        #     self._fit_ax.hist(self.island.fitness_list()[0], bins=10, histtype="step", color="g")
        #     self._fit_ax.hist(phi_list_carn, bins=10, histtype="step", color="r")
        #     self._fit_ax.title.set_text("Historgram of fitness")
        #     self._fit_ax = self._fig.add_subplot(3, 2, 5)


    def plot_island_map(self):
        #kart = """WWW\nWLW\nWWW"""
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

        #fig = plt.figure()
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
                              self.herbivore_list, 'g-')
            self._pop_ax.plot([i for i in range(len(self.carnivore_list))],
                              self.carnivore_list, 'r-')
            self._pop_ax.legend(['Herbivores', 'Carnivores'], loc='upper left')
        #else:

    def update_population_graph(self, population):
        # Bruker get_data først, deretter set_data'
        ydata = self.carnivore_line.get_data()
        ydata[self.num_years] = population
        self.carnivore_line.set_data(ydata)

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


    def update_graphics(self):
        # fig = plt.figure()
        # ax = fig.add_subplot(1, 1, 1)
        # ax.set_xlim(0, n_steps)
        # ax.set_ylim(0, 1)
        # line = ax.plot(np.arrange(n_steps), np.full(n_steps, np.nan), 'b-'[0])

        self.plot_population_graph()
        self.update_heatmap()
        plt.pause(0.1)

    def save_graphics(self):
        pass

if __name__ == '__main__':
    plt.ion()
    # default_map = """WWWWWWWWWWWWWWWWWWWWW\nWWWWWWWWHWWWWLLLLLLLW\nWHHHHHLLLLWWLLLLLLLWW\nWHHHHHHHHHWWLLLLLLWWW\nWHHHHHLLLLLLLLLLLLWWW\nWHHHHHLLLDDLLLHLLLWWW\nWHHLLLLLDDDLLLHHHHWWW\nWWHHHHLLLDDLLLHWWWWWW\nWHHHLLLLLDDLLLLLLLWWW\nWHHHHLLLLDDLLLLWWWWWW\nWWHHHHLLLLLLLLWWWWWWW\nWWWHHHHLLLLLLLWWWWWWW\nWWWWWWWWWWWWWWWWWWWWW"""
    default_map = """WWWWWWWWWW\nWDDDDDDDDW\nWDDDDDDDDW\nWDDDDDDDDW\nWDDDDDDDDW\nWDDDDDDDDW\nWDDDDDDDDW\nWDDDDDDDDW\nWDDDDDDDDW\nWWWWWWWWWW"""
    ini_herbs = [{'loc': (5, 5),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 50}
                          for _ in range(1000)]}]
    ini_carns = [{'loc': (5, 5),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 50}
                          for _ in range(1000)]}]

    sim = BioSim(island_map=default_map, ini_pop=ini_herbs,
                 seed=12345,
                 )

    sim.set_animal_parameters('Herbivore', {'mu':  1, 'omega': 0, "gamma": 0, "a_half": 1000})
    sim.set_animal_parameters('Carnivore', {'a_half': 1000, 'gamma': 0,
                                            'omega': 0, 'F': 0, "mu": 0})
    sim.set_landscape_parameters('L', {'f_max': 700})
    # print(sim.heat_map_herbivore())
    sim.simulate(num_years=100, vis_years=1, img_years=2000)
    sim.add_population(population=ini_carns)
    sim.simulate(num_years=300, vis_years=1, img_years=2000)


