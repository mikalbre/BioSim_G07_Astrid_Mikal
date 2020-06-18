# # -*- coding: utf-8 -*-
#
# __author__ = 'Astrid Sedal, Mikal Breiteig'
# __email__ = 'astrised@nmbu.no, mibreite@nmbu.no'
#
# from biosim.island import CreateIsland as island
# from biosim import landscape as Landscape
# from biosim.animals import Animals, Carnivore, Herbivore
# from biosim import island
# import textwrap
# import random
#
# import matplotlib.pyplot as plt
#
#
# class Visualization:
#     def __init__(self):
#
#         self.herb_data =[]
#         self.carn_data = []
#
#     def set_plot_first_time(self):
#         self.fig = plt.figure(figsize=(12, 6))
#         plt.axis("off")
#
#         self.fit_ax = self.fig.ass_subplot(6, 3, 16)
#         self.fit_ax.set_title("Fitness histogram")
#         self.fit_axis = None
#
#     def update_hist(self, fit_list=None):
#         self.fit_ax.clear()
#         self.fit_ax.set_title("Fitness hisotogram")
#
#         self.fit_ax.hist(fitness_list()[0], bins=10, histtype="step",
#                               color="g")
#         self.fit_ax.hist(fitness_list()[1], bins=10, histtype="step",
#                               color="r")

# if __name__ == "__main__":


                 # island_map,
                 # ini_pop,
                 # seed):
    #     random.seed(seed)
    #     self.island_map = island_map
    #     self.ini_pop = ini_pop
    #     self.island = island.CreateIsland(geography_island_string=island_map,
    #                                       initial_population=ini_pop)
    #
    #     self._fig = None
    #     self._map = None
    #     self._map_axis = None
    #     self._pop_ax = None
    #     self._pop_axis = None
    #     self._herb_heat_ax = None
    #     self._herb_heat_axis = None
    #     self._carn_heat_ax = None
    #     self._carn_heat_axis = None
    #
    #     self._fit_ax = None
    #     self._fit_axis = None
    #     self._age_ax = None
    #     self._age_axis = None
    #     self._weight_ax = None
    #     self._weight_axis = None
    #
    #     # self.img_base = img_base
    #     # self.img_fmt = img_fmt
    #     self._img_ctr = 0
    #     self.num_years = None
    #     self.last_year_simulated = 0
    #
    #     self.herbivore_list = [self.island.num_animals_per_species['Herbivore']]
    #     self.carnivore_list = [self.island.num_animals_per_species['Carnivore']]
    #
    # def set_animal_parameters(self, species, params):
    #     if species == 'Herbivore':
    #         Herbivore.set_parameters(params)
    #     elif species == 'Carnviore':
    #         Carnivore.set_parameters(params)
    #
    # def set_landscape_parameters(self, landscape, params):
    #     if landscape == 'W':
    #         Landscape.Water.cell_parameter(params)
    #     elif landscape == 'D':
    #         Landscape.Desert.cell_parameter(params)
    #     if landscape == 'H':
    #         Landscape.Highland.cell_parameter(params)
    #     elif landscape == 'L':
    #         Landscape.Lowland.cell_parameter(params)
    #
    # def add_population(self, population):
    #     self.island.add_population(population)
    #
    # def set_up_graphics(self):
    #     if self._fig is None:
    #         self._fig = plt.figure(figsize=(12, 6))
    #         self._fig.suptitle("Rossumøya", fontweight="bold")
    #
    #     if self._fit_axis is None:
    #         self._fit_ax = self._fig.add_subplot(3, 2, 5)
    #     #
    #
    #     # if self._age_ax is None:
    #     #     self.update_histogram_age(age_list_carn=, age_list_herb=)
    #     #
    #     # if self._weight_ax is None:
    #     #     self.update_histogram_weight(weight_list_carn=, weight_list_herb=)
    #
    # def update_histogram_fitness(self, num_years):
    #     # self._fit_ax.clear()
    #     # self._fig = plt.figure(figsize=(16, 9))
    #     # self._fit_ax = self._fig.add_subplot(3, 2, 5)
    #     # self._fit_ax.hist(phi_list_herb, bins=10, histtype="step", color="g")
    #     # self._fit_ax.hist(phi_list_carn, bins=10, histtype="step", color="r")
    #     # self._fit_ax.clear()
    #     self._fit_ax.hist(self.island.fitness_list()[0], bins=10, histtype="step",
    #                       color="g")
    #     self._fit_ax.hist(self.island.fitness_list()[1], bins=10, histtype="step",
    #                       color="r")
    #     self._fit_ax.title.set_text("Historgram of fitness")
    #     # self._fit_ax.title.set_text("Historgram of fitness")
    #
    # def update_histogram_age(self, age_list_herb=None, age_list_carn=None):
    #     # self._age_ax.clear()
    #     self._age_ax.title.set_text("Historgram of age")
    #     self._age_ax.hist(age_list_herb, bins=10, histtype="step", color="g")
    #     self._age_ax.hist(age_list_carn, bins=10, histtype="step", color="r")
    #
    # def update_histogram_weight(self, weight_list_herb=None, weight_list_carn=None):
    #
    #     # self._weight_ax.clear()
    #     self._weight_ax.title.set_text("Historgram of weight")
    #     self._weight_ax.hist(weight_list_herb, bins=10, histtype="step", color="g")
    #     self._weight_ax.hist(weight_list_carn, bins=10, histtype="step", color="r")
    #
    # def simulate(self, num_years, vis_years=1, img_years=None):
    #     if img_years is None:
    #         img_years = vis_years
    #
    #     self.set_up_graphics()
    #     # self.plot_island_map()
    #     self.num_years = num_years  # ??
    #
    #     for _ in range(num_years):
    #
    #         # self.island.fitness_list()[0],
    #         # self.island.fitness_list()[1]
    #         # if self._age_ax is None:
    #         #     self.update_histogram_age(age_list_carn=, age_list_herb=)
    #         #
    #         # if self._weight_ax is None:
    #         #     self.update_histogram_weight(weight_list_carn=, weight_list_herb=)
    #         #
    #         new_island_population = self.island.simulate_one_year()
    #         self.herbivore_list.append(new_island_population['Herbivore'])
    #         self.carnivore_list.append(new_island_population['Carnivore'])
    #
    #         if self._fit_ax is not None:
    #             self.update_histogram_fitness(num_years)
    #
    #         # if num_years % vis_years == 0:
    #         #     self.update_graphics()
    #         #
    #         # if num_years % img_years == 0:
    #         #     self.save_graphics()
    #         #
    #         self.last_year_simulated += 1
    #
    #
    #

