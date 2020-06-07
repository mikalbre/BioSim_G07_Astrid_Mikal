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



class TestAnimal:

    @pytest.fixture()
    def create_herbivore(self):
        herb = Herbivore(5, 10)
        return herb

    def test_positive_input(self, create_herbivore):
        assert create_herbivore.age > 0 and (create_herbivore.weight > 0)

    def test_animals_age_weight(self):
        herbivore = Herbivore()
        herbivore.age = 20
        assert herbivore.age == 20
        herbivore.age += 10
        assert herbivore.age == 30

    def test_positive_fitness(self, create_herbivore):
        assert create_herbivore.fitness_calculation() > 0

    def test_herbivore_weight_increase(self, create_herbivore):
        weight_herb = create_herbivore.weight
        weight_herb_inc = create_herbivore.feeding(30)
        assert weight_herb < weight_herb_inc

    def test_herbivore_reproduce_weight_dec(self, mocker):
        herb = Herbivore(2, 50)
        prev_weight_herb = herb.weight
        mocker.patch('numpy.random.random', return_value=0)
        herb.procreation(5)

        assert herb.weight < prev_weight_herb

    def test_animal_procreation_baby_weight_positive(self, mocker):
        herb = Herbivore(2, 40)
        mocker.patch("random.random()", return_value=0)
        baby_herb = herb.procreation(10)
        assert baby_herb.weight > 0


    def test_init(self):
        herb = Herbivore(5, 3)

        assert herb.age == 5
        assert herb.weight >= 0

        isinstance(herb.age, int)

    def test_gauss(mocker):
        mocker.patch('random.gauss', return_value=5)
        herb = Herbivore(3, None)
        assert herb.gauss_dist(8, 1.5) == 5

    def test_annual_age_increase(self):
        herbivore = Herbivore(3, 12)
        assert herbivore.age == 3

        herbivore.annual_age_increase()
        assert herbivore.age == 4

    def test_fitness_calculation(self):
        herb = Herbivore(6, 0)
        assert herb.phi == 0

        herb = Herbivore(5, 19)
        assert not herb.phi == 0

        herb = Herbivore(6, -3)
        assert herb.phi == 0

        herb = Herbivore(0, 5)
        assert approx(herb.phi) == 0.377414

        # Slette?
        test_animal = Animals()
        old_fitness = test_animal.fitness_calculation()
        test_animal.eat(50)
        new = test_animal.fitness_calculation()
        assert old_fitness < new

    def test_feeding(self):
        herb = Herbivore(5, 3)
        assert herb.feeding(50) == 40
        assert herb.feeding(11) == 1
        assert herb.feeding(10) == 0

    def test_annual_weight_decrease(self):
        herb = Herbivore(5, 40)
        herb.annual_weight_decrease()
        assert herb.weight < 40

        herb = Herbivore(0, 1)
        herb.annual_weight_decrease()
        assert not herb.weight == 12
        assert herb.weight == 0.98

    def test_prob_of_dying(self):
        herb = Herbivore(5, 40)
        fitness = herb.fitness_calculation()
        prob_die = Herbivore.prob_of_dying(0.4, fitness)

    def test_prob_of_procreation(self):
        herb = Herbivore(3, 2)
        prob_of_procreation = herb.prob_of_procreation(0.2, 8, 1.5)
        assert approx(prob_of_procreation) == 1.9

    def test_potential_death(self):
        herb = Herbivore(3, 0)
        assert herb.alive
        herb.potential_death()
        assert not herb.alive

        immortal_herb = Herbivore(2, 100)
        immortal_herb.potential_death()
        assert immortal_herb.alive






