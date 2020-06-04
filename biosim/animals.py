# -*- coding: utf-8 -*-

__author__ = 'Astrid Sedal, Mikal Breiteig'
__email__ = 'astrised@nmbu.no, mibreite@nmbu.no'

"""This file contains the Animal base class and child classes for herbivores and carnivores"""

from math import exp
import random


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
        animal_set_parameters = cls.params.update()

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

    def __init__(self, age=None, weight=None):
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

    def age_increase(self):
        """ Adds an increment of 1 to age, i.e. age increases by 1 each year."""
        self.age += 1
        self.fitness_calculation()

    def procreation(self, number_of_animals_in_cell):
        """
        Calculates the probability of animal having an offspring.
        Must be more than one animal in the cell to potensially create an offspring in the method.
        The offspring is of the same class as the parent animal. At birth the age of offspring
        is zero and its weight is calculated using gaussian distribution.
        At birth of offspring the parent animal looses weight relative to constant xi and the birthweight of offspring.
        :return:
        """

        if self.weight < self.params["zeta"] * \
                (self.params["w_birth"] + self.params["sigma_birth"]):  # if mother weight less than offspring
            return
        else:
            prob_offspring_birth = self.params["gamma"] * self.phi * (number_of_animals_in_cell - 1) # number of animals in cell??

        if random.random() <= prob_offspring_birth:
            birth_weight  = random.gauss(self.params["w_birth"], self.params["sigma_birth"])
            self.weight -= self.params["xi"] * birth_weight

            if isinstance(self, Herbivore):
                self.fitness_calculation()
                return Herbivore(0, birth_weight)
            elif isinstance(self, Carnivore):
                self.fitness_calculation()
                return Carnivore(0, birth_weight)


    def get_real_propensity(self, cell):
        """
        The method calulates realtive abundance of animals potensial destination.
        """
        fodder = 0
        if type(self) == Herbivore:
            fodder = cell.f
        elif type(self) == Carnivore:
        fodder = cell.total_w_herbivores


    def get_propensity(self, cell):
    """
    Calculate propensity of animals potensial destination.

    """
    rel_abundance = self.get_real_abundance()





    def movable(self):
        """
        Check if animal will move from current cell to new destination cell
        :return: Boolean value, True for move and False for stay in cell
        """
        prob_move = self.params["mu"] * self.phi
        if random.random() <= prob_move:
            return True
        else:
            return False

    def migrate(self, current_cell, neighbouring_cells):
        """
        If animal move, the method decides which cell to move to.
        :return: Boolean value, True for move and False for stay in cell
        """

class Herbivore(Animals):
    """

    """
    params = {
        'w_birth': 8.0,
        'sigma_birth': 1.5,
        'beta': 0.9,
        'eta': 0.05,
        'a_half': 40.0,
        'phi_age': 0.2,
        'w_half': 10.0,
        'phi_weight': 0.1,
        'mu': 0.25,
        'gamma': 0.2,
        'zeta': 3.5,
        'xi': 1.2,
        'omega': 0.4,
        'F': 10.0,
    }
    def __init__(self, age, weight):
        super().__init__(age, weight)

class Carnivore(Animals):

    params = {
        'w_birth': 6.0,
        'sigma_birth': 1.0,
        'beta': 0.75,
        'eta': 0.125,
        'a_half': 40.0,
        'phi_age': 0.3,
        'w_half': 4.0,
        'phi_weight': 0.4,
        'mu': 0.4,
        'gamma': 0.8,
        'zeta': 3.5,
        'xi': 1.1,
        'omega': 0.8,
        'F': 50.0,
        'DeltaPhiMax': 0
    }







