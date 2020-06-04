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

        self.fitness = 0
        self.fitness_calculation()


    def fitness_calculation(self):
        """
        Calculate fitness of animal.
        Fitness depends on weight and age of animal.
        :return:
        """
        positive_q = (1/(1+exp(self.params["phi"]*(self.age() - self.params["a_half"]))))
        negative_q = (1/(1+exp(-self.params["phi"]*(self.weight - self.params["w_half"]))))

        if self.weight == 0:
            self.params["phi"] = 0
        else:
            self.params["phi"] = positive_q*negative_q
        return self.params["phi"]

    def fitness(self):
        """
        Calculate fitness if weight or age to animal is changed.

        :return:
        """
        if self.compute_fitness == True:
            if self.weight <= 0:
                return 0

        self.compute_fitness = False
        self.fitness = fitness_calculation()


    def age(self):
        """ Adds an increment of 1 to age, i.e. age increases by 1 each year."""
        self.age += 1
        self.fitness_calculation()


    def birth(self):
        """
        Whether an animal will give birth.
        If animal gives birth, weight decreases and return offspring.
        :return:
        """
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
        pass


