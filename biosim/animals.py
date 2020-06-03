# -*- coding: utf-8 -*-

"This file contains the Animal base class and child classes for herbivores and carnivores"

class Animals():
    """
    Parent class
    """

    @classmethod
    def set_parameters(cls, w_birth=None, sigma_birth=None, beta=None, eta=None, a_half=None, phi_age=None,
                       w_half=None, phi_weight=None, mu=None, gamma=None, zeta=None, xi=None, omega=None,
                        F=None, DeltaPhiMax=None):
        """

        :param w_birth:
            average birth weight
        :param sigma_birth:
            std of birth weight
        :param beta:
            beta multiplied by fodder increases animal weight
        :param eta:
            eta multiplied by weight, decreases animal weight each year
        :param a_half:
            half age of Animals
        :param phi_age:
            scalar of age of fitness
        :param w_half:
            half weight of Animals
        :param phi_weight:
            scalar of weight of Animals
        :param mu:
            scalar for moving, animal moves with probability mu is multiplied with fitness
        :param gamma:
            scalar for birth, probability for birth
        :param zeta:
            scalar if birth will happen
        :param xi:
            Scalar for decrease in mother weight, decreases motherweight by zeta*birthweight
        :param omega:
            scalar for death, probability is omega*(1-fitness)
        :param F:
            Animals appetite, amount of food required for an animal in a year
        :param DeltaPhiMax:
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
