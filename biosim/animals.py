# -*- coding: utf-8 -*-

__author__ = 'Astrid Sedal, Mikal Breiteig'
__email__ = 'astrised@nmbu.no, mibreite@nmbu.no'

"""This file contains the Animal base class and child classes for herbivores and carnivores"""

from math import exp


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
        """

        :param age: int
        :param weight: float
        """
        if age is None:
            raise ValueError("The animal can not have age less then zero")
        else:
            self.age = age

        if weight is None:
            raise ValueError("The animal can not have negative weight")
        else:
            self.weight = weight

        self.alive = True
        self.has_migrated = False
        self.compute_fitness = True

        self.phi = 0
        self.fitness_calculation()

        self.reprod_weight = 


    def fitness_calculation(self):
        """
        Calculate fitness of animal.
        Fitness depends on weight and age of animal.
        :return:
        """
        positive_q = (1/(1+exp(self.phi*(self.age - self.params["a_half"]))))
        negative_q = (1/(1+exp(-self.phi*(self.weight - self.params["w_half"]))))

        if self.weight == 0:
            self.phi = 0
        else:
            self.phi = positive_q*negative_q
        return self.phi

    def age(self):
        """ Adds an increment of 1 to age, i.e. age increases by 1 each year."""
        self.age += 1
        self.fitness_calculation()

    def procreation(self):
        """
        Calculates the probability of animal having an offspring.
        Must be more than one animal in the cell to potensially create an offspring.
        :return:
        """
        offspring_weight = self.params["zeta"] * \
                                  (self.params["w_birth"] + self.params["sigma_birth"])
        if self.weight < prob_birth_to_offspring:  # if mother weight less than offspring
            return
        else:
            prob_offspring = self.params["gamma"]*self.phi*(n_animals_in_cell - 1)

        if random.random() <= pr


class Herbivore(Animals):
    """

    """
    params = {
        'w_birth': 8.0,
        'sigma_birth': 1.5,
        'beta': 0.9,
        'eta': 0.05,
        'a_half': 40,
        'phi_age': 0.2,
        'w_half': 10,
        'phi_weight': 0.1,
        'mu': 0.25,
        'lambda_animal': 1,
        'gamma': 0.2,
        'zeta': 3.5,
        'xi': 1.2,
        'omega': 0.4,
        'F': 10,
    }
    def __init__(self, age, weight):
        super().__init__(age, weight)

