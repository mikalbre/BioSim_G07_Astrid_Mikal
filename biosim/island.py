
from biosim.landscape import SingleCell, Highland, Lowland, Desert, Water
from biosim.animals import *
import random


def check_length_of_string(map_list):
    if not all(len(map_list[0]) == len(line) for line in map_list[1:]):
        return False
    return True


class CreateIsland:

    map_params_dict = {"H": Highland,
                       "L": Lowland,
                       "D": Desert,
                       "W": Water}

    def __init__(self, geography_island_string, initial_population):

        self.year_num = 0  # years simulated

        self.map = self.make_map(geography_island_string)  # simulation file
        self.add_population(initial_population)  # simulation file
        # self.island = {}

        self.len_map_x = None
        self.len_map_y = None

        #geography_island_string_map = geography_island_string.strip()
        #geography_island_string = geography_island_string_map.strip().split('\n')

    @property
    def num_animals(self):
        """Returns total number of animals on island.
        Returns: int of total number of animals.
        """

        num_animals = 0
        for num_type in self.num_animals_per_species.values():
            num_animals += num_type
        return num_animals

    @property
    def num_animals_per_species(self):
        """Returns number of herbivores and carnivores on island.
        Iterates through each cell and count number of animals.
        Returns: dict of number per species
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
        """Method to check whether the string of the landscape type of island are rectangular.
        Checks if all lines have same length as the first (base) line.
        If conditions are met, the method returns a list of strings in map_list.
        Parameters:
            geography_island_string: multilinestring of island map
        Returns: list of strings X: ['WWW', 'WLW', 'WWW']
        """
        #map_list = []
        #geography_island_string_map = [i.strip('[]') for i in geography_island_string]
        #map_list = geography_island_string_map.split('\n')

        geography_island_string_map = geography_island_string.strip().split('\n')
        map_list = geography_island_string_map

        if not check_length_of_string(map_list):
            raise ValueError("Multi line string must have equal length, must be a rectangle.")

        first_line_north = map_list[0]
        last_line_south = map_list[-1]
        first_column_west = [line[0] for line in map_list]
        last_column_east = [line[-1] for line in map_list]

        for landscape_type in (first_line_north + last_line_south):
            if not landscape_type == 'W':
                raise ValueError("Cells in both north and south must consist of water!")

        for landscape_type in (first_column_west + last_column_east):
            if not landscape_type == 'W':
                raise ValueError("Cells in west and east must consist of water!")

        return map_list  # X: ['WWW', 'WLW', 'WWW']

    def make_map(self, geography_island_string):
        """Create a dictionary from the multi- line string.
        Input is the multi- line string.
        Output is the island_map with;
        Key: Instance of cell (landscape type- 'Highland', 'Lowland', 'Desert', 'Water')
        Value: Coordinates in (x, y) tuple form. (1,1) is upper left corner
        Returns: dict where key: tuple, value: instance of landscape type
        """

        map_list = self.condition_for_island_map_string(geography_island_string)

        island_map = {}

        self.len_map_x = len(map_list[0])
        self.len_map_y = len(map_list)

        coord_x = 1
        for line in map_list:
            coord_y = 1
            for type_landscape in line:
                island_map[(coord_x, coord_y)] = self.map_params_dict[type_landscape]()
                coord_y += 1
            coord_x += 1

        return island_map  # X: {(1,1): Water, (1,2): Water, ... , (2,2): Lowland}

    def add_population(self, population):
        """Add population of both herbivores and carnivores to the island."""

        for map_location in population:
            loc = map_location['loc']  # Gets a coordinate X: (1, 1)
            if loc not in self.map.keys():  # Checks if (1,1) is key in self.map
                raise ValueError("Location does not exist")
            if not self.map[loc].accessability:
                raise ValueError("Animals not allowed to enter Water")

            pop = map_location['pop']  # Takes out 'pop' as key and gets the value
            self.map[loc].animals_allocate(pop)  # puts animal in location_cell in landscape.py file

    def feed_animal(self):
        for cell in self.map.values():
            cell.eat()  # X: Lowland.eat() and lowland- fodder grows and all animals eat.

    def procreation_animals(self):
        for cell in self.map.values():
            cell.procreation()

    def add_migrated_herb_to_new_cell(self, new_loc, herbivore):  # Works
        self.map[new_loc].add_herb_migrated(herbivore)

    def add_migrated_carn_to_new_cell(self, new_loc, carnivore):  # Works
        self.map[new_loc].add_carn_migrated(carnivore)

    def migration_neighboring_cells(self, loc):
        """Finds the location/cell North, East, West and South from current cell."""

        coord_x, coord_y = loc  # (2, 2)

        # Gets the location of the cell with coordinates
        cell_1 = (coord_x - 1, coord_y)  # North cell (1,2)
        cell_2 = (coord_x + 1, coord_y)  # South cell (3,2)
        cell_3 = (coord_x, coord_y - 1)  # West cell  (2,1)
        cell_4 = (coord_x, coord_y + 1)  # East cell  (2,3)


        # Checks the landscape type
        type_1 = self.map[cell_1]
        type_2 = self.map[cell_2]
        type_3 = self.map[cell_3]
        type_4 = self.map[cell_4]

        # X: [((2,2), Lowland), ((3,3), Highland),((3,1), Water), ((4,2),Lowland)]
        neighbor_cells = [(cell_1, type_1), (cell_2, type_2), (cell_3, type_3), (cell_4, type_4)]

        return neighbor_cells

        #return [cell for cell in neighbor_cells if cell[1] is not Water]
        #accessible_neighbor_cells = [cell for cell in neighbor_cells if cell[1] is not Water]
        #return accessible_neighbor_cells  # X: [((2,2), Lowland), ((3,3), Highland), ((4,2),Lowland)]

    def migration_animals(self):
        """Iterates through each cell """
        for loc, cell in self.map.items():  # X: dict_items( [ ((1,1), Water), ((1,2), Water),...] )

            if cell.accessability is True:  # cell is Lowland, Highland, Desert, Water
                neighboring_cells = self.migration_neighboring_cells(loc)

                if len(neighboring_cells) > 0:
                    migrated_herb, migrated_carn = cell.migrate(neighboring_cells)  # takes in new cell

                    for new_loc, herb in migrated_herb:
                        self.add_migrated_herb_to_new_cell(new_loc, herb)
                    for new_loc, carn in migrated_carn:
                        self.add_migrated_carn_to_new_cell(new_loc, carn)

    def new_year_reset(self):
        """Updates the migration to False for all animals when new year starts."""
        for cell in self.map.values():
            for herbivore in cell.present_carnivores:
                herbivore.set_migration_false()
            for carnivore in cell.present_carnivores:
                carnivore.set_migration_false()

    def aging_animals(self):
        """Increments age by one and reduces weight of each animal annually."""
        for cell in self.map.values():
            cell.aging()

    def death_animals(self):
        for cell in self.map.values():
            cell.animal_death()
        #for pos, cell in self.map.items():
        #   herb_death, carn_death = cell.animal_death()
        #   if self.store_stats:
        #       self.stats[self.year]['Herbivore']['death'][pos] = herb_death
        #       self.stats[self.year]['Carnivore']['death'][pos] = carn_death

    def year(self):
        return self.year_num

    # @year.setter
    # def year(self, new_year_value):
    #     self.year_num = new_year_value

    def simulate_one_year(self):
        self.new_year_reset()
        self.feed_animal()
        self.procreation_animals()
        self.migration_animals()
        self.aging_animals()
        self.death_animals()
        self.year += 1


if __name__ == '__main__':
    geography_island_string = """WWW
    WLW
    WWW"""
    F = CreateIsland(geography_island_string)
    F.conditions_for_island_map_string()

# for pos, cell in self.map.items():
#   herb_birth, carn_birth = cell.procreation()
#   if self.store_stats:
#       self.stats[self.year]['Herbivore']['birth'][pos] = herb_birth
#       self.stats[self.year]['Carnivore']['birth'][pos] = carn_birth