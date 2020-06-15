# -*- coding: utf-8 -*-

__author__ = 'Astrid Sedal, Mikal Breiteig'
__email__ = 'astrised@nmbu.no, mibreite@nmbu.no'

from biosim.island import CreateIsland


import matplotlib.pyplot as plt
import os

class Visual:

    density_heatmap = {'Herbivore': 275,
                       'Carnivore': 150}

    def __init__(self,
                 island,
                 num_years_sim,
                 ymax_animals=None,
                 cmax_animals=None,
                 img_base=None,
                 img_fmt='png'
                 ):

        self.img_num = 0
        self.x_len = len(island.condition_for_island_map_string(geography_island_string="""WWW\nWLW\nWWW""")[0])
        self.y_len = len(island.condition_for_island_map_string(geography_island_string="""WWW\nWLW\nWWW"""))
        self.num_years_sim = num_years_sim

        self.num_years_fig = island.year() + num_years_sim


        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals

        if ymax_animals is None:
            """Number specifying y-axis limit for graph showing animal numbers"""
            self.ymax_animals = 20000  # ??
        else:
            self.ymax_animals = ymax_animals

        if cmax_animals is None:
            """Dict specifying color-code limits for animal densities """
            self.cmax_animals = {'Herbivore': 50, 'Carnivore': 20}  # ??
        else:
            self.cmax_animals = cmax_animals

        self.img_fmt = img_fmt
        self.img_base = img_base

        if img_base is None:
            self.img_base = os.path.join('..', 'BioSim')
        else:
            self.img_base = img_base


        self.figure = None
        self.grid = None


        self.heat_map_herbivores_ax = None
        self.heat_map_herb_img_ax = None
        self.colorbar_herb_ax = None


        self.set_up_graphics(island)
        self.draw_heat_map_herbivore(self.get_data_heat_map(island, 'num_herbivores'))

    def empty_nested_list(self):
        empty_nested_list = []
        for y in range(self.y_len):
            empty_nested_list.append([])
            for x in range(self.x_len):
                empty_nested_list[y].append(None)
        return empty_nested_list

    def set_up_graphics(self, island):
        if self.figure is None:
            self.figure = plt.figure(constrained_layout=True, figsize=(16, 9))
            self.grid = self.figure.add_gridspec(2, 24)

        if self.heat_map_herbivores_ax is None:
            self.heat_map_herbivores_ax = self.figure.add_subplot(self.grid[1, :11])
            self.heat_map_herb_img_ax = None

        if self.colorbar_herb_ax is None:
            self.colorbar_herb_ax = self.figure.add_subplot(self.grid[1, 11])

    def get_data_heat_map(self, island, data_type):
        heat_map = self.empty_nested_list()
        for pos, cell in island.map.items():
            y, x = pos
            heat_map[y][x] = getattr(cell, data_type)
        return heat_map

    def draw_heat_map_herbivore(self, heat_map):
        self.heat_map_herbivores_ax.axis('off')
        self.heat_map_herbivores_ax.set_title('Tetste Herb')
        self.heat_map_herb_img_ax = self.heat_map_herbivores_ax.imshow(heat_map,
                                                                       cmap='inferno',
                                                                       vmax=self.cmax_animals['Herbivore'])
        plt.colorbar(self.heat_map_herb_img_ax, cax=self.colorbar_herb_ax)


    def updated_heat_maps(self, island):
        heat_map_herb = self.get_data_heat_map(island, 'num_herbivores')
        self.heat_map_herb_img_ax.set_data(heat_map_herb)

    def update_fig(self, island):
        self.updated_heat_maps(island)
        plt.pause(1e-10)


if __name__ == '__main__':
    default_map = """WWW\nWLW\nWWW"""

    ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(150)]}]

    island = CreateIsland(geography_island_string="""WWW\nWLW\nWWW""", initial_population=ini_herbs)
    vis = Visual(island, 50)

    for _ in range(50):
        island.simulate_one_year()























# from biosim.landscape import Lowland
# import matplotlib.pyplot as plt
# import random
# random.seed(1)
#
#
# listof = [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(50)]
# listofcarns = [{'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(20)]
#
# #create a Lowland Object
# l = Lowland()
# # place them in list in l
#
# l.animals_allocate(listof)
# l.animals_allocate(listofcarns)
#
# #for i in l.herb_list:
#  #   print(type(i))
# #
# print(0, " Year End Herb numbers :-", len(l.present_herbivores))
# print(0, " Year End Carn numbers :-", len(l.present_carnivores))
# #
# #Making figure
# fig = plt.figure(figsize=(8, 6.4))
# plt.plot(0, len(l.present_herbivores),  '*-', color='g', lw=0.5)
# plt.plot(0, len(l.present_carnivores),  '*-', color='r', lw=0.5)
# plt.draw()
# plt.pause(0.01)
#
# count_herb = [len(l.present_herbivores)]
# count_carn = [len(l.present_carnivores)]
#
# for i in range(200):
#     l.fodder_regrow()
#     l.eat()
#     l.procreation()
#     l.animal_death()
#     l.aging()
#
#     count_herb.append(len(l.present_herbivores))
#     count_carn.append(len(l.present_carnivores))
#
#     # plotting
#     plt.plot(list(range(i + 2)),  count_herb, '*-', color='g', lw=0.5)
#     plt.plot(list(range(i + 2)), count_carn, '*-', color='r', lw=0.5)
#     plt.draw()
#     plt.pause(0.001)
