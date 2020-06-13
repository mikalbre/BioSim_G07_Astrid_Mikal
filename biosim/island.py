
from .landscape import SingleCell, Highland, Lowland, Desert, Water

class CreateIsland:

    map_params_dict = {"H": Highland,
                       "L": Lowland,
                       "D": Desert,
                       "W": Water}

    def __init__(self, geography_island_string, initial_population):
        """

        Parameters
        ----------
        geography_island_string: str
            Multilinestring of the geography_string of the map
        initial_population: dict
            key: Coordinates, Values: list of dict
        """
        self.len_map_x = None  # width of map
        self.len_map_y = None  # length of map
        self.year_num = 0  # years simulates

        # Makes the map based on the multi- line string passed in
        self.map = self.make_map(geography_island_string)  # simulation file
        # Passes in the population
        self.add_population(initial_population)  # simulation file

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

        map_list = []  # Converts multilinestring into a list og strings
        multilinesstring = geography_island_string.splitlines()

        for row_num_string in multilinesstring:
            if not len(row_num_string) == len(multilinesstring()[0]):
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

    def add_population(self, population):
        """Population is dict.
        Method feeds the dict to a cell by position.
        """
        #SingleCell.animals_allocate(population)

        for map_location in population:  # map_location: dict with loc
            loc = map_location["loc"]

            if loc not in self.map.keys():
                raise ValueError("Given location does not exist")

            if not self.map[loc].passable:  # NEI
                raise ValueError("The location is not passable")

            animals_dict = map_location["pop"]
            self.map[loc].animal_allocate(animals_dict)

    def new_year_reset(self):
        #remember that fodder gets regrown in feed_animals- method
        pass
    @property
    def year(self):
        return self.year_num

    # Trenger en setter for year???

    def feed_animals(self):
        """Iterate over each cell and use eat-method from landscape to make fodder grow, herb eat
        and carn eat herb. """
        for cell in self.map.values():
            cell.eat()

    def procreation_animals(self):
        """Iterate over each cell and use procreation- method from landscape to make both herb
        and carn procreate."""
        for cell in self.map.values():
            cell.procreation()

    def aging_animals(self):
        """Iterate over each cell and use aging method from landscape to increase age and decrease
        weight of both herb and carn."""
        for cell in self.map.values():
            cell.aging()

    def death_animals(self):
        """Iterate over each cell and use death-method from landscape to kill those her and carn
        who is suppose to die."""
        for cell in self.map.values():
            cell.animal_death()

    def simulate_one_year(self):
        """Simulate one year where we have an island consisting of different cells of
        four different landscape types, and use the methods above to simulate
        the ecosystem."""
        self.new_year_reset()
        self.feed_animals()
        self.procreation_animals()
        self.aging_animals()
        self.death_animals()
        self.year_num += 1



if __name__=='__main__':
    mls = """WWW
    WLW
    WWW"""
    F = CreateIsland(mls)
    F.conditions_for_island_map_string()
    print(F)

