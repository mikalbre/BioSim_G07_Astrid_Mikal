from .animals import Animals, Herbivore
import numpy as np
from numpy import random

class SingleCell:
    """
    A superclass for the properties of a single cell on an island.
    The different types of landscape inherits from this class.


    f_max: Max amount of available food in cell. Cannot be negative.
    alpha: Regrowth of fodder constant. Alpha is how much a cell is able to regrow each year.

    """
    params = {'f_max': 0}

    @classmethod
    def cell_parameters(cls, parameters):
        """
        This method updates the values of available amount of fodder, f_max.

        Error raised if there are undefined parameters in the dictionary, or if values are
        illegal for the parameters.
        Parameters
        ----------
        parameters
            Dictionary containing f_max and alpha

        Returns
        -------

        """
        for iterators in parameters:
            if iterators in cls.params:
                if iterators == 'f_max' and parameters[iterators] < 0:
                    raise ValueError("f_max cannot be negative")
                cls.params[iterators] = parameters[iterators]
            else:
                raise ValueError("This specific parameter not defined for this cell")

    def __init__(self):
        self.available_fodder = 0
        self.present_herbivores = []
        self.fodder_left = 0
        self.herb = Animals()

    def fodder_regrow(self):
        """
        The method updates the amount of available food.
        Zero is the given default value of regrowth.
        Returns
        -------

        """
        self.available_fodder += 0

    def randomise_list(self):
        random_list = self.present_herbivores.copy()
        np.random.shuffle(random_list)
        return random_list

    def animals_eat(self):  # herbivore feeding
        randomized_order = self.randomise_list()
        for herb in randomized_order:
            if self.available_fodder >= herb.get_F():
                self.available_fodder -= herb.eat()

    def procreation(self):
        """
        Checks if there are at least one other animal of the same species in this cell
        and having proper weight for both
        then they will make a new offspring.
        Returns
        -------
        """
        for herb in self.present_herbivores:
            newborn_weight = herb.initial_weight()
            if herb.prob_birth_offspring(len(self.present_herbivores), newborn_weight):
                self.create_new_animal(newborn_weight)

    def create_new_animal(self, newborn_weight):
        new_animal = Animals(weight=newborn_weight)
        self.present_herbivores.append(new_animal)

    def animal_death(self):
        pass

    def migrate(self):
        pass

    def get_fodder(self):
        return self.available_fodder

    def get_num_animals(self):
        return len(self.present_herbivores)



class Highland(SingleCell):
    """
    The landscape type Highland is a sub-class of the superclass Cell.
    Highland has fodder.
    Fodder in Highland is less than fodder in Lowland.
    Carnivores can prey on herbivores in Highland.
    """
    params = {"f_max": 300}

    def __init__(self):
        super().__init__()
        self.available_fodder = self.params["f_max"]

    def fodder_regrow(self):
        """
        When called, the method restores the amount of available fodder to f_max
        Returns
        -------

        """
        self.available_fodder = self.params["f_max"]


class Lowland(SingleCell):
    """
    The landscape type Lowland is a sub-class of the superclass Cell.
    Lowland has fodder.
    Carnivores can prey on herbivores in Highland.
    """
    params = {"f_max": 800}

    def __init__(self):
        super().__init__()
        self.available_fodder = self.params["f_max"]

    def fodder_regrow(self):
        """
        Restores the amount of available fodder to f_max when this method is called
        Returns
        -------

        """
        self.available_fodder = self.params["f_max"]


class Desert(SingleCell):
    """
    The landscape type Desert is a sub-class of the superclass Cell.
    There is no fodder in Desert, so nothing to eat for herbivores.
    Carnivores can prey on herbivores in the Desert.
    """

    def __init__(self):
        super().__init__()


class Water(SingleCell):
    """
    The landscape type Water is a sub-class of the superclass Cell.
    Water are passive cell because the animals can not enter.
    """
    def __init__(self):
        super().__init__()

class PassedBounds:
    """
    Makes sure no animal can go beyond the map created.
    Can not add animals to this cell, and no animal can access it.
    """
    pass
