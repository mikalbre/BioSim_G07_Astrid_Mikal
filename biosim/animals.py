# -*- coding: utf-8 -*-

__author__ = 'Astrid Sedal, Mikal Breiteig'
__email__ = 'astrised@nmbu.no, mibreite@nmbu.no'

"""This file contains the Animal base class and child classes for herbivores and carnivores"""

from math import exp
import random
random.seed(1)


class Animals:
    # """
    # Animal parent class, i.e. all animals in the simulation must be subclasses of this parent class.
    # It represents a single animal, and does not specify the type of animal.
    # It contains methods, variables and properties that are common for both carnivore and herbivore.
    # """
    # params = None  # instead of setting all parameter equal to None
    #
    # ""@classmethod
    # def set_parameters(cls, params):
    #     """
    #     Takes a dictionary of parameter as input.
    #     :param params:
    #     :return:
    #     """
    #
    #     animal_set_parameters = cls.params.update()
    #
    #     for parameter in animal_set_parameters:
    #         if parameter in cls.params:
    #             if params[parameter] < 0:
    #                 raise ValueError(f"{parameter} cannot be negative.")
    #             if parameter == "DeltaPhiMax" and params[parameter] <= 0:
    #                 raise ValueError("DeltaPhiMax must be larger than zero")
    #             if parameter == "eta" and not 0 <= params[parameter] <= 1:
    #                 raise ValueError("Eta must be greater than zero and smaller than one")
    #         else:
    #             raise ValueError("Parameter not defined for this animal")""

    def __init__(self, age=0, weight=None):
        """

        :param age: int
            The age of the animal
        :param weight: float
            The weight of the animal
        """

        if age < 0 or age is float:
            raise ValueError("Age of animal must be positive and integer.")
        else:
            self.age = age

        if weight is None:
            self.weight = self.get_initial_weight_offspring()
        else:
            self.weight = weight

        # sjekk dette
        self.alive = True
        self.has_migrated = False
        self.eaten_amount = 0 

        self.phi = 0
        self.fitness_calculation()

    def set_migration_flag_true(self):
        self.has_migrated = True

    def set_migration_flag_False(self):
        self.has_migrated = False

    def __repr__(self):
        string = f'Type: {type(self).__name__}, Age: {self.get_age()}, Fitness: {self.phi}'
        return string

    def get_initial_weight_offspring(self):
        offspring_weight = random.gauss(self.params["w_birth"], self.params["sigma_birth"])
        return offspring_weight

    @staticmethod
    def sigmoid(x, x_half, phi_, p):
        """
        Used to calculate the fitness of the animal
        Parameters
        ----------
        x
        x_half
        phi_
        p

        Returns
        -------
        """

        sigmoid = (1/(1 + exp(p * phi_ * (x - x_half))))
        return sigmoid

    def fitness_calculation(self):
        """
        Calculate fitness of animal.
        Fitness depends on weight and age of animal.
        :return:
        """

        if self.weight <= 0:
            self.phi = 0
        else:
            q_age = self.sigmoid(self.age, self.params["a_half"], self.params["phi_age"], 1)
            q_weight = self.sigmoid(self.weight,
                                    self.params["w_half"], self.params["phi_weight"], -1)
            self.phi = q_age * q_weight
        return self.phi

    def procreation(self, num_same_species):
        """
        Calculates the probability of animal having an offspring.
        If only one animal of same species in a cell, the probability of
        offspring will be zero.
        Must be more than one animal in the cell to potensially create an offspring in the method.
        The offspring is of the same class as the parent animal. At birth the age of offspring
        is zero and its weight is calculated using gaussian distribution.

        How to implement maximum one child per animal?????

        At birth of offspring the parent animal looses weight relative to constant xi and the
        birthweight of offspring. Recalculates the parent animal's fitness after birth.

        :param num_same_species: int
            The amount of animals of the same species in a single cell.

        :return:
        offspring: Object
        """

        if (self.weight < self.params["zeta"] *
                (self.params["w_birth"] + self.params["sigma_birth"])):
            return

        if random.random() <= min(1, self.params["gamma"] * self.phi * (num_same_species - 1)):
            offspring = type(self)()
            self.weight -= self.params["xi"] * offspring.weight
            self.fitness_calculation()
            print(offspring)
            return offspring

    def prob_migrate(self):
        """
        Calculates the probability for the animal to migrate
        :return:
        """

        return self.params["mu"] * self.phi

    def growing_older(self):
        """
        When animals grows older the age increases by one and the weight decreases with a
        constant that is based on its weight.
        Returns
        -------

        """

        self.age += 1
        self.weight -= self.params["eta"] * self.weight
        self.fitness_calculation()

    def animal_dying(self):
        """
        Calculate the probability of the animal dying
        :return:
        """
        if self.weight == 0:
            return True
        elif random.random() < self.params["omega"] * (1 - self.phi):
            return True
        elif random.random() >= self.params["omega"] * (1 - self.phi):
            return False

    def get_age(self):
        return self.age

    def get_weight(self):
        return self.weight

    def get_fitness(self):
        return self.phi


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

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)

    def feeding(self, available_food):
        """
        Calculates amount of fodder the animal eats in current cell, and returns the
        amount of fodder remaining.
        If available food in cell is negative the method returns an error message.
        If F is less or equal to available fodder in cell, the weight increases by constant beta
        multiplied with the amount eated.
        If F is more than available fodder in cell, the weight increases by constant beta times the
        available fodder in cell.

        Due to the increase in weight, the fitness must be recalculated.

        :param available_food: float
            available fodder in cell
        :return: float
            remaining fodder in cell
        """

        if available_food < 0:
            self.eaten = 0
        else:
            self.eaten = min(self.params["F"], available_food)

        self.weight += self.params["beta"] * self.eaten
        self.fitness_calculation()
        return self.eaten


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
        'DeltaPhiMax': 10.0
    }

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)

    def hunt_herb(self, herbi_phi_sorted_list):

        del_herb = []
        for herb in herbi_phi_sorted_list:

            if self.phi <= herb.phi:
                kill_prob = 0
            elif self.phi - herb.phi < self.params["DeltaPhiMax"]:
                kill_prob = (self.phi - herb.phi) / (self.params["DeltaPhiMax"])
            else:
                kill_prob = 1

            if random.random() <= kill_prob:
                self.eaten_amount += min(self.params["F"], herb.weight)
                if self.eaten_amount > self.params["F"]:
                    break
                self.weight += self.params["beta"] * self.eaten_amount
                herb.alive = False
                del_herb.append(herb)
                self.fitness_calculation()

        return del_herb
