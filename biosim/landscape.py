from animals import Animals, Herbivore
from numpy import random
import random


class SingleCell:
    """
    A superclass for the properties of a single cell on an island.
    The different types of landscape inherits from this class.


    f_max: Max amount of available food in cell. Cannot be negative.
    alpha: Regrowth of fodder constant. Alpha is how much a cell is able to regrow each year.

    """
    params = None

    @classmethod
    def cell_parameters(cls, parameters):
        """
        This method updates the values of available amount of fodder, f_max.

        Error raised if there are undefined parameters in the dictionary, or if values are
        illegal for the parameters.
        Parameters
        ----------
        parameters
            Dictionary containing f_max

        Returns
        -------

        """
        if not isinstance(parameters, dict):
            raise TypeError("Parameter must be type dict")

        for iterators in parameters:
            if iterators in cls.params:
                if iterators == 'f_max' and parameters[iterators] < 0:
                    raise ValueError("f_max cannot be negative")
                cls.params[iterators] = parameters[iterators]
            else:
                raise ValueError("This specific parameter not defined for this cell")

        cls.params.update(parameters)

    def __init__(self):
        self.available_fodder = 0
        self.present_herbivores = []

    def animals_allocate(self, animals):
        """
        Adds given animals of a given species to a given cell on the island.
        Parameters
        ----------
        animals: list
            List of instances of a given species.
        """
        pass

    def num_herb(self):
        return len(self.present_herbivores)

    def fodder_regrow(self):
        """
        The method updates the amount of available food.
        Zero is the given default value of regrowth.

        evt Pass
        Returns
        -------

        """
        pass

    def randomise_herb(self): # sett direkte inn
        return random.shuffle(self.present_herbivores)

    def eat(self):  # herbivore feeding
        self.fodder_regrow()
        self.feed_herb()

    def feed_herb(self):
        random.shuffle(self.present_herbivores)
        for herb in self.randomise_herb():  # sett in random.shuffle() direkte inn
            if self.available_fodder > 0:
                eaten = herb.feeding(self.available_fodder)
                self.available_fodder -= eaten

    def procreation(self):
        """
        Checks if there are at least two other animal of the same species in this cell
        and having proper weight for both
        then they will make a new offspring.
        Returns
        -------
        """
        herb_newborn = []
        number_of_herbivores_in_cell = self.num_herb()
        if number_of_herbivores_in_cell >= 2:
            for herbivores in self.present_herbivores:
                new_herb_offspring = herbivores.birth_check()  # Endre til .procreation()
                if not new_herb_offspring:
                    continue
                herb_newborn.append(new_herb_offspring)
                self.present_herbivores.extend(herb_newborn)

    def animal_death(self):
        dead_herbi = []
        for herbivore in self.present_herbivores:
            if herbivore.potential_death():
                dead_herbi.remove(self.present_herbivores)  # ikke ta ting ut av løkke

    def migrate(self):
        pass

    def get_fodder(self):
        return self.available_fodder


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


if __name__ == "__main__":
    a = Herbivore()
    c = Lowland()
    c.present_herbivores.append()
