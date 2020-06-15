from biosim.island import CreateIsland
from landscape import Highland, Lowland, Desert, Water
from animals import Herbivore, Carnivore
from biosim import animals
from biosim import landscape as Landscape
from biosim import island

import random
import os
from matplotlib import colors
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import subprocess

class BioSim:

    default_map = """WWW\nWLW\nWWW"""
    #
    # default_population = [{"loc": (2, 2),"pop": [{'species': 'Herbivore', 'age': 5, 'weight': 20}
    #                                               for _ in range(150)]},
    #                        {"loc": (2, 2), "pop": [{'species': 'Carnivore', 'age': 5, 'weight': 20}
    #                                                for _ in range(40)]}]
    def __init__(self,
                 island_map=None,
                 ini_pop=None,
                 seed=None,
                 ymax_animals=None,
                 cmax_animals=None,
                 hist_specs=None,
                 img_base=None,
                 img_fmt='png'
                 ):

        if seed is not None:
            random.seed(seed)

        self.island_map = island_map

        if island_map is None:
            self.island = CreateIsland(self.default_map, ini_pop)
        else:
            self.island = CreateIsland(island_map, ini_pop)

        #     self.island = CreateIsland(island_map_str, ini_pop)
        #     self.island_map_str = self.default_map
        # else:
        #     self.island_map_str = island_map_str

        # if ini_pop is None:
        #     self.ini_pop = self.default_population
        # else:
        #     self.ini_pop = ini_pop




        #self.island_map = CreateIsland.make_map(island_map_str)

        #self.ini_pop = CreateIsland.add_population(ini_pop)

        if ymax_animals is None:
            """Number specifying y-axis limit for graph showing animal numbers"""
            self.ymax_animals = 15000  # ??
        else:
            self.ymax_animals = ymax_animals

        if cmax_animals is None:
            """Dict specifying color-code limits for animal densities """
            self.cmax_animals = {'Herbivore': 50, 'Carnivore': 20}  # ??
        else:
            self.cmax_animals = cmax_animals

        if not 'fitness' and 'age' and 'weight' in hist_specs:
                raise ValueError('Does not accept this input!')
                # Riktig?

        self.img_ctr = 0
        self.final_year = None
        self.img_fmt = img_fmt

        if img_base is None:
            self.img_base = os.path.join('..', 'BioSim')
        else:
            self.img_base = img_base

        # fig = plt.figure(figsize=(10, 7), constrained_layout=True)
        # gs = fig.add_gridspec(4, 6)
        self.fig = None
        self.ax_heat_h = None
        self.herb_denisty = None

        self.x_len = len(
            CreateIsland.condition_for_island_map_string(geography_island_string="""WWW\nWLW\nWWW""")[0])
        self.y_len = len(
            CreateIsland.condition_for_island_map_string(geography_island_string="""WWW\nWLW\nWWW"""))
        #self.x_len = island.CreateIsland.num_animals_per_species
        # self.y_len


    @staticmethod
    def set_animal_parameters(species, params):
        if species == 'Herbivore':
            animals.Herbivore.set_parameters(params)
        elif species == 'Carnviore':
            animals.Carnivore.set_parameters(params)

    @staticmethod
    def set_landscape_parameters(landscape, params):
        # if landscape is 'W':
        #     Landscape.Water.cell_parameter(params, accessability=False)
        # elif landscape is 'D':
        #     Landscape.Desert.cell_parameter(params, accessabiliy=True)
        if landscape == 'H':
            Landscape.Highland.cell_parameter(params, accessability=True)
        elif landscape == 'L':
            Landscape.Lowland.cell_parameter(params)

    def sim_ez(self, num_years):
        index = 1
        while index <= num_years:
            CreateIsland.simulate_one_year()
            # self.Cr.simulate_one_year()
            index +=1

    def add_population(self, population):
        return self.island.add_population(population)

    @property
    def year(self):
        return self.island.year()

    def empty_nested_list(self):
        empty_nested_list = []
        for y in range(self.y_len):
            for x in range(self.x_len):
                empty_nested_list[y].append(None)
        return empty_nested_list

    @property
    def animal_dist(self):
        data = {}
        rows = []
        col = []
        herbs = []
        #carns = []

        for coord, cell in self.island.make_map(geography_island_string=default_map).items():
            herbs.append(cell.present_herbivores)
            #carns.append(cell.present_herbivores)
            rows.append(coord[0])
            col.append(coord[1])
        data['Row'] = rows
        data['Col'] = col
        data['Herbivore'] = herbs
        #data['Carnivore'] = carns
        return pd.DataFrame(data)

    def herb_dist(self):
        row_num = np.shape()


    def heat_map_herbivore(self):
        # herb_cell = self.animal_dist.pivot('Row', 'Col', 'Herbivore')
        # herb_cell(np.reshape(self.animal_dist['Herbivore'].values), newshape=(3, 3))
        self.herb_denisty = self.ax_heat_h.imshow(np.reshape(self.animal_dist['Herbivore'].values,
                                                             newshape=(3, 3)),
                                                  vmax=self.cmax_animals['Herbivore']
                                                  )
        self.ax_heat_h.set_title('Test HERB DENS')


    def update_all(self):
        self.heat_map_herbivore()


    def set_up_grafics(self):
        if self.fig is None:
            self.fig = plt.figure()
            # self.fig.suptilte('Test overskrift', fontsize=16)
            self.fig.tight_layout()

        if self.herb_denisty is None:
            self.ax_heat_h = self.fig.add_subplot(2, 2, 4)
            self.heat_map_herbivore()

    def simulate(self, num_years, vis_years=1, img_years=None):
        # sim.simulate(num_years=100, vis_years=1, img_years=2000)
        if img_years is None:
            img_years = vis_years

        self.set_up_grafics()
        self.final_year = 1 + num_years

        while self.year < self.final_year:
            if self.year % vis_years == 0:
                self.update_all()
            self.island.simulate_one_year()