#
# if __name__ == '__main__':
#     plt.ion()
#     default_map = """WWWWWWWWWWWWWWWWWWWWW\nWWWWWWWWHWWWWLLLLLLLW\nWHHHHHLLLLWWLLLLLLLWW\nWHHHHHHHHHWWLLLLLLWWW\nWHHHHHLLLLLLLLLLLLWWW\nWHHHHHLLLDDLLLHLLLWWW\nWHHLLLLLDDDLLLHHHHWWW\nWWHHHHLLLDDLLLHWWWWWW\nWHHHLLLLLDDLLLLLLLWWW\nWHHHHLLLLDDLLLLWWWWWW\nWWHHHHLLLLLLLLWWWWWWW\nWWWHHHHLLLLLLLWWWWWWW\nWWWWWWWWWWWWWWWWWWWWW"""
#
#     ini_herbs = [{'loc': (10, 10),
#                   'pop': [{'species': 'Herbivore',
#                            'age': 5,
#                            'weight': 20}
#                           for _ in range(150)]}]
#     ini_carns = [{'loc': (10, 10),
#                   'pop': [{'species': 'Carnivore',
#                            'age': 5,
#                            'weight': 20}
#                           for _ in range(40)]}]
#
#     sim = Visualization(island_map=default_map, ini_pop=ini_herbs,
#                  seed=123456,
#                  )
#
#     sim.set_animal_parameters('Herbivore', {'zeta': 3.2, 'xi': 1.8})
#     sim.set_animal_parameters('Carnivore', {'a_half': 70, 'phi_age': 0.5,
#                                             'omega': 0.3, 'F': 65,
#                                             'DeltaPhiMax': 9.})
#     sim.set_landscape_parameters('L', {'f_max': 700})
#     # print(sim.heat_map_herbivore())
#     sim.simulate(num_years=100, vis_years=1, img_years=2000)
#     sim.add_population(population=ini_carns)
#     sim.simulate(num_years=300, vis_years=1, img_years=2000)













#
#
#
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
