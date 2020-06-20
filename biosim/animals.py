# -*- coding: utf-8 -*-

__author__ = 'Astrid Sedal, Mikal Breiteig'
__email__ = 'astrised@nmbu.no, mibreite@nmbu.no'

"""
This file contains the Animal base class and child classes for herbivores and carnivores
"""

from math import exp
import random


class Animals:

    params_dict = None

    @classmethod
    def set_parameters(cls, params):
        """
        Takes a dictionary of parameter as input.
        Checks for invalid values of parameters.
        Set class parameters.

        Parameters
        ----------
        params : dict
            Dictionary with class parameters.

        Raises
        -------
        ValueError
        """
        # cls.params_dict.update(params)
        for parameter in params:
            # cls.params_dict.update(params)
            if parameter in cls.params_dict:
                if params[parameter] < 0:
                    raise ValueError(f"{parameter} cannot be negative.")
                if parameter == "DeltaPhiMax" and params[parameter] <= 0:
                    raise ValueError("DeltaPhiMax must be larger than zero")
                if parameter == "eta" and not 0 <= params[parameter] <= 1:
                    raise ValueError("Eta must be greater than zero and smaller than one")
                cls.params_dict.update(params)
            else:
                raise ValueError("Parameter not defined for this animal")

    def __init__(self, age=0, weight=None):
        """
        Animal parent class, i.e. all animals in the simulation must be subclasses of
        this parent class.
        It represents a single animal, and does not specify the type of animal.
        It contains methods, variables and properties that are common for both carnivore
        and herbivore.

        Initialises instance. If weight not specified, weight is determine from the gaussian
        distribution.

        Parameters
        ----------
        age : int
            The age of the animal
        weight : float
            The weight of the animalo

        Attributes
        ----------
        self.age : int
        self.weight : float
        self.alive : bool
        self.has_migrated : bool
        self.eaten : int, float
        self.phi : float
        """

        if age < 0 or age is float:
            raise ValueError("Age of animal must be positive and integer.")
        else:
            self.age = age

        if weight is None:
            self.weight = self.get_initial_weight_offspring()
        else:
            self.weight = weight

        self.alive = True
        self.has_migrated = False
        self.eaten = 0

        self.phi = 0
        self.fitness_calculation()

    def __repr__(self):
        """
        If instance is called, __repr__ will present it with a string.

        Returns
        -------
        string : chr
        """

        string = f'Type: {type(self).__name__}, Age: {self.get_age()}, Fitness: {self.phi}'
        return string

    def get_initial_weight_offspring(self):
        """
        Draws the weight of an animal from a gaussian distribution.

        Returns
        -------
        offspring_weight : float
        """

        offspring_weight = random.gauss(self.params_dict["w_birth"],
                                        self.params_dict["sigma_birth"])
        return offspring_weight

    @staticmethod
    def sigmoid(x, x_half, phi_, p):
        """
        Calculates components for the fitness of the animal.

        Parameters
        ----------
        x : Age or weight component of the fitness calculation
        x_half : Age or weight component of the fitness calculation
        phi_ : Age or weight component of the fitness calculation
        p : Determines whether positive or negative element

        Returns
        -------
        sigmoid : float
        """

        sigmoid = (1/(1 + exp(p * phi_ * (x - x_half))))
        return sigmoid

    def fitness_calculation(self):
        """
        Calculates the fitness of the animal.
        Fitness depends on weight and age of animal.

        Returns
        -------
        phi : float
        """

        if self.weight <= 0:
            self.phi = 0
        else:
            q_age = self.sigmoid(self.age,
                                 self.params_dict["a_half"], self.params_dict["phi_age"], 1)
            q_weight = self.sigmoid(self.weight,
                                    self.params_dict["w_half"], self.params_dict["phi_weight"], -1)
            self.phi = q_age * q_weight

        return self.phi

    def procreation(self, num_same_species):
        """
        Calculates the probability of animal having an offspring.

        Must be more than one animal in the cell to potentially create an offspring in the method.
        The offspring is of the same class as the parent animal. At birth the age of offspring
        is zero and its weight is calculated using gaussian distribution.

        At birth of offspring the parent animal looses weight relative to constant xi and the
        birth weight of offspring. If the conditions are met, the method will recalculate
        the parent animal fitness after birth.

        Parameters
        ----------
        num_same_species : int
            The amount of animals of the same species in a single cell.

        Returns
        -------
        offspring : Object
        """

        if (self.weight < self.params_dict["zeta"] *
                (self.params_dict["w_birth"] + self.params_dict["sigma_birth"])):
            return

        if random.random() <= min(1, self.params_dict["gamma"] * self.phi * (num_same_species - 1)):
            offspring = type(self)()
            self.weight -= self.params_dict["xi"] * offspring.weight
            self.fitness_calculation()
            return offspring

    def prob_migrate(self):
        """
        Calculates the probability for the animal to migrate to new cell.

        Returns
        -------
        bool
        """

        if self.has_migrated is False:
            return bool(random.random() < self.params_dict["mu"] * self.phi)
        return False

    def set_migration_true(self):
        """
        Flags migration for animal in cell as True.
        """

        self.has_migrated = True

    def set_migration_false(self):
        """
        Flags migration for animal in cell as False.
        """

        self.has_migrated = False

    def growing_older(self):
        """
        When animals grows older the age increases by one and the weight decreases with a
        constant that is based on its weight. Then recalculates the fitness.
        """

        self.age += 1
        self.weight = self.weight - (self.params_dict["eta"] * self.weight)
        self.fitness_calculation()

    def animal_dying(self):
        """
        Calculate if the animal dies or not.

        Returns
        -------
        bool
        """

        if self.weight == 0:
            return True
        elif random.random() < self.params_dict["omega"] * (1 - self.phi):
            return True
        elif random.random() >= self.params_dict["omega"] * (1 - self.phi):
            return False

    def get_age(self):
        return self.age

    def get_weight(self):
        return self.weight

    def get_fitness(self):
        return self.phi


