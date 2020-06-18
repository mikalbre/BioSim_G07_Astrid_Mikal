# -*- coding: utf-8 -*-

__author__ = 'Astrid Sedal, Mikal Breiteig'
__email__ = 'astrised@nmbu.no, mibreite@nmbu.no'

"""
File with classes for the different kinds of landscapes the map contains. 
"""

from biosim.animals import Carnivore, Herbivore
import random


class SingleCell:

    params_dict = None

    @classmethod
    def cell_parameter(cls, parameter, accessibility=None):
        """
        This method updates the values of available amount of fodder, f_max.

        Error raised if there are undefined parameters in the dictionary, or if values are
        illegal for the parameters.

        Parameters
        ----------
        parameter : dict
            Dictionary with class parameter
        accessibility : bool
            If animal can enter cell
        """

        if not isinstance(parameter, dict):
            raise TypeError("Parameter must be type dict")

        for param in parameter:
            if param in cls.params_dict:
                if param == 'f_max' and parameter[param] < 0:
                    raise ValueError("f_max cannot be negative")
            else:
                raise TypeError("This specific parameter not defined for this cell")
        cls.params_dict.update(parameter)


        accessibility_boolean = False
        if accessibility:
            if type(accessibility) is bool:
                accessibility_boolean = True
            else:
                raise ValueError('The only argument for passable is bool.')
        # if accessibility_boolean is True:
        #     cls.params = accessibility

    def __init__(self):
        """
        A superclass for the properties of a single cell on an island.
        The different types of landscape inherits from this class.
        Initializes the cell and creates empty lists for herbivores and carnivores.

        Attributes
        ----------
        self.available_fodder : float
        self.present_herbivores : list
        self.present_carnivore : list
        """

        self.available_fodder = 0
        self.present_herbivores = []
        self.present_carnivores = []

    def __repr__(self):
        """
        If instance is called, __repr__ will present it with a string.

        Returns
        -------
        string : chr
        """

        string = f'{type(self).__name__}'
        return string

    def animals_allocate(self, ini_animals):
        """
        Allocate herbivores and carnivores to its own list where it belongs.

        Parameters
        ----------
        ini_animals : dict
            Dictionary contain the species, age and weight of animal.
        Raises
        -------
        TypeError
        """

        for animal in ini_animals:
            species = animal["species"]
            age = animal["age"]
            weight = animal["weight"]
            if species == "Herbivore":
                self.present_herbivores.append(Herbivore(age, weight))
            elif species == "Carnivore":
                self.present_carnivores.append(Carnivore(age, weight))
            else:
                raise TypeError("This animal is not a valid animal")

    def eat(self):
        """
        First calls the fodder_regrow method to make fodder available, depends on
        type of landscape. Thereafter the feed_herb method is called and the herb
        gets to eat in random. Lastly, the carnivores get to eat the herbivores in a order
        decided by the animals of both species' fitness.
        """

        self.fodder_regrow()
        self.feed_herb()
        self.feed_carn_with_herb()

    def fodder_regrow(self):
        """
        Grows fodder. Amount of fodder decided by type of landscape.
        """

        pass

    def feed_herb(self):
        """
        Method to feed herbivores randomly with fodder.
        """

        random.shuffle(self.present_herbivores)
        for herb in self.present_herbivores:
            if self.available_fodder > 0:
                eaten = herb.feeding(self.available_fodder)
                self.available_fodder -= eaten

    def feed_carn_with_herb(self):
        """
        Method to feed carnivores with herbivores. Both species gets sorted based on each
        individual animals' fitness, carnivores from highest to lowest and herbivores from
        lowest to highest. Carnivores with highest fitness get to first try to kill the
        herbivore with the least amount of fitness.
        """

        self.present_herbivores = sorted(self.present_herbivores, key=lambda x: getattr(x, 'phi'))
        self.present_carnivores = sorted(self.present_carnivores, key=lambda x: getattr(x, 'phi'),
                                         reverse=True)

        for carn in self.present_carnivores:
            if len(self.present_herbivores) > 0:
                dead_herbs = carn.hunt_herb(self.present_herbivores)
                self.present_herbivores = list(set(self.present_herbivores) - set(dead_herbs))
                self.present_herbivores = sorted(self.present_herbivores,
                                                 key=lambda x: getattr(x, 'phi'))

    def procreation(self):
        """
        Checks if there are at least two other animal of the same species in this cell.
        If it is, an offspring might occur.
        """

        herb_newbord = []
        carn_newbord = []

        if len(self.present_herbivores) >= 2:
            for herbivores in self.present_herbivores:
                offspring = herbivores.procreation(len(self.present_herbivores))
                if not offspring:
                    continue
                herb_newbord.append(offspring)
            self.present_herbivores.extend(herb_newbord)


        if len(self.present_carnivores) >= 2:
            for carnivores in self.present_carnivores:
                offspring = carnivores.procreation(len(self.present_carnivores))
                if not offspring:
                    continue
                carn_newbord.append(offspring)
            self.present_carnivores.extend(carn_newbord)

    def migrate(self, neighboring_cells):
        """
        Input is the four adjacent cells. The method uses random.choice to choose a cell, if
        restrictions are not met. If the chosen cell is water, the animals will not migrate
        that year.

        Parameters
        ----------
        neighboring_cells : list

        Returns
        -------
        migrated_herb : list
        migrated_carn : list
        """

        migrated_herb = []
        migrated_carn = []

        for herb in self.present_herbivores:
            if not herb.has_migrated and herb.prob_migrate():
                chosen_cell = random.choice(neighboring_cells)
                new_loc = chosen_cell[0]
                landscape_type = chosen_cell[1]
                if isinstance(landscape_type, Water):
                    continue
                else:
                    migrated_herb.append((new_loc, herb))
            herb.set_migration_true()

        self.present_herbivores = [herb for herb in self.present_herbivores
                                   if herb not in migrated_herb]

        for carn in self.present_carnivores:
            if not carn.has_migrated and carn.prob_migrate():
                chosen_cell = random.choice(neighboring_cells)
                new_loc = chosen_cell[0]
                landscape_type = chosen_cell[1]
                if isinstance(landscape_type, Water):
                    continue
                else:
                    migrated_carn.append((new_loc, carn))
            carn.set_migration_true()

        self.present_carnivores = [carn for carn in self.present_carnivores
                                   if carn not in migrated_carn]

        return migrated_herb, migrated_carn

    def add_herb_migrated(self, herb):
        """
        Adds migrated herbs to the list of herbivores in this cell.
        Parameters
        ----------
        herb : object
        """

        self.present_herbivores.append(herb)

    def add_carn_migrated(self, carn):
        """
        Adds migrated carns to the list of carnivores in this cell.

        Parameters
        ----------
        carn : object
        """

        self.present_carnivores.append(carn)

    def remove_herb_migrated(self, herb):
        """
        Removes migrated herbs from the list of herbivores in this cell.

        Parameters
        ----------
        herb : object
        """

        self.present_herbivores.remove(herb)

    def remove_carn_migrated(self, carn):
        """
        Removes migrated carns from the list of carnivores in this cell.

        Parameters
        ----------
        carn : object
        """

        self.present_carnivores.remove(carn)

    def aging(self):
        """
        Method to increment age by 1 and decrease weight for every animal each year.
        """

        for herbivore in self.present_herbivores:
            herbivore.growing_older()

        for carnivore in self.present_carnivores:
            carnivore.growing_older()

    def animal_death(self):
        """
        Checks if animal dies. If it dies, the method removes the animal from the
        list of current animals.
        """

        self.present_herbivores = [herbivore for herbivore in self.present_herbivores if
                                   not herbivore.animal_dying()]

        self.present_carnivores = [carnivore for carnivore in self.present_carnivores if
                                   not carnivore.animal_dying()]

    def get_fodder(self):
        return self.available_fodder

    @property
    def num_herbivores(self):
        return len(self.present_herbivores)

    @property
    def num_carnivores(self):
        return len(self.present_carnivores)

    @property
    def num_animals(self):
        return self.num_herbivores + self.num_carnivores


