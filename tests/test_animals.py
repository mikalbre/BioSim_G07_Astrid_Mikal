"""Tests the animals.py file in the biosim folder."""

from biosim.animals import Animals, Herbivore, Carnivore
import pytest
from pytest import approx


class Test_Animals:
    @pytest.fixture
    def set_parameters(request):
        Animals.set_parameters(request.param)
        yield
        Animals.set_parameters(Animals.params)

    def test_init(self):
        herb = Herbivore(5, 3)
        isinstance(herb.age, int)
        assert herb.age == 5
        assert herb.weight >= 0

        with pytest.raises(ValueError):
            Animals(Carnivore(-2, None))

    def test_get_initial_weight(self, mocker):
        mocker.patch('random.gauss', return_value=5)

        herb = Herbivore(3, None)
        assert herb.get_initial_weight_offspring() == 5

        carn = Carnivore(2, None)
        assert carn.get_initial_weight_offspring() == 5

    def test_sigmoid(self):


    def test_fitness_calculation(self):
        herb = Herbivore(6, 0)
        assert herb.phi == 0

        herb = Herbivore(2, 13)
        assert not herb.phi == 0

        herb = Herbivore(0, 5)
        assert approx(herb.phi) == 0.377414

        herb = Herbivore(6, -3)
        assert herb.phi == 0

    def test_procreation(self, mocker):
        herb = Herbivore(4, 30)
        herb_born = herb.procreation(1)
        assert herb_born is None

        carn = Carnivore(4, 30)
        carn_born = carn.procreation(1)
        assert carn_born is None

        herb = Herbivore(4, 30)
        weight = herb.weight
        lose_weight = herb.params["zeta"] * (herb.params["w_birth"] + herb.params["sigma_birth"]) #33.25
        assert weight < lose_weight
        for _ in range(10):
            procreation = herb.procreation(10)
            assert procreation is None

        herb = Herbivore(5, 40)
        herb.procreation(2)
        mocker.patch('random.gauss', return_value=5)
        new_weight = herb.weight - herb.params["xi"] * herb.get_initial_weight_offspring()
        assert new_weight == 34

    def test_migrate(self):
        herb = Herbivore(0, 5)
        phi = herb.fitness_calculation()
        assert herb.params['mu'] * phi == approx(0.0943535)

    def test_growing_older(self):
        herbivore = Herbivore(3, 12)
        assert herbivore.age == 3
        assert herbivore.weight == 12

        herbivore.growing_older()
        assert herbivore.age == 4
        assert herbivore.weight == 11.4

    def test_animal_dying(self, mocker):
        herb = Herbivore(5, 40)
        dead = herb.animal_dying()
        assert dead is False

        carn = Carnivore(20, 0)
        dead = carn.animal_dying()
        assert dead is True

        carn = Carnivore(5, 20)
        mocker.patch('random.random', return_value=0.9)
        dead = carn.animal_dying()
        assert dead is False


class TestHerbivore:
    def test_feeding(self):
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


class TestCarnivore:
    def test_hunt_herb(self, mocker):
        herb_phi_sorted_list = [Herbivore(5, 20), Herbivore(20, 2), Herbivore(3, 16)]
        herb_phi_sorted_list = sorted(herb_phi_sorted_list, key=lambda x: getattr(x, 'phi'))
        num_herb = len(herb_phi_sorted_list)

        carn = Carnivore(10, 2)
        del_herb = carn.hunt_herb(herb_phi_sorted_list)
        assert carn.phi < herb_phi_sorted_list[2].phi
        assert del_herb == [] and num_herb == 3

        carn = Carnivore(5, 20)
        assert carn.phi > herb_phi_sorted_list[2].phi

        mocker.patch('random.random', return_value=0.01)
        del_herb = carn.hunt_herb(herb_phi_sorted_list)
        assert len(del_herb) == 3

        carn = Carnivore(5, 20)
        herb_phi_sorted_list = [Herbivore(20, 2)]
        carn.hunt_herb(herb_phi_sorted_list)
        assert carn.weight == 21.5
