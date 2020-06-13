from biosim.animals import Herbivore, Carnivore
from biosim.landscape import SingleCell, Lowland, Highland, Desert, Water
# import unittest
import pytest
# import numpy as np
import random
random.seed(1)

class TestSingleClass:

    # @pytest.fixture
    # def test_cell_parameters(self, request):
    #     request =[{'species': 'Herbivore',
    #                    'age': 5,
    #                    'weight': 20}]
    #     if request.param == "Herbivore":
    #         assert Herbivore()
    #     elif request.param == "Carnivore":
    #         assert Carnivore()
    #     else:
    #         assert ValueError("Invalid species!")

    def test_cell_parameters(self):
        test_input = 'f_max: 50.0'
        with pytest.raises(TypeError):
            SingleCell.cell_parameter(test_input)

        params = {'f_max': -10}  # ValueError
        with pytest.raises(TypeError):  # TypeError not ValueError, gir ikke mening
            SingleCell.cell_parameter(params)

        params = {'Invalid parameter': 100}  # TypeError
        with pytest.raises(TypeError):  # TypeError not ValueError
            SingleCell.cell_parameter(params)

    def test_init(self):
        cell = SingleCell()
        assert type(cell.present_herbivores) is list
        assert type(cell.present_carnivores) is list
        assert cell.get_fodder() == 0

    def test_grow(self):
        cell = SingleCell()
        cell.fodder_regrow()
        assert True

    def test_animal_allocates(self):
        lowland = Lowland()
        ini_animal = [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(20)]
        lowland.animals_allocate(ini_animal)
        num_herb = len(lowland.present_herbivores)
        assert num_herb == 20
        add_new_herb = [{'species': 'Herbivore', 'age': 5, 'weight': 20}]
        lowland.animals_allocate(add_new_herb)
        assert len(lowland.present_herbivores) == 21

        ini_animal = [{'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(20)]
        lowland.animals_allocate(ini_animal)
        num_carn = len(lowland.present_carnivores)
        assert num_carn == 20

        ini_animal = [{'species': 'Dog', 'age': 5, 'weight': 20}]
        with pytest.raises(TypeError):
            SingleCell.animals_allocate(ini_animal)

        highland = Highland()
        add_herbs_to_island = [{'species': 'Herbivore', 'age': 3, 'weight': 10},
                               {'species': 'Herbivore', 'age': 5, 'weight': 14},
                               {'species': 'Herbivore', 'age': 13, 'weight': 23}]
        highland.animals_allocate(add_herbs_to_island)
        herbivore_0 = highland.present_herbivores[0]
        herbivore_1 = highland.present_herbivores[1]

        assert herbivore_0.age == add_herbs_to_island[0]['age']
        assert herbivore_0.weight == add_herbs_to_island[0]['weight']
        assert herbivore_1.age == add_herbs_to_island[1]['age']
        assert herbivore_1.weight == add_herbs_to_island[1]['weight']

    def test_eat(self):
        for herb in Lowland().present_herbivores:
            herb_weight = herb.weight
            herb.eat()
            herb_weight_eaten = herb.weight
            assert herb_weight < herb_weight_eaten

        for carn in Lowland().present_carnivores:
            carn_weight = carn.weight
            carn.feed_carn_with_herb()  # Endret fra carn.eat()
            carn_weight_eaten = carn.weight
            assert carn_weight < carn_weight_eaten

        highland = Highland()
        highland.eat()
        available_fodder = highland.available_fodder
        assert available_fodder == 300
        # kan også teste eat ved å sjekke om fodder_available er red., og om #herb er red.

    def test_fodder_regrow(self):
        lowland = Lowland()
        available_fodder = lowland.available_fodder
        assert available_fodder == 800

        cell = SingleCell()
        cell.fodder_regrow()
        assert True

    def test_feed_herb(self):
        lowland = Lowland()
        lowland.present_herbivores.append(Herbivore())
        lowland.available_fodder = 15
        lowland.feed_herb()
        assert lowland.available_fodder == 5

        lowland.available_fodder = 8
        lowland.feed_herb()
        assert lowland.available_fodder == 0

    def test_feed_carn_with_herb(self):
        # mocker.patch('random.random', return_value=0.8)

        lowland = Lowland()

        lowland.animals_allocate([{'species': 'Herbivore', 'age': 6, 'weight': 20},
                                  {'species': 'Herbivore', 'age': 3, 'weight': 7},
                                  {'species': 'Herbivore', 'age': 6, 'weight': 6},
                                  {'species': 'Herbivore', 'age': 1, 'weight': 3}])

        lowland.animals_allocate([{'species': 'Carnivore', 'age': 5, 'weight': 20},
                                  {'species': 'Carnivore', 'age': 4, 'weight': 15},
                                  {'species': 'Carnivore', 'age': 5, 'weight': 25}])

        lowland.feed_carn_with_herb()
        sorted_phi_herb = [herb.phi for herb in lowland.present_herbivores]
        assert (sorted_phi_herb[0] < sorted_phi_herb[1] < sorted_phi_herb[2])

        available_herb = len(lowland.present_herbivores)
        for _ in range(100):
            lowland.feed_carn_with_herb()
        available_herb_after = len(lowland.present_herbivores)
        assert available_herb > available_herb_after

        sorted_phi_carn = [carn.phi for carn in lowland.present_carnivores]
        assert sorted_phi_carn[0] > sorted_phi_carn[1]

    def test_procreation(self, mocker):
        mocker.patch('random.random', return_value=0.0)
        mocker.patch('random.gauss', return_value=5)
        lowland = Lowland()
        lowland.animals_allocate([{'species': 'Carnivore', 'age': 5, 'weight': 20},
                                  {'species': 'Carnivore', 'age': 4, 'weight': 15},
                                  {'species': 'Carnivore', 'age': 5, 'weight': 25}])
        num_carn = len(lowland.present_carnivores)  # 3
        for _ in range(100):
            lowland.procreation()
        num_carn_after_procreation = len(lowland.present_carnivores)
        assert num_carn < num_carn_after_procreation


        # NOT WORKING:
        lowland.animals_allocate([{'species': 'Herbivore', 'age': 5, 'weight': 30},
                                  {'species': 'Herbivore', 'age': 3, 'weight': 30},
                                  {'species': 'Herbivore', 'age': 5, 'weight': 30},
                                  {'species': 'Herbivore', 'age': 10, 'weight': 30}])
        num_herb = len(lowland.present_herbivores)  # 4
        print('\n')
        print(lowland.present_herbivores)
        for _ in range(100):
            lowland.procreation()
        num_herb_after_procreation = len(lowland.present_herbivores)
        print('\n number after', num_herb_after_procreation)

        assert num_herb < num_herb_after_procreation

    def test_aging(self):
        lowland = Lowland()
        lowland.animals_allocate(
            [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(20)])
        lowland.animals_allocate(
            [{'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(150)])

        herb = lowland.present_herbivores[0].age
        carn = lowland.present_carnivores[1].age

        lowland.aging()

        herb_aged = lowland.present_herbivores[0].age
        carn_aged = lowland.present_carnivores[1].age

        assert herb < herb_aged
        assert carn < carn_aged

    def test_animal_death(self):
        lowland = Lowland()
        lowland.animals_allocate(
            [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(20)])
        lowland.animals_allocate(
            [{'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(20)])

        carn_dying = lowland.present_carnivores[0]
        carn_dying.weight = 0

        herb_dying = lowland.present_herbivores[0]
        herb_dying.weight = 0

        lowland.animal_death()
        assert carn_dying not in lowland.present_carnivores
        assert herb_dying not in lowland.present_herbivores

        carn_not_dying = lowland.present_herbivores[4]
        carn_not_dying.weight = 10

        lowland.animal_death()
        assert carn_not_dying in lowland.present_herbivores


class TestHighland:
    def test_init(self):
        highland = Highland()
        assert type(highland.present_herbivores) is list
        assert type(highland.present_carnivores) is list
        assert highland.get_fodder() == 300


class TestLowland:
    def test_init(self):
        lowland = Lowland()
        assert type(lowland.present_herbivores) is list
        assert type(lowland.present_carnivores) is list
        assert lowland.get_fodder() == 800


class TestDesert:
    def test_init(self):
        desert = Desert()
        assert type(desert.present_herbivores) is list
        assert type(desert.present_carnivores) is list
        assert desert.get_fodder() == 0


class TestWater:
    def test_init(self):
        water = Water()
        assert type(water.present_herbivores) is list
        assert type(water.present_carnivores) is list
        assert water.get_fodder() == 0
