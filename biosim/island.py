
from biosim.landscape import SingleCell, Highland, Lowland, Desert, Water


def check_length_of_string(map_list):
    if not all(len(map_list[0]) == len(line) for line in map_list[1:]):
        return False
    return True

class CreateIsland:

    map_params_dict = {"H": Highland,
                       "L": Lowland,
                       "D": Desert,
                       "W": Water}

    def __init__(self, geography_island_string):

        self.year_num = 0  # years simulates

        # Makes the map based on the multi- line string passed in
        self.map = self.make_map()  # simulation file
        # Passes in the population
        # self.add_population(initial_population)  # simulation file


    @staticmethod
    def condition_for_island_map_string():
        """Method to check whether the string of the landscape type of island are rectangular.
        Checks if all lines have same length as the first (base) line.
        If conditions are met, the method returns a list of strings in map_list.
        Parameters:
            geography_island_string: multilinestring of island map
        Returns: list of strings X: ['WWW', 'WLW', 'WWW']
        """

        geography_island_string_map = geography_island_string.strip()
        map_list = geography_island_string_map.split('\n')

        if not self.check_length_of_string(map_list):
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



    def boundaries_all_water(self):
        """Checks if all boundaries in the given multi-line- string is Water."""

        map_list = self.condition_for_island_map_string()

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

        return map_list


    def make_map(self):
        """Create a dictionary from the multi- line string.
        Input is the multi- line string.
        Output is the island_map with;
        Key: Instance of cell (landscape type- 'Highland', 'Lowland', 'Desert', 'Water')
        Value: Coordinates in (x, y) tuple form. (1,1) is upper left corner
        Returns: dict where key: tuple, value: instance of landscape type
        """
        # se mer på denne metoden
        map_list = self.conditions_for_island_map_string(self.geography_island_string)

        island_map = {}

        coord_x = 1
        for line in map_list:
            coord_y = 1
            for type_landscape in line:
                island_map[(coord_x, coord_y)] = self.map_params_dict[type_landscape]()
                coord_y += 1
            coord_x += 1

        return island_map  # X: {(1,1): Water, (1,2): Water, ... , (2,2): Lowland}


if __name__=='__main__':
    geography_island_string = """WWW
    WLW
    WWW"""
    F = CreateIsland(geography_island_string)
    F.conditions_for_island_map_string()

