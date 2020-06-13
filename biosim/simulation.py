from .island import CreateIsland
from .landscape import Highland, Lowland, Desert, Water
from .animals import Herbivore, Carnivore

import random

class Simulation:

        default_map = """WWW
                        WLW
                        WWW
                        """

        default_population = [
            {"loc": (2, 2),
             "pop": [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(150)],
             },
            {"loc": (2, 2),
             "pop": [{'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(40)],
             }
        ]

    def __init__(self,
                 map_string=None,
                 initial_population=None,
                 seed=None,
                 ymax_animals=None,
                 cmax_animals=None,
                 hist_specs=None,
                 img_base=None,
                 img_fmt='png'):
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

        if initial_population is None:
            initial_population = self.default_population

        if seed is not None:
            random.seed(seed)

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
        map_params_dict[lands

    def simulate(self, num_years):
        current_year = 1
        while current_year <= num_years:
            current_year += 1

    def add_population(self, population):
        self.Crea

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