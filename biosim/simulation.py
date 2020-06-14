from biosim.island import CreateIsland
from .landscape import Highland, Lowland, Desert, Water
from .animals import Herbivore, Carnivore
from biosim import animals
from biosim import landscape as Landscape
from biosim import island as Island

import random
import os


class Simulation:

        # default_map = """WWW
        #                 WLW
        #                 WWW
        #                 """

        # default_population = [
        #     {"loc": (2, 2),
        #      "pop": [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(150)],
        #      },
        #     {"loc": (2, 2),
        #      "pop": [{'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(40)],
        #      }
        # ]

    def __init__(self,
                 island_map_str,
                 ini_pop,
                 seed,
                 ymax_animals=None,
                 cmax_animals=None,
                 hist_specs=None,
                 img_base=None,
                 img_fmt='png'
                 ):

        random.seed(seed)
        self.island_map = CreateIsland.make_map(island_map_str)
        self.ini_pop = CreateIsland.add_population(ini_pop)

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

        if  not 'fitness' or 'age' or 'weight' in hist_spec:
                raise ValueError('Does not accept this input!')
                # Riktig?

        self.img_ctr = 0
        self.final_year = None
        self.img_fmt = img_fmt

        if img_base is None:
            self.img_base = os.path.join('..', 'BioSim')
        else:
            self.img_base = img_base


    @staticmethod
    def set_animal_parameters(species, params):
        if species is 'Herbivore':
            animals.Herbivore.set_parameters(params)
        elif species is 'Carnviore':
            animals.Carnivore.set_parameters(params)

    @staticmethod
    def set_landscape_parameters(landscape, params):
        # if landscape is 'W':
        #     Landscape.Water.cell_parameter(params, accessability=False)
        # elif landscape is 'D':
        #     Landscape.Desert.cell_parameter(params, accessabiliy=True)
        if landscape is 'H':
            Landscape.Highland.cell_parameter(params,accessability=True)
        elif landscape is 'L':
            Landscape.Lowland.cell_parameter(params, accessability=True)

    @property
    def year(self):
        return self.year()

    def add_population(self, population):
        Island.CreateIsland.add_population(population)

    def simulate(self):
        # sim.simulate(num_years=100, vis_years=1, img_years=2000)









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

    sim.simulate(num_years=100, vis_years=1, img_years=2000)

    sim.add_population(population=ini_carns)
    sim.simulate(num_years=100, vis_years=1, img_years=2000)






    @staticmethod
    def set_animal_parameters(self, species, img_fmt):
        animal_species = {'Hervivore': Herbivore,
                          'Carnivore': Carnivore}
        animal_species[species].set_parameters(params)  # se mer på

    @staticmethod
    def set_landscape_parameters(self)
        map_params_dict = {"H": Highland,
                            "L": Lowland,
                            "D": Desert,
                            "W": Water}

    def simulate(self, num_years):
        current_year = 1
        while current_year <= num_years:
            current_year += 1

    def add_population(self, population):
        self.Island.CreateIsland(population)

    @property
    def year(self):
        return self.island.y

    @property
    def num_animals(self):
        return

    @property
    def num_animals_per_species(self):
        return




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