"""Tests the animals.py file in the biosim folder."""

from biosim.animals import Animals, Herbivore
import pytest


@pytest.fixture
def set_parameters(request):
    Animals.set_parameters(request.param)
    yield
    Animals.set_parameters(Animals.params)


def test_init():
    herb = Herbivore(5, 40)

    assert herb.age == 5
    assert herb.weight == 40


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


def test_annual_weight_decrease():
    herb = Herbivore(5, 40)
    herb.annual_weight_decrease()

    assert herb.weight < 40


def test_procreation():
    herb = Herbivore(4, 30)
    





