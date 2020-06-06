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

    def fodder_regrow(self):
        """
        The method updates the amount of available food.
        Zero is the given default value of regrowth.
        Returns
        -------

        """
        self.available_fodder += 0


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
