
from biosim.landscape import SingleCell, Highland, Lowland, Desert, Water

class CreateIsland:

    map_params_dict = {"H": Highland,
                       "L": Lowland,
                       "D": Desert,
                       "W": Water}

    def __init__(self, geography_island_string):
        """

        Parameters
        ----------
        geography_island_string: str
            Multilinestring of the geography_string of the map
        initial_population: dict
            key: Coordinates, Values: list of dict
        """
        #self.len_map_x = None  # width of map
        #self.len_map_y = None  # length of map
        self.year_num = 0  # years simulates

        # Makes the map based on the multi- line string passed in
        #self.map = self.make_map(geography_island_string)  # simulation file
        # Passes in the population
        #self.add_population(initial_population)  # simulation file

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
    def conditions_for_island_map_string(geography_island_string):
        """Method to check whether the string of the landscape type of island are rectangular.
        Checks if all lines have same length as the first (base) line.
        If conditions are met, the method returns a list of strings in map_list.
        Parameters:
            geography_island_string: multilinestring of island map
        Returns: list of strings X: ['WWW', 'WLW', 'WWW']
        """

        map_list = []  # Converts multilinestring into a list of strings
        multi_line_string = geography_island_string.splitlines()
        multi_line_string = multi_line_string.split('\n')

        for row_num_string in multi_line_string:
            if not len(row_num_string) == len(multi_line_string()[0]):
                raise ValueError("The map of the island is not rectangular")
            else:
                map_list.append(row_num_string)

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

        return map_list  # list of strings

    def make_map(self, geography_island_string):
        """Create a dictionary from the multi- line string.
        Input is the multi- line string.
        Output is the island_map with;
        Key: Instance of cell (landscape type- 'Highland', 'Lowland', 'Desert', 'Water')
        Value: Coordinates in (x, y) tuple form. (1,1) is upper left corner
        Returns: dict where key: tuple, value: instance of landscape type
        """
        # se mer på denne metoden
        map_list = self.conditions_for_island_map_string(geography_island_string)

        island_map = {}

        coord_x = 1
        for line in map_list:
            coord_y = 1
            for type_landscape in line:
                island_map[(coord_x, coord_y)] = self.map_params_dict[type_landscape]()
                coord_y += 1
            coord_x += 1

        return island_map  # X: {(1,1): Water, (1,2): Water, ... , (2,2): Landscape}

if __name__=='__main__':
    geography_island_string = """WWW
    WLW
    WWW"""
    F = CreateIsland(geography_island_string)
    F.conditions_for_island_map_string()

