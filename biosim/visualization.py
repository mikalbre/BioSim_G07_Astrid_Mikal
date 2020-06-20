# -*- coding: utf-8 -*-

__author__ = 'Astrid Sedal, Mikal Breiteig'
__email__ = 'astrised@nmbu.no, mibreite@nmbu.no'


import matplotlib.pyplot as plt
import numpy as np


class Visualization:

    density_heatmap = {'Herbivores': 200,
                       'Carnivores': 50}

    def __init__(self):
        """

        """

        self.steps = 0
        self.current_herbivore_data = []
        self.current_carnivore_data = []

        self.step = 0
        self.final_year = None

        self.herbivore_line = None
        self.carnivore_line = None

        self.grid = None
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

    def graphics_setup(self, kart_rgb=None):
        if self._fig is None:
            self._fig = plt.figure(figsize=(16, 10))
            plt.axis('off')

        if self._fit_ax is None:
            self._fit_ax = self._fig.add_subplot(6, 3, 16)
            self._fit_ax.title.set_text('Histogram fitness')
            self._fit_axis = None

        if self._age_ax is None:
            self._age_ax = self._fig.add_subplot(6, 3, 17)
            self._age_ax.title.set_text('Histogram age')

        if self._weight_ax is None:
            self._weight_ax = self._fig.add_subplot(6, 3, 18)
            self._weight_ax.title.set_text('Histogram weight')

        if self._herb_heat_ax is None:
            self._herb_heat_ax = self._fig.add_axes([0.1, 0.28, 0.3, 0.3])
            self._herb_heat_ax.title.set_text('Herbivore distribution')
            self._herb_heat_ax.set_yticklabels([])
            self._herb_heat_ax.set_xticklabels([])

        if self._carn_heat_ax is None:
            self._carn_heat_ax = self._fig.add_axes([0.5, 0.28, 0.3, 0.3])
            self._carn_heat_ax.title.set_text('Carnivore distribution')
            self._carn_heat_ax.set_yticklabels([])
            self._carn_heat_ax.set_xticklabels([])

        if self._map is None:
            self._map = self._fig.add_axes([0.1, 0.65, 0.4, 0.3])
            self._map.title.set_text('Rossumøya')
            self._map.set_yticklabels([])
            self._map.set_xticklabels([])

            self._map.imshow(kart_rgb)
            self._map.set_xticks(
                np.arange(0, len(kart_rgb[0]), 2))  # sets the location
            self._map.set_xticklabels(
                np.arange(1, 1 + len(kart_rgb[0]), 2))  # sets the displayed txt
            self._map.set_yticks(np.arange(0, len(kart_rgb), 2))
            self._map.set_yticklabels(np.arange(1, 1 + len(kart_rgb), 2))

            #                   R    G    B
            rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                         'L': (0.0, 0.6, 0.0),  # dark green
                         'H': (0.5, 1.0, 0.5),  # light green
                         'D': (1.0, 1.0, 0.5)}  # light yellow

            axlg = self._fig.add_axes(
                [0.03, 0.662, 0.05, 0.35])  # llx, lly, w, h
            axlg.axis('off')
            for ix, name in enumerate(('Water', 'Lowland', 'Highland', 'Desert')):
                axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                             edgecolor='none',
                                             facecolor=rgb_value[name[0]]))
                axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

        if self._pop_ax is None:
            self._pop_ax = self._fig.add_axes([0.5, 0.65, 0.4, 0.3])
            if self._ymax_animals is not None:
                self._pop_ax.set_ylim(0, self._ymax_animals)

        if self._txt_year is None:
            self._txt_year = self._fig.add_axes([0.5, 0.95, 0.05, 0.05])
            self._txt_year.axis('off')
            self._changing_text = self._txt_year.text(0.2, 0.5, 'Year:' + str(0),
                                                      fontdict={'weight': 'bold', 'size': 15})

        plt.pause(0.001)

    def update_graphics(self, years, distribution=None, num_species_dict=None):
        self.steps += 1
        self._changing_text.set_text('Year:' + str(self.steps))

        if self._cmax_animals is None:
            self._cmax_animals = self.density_heatmap
        if self._herb_heat_axis is None:
            self._herb_heat_axis = self._herb_heat_ax.imshow(distribution[0],
                                                             interpolation='nearest',
                                                             cmap='BuGn',
                                                             vmax=self._cmax_animals['Herbivores'])
            self._herb_heat_ax.figure.colorbar(self._herb_heat_axis, ax=self._herb_heat_ax,
                                               orientation='horizontal', fraction=0.07, pad=0.04)
        else:
            self._herb_heat_axis.set_data(distribution[0])
        if self._carn_heat_axis is None:
            self._carn_heat_axis = self._carn_heat_ax.imshow(distribution[1],
                                                             interpolation='nearest',
                                                             cmap='OrRd',
                                                             vmax=self._cmax_animals['Carnivores'])
            self._carn_heat_ax.figure.colorbar(self._carn_heat_axis, ax=self._carn_heat_ax,
                                               orientation='horizontal', fraction=0.07, pad=0.04)
        else:
            self._carn_heat_axis.set_data(distribution[1])

        self.current_herbivore_data.append(num_species_dict["Herbivore"])
        self.current_carnivore_data.append(num_species_dict["Carnivore"])
        length = len(self.current_carnivore_data)
        x_value = list(np.arange(length))

        if self._pop_ax is not None:
            x_val = []
            for val in x_value:
                x_val.append(val * years)
            self._pop_ax.set_ylim(0, max(self.current_herbivore_data)+10)

            self._pop_ax.title.set_text("Number of animals by species")
            self._pop_ax.set_xlabel('Years')
            self._pop_ax.set_ylabel('Number of each species')

            self._pop_ax.plot(x_val, self.current_herbivore_data,
                                   '-', color='g', linewidth=0.5)
            self._pop_ax.plot(x_val, self.current_carnivore_data,
                                   '-', color='r', linewidth=0.5)

        plt.pause(0.01)

    def update_histogram_fitness(self, fitness_list_herb=None, fitness_list_carn=None,
                                 hist_specs=None):

        if hist_specs is None:
            self._fit_ax.clear()
            self._fit_ax.hist(fitness_list_herb,
                              histtype="step", color="g",)
            self._fit_ax.hist(fitness_list_carn,
                              histtype="step", color="r",)
            self._fit_ax.title.set_text("Histogram of fitness")
        else:
            fit_bins = (int(hist_specs["fitness"]["max"] / hist_specs["fitness"]["delta"]))
            self._fit_ax.clear()
            self._fit_ax.hist(fitness_list_herb, bins=fit_bins,
                              histtype="step", color="g",
                              range=(0, hist_specs["fitness"]["max"]))
            self._fit_ax.hist(fitness_list_carn, bins=fit_bins,
                              histtype="step", color="r",
                              range=(0, hist_specs["fitness"]["max"]))
            self._fit_ax.title.set_text("Histogram of fitness")

    def update_histogram_age(self, age_list_herb=None, age_list_carn=None, hist_specs=None):
        if hist_specs is None:
            self._age_ax.clear()
            self._age_ax.hist(age_list_herb,
                              histtype="step", color="g")
            self._age_ax.hist(age_list_carn,
                              histtype="step", color="r")
            self._age_ax.title.set_text("Histogram of age")
        else:
            age_bins = (int(hist_specs["age"]["max"] / hist_specs["age"]["delta"]))
            self._age_ax.clear()
            self._age_ax.hist(age_list_herb, bins=age_bins,
                              histtype="step", color="g", range=(0, hist_specs["age"]["max"]))
            self._age_ax.hist(age_list_carn, bins=age_bins,
                              histtype="step", color="r", range=(0, hist_specs["age"]["max"]))
            self._age_ax.title.set_text("Histogram of age")

    def update_histogram_weight(self, weight_list_herb=None,
                                weight_list_carn=None, hist_specs=None):
        if hist_specs is None:
            self._weight_ax.clear()
            self._weight_ax.hist(weight_list_herb,
                                 histtype="step", color="g")
            self._weight_ax.hist(weight_list_carn,
                                 histtype="step", color="r")
            self._weight_ax.title.set_text("Histogram of weight")
        else:
            weight_bins = (int(hist_specs["weight"]["max"] / hist_specs["weight"]["delta"]))
            self._weight_ax.clear()
            self._weight_ax.hist(weight_list_herb, bins=weight_bins,
                                 histtype="step", color="g",
                                 range=(0, hist_specs["weight"]["max"]))
            self._weight_ax.hist(weight_list_carn, bins=weight_bins,
                                 histtype="step", color="r",
                                 range=(0, hist_specs["weight"]["max"]))
            self._weight_ax.title.set_text("Histogram of weight")

    @property
    def map(self):
        return self._map
