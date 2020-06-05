"""Tests the animals.py file in the biosim folder."""

from biosim.animals import Animals, Herbivore
import pytest
from pytest import approx
# import pytest_mock
# from unittest import mock


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

def test_gauss(mocker):
    mocker.patch('random.gauss', return_val=5)
    h = Herbivore(3, None)
    assert h.weight == 5




def test_annual_age_increase():
    herbivore = Herbivore(3, 12)
    assert herbivore.age == 3

    herbivore.annual_age_increase()
    assert herbivore.age == 4


def test_fitness_calulation():
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
    assert herb.feeding(50) == 40
    assert herb.feeding(11) == 1
    assert herb.feeding(10) == 0


def test_annual_weight_decrease():
    herb = Herbivore(5, 40)
    herb.annual_weight_decrease()

    assert herb.weight < 40

def test_prob_of_birth():
    herb = Herbivore(3, 2)
    prob_of_birth = herb.prob_of_birth(0.2, 8, 1.5)
    assert approx(prob_of_birth) == 1.9


def test_procreation():
    pass


def test_potential_death():
    herb = Herbivore(3, 0)
    assert herb.alive
    herb.potential_death()
    assert not herb.alive

    immortal_herb = Herbivore(2, 100)
    immortal_herb.potential_death()
    assert immortal_herb.alive


def test_prob_of_birth():
    h = Herbivore(0, 2)
    ppp = h.prob_of_birth(0.2, 8, 1.5)
    assert approx(ppp) == 1.9


def test_gauss_dist():
    a = Animals()
    g = a.gauss_dist(1.5, 0.25)
    assert g