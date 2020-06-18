# -*- coding: utf-8 -*-

__author__ = 'Astrid Sedal, Mikal Breiteig'
__email__ = 'astrised@nmbu.no, mibreite@nmbu.no'



from biosim.island import CreateIsland as Island
from biosim.landscape import Lowland, Highland, Desert, Water
from biosim.animals import Herbivore, Carnivore

import matplotlib.pyplot as plt
import numpy as np


class Visualization:

    density_heatmap = {'Herbivore': 200,
                       'Carnivore': 50}

    def __init__(self):

        self.steps = 0
        self.current_herbivore_data = []
        self.current_carnivore_data = []
        self.herbivore_list = [self.Island.num_animals_per_species['Herbivore']]
        self.carnivore_list = [self.Island.num_animals_per_species['Carnivore']]

        self.step = 0
        self.final_year =None

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

        self._txt_year = None
        self._ymax_animals = None
        self._cmax_animals = None
        self._changing_text = None
        self.linegraph_ax = None
        self.hist_specs = None
        self.plot_island_map = None

    def graphics_setup(self, rgb_map=None):
        if self._fig is None:
            self._fig = plt.figure(figsize=(16, 10))
            plt.axes('off')

        if self._fit_ax is None:
            self._fit_ax = self._fig.add_subplot(6, 3, 16)
            self._fit_ax.title_text('Histogram fitness')
            self._fit_axis = None

        if self._age_ax is None:
            self._age_ax = self._fig.add_subplot(6, 3, 17)
            self._age_ax.title.set_title('Histogram age')

        if self._weight_ax is None:
            self._weight_ax = self._fig.add_subplot(6, 3, 18)
            self._weight_ax.title.set_text('Histogram weight')

        # setting up heatmap
        if self._herb_heat_ax is None:
            self._herb_heat_ax = self._fig.add_axes([0.1, 0.28, 0.3, 0.3])
            self._herb_heat_ax.title.set_text('Heatmap: Herbivore distribution')
            self._herb_heat_ax.set_yticklabels([])
            self._herb_heat_ax.set_xticklabels([])

        if self._carn_heat_ax is None:
            self._carn_heat_ax = self._fig.add_axes([0.5, 0.28, 0.3, 0.3])
            self._carn_heat_ax.title.set_text('Heatmap: Carnivore distribution')
            self._carn_heat_ax.set_yticklabels([])
            self._carn_heat_ax.set_xticklabels([])

        #Island map
        if self._map is None:
            self._map = self._fig.add_axes([0.1, 0.65, 0.4, 0.3])
            self._map.title_set_title('Island map')
            self._map.set_yticklabels([])
            self._map.set_xticklabels([])

        #Line graphs
        if self._pop_ax is None:
            self._pop_ax = self._fig.add_axes([0.5, 0.65, 0.5, 0.3])
            if self._ymax_animals is not None:
                self._pop_ax.set_ylim(0, self._ymax_animals)

        #Year counter
        if self._txt_year is None:
            self._txt_year = self._fig.add_axes([0.5, 0.95, 0.05, 0.05])
            self._txt_year.axis('off')
            self._changing_text = self._txt_year.text(0.2, 0.5, 'Year:' + str(0),
                                                      fontdict={'weight': 'bold', 'size': 14})

        plt.pause(0.001)

    def update_graphics(self, distribution=None, num_species_dict=None):
        self.steps += 1
        self._changing_text.set_text('Year:' + str(self.steps))

        #heatmap update
        if self._cmax_animals is None:
            self._cmax_animals = self.density_heatmap
        if self._herb_heat_axis is None:
            self._herb_heat_axis = self._carn_heat_ax.imshow(distribution[0],
                                                             interpolation='nearest',
                                                             cmap='BuGn',
                                                             vmax=self._cmax_animals['Herbivore'])
            self._herb_heat_ax.figure.colorbar(self._herb_heat_axis, ax=self._herb_heat_ax,
                                               orientation='horizontal', fraction=0.07, pad=0.04)
        else:
            self._herb_heat_ax.set_data(distribution[0])
        if self._carn_heat_axis is None:
            self._carn_heat_axis = self._carn_heat_ax.imshow(distribution[1],
                                                             interpolation='nearest',
                                                             cmap='OrRd',
                                                             vmax=self._cmax_animals['Carnivores'])
            self._carn_heat_ax.figure.colorbar(self._carn_heat_axis, ax=self._carn_heat_ax,
                                               orientation='horizontal', fraction=0.07, pad=0.04)
        else:
            self._carn_heat_axis.set_data(distribution[1])

        #line graph plot update
        self.current_herbivore_data.append(self.herbivore_list)
        self.current_carnivore_data.append(self.carnivore_list)
        length = len(self.current_carnivore_data)
        x_value = list(np.arange(length))
        self.linegraph_ax.set_ylim(0, max(self.current_herbivore_data))

        self.linegraph_ax.title.set_text("# of animals by species")
        self.linegraph_ax.set_xlabel('years')
        self.linegraph_ax.set_ylabel('Number og species')

        self.linegraph_ax.plot(x_value, self.current_herbivore_data, '-', color='g', linewidth=0.5)
        self.linegraph_ax.plot(x_value, self.current_carnivore_data, '-', color='r', linewidth=0.5)

        plt.pause(0.0001)

    def update_histogram_fitness(self, fitness_list_herb=None, fitness_list_carn=None):

        if self.hist_specs is None:
            self._fit_ax.clear()
            self._fit_ax.hist(fitness_list_herb,
                              histtype="step", color="g",)
            self._fit_ax.hist(fitness_list_carn,
                              histtype="step", color="r",)
            self._fit_ax.title.set_text("Histogram of fitness")
        else:
            fit_bins = (int(self.hist_specs["fitness"]["max"] / self.hist_specs["fitness"]["delta"]))
            self._fit_ax.clear()
            self._fit_ax.hist(fitness_list_herb, bins=fit_bins,
                              histtype="step", color="g",
                              range=(0, self.hist_specs["fitness"]["max"]))
            self._fit_ax.hist(fitness_list_carn, bins=fit_bins,
                              histtype="step", color="r",
                              range=(0, self.hist_specs["fitness"]["max"]))
            self._fit_ax.title.set_text("Histogram of fitness")

    def update_histogram_age(self, age_list_herb=None, age_list_carn=None):
        if self.hist_specs is None:
            self._age_ax.clear()
            self._age_ax.hist(age_list_herb,
                              histtype="step", color="g")
            self._age_ax.hist(age_list_carn,
                              histtype="step", color="r")
            self._age_ax.title.set_text("Histogram of age")
        else:
            age_bins = (int(self.hist_specs["age"]["max"] / self.hist_specs["age"]["delta"]))
            self._age_ax.clear()
            self._age_ax.hist(age_list_herb, bins=age_bins,
                              histtype="step", color="g", range=(0, self.hist_specs["age"]["max"]))
            self._age_ax.hist(age_list_carn, bins=age_bins,
                              histtype="step", color="r", range=(0, self.hist_specs["age"]["max"]))
            self._age_ax.title.set_text("Histogram of age")

    def update_histogram_weight(self, weight_list_herb=None, weight_list_carn=None):
        if self.hist_specs is None:
            self._weight_ax.clear()
            self._weight_ax.hist(weight_list_herb,
                                 histtype="step", color="g")
            self._weight_ax.hist(weight_list_carn,
                                 histtype="step", color="r")
            self._weight_ax.title.set_text("Histogram of weight")
        else:
            weight_bins = (int(self.hist_specs["weight"]["max"] / self.hist_specs["weight"]["delta"]))
            self._weight_ax.clear()
            self._weight_ax.hist(weight_list_herb, bins=weight_bins,
                                 histtype="step", color="g",
                                 range=(0, self.hist_specs["weight"]["max"]))
            self._weight_ax.hist(weight_list_carn, bins=weight_bins,
                                 histtype="step", color="r",
                                 range=(0, self.hist_specs["weight"]["max"]))
            self._weight_ax.title.set_text("Histogram of weight")

