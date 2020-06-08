"""Tests the animals.py file in the biosim folder."""

from biosim.animals import Animals, Herbivore
import pytest
from pytest import approx
import numpy as np

@pytest.fixture
def set_parameters(request):
    Animals.set_parameters(request.param)
    yield
    Animals.set_parameters(Animals.params)


def test_init():
    herb = Herbivore(5, 3)
    assert herb.age == 5
    assert herb.weight >= 0

    isinstance(herb.age, int)


def test_get_initial_weight(mocker):
    mocker.patch('random.gauss', return_value=5)

    herb = Herbivore(3, None)
    assert herb.get_initial_weight_offspring() == 5


# def test_weight_loss_mother(mocker):
#     mocker.patch('random.gauss', return_value=5)
#
#     herb = Herbivore(2, 6)
#     assert herb.weight_loss_mother(1.2) == 6

def test_fitness_calculation():
    herb = Herbivore(6, 0)
    assert herb.phi == 0

    herb = Herbivore(2, 13)
    assert not herb.phi == 0

    herb = Herbivore(0, 5)
    assert approx(herb.phi) == 0.377414

    herb = Herbivore(6, -3)
    assert herb.phi == 0

def test_feeding():
    herb = Herbivore(5, 3)
    assert herb.feeding(50) == 10
    assert herb.feeding(10) == 10
    assert herb.feeding(5) == 5
    assert herb.feeding(0) == 0
    assert herb.feeding(-5) == 0

    weight_before = herb.weight
    herb.feeding(10)
    weight_after = herb.weight
    assert weight_before < weight_after

def test_procreation(mocker):
    herb = Herbivore(4, 30)
    herb_born = herb.procreation(1)
    assert herb_born is None

    herb = Herbivore(4, 30)
    weight = herb.weight
    lose_weight = herb.params["zeta"] * (herb.params["w_birth"] + herb.params["sigma_birth"]) #33.25
    assert weight < lose_weight
    assert herb.procreation(10) is None

    herb = Herbivore(5, 40)
    mocker.patch('random.gauss', return_value=5)
    assert herb.get_initial_weight_offspring() == 5

def test_migrate(mocker):
    herb = Herbivore(0, 5)
    phi = herb.fitness_calculation()
    assert herb.params['mu'] * phi == approx(0.0943535)


def test_growing_older():
    herbivore = Herbivore(3, 12)
    assert herbivore.age == 3
    assert herbivore.weight == 12

    herbivore.growing_older()
    assert herbivore.age == 4
    assert herbivore.weight == 11.4


def test_prob_of_dying():
    herb = Herbivore(5, 40)
    fitness = herb.fitness_calculation()
    prob_die = Herbivore.dying(0.4, fitness)



# def test_prob_of_procreation():
#     herb = Herbivore(3, 2)
#     prob_of_procreation = herb.prob_of_procreation(0.2, 8, 1.5)
#     assert approx(prob_of_procreation) == 1.9



def test_potential_death():
    herb = Herbivore(3, 0)
    assert herb.alive
    herb.potential_death()
    assert not herb.alive

    immortal_herb = Herbivore(2, 100)
    immortal_herb.potential_death()
    assert immortal_herb.alive


def test_herbi_sim():
    pass