class Highland(SingleCell):
    """
    The landscape type Highland is a sub-class of the superclass SingleCell.
    Highland has fodder.
    Fodder in Highland is less than fodder in Lowland.
    Carnivores can prey on herbivores in Highland.
    """

    accessibility = True
    params_dict = {"f_max": 300}

    def __init__(self):
        super().__init__()
        self.available_fodder = self.params_dict["f_max"]

    def fodder_regrow(self):
        """
        When called, the method restores the amount of available fodder to f_max.
        """

        self.available_fodder = self.params_dict["f_max"]


class Lowland(SingleCell):
    """
    The landscape type Lowland is a sub-class of the superclass SingleCell.
    Lowland has fodder.
    Carnivores can prey on herbivores in Highland.
    """

    accessibility = True
    params_dict = {"f_max": 800}

    def __init__(self):
        super().__init__()
        self.available_fodder = self.params_dict["f_max"]

    def fodder_regrow(self):
        """
        Restores the amount of available fodder to f_max when this method is called.
        """

        self.available_fodder = self.params_dict["f_max"]


class Desert(SingleCell):
    """
    The landscape type Desert is a sub-class of the superclass SingleCell.
    There is no fodder in Desert, so nothing to eat for herbivores.
    Carnivores can prey on herbivores in the Desert.
    """

    accessibility = True
    params = {"f_max": 0}

    def __init__(self):
        super().__init__()
        self.available_fodder = self.params["f_max"]

    def fodder_regrow(self):
        """
        Restores the amount of available fodder to f_max when this method is called.
        """

        self.available_fodder = self.params["f_max"]


class Water(SingleCell):
    """
    The landscape type Water is a sub-class of the superclass SingleCell.
    Water are passive cell because the animals can not enter.
    """

    accessibility = False
    params = {"f_max": 0}

    def __init__(self):
        super().__init__()
        self.available_fodder = self.params["f_max"]

    def fodder_regrow(self):
        """
        Restores the amount of available fodder to f_max when this method is called.
        """

        self.available_fodder = self.params["f_max"]


if __name__ == "__main__":
    random.seed(1)
    c = Lowland()
    poph = [{'species': 'Herbivore',
            'age': 5,
            'weight': 20} for _ in range(50)
            ]
    popc = [{'species': 'Carnivore',
            'age': 5,
             'weight': 20} for _ in range(20)
            ]
    c.params_dict= {'f_max': 800}
    print(f"fodder: {c.available_fodder}")
    c.animals_allocate(poph)
    # c.animals_allocate(popc)
    # print(f"num_an herb: {len(c.present_herbivores)}")
    # print(f"num_an carn: {len(c.present_carnivores)}")

    # if years == 50:
    c.animals_allocate(popc)


    for j in range(10):
        for years in range(200):
            c.eat()
            c.procreation()
            c.aging()
            c.animal_death()
        print("______ Etter syklus ______")
        print(f'Herb num: {len(c.present_herbivores)}')
        print(f'Carn num: {len(c.present_carnivores)}')

        #print(c.present_herbivores)
        #print(c.present_carnivores)
