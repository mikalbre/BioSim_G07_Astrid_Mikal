
from .landscape import Highland, Lowland, Desert, Water, PassedBounds
from .animals import Herbivore, Carnivore

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
        self.len_map_x = None
        self.len_map_y = None
        self.num_years = 0

        self.map_island_coord = {}
        self.population_animal = {}
        self.map = {}

        self.geography_string = geography_island_string  # geography_island is a multilinestring
        self.initial_pop = initial_population  # specifies initial pop in each cell (list of dicts)

        self.map_list = []  # This is where the multilinestring goes
        self.len_rows_map_list = 0
        self.len_columns_map_list = 0

    def check_lines_of_geography_island_string(self):  # if lines are equal length
        """Method to check whether the string of the landscape type of island are rectangular.
        Checks if all lines have same length as the first (base) line.
        If they are """

        for row_num_string in self.geography_string.splitlines():
            if not len(row_num_string) == len(self.geography_string.splitlines()[0]):
                raise ValueError("The map of the island is not rectangular")
            else:
                self.map_list.append(row_num_string)
        return self.map_list  # save landscape type of island in a list    X: ['WWW', 'WLW', 'WWW']

    def check_all_boundaries_are_water(self):  # @classmethod??
        """Checks that all outer cells are ocean."""

        for row_num in range(len(self.map_list)):  # iterates through each line in the list
            if row_num == 0:  # Checks if first line is all Water
                for element_in_line in self.map_list[row_num]:  # Iterates through each landscape type in the line and sees if all are water
                    if element_in_line is not "W":
                        raise ValueError("The most northern cells of island has to be Water")

            elif 0 < row_num < (len(self.map_list) - 1):  # Checks if the middle lines are water first and last in the line
                if self.map_list[row_num][0] is not "W":  # Water in first column
                    raise ValueError("All the cells east of the island has to be Water")
                elif self.map_list[row_num][-1] is not "W":  # Water is last column
                    raise ValueError("All the cells west of the island has to be Water")

            else:
                for element_in_line in self.map_list[row_num]:
                    if element_in_line is not "W": # Water in last row
                        raise ValueError("The southern cells of island has to be Water")

        # Same code as above, just simpler
        # for row_index in range(len(self.geography_string[0])):
        #     if self.geography_string[0][row_index] is not "W" or self.geography_string[-1][row_index] is not "W":
        #         raise ValueError("The northern and southern cells on "
        #                          "the map must be of type water.")
        #
        # for row_index in range(len(self.geography_string)):
        #     if self.geography_string[row_index][0] is not "W" or self.geography_string[row_index][-1] is not "W":
        #         raise ValueError("The cells to the west and east must be of type water.")

        # Same as above, but more compact!
        # first_line_north = map_of_lines[0]
        # last_line_south = map_of_lines[-1]
        # first_column_west = [line[0] for line in map_of_lines]
        # last_column_east = [line[-1] for line in map_of_lines]
        #for landscape_type in (first_line_north + last_line_south):
        #   if not landscape_type == 'W':
        #       raise ValueError("Cells in both north and south must consist of water!")
        #for landscape_type in (first_line_west + last_line_east):
        #   if not landscape_type == 'W':
        #       raise ValueError("Cells in west and east must consist of water!")

    def create_dict_geography(self):  # make_map
        """Geography string to a dict with coordinates as key and the type of landscape as value
        Coordinates: tuples of x- and y- coordinates.
        Takes the first row of multilinestring and converts it into coordinates, then do the same
        with the next line.
        Key: coordinates (x,y)
        Value: type of landscape ('L', 'H', 'D', 'W')
        """
        self.check_all_boundaries_are_water()
        self.check_lines_of_geography_island_string()

        # (1,1) is top left corner.
        cord_x = 1
        for line in self.geography_string.splitlines():
            cord_y = 1
            for type_of_landscape in line:
                self.map_island_coord[(cord_x, cord_y)] = type_of_landscape  # X: (1,1),(1,2),(1,3), (2,1).. assigns a coordinate to the type of landscape
                cord_y += 1
            cord_x += 1

    def create_dict_population(self):
        """Create dictionary from a list of population.
        key: coordinates (x,y)
        Value: list of the animals properties at the cell (species, age, weight)
        """

        for cell in self.initial_pop:
            if cell["loc"] in self.population_animal.keys():
                self.population_animal[cell["loc"]].extend(cell["pop"])
            else:
                self.population_animal[cell["loc"]] = cell["pop"]

    def add_new_population(self, new_pop):
        """Adds new population to existing population"""
        new_population = {}
        for population_info in new_pop:
            new_population[population_info]["loc"] = population_info["pop"]

        for location, population in new_population.items():
            for info_animal in new_pop:
                if info_animal["species"] == "Carnivore":
                    self.map_island_coord[location].\
                        present_carnivores.append(Carnivore(info_animal))
                else:
                    self.map_island_coord[location].\
                        present_herbivores.append(Herbivore(info_animal))

    def create_map_dict(self):
        """Creates new dict of entire island by iterating through the geography_string dict.
        The keys are coordinates and the landscape types are values.
        """
        self.create_dict_geography()
        self.create_dict_population()

        for location, type_of_landscape in self.map_island_coord.items():  # .items() returns the dict's key, value as tuple in a list

            if type_of_landscape is "L":

                if location in self.population_animal.keys(): # if self.population_animals["location"]:
                    self.map[location] = Lowland(self.population_animal[location])
                else:
                    self.map[location] = Lowland([])  # Empty list

            if type_of_landscape is "H":

                if location in self.population_animal.keys():  # if self.population_animals["location"]:
                    self.map[location] = Highland(self.population_animal[location])
                else:
                    self.map[location] = Highland([])  # Empty list

            if type_of_landscape is "D":

                if location in self.population_animal.keys():  # if self.population_animals["location"]:
                    self.map[location] = Desert(self.population_animal[location])
                else:
                    self.map[location] = Desert([])  # Empty list

            if type_of_landscape is "W":

                if location in self.population_animal.keys():  # if self.population_animals["location"]:
                    self.map[location] = Water(self.population_animal[location])
                else:
                    self.map[location] = Water([])  # Empty list

    def add_population(self):
        """Add population of both herbivores and carnivores to the island."""
        pass

    def feed_animals(self):
        """Iterate over each cell and use eat-method from landscape to make fodder grow, herb eat
        and carn eat herb. """
        for type_landscape in self.map.values():
            type_landscape.eat()

    def procreation_animals(self):
        """Iterate over each cell and use procreation- method from landscape to make both herb
        and carn procreate."""
        for type_landscape in self.map.values():
            type_landscape.procreation()

    def aging_animals(self):
        """Iterate over each cell and use aging method from landscape to increase age and decrease
        weight of both herb and carn."""
        for type_landscape in self.map.values():
            type_landscape.aging()

    def death_animals(self):
        """Iterate over each cell and use death-method from landscape to kill those her and carn
        who is suppose to die."""
        for type_landscape in self.map.values():
            type_landscape.animal_death()

    def simulate_one_year(self):
        """Simulate one year where we have an island consisting of different cells of
        four different landscape types, and use the methods above to simulate
        the ecosystem."""
        self.feed_animals()
        self.procreation_animals()
        self.aging_animals()
        self.death_animals()