if __name__ == "__main__":
    plt.ion()
    default_map = """WWW\nWLW\nWWW"""

    ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(150)]}]

    sim = BioSim(island_map=default_map, ini_pop=ini_herbs,
                 seed=123456,
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60, 'delta': 2}},
                 )

    sim.set_animal_parameters('Herbivore', {'zeta': 3.2, 'xi': 1.8})
    sim.set_animal_parameters('Carnivore', {'a_half': 70, 'phi_age': 0.5,
                                            'omega': 0.3, 'F': 65,
                                            'DeltaPhiMax': 9.})
    sim.set_landscape_parameters('L', {'f_max': 700})
    # print(sim.heat_map_herbivore())
    sim.simulate(num_years=100, vis_years=1, img_years=2000)

    # sim.add_population(population=ini_carns)
    # sim.simulate(num_years=100, vis_years=1, img_years=2000)


    #
    #
    #
    #
    # @staticmethod
    # def set_animal_parameters(self, species, img_fmt):
    #     animal_species = {'Hervivore': Herbivore,
    #                       'Carnivore': Carnivore}
    #     animal_species[species].set_parameters(params)  # se mer på
    #
    # @staticmethod
    # def set_landscape_parameters(self)
    #     map_params_dict = {"H": Highland,
    #                         "L": Lowland,
    #                         "D": Desert,
    #                         "W": Water}
    #
    # def simulate(self, num_years):
    #     current_year = 1
    #     while current_year <= num_years:
    #         current_year += 1
    #
    # def add_population(self, population):
    #     self.Island.CreateIsland(population)
    #
    # @property
    # def year(self):
    #     return self.island.y
    #
    # @property
    # def num_animals(self):
    #     return
    #
    # @property
    # def num_animals_per_species(self):
    #     return
    #
    #
    #

"""
    Set population
    initial year = 0
    increase year
    set_animal_parameters
    set_landscape_parameters
    simulate
    num_animals_per_species
    num_animals_on_island

herb_list = []

num_animals = 5
# Appends herbivores to list
for iterator in range(num_animals):
    herb = Herbivore()
    herb_list.append(herb)
    print(herb_list)

# Print the age, weight, fitness for each herbivore in the list
for herb in herb_list:
    print("Age: ", herb.get_age(),
          "weight: ", herb.get_weight(),
          "fitness: ", herb.fitness_calculation())

# simulates 10 years
for iterator in range(10):  # years
    for herb in herb_list:# herbivore
        herb.feeding(11)
        herb.procreation(num_animals)
        herb.growing_older()  # adds year and
        herb.dying()

        print("Age: ", herb.get_age(),
              "weight: ", herb.get_weight(),
              "fitness: ", herb.get_fitness())

"""

"""

Parameters
----------
geography_island_string
    Multi- line string specifying island geography
initial_population
    List of dictionaries specifying initial population
seed
    Integer used as random number seed
ymax_animals
    Number of specifying y-axis limit for graph showing animal numbers
cmax_animals
    Dict specifying color-code limits for animal densities
hist_specs
    Specifications for histogram. Dictionary.
img_base
    String with the beginning of file name for figures, including path
img_fmt
    String with type for figures, e.g. 'png'
"""