# -*- coding: utf-8 -*-

__author__ = 'Astrid Sedal, Mikal Breiteig'
__email__ = 'astrised@nmbu.no, mibreite@nmbu.no'

"""
File for island with many cells
"""
from biosim.landscape import Highland, Lowland, Desert, Water


def check_length_of_string(map_list):
    """
    Compares length of all lines in a list of lines to the first line in the list.
    Parameters
    ----------
    map_list : list
        list of lines

    Returns
    -------
    bool
        False if not all lines are equal, True if all lines are equal.
    """

    if not all(len(map_list[0]) == len(row) for row in map_list[1:]):
        return False
    return True


class CreateIsland:

    map_params_dict = {"H": Highland,
                       "L": Lowland,
                       "D": Desert,
                       "W": Water}

    def __init__(self,
                 geography_island_string,
                 initial_population
                 ):
        """
        Initiates the CreateIsland class.
        Class attribute map_params_dict holds information of which letter relates to which class in
        landscape.py.

        The CreateIsland takes a multilinestring and initial population on Rossumøya as input.
        Initializes instance of CreateIsland.

        Parameters
        ----------
        geography_island_string : str
            Multilinestring of map
        initial_population : dict
            Key: location given in coordinates - Value: list of dict
        """

        self.year_num = 0

        self.map = self.make_map(geography_island_string)
        self.add_population(initial_population)

    @property
    def num_animals(self):
        """
        This property method returns number of total animals on Rossumøya.

        Returns
        -------
        num_animals : int
            Total number of animals on island
        """

        num_animals = 0
        for num_type in self.num_animals_per_species.values():
            num_animals += num_type
        return num_animals

    @property
    def num_animals_per_species(self):
        """
        This property method returns the number of herbivores and carnivores on island.
        Iterates through each cell on island and count number of animals.

        Returns
        -------
        num_animals_per_species : dict
            Key: Species - Values: Total number of the specific animal

        """

        num_animals_per_species = {}
        num_herbivores = 0
        num_carnivores = 0

        for cell in self.map.values():
            num_herbivores += cell.num_herbivores
            num_carnivores += cell.num_carnivores

        num_animals_per_species["Herbivore"] = num_herbivores
        num_animals_per_species["Carnivore"] = num_carnivores

        return num_animals_per_species

    @staticmethod
    def condition_for_island_map_string(geography_island_string):
        """
        Method to check whether the string of the landscape type of island are rectangular,
        if they are not equal length a ValueError will occur.
        If map is rectangular, the method checks if the island is surrounded by water.
        If all these conditions are met, the method returns a list of strings in map_list.

        Parameters
        ----------
        geography_island_string : multilinestring

        Returns
        -------
        map_list : list
            list of strings
        """

        map_params_dict = {"H": Highland,
                           "L": Lowland,
                           "D": Desert,
                           "W": Water}

        geography_island_string_map = geography_island_string.strip().split('\n')
        map_list = geography_island_string_map

        if not check_length_of_string(map_list):
            raise ValueError("Multi line string must have equal length, must be a rectangle.")

        for cell in map_list:
            for l_type in cell:
                if l_type not in map_params_dict.keys():
                    raise ValueError("Must be of correct landscape type")

        first_line_north = map_list[0]
        last_line_south = map_list[-1]
        first_column_west = [line[0] for line in map_list]
        last_column_east = [line[-1] for line in map_list]

        for landscape_type in (first_line_north + last_line_south):
            if not landscape_type == 'W':
                raise ValueError("Cells in north and south of island must consist of water!")

        for landscape_type in (first_column_west + last_column_east):
            if not landscape_type == 'W':
                raise ValueError("Cells in west and east of island must consist of water!")

        return map_list

    def make_map(self, geography_island_string):
        """
        Create a dictionary from the multilinestring given as input.
        Coordinate (1, 1) is upper left corner.

        Parameters
        ----------
        geography_island_string : multilinestring

        Returns
        -------
        island_map : dict
            key: tuple with cell coordinate - Value: Instance of subclass of SingleCell
        """
        island_map = {}

        map_list = self.condition_for_island_map_string(geography_island_string)

        coord_x = 1
        for line in map_list:
            coord_y = 1
            for type_landscape in line:
                island_map[(coord_x, coord_y)] = self.map_params_dict[type_landscape]()
                coord_y += 1
            coord_x += 1

        return island_map

    def add_population(self, population):
        """
        Add population of both herbivores and carnivores to the island.
        The method feeds a population to cells.

        Parameters
        ----------
        population: list
            loc: tuple
            pop: dict

        Methods
        -------
        SingleCell.animals_allocate()
        """

        for map_location in population:
            loc = map_location['loc']  # Gets a coordinate X: (1, 1)
            if loc not in self.map.keys():  # Checks if (1,1) is key in self.map
                raise ValueError("Location does not exist")
            if not self.map[loc].accessibility:
                raise ValueError("Animals not allowed to enter Water")

            pop = map_location['pop']  # Takes out 'pop' as key and gets the value
            self.map[loc].animals_allocate(pop)  # puts animal in location_cell in landscape.py file

    def feed_animal(self):
        """
        Calls eat in all cells of the map.
        Fodder grows and herbivores and carnivores gets to eat.

        Methods
        -------
        SingleCell.eat()
        """
        for cell in self.map.values():
            cell.eat()  # X: Lowland.eat() and lowland- fodder grows and all animals eat.

    def procreation_animals(self):
        """
        Calls procreate in all cells of the map.

        Methods
        -------
        SingleCell.procreation()
        """

        for cell in self.map.values():
            cell.procreation()

    def add_migrated_herb_to_new_cell(self, new_loc, herbivore):
        """
        Adds migrated herbivore to new cell by position.

        Parameters
        ----------
        new_loc : tuple
        herbivore : object
        """

        self.map[new_loc].add_herb_migrated(herbivore)

    def add_migrated_carn_to_new_cell(self, new_loc, carnivore):
        """
        Adds migrated herbivore to new cell by position.

        Parameters
        ----------
        new_loc : tuple
        carnivore : object
        """

        self.map[new_loc].add_carn_migrated(carnivore)

    def migration_neighboring_cells(self, loc):
        """
        Finds the cells adjacent to the current cell.
        Meaning the cells located north, east, west and south from current cell.

        Parameters
        ----------
        loc : tuple
            Coordinate

        Returns
        -------
        neighbor_cells : list
            Contains location and landscape type of adjacent cells.
        """

        coord_x, coord_y = loc

        cell_1 = (coord_x - 1, coord_y)
        cell_2 = (coord_x + 1, coord_y)
        cell_3 = (coord_x, coord_y - 1)
        cell_4 = (coord_x, coord_y + 1)

        type_1 = self.map[cell_1]
        type_2 = self.map[cell_2]
        type_3 = self.map[cell_3]
        type_4 = self.map[cell_4]

        neighbor_cells = [(cell_1, type_1), (cell_2, type_2), (cell_3, type_3), (cell_4, type_4)]

        return neighbor_cells

    def migration_animals(self):
        """
        Checks each cell in the map if it is accessible for the animals, and if the condition is
        met it finds the cells' neighbors. It then calls migrate method from SingleCell and
        returns the herbivores and carnivores, if any, that has migrated to a new cell.
        In migrate method in SingleCell the migrated animal gets deleted from that cell.
        The migrated animal gets added to the new cell that was selected randomly.

        Methods
        -------
        SingleCell.migrate()
        """

        for loc, cell in self.map.items():
            if cell.accessibility is True:
                neighboring_cells = self.migration_neighboring_cells(loc)
                migrated_herb, migrated_carn = cell.migrate(neighboring_cells)

                for new_loc, herb in migrated_herb:
                    self.add_migrated_herb_to_new_cell(new_loc, herb)
                    cell.remove_herb_migrated(herb)

                for new_loc, carn in migrated_carn:
                    self.add_migrated_carn_to_new_cell(new_loc, carn)
                    cell.remove_carn_migrated(carn)

    def new_year_reset(self):
        """
        Updates the migration to False for all animals when new year starts.
        """

        for cell in self.map.values():
            for herbivore in cell.present_carnivores:
                herbivore.set_migration_false()

            for carnivore in cell.present_carnivores:
                carnivore.set_migration_false()

    def aging_animals(self):
        """
        Every year, increment the age of every animal by 1 and reduce the weight of the animal.
        """
        for cell in self.map.values():
            cell.aging()

    def death_animals(self):
        """
        Calls animal_death in all cells on the map.
        """
        for cell in self.map.values():
            cell.animal_death()

    @property
    def year(self):
        return self.year_num

    @year.setter
    def year(self, new_year_value):
        self.year_num = new_year_value

    def weight_list(self):
        """
        Lists of weights of all animals on island.

        Returns
        -------
        herb_weight_list : list
        carn_weight_list : list
        """

        herb_weight_list = []
        carn_weight_list = []
        for cell in self.map.values():
            for herb in cell.present_herbivores:
                herb_weight_list.append(herb.weight)

        for cell in self.map.values():
            for carn in cell.present_carnivores:
                carn_weight_list.append(carn.weight)

        return herb_weight_list, carn_weight_list

    def age_list(self):
        """
        Lists of ages of all animals on island.

        Returns
        -------
        herb_age_list : list
        carn_age_list : list
        """

        herb_age_list = []
        carn_age_list = []

        for cell in self.map.values():
            for herb in cell.present_herbivores:
                herb_age_list.append(herb.age)

        for cell in self.map.values():
            for carn in cell.present_carnivores:
                carn_age_list.append(carn.age)

        return herb_age_list, carn_age_list

    def fitness_list(self):
        """
        Lists of fitness for all animals on island.

        Returns
        -------
        herb_age_list : list
        carn_age_list : list
        """

        herb_fitness_list = []
        carn_fitness_list = []

        for cell in self.map.values():
            for herb in cell.present_herbivores:
                herb_fitness_list.append(herb.phi)

        for cell in self.map.values():
            for carn in cell.present_carnivores:
                carn_fitness_list.append(carn.phi)

        return herb_fitness_list, carn_fitness_list

    def simulate_one_year(self):
        """
        Simulates a whole year by the following sequence.

        Returns
        -------
        num_animals_per_species : dict
        """

        # self.new_year_reset()
        self.feed_animal()
        self.procreation_animals()
        self.migration_animals()
        self.aging_animals()
        self.death_animals()
        self.year += 1

        return self.num_animals_per_species


if __name__ =='__main__':

    default_map = """WWWW\nWLHW\nWLWW\nWWWW"""

    default_population = [{"loc": (2, 2), "pop": [{'species': 'Herbivore', 'age': 5, 'weight': 20}
                                                  for _ in range(150)]}]
    CreateIsland(default_map, default_population).simulate_one_year()


# for pos, cell in self.map.items():
#   herb_birth, carn_birth = cell.procreation()
#   if self.store_stats:
#       self.stats[self.year]['Herbivore']['birth'][pos] = herb_birth
#       self.stats[self.year]['Carnivore']['birth'][pos] = carn_birth


    # default_population = [{"loc": (2, 2),"pop": [{'species': 'Herbivore', 'age': 5, 'weight': 20}
    #                                               for _ in range(150)]},
    #                        {"loc": (2, 2), "pop": [{'species': 'Carnivore', 'age': 5, 'weight': 20}
    #                                                for _ in range(40)]}]