# -*- coding: utf-8 -*-

__author__ = 'Astrid Sedal, Mikal Breiteig'
__email__ = 'astrised@nmbu.no, mibreite@nmbu.no'

"""This file contains the Animal base class and child classes for herbivores and carnivores"""

from math import exp
import random
import numpy as np


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


    def __init__(self, age=0, weight=None):
        """

        :param age: int
            The age of the animal
        :param weight: float
            The weight of the animal
        """
        if age < 0:
            raise ValueError("The animal must have an age.")
        else:
            self.age = age

        if not isinstance(self.age, int):
            self.age = int(self.age)

        if weight is None:
            self.weight = self.gauss_dist(self.params["w_birth"], self.params["sigma_birth"])
            if self.weight < 0:
                self.weight = 0  # Dies at end of year
        elif weight is not None:
            self.weight = weight

        # sjekk dette
        self.alive = True
        self.has_migrated = False
        self.offspring = False  # Får denne inn i method procreation, offsprint = false??
        self.eaten = 0

        self.phi = 0
        self.fitness_calculation()


    @staticmethod
    def random_number():
        """
        Method for all the random.random() functions
        Returns
        -------

        """
        random_num = random.random()
        return random_num

    @staticmethod
    def gauss_dist(weight_birth, sigma_birth):
        """
        Draws birth weight of animals from Gaussian distribution.
        Parameters
        ----------
        weight_birth
        sigma_birth

        Returns
        -------

        """
        gauss_dist = random.gauss(weight_birth, sigma_birth)
        return gauss_dist

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
        positive_q = self.sigmoid(self.age, self.params["a_half"], self.params["phi_age"], 1)
        negative_q = self.sigmoid(self.weight, self.params["w_half"], self.params["phi_weight"], -1)

        if self.weight <= 0:
            self.phi = 0
        else:
            self.phi = positive_q * negative_q
        return self.phi

    def weight_loss_mother(self, xi):
        """
        Calculates how much weight the mother loses due to procreation.
        Parameters
        ----------
        xi

        Returns
        -------

        """
        weight_loss_mother = xi * self.gauss_dist
        return weight_loss_mother

    @staticmethod
    def prob_birth_offspring(gamma, phi, num_same_species):
        """
        Calculates probability for getting an offspring.
        Required to have more than one animal of the same species for offspring to be possible.
        Parameters
        ----------
        gamma
        phi
        num_same_species

        Returns
        -------

        """
        prob_birth_offspring = np.min(1, gamma * phi * (num_same_species - 1))
        return prob_birth_offspring

    def prob_of_procreation(self, num_same_species):
        """
        Checks if procreation will is possible or not.
        If procreation is possible, we direct to the procreation method.
        Parameters
        ----------
        num_same_species

        Returns
        -------

        """
        if self.prob_birth_offspring(self.params["gamma"], self.phi, num_same_species) and \
                self.weight > self.weight_loss_mother(self.params["xi"]):
            return self.procreation(num_same_species)

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
        """
        if self.random_number() <= self.prob_birth_offspring(self.params["gamma"], self.phi,
                                                             num_same_species):
            birth_weight = self.gauss_dist(self.params["w_birth"], self.params["sigma_birth"])
            self.weight -= self.weight_loss_mother(self.params["xi"])
            self.fitness_calculation()

            if isinstance(self, Herbivore):
                self.fitness_calculation()
                return Herbivore(0, birth_weight)

            # elif isinstance(self, Carnivore):
            #     self.fitness_calculation()
            #     return Carnivore(0, birth_weight)

    def prob_migrate(self):
        """
        Calculates the probability for the animal to migrate
        :return:
        """
        return self.params["mu"] * self.phi

    # def annual_age_increase(self):
    #     """
    #     Adds an increment of 1 to age, i.e. age increases by 1 each year.
    #     Recalculates the animal fitness because it depends on age.
    #     :return:
    #     """
    #     self.age += 1
    #     self.fitness_calculation()

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

    # def annual_weight_decrease(self):
    #     """
    #     Each year the weight of the animal decreases by the constants omega and eta.
    #     Recalculates the fitness of the animal because it's depending on the animal's weight.
    #     :return:
    #     """
    #     self.weight -= self.params["eta"] * self.weight
    #     self.fitness_calculation()

    @staticmethod
    def prob_of_dying(omega, phi):
        """
        Calculates the probability for the animal to die
        Parameters
        ----------
        omega
        phi

        Returns
        -------

        """
        prob_of_dying = omega * (1 - phi)
        return prob_of_dying

    def potential_death(self):
        """
        Calculate the probability of the animal dying
        :return:
        """
        if self.weight == 0:  # Phi or Weight is zero?
            self.alive = False

        elif self.phi == 1:
            self.alive = True

        else:
            prob_death = self.prob_of_dying(self.params["omega"], self.phi)
            self.alive = self.random_number() >= prob_death

        return self.alive

    def eat(self):
        """
        Fjerne?

        self.eaten += self.params['F']
        self.weight += self.params['F']
        self.fitness_calculation()
        return self.params['F']
        Parameters
        ----------
        amount

        Returns
        -------

        """
        pass

    def get_age(self):
        return self.age

    def get_weight(self):
        return self.weight

    def get_fitness(self):
        return self.phi

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
            raise ValueError("Available food in cell must be zero or a positive number.")

        elif self.params["F"] < available_food:
            self.weight += self.params["beta"] * self.params["F"]
            self.fitness_calculation()
            available_food -= self.params["F"]
            return available_food

        elif self.params["F"] >= available_food:
            self.weight = self.params["beta"] * available_food
            self.fitness_calculation()
            return 0





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




# class Carnivore(Animals):
#
#     params = {
#         'w_birth': 6.0,
#         'sigma_birth': 1.0,
#         'beta': 0.75,
#         'eta': 0.125,
#         'a_half': 40.0,
#         'phi_age': 0.3,
#         'w_half': 4.0,
#         'phi_weight': 0.4,
#         'mu': 0.4,
#         'gamma': 0.8,
#         'zeta': 3.5,
#         'xi': 1.1,
#         'omega': 0.8,
#         'F': 50.0,
#         'DeltaPhiMax': 0
#     }
#