class Herbivore(Animals):
    """
    The subclass Herbivore inheritance from the parent class Animal.
    """

    params_dict = {
        'w_birth': 8.0,
        'sigma_birth': 1.5,
        'beta': 0.9,
        'eta': 0.05,
        'a_half': 40.0,
        'phi_age': 0.6,
        'w_half': 10.0,
        'phi_weight': 0.1,
        'mu': 0.25,
        'gamma': 0.2,
        'zeta': 3.5,
        'xi': 1.2,
        'omega': 0.4,
        'F': 10.0,
    }

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)

    def feeding(self, available_food):
        """
        Calculates amount of fodder the animal eats in current cell.

        If F is less or equal to available fodder in cell, the weight increases by constant beta
        multiplied with the amount eaten.
        If F is more than available fodder in cell, the weight increases by constant beta times the
        available fodder in cell.

        Due to the increase in weight, the fitness must be recalculated.

        Parameters
        ----------
        available_food : float

        Returns
        -------
        self.eaten : float
            The eaten amount for a herbivore.
        """

        if available_food < 0:
            self.eaten = 0
        else:
            self.eaten = min(self.params_dict["F"], available_food)

        self.weight += self.params_dict["beta"] * self.eaten
        self.fitness_calculation()

        return self.eaten


class Carnivore(Animals):
    """
    The subclass Herbivore inheritance from the parent class Animal.
    """

    params_dict = {
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
        'DeltaPhiMax': 10.0
    }

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)

    def hunt_herb(self, herb_phi_sorted_list):
        """
        The method has all the herbivore in currents cell sorted by fitness as input.
        If the animal eat, the animal eats a herbivore. The weight of the carnivore will increase
        and the fitness is recalculated.

        Parameters
        ----------
        herb_phi_sorted_list : list
            Increasing fitness.

        Returns
        -------
        dead_herbs : list
            List of herbivore(s) eaten by a single carnivore
        """

        self.eaten = 0
        dead_herbs = []
        weight_killed_herb = 0

        for herb in herb_phi_sorted_list:
            if self.phi <= herb.phi:
                kill_prob = 0
            elif (self.phi - herb.phi) < self.params_dict["DeltaPhiMax"]:
                kill_prob = (self.phi - herb.phi) / (self.params_dict["DeltaPhiMax"])
            else:
                kill_prob = 1

            if random.random() <= kill_prob:
                eat = min(herb.weight, self.params_dict["F"] - weight_killed_herb)
                self.weight += self.params_dict["beta"] * eat
                herb.alive = False
                self.fitness_calculation()
                dead_herbs.append(herb)
                weight_killed_herb += eat

                if weight_killed_herb >= self.params_dict["F"]:
                    return dead_herbs

        return dead_herbs
