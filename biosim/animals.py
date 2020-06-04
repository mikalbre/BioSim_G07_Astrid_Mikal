# -*- coding: utf-8 -*-

"""This file contains the Animal base class and child classes for herbivores and carnivores"""

class Animals:
    """
    Animal parent class, i.e. all animals in the simulation must be subclasses of this parent class.
    It represents a single animal, and does not specify the type of animal.
    It contains methods, variables and properties that are common for both carnivore and herbivore.
    """
    params = None  # instead of setting all parameters equal to None

    @classmethod
    def set_parameters(cls, params):
        """
        Takes a dictionary of parameters as input.
        :param params:
        :return:
        """
        animal_set_parameters = params.update()

        for iterator in animal_set_parameters:
            if iterator in cls.params:
                if params[iterator] < 0:
                    raise ValueError(f"{iterator} cannot be negative.")
                if iterator == "DeltaPhiMax" and params[iterator] <= 0:
                    raise ValueError("DeltaPhiMax must be larger than zero")
                if iterator == "eta" and not 0 <= params[iterator] <= 1:
                    raise ValueError("Eta must be greater than zero and smaller than one")

            else:
                raise ValueError("Parameter not defined for this animal")  # DeltaPhiMax for carni


    def __init__(self, age, weight):
        """"""
        pass

    def birth(self):
        """
        Whether an animal will give birth.
        If animal gives birth, weight decreases and return offspring.
        :return:
        """
        pass

    def age(self):
        """ Adds an increment of 1 to age, i.e. age increases by 1 each year."""
        pass

    def weight(self):
        """ """
        pass

    def decrease_weight(self):
        """
        Weight of animal decreases passively each year.
        Annual weight loss

        :return:
        """
        pass

    def fitness(self):
        """
        Calculate fitness if weight or age to animal is changed.

        :return:
        """
        pass

    def feed(self):
        """
        Animal eats food in cell.
        Weight of animal gets update.
        Returns new amount of fodder left in cell

        :return:
        """
        pass

    def can_migrate(self):
        """
        If animal has not moved to new cell, it calculates whether it will move or not.

        :return:
        """
        pass
    def death(self):
        """
        Whether an animal dies is calculated by probability.
        Fitness = 0, animal will die.

        :return:
        """



class herbivores(Animals):
    params = {'w_birth': 8.0,
                          'sigma_birth': 1.5,
                          'beta': 0.9,
                          'eta': 0.05,
                          'a_half': 40,
                          'phi_age': 0.6,
                          'w_half': 10,
                          'phi_weight': 0.1,
                          'mu': 0.25,
                          'gamma': 0.2,
                          'zeta': 3.5,
                          'xi': 1.2,
                          'omega': 0.4,
                          'F': 10,
                          'DeltaPhiMax': None} # slette DeltaPhiMax?




class carnivores(Animals):
    pass



   """
        Sets the class parameters and check if input is in the right format.

        :param w_birth: float
            average birth weight
        :param sigma_birth: float
            std of birth weight
        :param beta: float
            beta multiplied by fodder increases animal weight
        :param eta: float
            eta multiplied by weight, decreases animal weight each year
        :param a_half: float
            Age component of fitness calculation, scalar
        :param phi_age: float
            Age component of fitness calculation, scalar
        :param w_half: float
            Weight component of fitness calculation, scalar
        :param phi_weight: float
            Weight component of fitness calculation, scalar
        :param mu: float
            scalar for moving, animal moves with probability mu is multiplied with fitness
            Constant for the probability of migrating
        :param gamma: float
            scalar for birth, probability for birth
            Probability of birth constant
        :param zeta: float
            scalar if birth will happen
            Probability constant for birth relative to weight
        :param xi: float
            Scalar for decrease in mother weight, decreases motherweight by zeta*birthweight
        :param omega: float
            scalar for death, probability is omega*(1-fitness)
            Death probability factor, scalar
        :param F: float
            Animals appetite, amount of food required for an animal in a year
            Maximum food capacity
        :param DeltaPhiMax: float
            Used by carnivore to calculate if they can kill a herbivore.
            Maximum difference in fitness between carnivore and herbivore.

        :return:
    """

w_birth = 8.0
sigma_birth = 1.5
beta = 0.9
eta = 0.05
a_half = 40
phi_age = 0.6
w_half = 10
phi_weight = 0.1
mu = 0.25
gamma = 0.2
zeta = 3.5
xi = 1.2
omega = 0.4
F = 10.0