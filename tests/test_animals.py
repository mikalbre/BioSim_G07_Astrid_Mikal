"""Tests the animals.py file in the biosim folder."""

from biosim.animals import Animals, Herbivore
import pytest
from pytest import approx



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
    mocker.patch('random.gauss', return_value=5)

    herb = Herbivore(3, None)
    assert herb.gauss_dist(8, 1.5) == 5

def test_weight_loss_mother(mocker):
    mocker.patch('random.gauss', return_value=5)

    herb = Herbivore(2, 6)
    assert herb.weight_loss_mother(1.2) == 6


def test_prob_birth_offspring():
    pass


def test_prob_of_procreation():
    pass


def test_procreation():
    pass


def test_annual_age_increase():
    herbivore = Herbivore(3, 12)
    assert herbivore.age == 3

    herbivore.annual_age_increase()
    assert herbivore.age == 4


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
    assert herb.feeding(50) == 40
    assert herb.feeding(11) == 1
    assert herb.feeding(10) == 0


def test_annual_weight_decrease():
    herb = Herbivore(5, 40)
    herb.annual_weight_decrease()

    assert herb.weight < 40

def test_prob_of_dying():
    herb = Herbivore(5, 40)
    fitness = herb.fitness_calculation()
    prob_die = Herbivore.prob_of_dying(0.4, fitness)



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


