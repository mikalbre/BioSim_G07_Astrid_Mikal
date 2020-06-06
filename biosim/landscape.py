
from .animals import Animals, Herbivore
import numpy as np
from numpy import random

class Cell:
    """

    """
    def __init__(self):
        self.herbivore_list = []
        self.available_fodder = 0

    def place_animals(self):
        pass

    def random_list(self):
        random_list = self.herbivore_list.copy()
        np.random.shuffle(random_list)
        return random_list

    def eat(self):
        randomize_eat = self.random_list()
        for animal in randomize_eat:
            pass

    def procreation(self):
        if 

    def offspring(self):
        pass

    def migrate(self):
        pass

    def get_fodder(self):
        pass

    def get_num_animals(self):
        pass

class Highland(Cell):
    pass

class Lowland(Cell):
    pass

class Desert(Cell):
    pass

class Water(Cell):
    pass

class Single_Cell:
    """
    f_max: Max amount of available food in cell. Cannot be negative.
    alpha: Regrowth of fodder constant. Alpha is how much a cell is able to regrow each year.

    """

    params = {'f_max': 0, 'alpha'}

    @classmethod
    def cell_parameters(cls, parameters):
        """
        This method updates the values of available amount of fodder,f_max, and the regrowth
        constant alpha.
        Parameters
        ----------
        parameters
            Dictionary containing f_max and alpha

        Returns
        -------

        """
        for iterators in parameters:
            if iterators in cls.params:
                if iterators == 'f_max' and params[iterators] < 0:













