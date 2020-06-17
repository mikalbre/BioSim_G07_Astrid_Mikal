"""Tests the animals.py file in the biosim folder."""

from biosim.animals import Animals, Herbivore, Carnivore
import pytest
from pytest import approx
import math
import scipy.stats as stats

from scipy.stats import stats


class Test_Animals:
    # @pytest.fixture
    # def set_parameters(request):
    #     Animals.set_parameters(request.param)
    #     yield
    #     Animals.set_parameters(Animals.params)

    def test_set_parameters(self):
        params = {'w_birth': -8.0, 'eta': 2, 'DeltaPhiMax': 0}

        with pytest.raises(ValueError):
            Herbivore().set_parameters(params)

        params = {'eta': 2, 'DeltaPhiMax': 10.0}
        with pytest.raises(ValueError):
            Herbivore().set_parameters(params)

        params = {'DeltaPhiMax': 0}
        with pytest.raises(ValueError):
            Carnivore().set_parameters(params)

        params = {'Invalid parameter': 0}
        with pytest.raises(ValueError):
            Carnivore().set_parameters(params)

    def test_init(self):
        herb = Herbivore(5, 3)
        isinstance(herb.age, int)
        assert herb.age == 5
        assert herb.weight >= 0

        # carn = Carnivore(age=3.2, weight=5)
        # with pytest.raises(ValueError):
        #     carn.__init__(age=0, weight=None)

    def test_repr(self):
        herb = Herbivore(5, 20)
        string = 'Type: Herbivore, Age: 5, Fitness: 0.7310585780756752'
        assert string == Animals.__repr__(herb)

    def test_get_initial_weight(self, mocker):
        mocker.patch('random.gauss', return_value=5)

        herb = Herbivore(3, None)
        assert herb.get_initial_weight_offspring() == 5

        carn = Carnivore(2, None)
        assert carn.get_initial_weight_offspring() == 5

    # def test_get_initial_weight_gaussian_dist(self):
    #     weight = []
    #     herbivores = [Herbivore(0, None) for _ in range(2000)]
    #     for herb in len(herbivores):
    #         weight.append(herb.get_initial_weight_offspring)
    #         ks_statistic, p-value = stats.kstest(weight, 'norm')
    #         assert p-value < 0.05


    def test_sigmoid(self):
        pass


    def test_fitness_calculation(self):
        herb = Herbivore(6, 0)
        assert herb.phi == 0

        herb = Herbivore(2, 13)
        assert not herb.phi == 0

        herb = Herbivore(0, 5)
        assert approx(herb.phi) == 0.377541

        herb = Herbivore(6, -3)
        assert herb.phi == 0

    def test_procreation(self, mocker):
        herb = Herbivore(4, 30)
        herb_born = herb.procreation(1)
        assert herb_born == 0

        carn = Carnivore(4, 30)
        carn_born = carn.procreation(1)
        assert carn_born == 0

        herb = Herbivore(4, 30)
        weight = herb.weight
        lose_weight = herb.params["zeta"] * (herb.params["w_birth"] + herb.params["sigma_birth"]) #33.25
        assert weight < lose_weight
        for _ in range(10):
            procreation = herb.procreation(10)
            assert procreation == 0

        herb = Herbivore(5, 40)
        phi = herb.phi
        mocker.patch('random.random', return_value=0.01)
        herb.procreation(2)
        mocker.patch('random.gauss', return_value=5)

        #herb.weight -= herb.params["xi"] * herb.get_initial_weight_offspring()
        phi_procreated = herb.phi
        #assert herb.weight == 34  # NOT WORKING CHECK IT OUT!!!!
        assert phi > phi_procreated
        #
        # herb = Herbivore(5, 20)
        # mocker.patch('random.random', return_value=0.001)
        # offspring = herb.procreation(2)
        # assert offspring["Type"] == "Herbivore"

    def test_has_moved(self):
        herb = Herbivore()
        herb.prob_migrate()
        assert herb.has_migrated is True
        assert herb.set_migration_true() is True
        assert herb.set_migration_false() is not False

    # def test_has_migrate(self, mocker):
    #     mocker.patch('random.random', return_value=0.01)
    #     herb = Herbivore()
    #     herb.prob_migrate()
    #     assert herb.has_migrated is True

    def test_growing_older(self):
        herbivore = Herbivore(3, 12)
        assert herbivore.age == 3
        assert herbivore.weight == 12

        herbivore.growing_older()
        assert herbivore.age == 4
        assert herbivore.weight == 11.4

    def test_animal_dying(self, mocker):
        carn = Carnivore(20, 0)
        dead = carn.animal_dying()
        assert dead is True

        herb = Herbivore(5, 20)
        mocker.patch('random.random', return_value=0.001)
        dead = herb.animal_dying()
        assert dead is True

        carn = Carnivore(5, 20)
        mocker.patch('random.random', return_value=0.9)
        dead = carn.animal_dying()
        assert dead is False

    def test_death_z(self):  # NOT WORKING
        #
        b = Herbivore(age=0, weight=10)
        b = Herbivore()
        p = 0.4
        N = 10
        n = sum([(b.animal_dying() for _ in range(N))])

        mean = N * p
        var = N * p * (1-p)
        Z = (n - mean) / math.sqrt(var)
        phi = 2 * stats.norm.cdf(-abs(Z))
        assert phi > 0.01

    def test_get_age(self):
        herb = Herbivore(5, 20)
        assert herb.get_age() == 5

    def test_get_weight(self):
        herb = Herbivore(5, 20)
        assert herb.get_weight() == 20

    def test_get_fitness(self):
        herb = Herbivore(5, 20)
        phi = herb.phi
        assert herb.get_fitness() == phi

    @pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_initial_weight_gaussian_dist(self, Species):
        list_of_initial_weights = []
        for _ in range(1000):
            s = Species()
            list_of_initial_weights.append(s.weight)
            ka_statistics, p_value = stats.kstest(list_of_initial_weights, 'norm')
            assert p_value < 0.01

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

        herb = Herbivore(5, 3)
        pre_eat_weight = herb.weight
        herb.feeding(17)
        post_eat_weight = herb.weight
        assert post_eat_weight == pre_eat_weight + herb.params["beta"] * herb.params["F"]


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
        phi_not_eaten = carn.phi
        herb_phi_sorted_list = [Herbivore(20, 2)]
        carn.hunt_herb(herb_phi_sorted_list)
        phi_eaten = carn.phi
        assert carn.weight == 21.5
        assert phi_not_eaten < phi_eaten

        carn = Carnivore(5, 20)
        herb_phi = [Herbivore(5, 0)]
        del_herb = carn.hunt_herb(herb_phi)
        assert len(del_herb) == 1

        carn = Carnivore(5, 20)
        herb_phi_sorted_list = [Herbivore(3, 10), Herbivore(3, 10), Herbivore(3, 10),
                                Herbivore(3, 10), Herbivore(3, 10), Herbivore(20, 60),
                                Herbivore(3, 10)]
        del_herb = carn.hunt_herb(herb_phi_sorted_list)
        assert len(del_herb) == 5

