
from .landscape import Highland, Lowland, Desert, Water, PassedBounds

class Island:

    map_params_dict = {"H": Highland,
                       "L": Lowland,
                       "D": Desert,
                       "W": Water}

    def __init__(self, geography_island_string, initial_population):
        # geography_island is a multilinestring
        # specifies initial pop in each cell (list of dicts)

        self.num_years = 0

        self.population_animal = {}
        self.geogr = {}
        self.map = {}

        self.map_list = []  # This is where the multilinestring goes
        self.len_rows_map_list = 0
        self.len_columns_map_list = 0
        self.geography = geography_island_string
        self.initial_pop = initial_population

    def check_lines_of_map_geography(self):
        """Method to check whether the string of the landscape type of island are rectangular.
        Checks if all lines have same length as the first (base) line.
        If """

        for row_num_string in self.geography.splitlines():
            if not len(row_num_string) == len(self.geography.splitlines()[0]):
                raise ValueError("The map of the island is not rectangular")
            else:
                 self.map_list.append(row_num_string)
        return self.map_list  # stores the landscape type of the island in a list X:['WWW','WLW','WWW']



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
        # for row_index in range(len(self.geography[0])):
        #     if self.geography[0][row_index] is not "W" or self.geography[-1][row_index] is not "W":
        #         raise ValueError("The northern and southern cells on "
        #                          "the map must be of type water.")
        #
        # for row_index in range(len(self.geography)):
        #     if self.geography[row_index][0] is not "W" or self.geography[row_index][-1] is not "W":
        #         raise ValueError("The cells to the west and east must be of type water.")



    def create_dict_geography(self):
        """Geography string to a dict with coordinates as key and the type of landscape as value
        Coordinates: tuples of x- and y- coordinates.
        Takes the first row of multilinestring and converts it into coordinates, then do the same
        with the next line.
        """
        self.check_all_boundaries_are_water()
        self.check_lines_of_map_geography()

        # (0,0) is top left corner.
        cord_x = 0
        for line in self.geography.splitlines(): # columns
            cord_y = 0
            for type_of_landscape in line:  # rows
                self.geography[(cord_x), (cord_y)] = type_of_landscape  # X: (0,0),(0,1),(0,2), (1,0)..
                cord_y +=1
            cord_x += 1



    def create_dict_population(self):
        """List of population to a dict with coordinates as keys and lists of the animals properties
        at the location as values"""
        for cell in self.initial_pop:
            if cell["location"] in self.population_animal.keys():
                self.population_animal[cell["location"]].extend(cell["population"])
            else:
                self.population_animal[cell["location"]] = cell["population"]

    def add_new_population(self):
        """Adds new population to existing population"""
        pass



    def create_map_dict(self):
        """Creates new dict of entire island by iterating through the geography dict.
        The keys are coordinates and the landscape types are values.
        """
        self.create_geogr_dict()

        for location, type_of_landscape in self.geography.items():  # .items() returns the dict's key, value as tuple in a list
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






    def make_map(self, geography_island_string):

        island_map = {}
        map_lines = self.check_lines_of_map_geography()
        map_lines = self.check_all_boundaries_are_water()







    def add_population(self):
        """Add population of both herbivores and carnivores to the island."""
        map_
        pass

    def num_animals_on_island(self):
        pass

    def num_of_each_species_on_island(self):
        pass

    def ready_for_new_year(self):
        pass

    def feed(self):
        """Iterate over each cell and use eat-method from landscape to make fodder grow, herb eat
        and carn eat herb. """
        for cell in self.map_list:


    def procreation(self):
        """Iterate over each cell and use procreation- method from landscape to make both herb
        and carn procreate."""
        pass

    def aging_animals(self):
        """Iterate over each cell and use aging method from landscape to increase age and decrease
        weight of both herb and carn."""
        pass

    def death_animals(self):
        """Iterate over each cell and use death-method from landscape to kill those her and carn
        who is suppose to die."""
        pass

    def simulate_one_year(self):
        """Simulate one year where we have a simple island, and use the methods above to simulate
        the ecosystem."""
        pass






