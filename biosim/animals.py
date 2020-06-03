# -*- coding: utf-8 -*-

"""This file contains the Animal base class and child classes for herbivores and carnivores"""

class Animals():
    """
    Animal superclass, i.e. all animals in the simulation must be subclasses of this parent class.
    Represents a single animal.
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


    @classmethod
    def set_parameters(cls, w_birth=None, sigma_birth=None, beta=None, eta=None, a_half=None,
                       phi_age=None, w_half=None, phi_weight=None, mu=None, gamma=None, zeta=None,
                       xi=None, omega=None, F=None, DeltaPhiMax=None):
        """

        :param w_birth: float
            average birth weight
        :param sigma_birth: float
            std of birth weight
        :param beta: float
            beta multiplied by fodder increases animal weight
        :param eta: float
            eta multiplied by weight, decreases animal weight each year
        :param a_half: float
            half age of Animals
        :param phi_age: float
            scalar of age of fitness
        :param w_half: float
            half weight of Animals
        :param phi_weight: float
            scalar of weight of Animals
        :param mu: float
            scalar for moving, animal moves with probability mu is multiplied with fitness
        :param gamma: float
            scalar for birth, probability for birth
        :param zeta: float
            scalar if birth will happen
        :param xi: float
            Scalar for decrease in mother weight, decreases motherweight by zeta*birthweight
        :param omega: float
            scalar for death, probability is omega*(1-fitness)
        :param F: float
            Animals appetite, amount of food required for an animal in a year
        :param DeltaPhiMax: float
            Used by carnivore to calculate if they can kill a herbivore.

        :return:
        """


    def __init__(self):
        """"""
        pass

    def birth(self):
        """"""
        pass

    def age(self):
        """"""
        pass

    def weight(self):
        """"""
        pass

    def decrease_weight(self):
        """"""
        pass

    def fitness(self):
        """"""
        pass

    def feed(self):
        """"""
        pass

    def can_migrate(self):
        """"""
        pass






class herbivores(Animals):
    pass

class carnivores(Animals):
    pass
