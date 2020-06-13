from biosim.animals import Carnivore, Herbivore
import random

class SingleCell:
    """
    A superclass for the properties of a single cell on an island.
    The different types of landscape inherits from this class.

    f_max: Max amount of available food in cell. Cannot be negative.
    alpha: Regrowth of fodder constant. Alpha is how much a cell is able to regrow each year.

    """

    params = None  # {}

    @classmethod
    def cell_parameter(cls, parameter):
        """
        This method updates the values of available amount of fodder, f_max.

        Error raised if there are undefined parameters in the dictionary, or if values are
        illegal for the parameters.
        Parameters
        ----------
        parameter
            Dictionary containing f_max

        Returns
        -------

        """

        # if not isinstance(parameter, dict):
        #     raise TypeError("Parameter must be type dict")
        #
        # #cls.params.update(parameter)  # Trenger?
        #
        # for iterators in parameter:
        #     if iterators in cls.params:
        #         if iterators == 'f_max' and parameter[iterators] < 0:
        #             raise ValueError("f_max cannot be negative")
        #     else:
        #         raise ValueError("This specific parameter not defined for this cell")
        #
        if not isinstance(parameter, dict):
            raise TypeError("Parameter must be type dict")

        for param in parameter:
            if param in cls.params:
                if param == 'f_max' and parameter[param] < 0:
                    raise ValueError("f_max cannot be negative")
                cls.params[param] = parameter[param]
            else:
                raise ValueError("This specific parameter not defined for this cell")
        cls.params.update(parameter)

    def __init__(self):
        self.available_fodder = 0
        self.present_herbivores = []
        self.present_carnivores = []

    def animals_allocate(self, ini_animals):
        """Allocate herbivores and carnivores to its own list where it belongs.
        ini_animal is a list of dice. Dictionary contain the species, age and weight of animal."""

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


    @property
    def num_herbivores(self):
        return len(self.present_herbivores)

    @property
    def num_carnivores(self):
        return len(self.present_carnivores)

    @property
    def num_animals(self):
        return self.num_herbivores + self.num_carnivores

    def eat(self):
        """First calls the fodder_regrow- method to make fodder available, depends on
        type of landscape. Thereafter the feed_herb- method is called and the herb
        gets to eat in random. Lastly, the carnivores get to eat the herbivores in a order
        decided by the animals of both species' fitness."""
        self.fodder_regrow()
        self.feed_herb()
        self.feed_carn_with_herb()

    def fodder_regrow(self):
        """Grows fodder. Amount of fodder descided by type of landscape."""
        pass

    def feed_herb(self):
        """Method to feed herbivores randomly with fodder."""

        random.shuffle(self.present_herbivores)
        for herb in self.present_herbivores:
            if self.available_fodder > 0:
                eaten = herb.feeding(self.available_fodder)
                self.available_fodder -= eaten

    def feed_carn_with_herb(self):
        """Method to feed carnivores with herbivores. Both species gets sorted based on each
        individual animals' fitness, carnivores from highest to lowest and herbivores from
        lowest to highest. Carnivores with highest fitness get to first try to kill the
        herbivore with the least amount of fitness."""

        self.present_herbivores = sorted(self.present_herbivores, key=lambda x: getattr(x, 'phi'))
        self.present_carnivores = sorted(self.present_carnivores, key=lambda x: getattr(x, 'phi'),
                                         reverse=True)

        for carn in self.present_carnivores:
            self.present_herbivores = list(set(self.present_herbivores) -
                                               set(carn.hunt_herb(self.present_herbivores)))
        return

        # for carn in self.present_carnivores:
        #     if len(self.present_herbivores) == 0:
        #         break
        #     else:
        #         self.present_herbivores = list(set(self.present_herbivores) -
        #                                        set(carn.hunt_herb(self.present_herbivores)))
        #         self.present_herbivores = sorted(self.present_herbivores,
        #                                          key=lambda x: getattr(x, 'phi'))  # Men nye kan ikke dø første året?

    def procreation(self):
        """
        Checks if there are at least two other animal of the same species in this cell.
        If it is, an offspring might happen."""

        herb_newbord = []
        if len(self.present_herbivores) >= 2:
            for herbivores in self.present_herbivores:
                offspring = herbivores.procreation(len(self.present_herbivores))
                if not offspring:
                    continue
                self.present_herbivores.append(offspring)
                herb_newbord.append(offspring)

        carn_newbord = []
        if len(self.present_carnivores) >= 2:
            for carnivores in self.present_carnivores:
                offspring = carnivores.procreation(len(self.present_carnivores))
                if not offspring:
                    continue
                self.present_carnivores.append(offspring)
                carn_newbord.append(carn_newbord)

            return herb_newbord, carn_newbord

    def migrate(self):
        pass

    def aging(self):
        """Method to increment age by 1 and decrease weight for every animal."""
        for herbivore in self.present_herbivores:
            herbivore.growing_older()

        for carnivore in self.present_carnivores:
            carnivore.growing_older()

    def animal_death(self):
        """Checks if animal dies. If it dies, the method removes the animal from the
        list of current animals."""
        self.present_herbivores = [herbivore for herbivore in self.present_herbivores if
                                   not herbivore.animal_dying()]

        self.present_carnivores = [carnivore for carnivore in self.present_carnivores if
                                   not carnivore.animal_dying()]

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
    params = {"f_max": 0}

    def __init__(self):
        super().__init__()


class Water(SingleCell):
    """
    The landscape type Water is a sub-class of the superclass Cell.
    Water are passive cell because the animals can not enter.
    """
    params = {"f_max": 0}

    def __init__(self):
        super().__init__()


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

    print(f"fodder: {c.get_fodder()}")
    # poph = [{'species': 'Herbivore', 'age': 5, 'weight': 20},
    #         {'species': 'Herbivore', 'age': 5, 'weight': 20},
    #         {'species': 'Herbivore', 'age': 5, 'weight': 20}]
    # popc = [{'species': 'Carnivore', 'age': 5, 'weight': 20},
    #         {'species': 'Carnivore', 'age': 5, 'weight': 20},
    #         {'species': 'Carnivore', 'age': 5, 'weight': 20}]

    c.animals_allocate(poph)
    #c.animals_allocate(popc)
    print(f"num_an herb: {len(c.present_herbivores)}")
    print(f"num_an carn: {len(c.present_carnivores)}")
    # print(c.present_herbivores)
    # print(c.present_carnivores)

    for j in range(1):
        for years in range(250):
            if years == 50:
                c.animals_allocate(popc)
            c.eat()
            # print(f"Fodder_after_eating: {c.available_fodder}")
            # print(f"num_herb: {len(c.present_herbivores)}")
            # print(f"num_carn: {len(c.present_carnivores)}")  # looks like carn can procreate

            c.procreation()  # carn not procreate, herb does
            # print(f"num_herb_proc: {len(c.present_herbivores)}")
            # print(f"num_carn_proc: {len(c.present_carnivores)}")  # looks like carn can procreate

            c.aging()

            c.animal_death()  # works for herb, carns has []
            # print(f"num_herb_d: {len(c.present_herbivores)}")
            # print(f"num_carn_d: {len(c.present_carnivores)}")  # looks like carn can procreate

            print("______ Etter syklus ______")
            print(f'Herb: {len(c.present_herbivores)}')
            print(f'Carn: {len(c.present_carnivores)}')

        print(c.present_herbivores)
        print(c.present_carnivores)

