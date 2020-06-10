from animals import Herbivore, Carnivore
from numpy import random
import random
from operator import itemgetter, attrgetter

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



    def animals_allocate(self, animal_h):
        """
        Adds given animals of a given species to a given cell on the island.

        Parameters
        ----------
        animal_list

        Returns
        -------

        """
        #        #Except
        for animal in animal_h:
            species = animal["species"]
            age = animal["age"]
            weight = animal["weight"]
            if species == "Herbivore":
                self.present_herbivores.append(Herbivore(age, weight))
            if species == "Carnivore":
                self.present_carnivores.append(Carnivore(age, weight))

        # for animal in h_list:
        #     species = animal["species"]
        #     age = animal["age"]
        #     weight = animal["weight"]
        #     if species == "Carnivore":
        #         self.present_carnivores.append(Carnivore(age, weight))


    def num_herb_in_cell(self):
        return len(self.present_herbivores)

    def num_carn_in_cell(self):
        return len(self.present_carnivores)

    def eat(self):  # herbivore feeding
        self.fodder_regrow()
        self.feed_herb()
        self.feed_carn_with_herb()

    def fodder_regrow(self):
        pass

    def feed_herb(self):
        random.shuffle(self.present_herbivores)
        for herb in self.present_herbivores:
            if self.available_fodder > 0:
                eaten = herb.feeding(self.available_fodder)
                self.available_fodder -= eaten

    # def phi_sorted_list(self, list_to_sort):
    #     #self.present_herbivores = sorted(self.present_herbivores, key=attrgetter('phi'))
    #     phi_sorted_list_herb = sorted(self.present_herbivores, key=lambda x: getattr(x, 'phi'))
    #     phi_sorted_list_carn = sorted(self.present_carnivores, key=lambda x: getattr(x, 'phi'), reverse=True)
    #     return phi_sorted_list_herb, phi_sorted_list_carn


    def feed_carn_with_herb(self):
        self.present_herbivores = sorted(self.present_herbivores, key=lambda x: getattr(x, 'phi'))
        self.present_carnivores = sorted(self.present_carnivores, key=lambda x: getattr(x, 'phi'),
                                         reverse=True)
        for carn in self.present_carnivores:
            self.present_herbivores = list(set(self.present_herbivores) - set(carn.hunt_herb(self.present_herbivores)))
        return

    def procreation(self):
        """
        Checks if there are at least two other animal of the same species in this cell
        and having proper weight for both
        then they will make a new offspring.
        Returns
        -------
        """

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
    import numpy as np
    np.random.seed(1)
    c = Lowland()
    poph = [{'species': 'Herbivore',
            'age': 5,
            'weight': 20} for _ in range(50)
            ]
    popc = [{'species': 'Carnivore',
            'age': 5,
             'weight': 20} for _ in range(20)
            ]


    print(f"fodder: {c.get_fodder()}")
    # h1 = Herbivore()
    # h2 = Herbivore()
    # h3 = Herbivore()
    # h4 = Herbivore()
    # h5 = Herbivore()
    # h6 = Herbivore()
    # h7 = Herbivore()
    # h8 = Herbivore()
    # c1 = Carnivore()
    # h_list = [h1, h2, h3, h4, h5, h6, h7, h8, c1]
    # h_list = [Herbivore(), Herbivore(), Carnivore()]
    c.animals_allocate(poph)
    c.animals_allocate(popc)
    print(f"num_an herb: {c.num_herb_in_cell()}")
    print(f"num_an carn: {c.num_carn_in_cell()}")
    print(c.present_herbivores)
    print(c.present_carnivores)


    for j in range(4):
        for years in range(2):
            c.eat()
            c.feed_carn_with_herb()
            c.procreation()
            c.aging()
            c.animal_death()
            print("______ Etter syklus ______")
            print(f'Herb: {c.num_herb_in_cell()}')
            print(f'Carn: {c.num_carn_in_cell()}')

    print(c.present_herbivores)
    print(c.present_carnivores)

