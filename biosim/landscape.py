from animals import Herbivore, Carnivore
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
        self.present_carnivores = []

    def animals_allocate(self, animal_list):
        """
        Adds given animals of a given species to a given cell on the island.

        Parameters
        ----------
        animal_list

        Returns
        -------

        """
        for animal in animal_list:
            if animal is isinstance(animal, Herbivore):
                self.present_herbivores.append(animal)
            elif animal is isinstance(animal, Carnivore):
                self.present_carnivores.append(animal)

    def num_herb_in_cell(self):
        return len(self.present_herbivores)

    def num_carn_in_cell(self):
        return len(self.present_carnivores)

    def eat(self):  # herbivore feeding
        self.fodder_regrow()
        self.feed_herb()

    def fodder_regrow(self):
        """
        The method updates the amount of available food.

        evt Pass
        Returns
        -------

        """
        pass

    def feed_herb(self):
        random.shuffle(self.present_herbivores)
        for herb in self.present_herbivores:
            if self.available_fodder > 0:
                eaten = herb.feeding(self.available_fodder)
                self.available_fodder -= eaten

    def feed_carn_with_herb(self):
        pass

    def procreation(self):
        """
        Checks if there are at least two other animal of the same species in this cell
        and having proper weight for both
        then they will make a new offspring.
        Returns
        -------
        """

       # if self.num_herb_in_cell() >= 2 or self.num_carn_in_cell() >= 2:
            #herb_newborn = []
            #carn_newborn =[]

        herb_newborn = []
        if self.num_herb_in_cell() >= 2:
            for herbivores in self.present_herbivores:
                offspring = herbivores.procreation(self.num_herb_in_cell())
                if not offspring:
                    continue
                self.present_herbivores.append(offspring)
                herb_newborn.append(offspring)

        carn_newborn = []
        if self.num_carn_in_cell() >= 2:
            for carnivores in self.present_carnivores:
                offspring = carnivores.procreation(self.num_carn_in_cell())
                if not offspring:
                    continue
                self.present_carnivores.append(offspring)
                carn_newborn.append(offspring)

        return herb_newborn, carn_newborn

    def animal_death(self):
        self.present_herbivores = [herbivore for herbivore in self.present_herbivores if
                                   not herbivore.animal_dying()]

        self.present_carnivores = [carnivore for carnivore in self.present_carnivores if
                                   not carnivore.animal_dying()]

    def migrate(self):
        pass

    def get_fodder(self):
        return self.available_fodder

    def aging(self):
        for herbivore in self.present_herbivores:
            herbivore.growing_older()

        for carnivore in self.present_carnivores:
            carnivore.growing_older()


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
    c = Lowland()
    print(f"fodder: {c.get_fodder()}")
    h1 = Herbivore()
    h2 = Herbivore()
    h3 = Herbivore()
    h4 = Herbivore()
    h5 = Herbivore()
    h6 = Herbivore()
    h7 = Herbivore()
    h8 = Herbivore()
    c1 = Carnivore()
    h_list = [h1, h2, h3, h4, h5, h6, h7, h8, c1]
    c.animals_allocate(h_list)
    # print(f"num_an carn: {c.num_carn_in_cell}")
    # print(f"num_an herb: {c.num_herb_in_cell}")

    print("___________")
    print(c1.get_weight())
    c1.aging()
    print(c1.get_weight())
    print("___________")


    # print(f'Carn 1 (phi) = {c1.phi}')
    # print(f'Carn 1 (weight) = {c1.weight}')
    # print(f'Carn 1 (age) = {c1.age}')
    # c1.aging()
    # print(f'Carn 1 (age) = {c1.get_age()}')
    #

    print(f"h1_weight to h1: {h1.get_weight()}")
    c.eat()
    print(f"h1_weight to h1: {h1.get_weight()}")
    print(f"fodder: {c.get_fodder()}")
    print(f"num of animal: {c.num_herb_in_cell()}")
    c.animal_death()
    print(f"num of animal: {c.num_herb_in_cell()}")


#     print("______________")
#     print(c.num_herb_in_cell())
#     c.animal_death()
#     print(c.num_herb_in_cell())
#
#     print("______________")
#
#     print(c.num_herb_in_cell())
#     c.procreation()
#     print(c.num_herb_in_cell())
#
#
    # print("______________")
    # import timeit
    #
    # for j in range(10):
    #     for years in range(200):
    #         c.eat()
    #
    #         c.procreation()
    #         c.aging()
    #         c.animal_death()
    #
    #     print(c.num_herb_in_cell())
    #
    # print(timeit.timeit(number=1000))
