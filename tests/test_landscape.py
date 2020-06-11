from biosim.animals import Herbivore, Carnivore
from biosim.landscape import SingleCell, Lowland, Highland, Desert, Water
import unittest
import pytest
import numpy as np
import random
random.seed(1)

class TestSingleClass:
    def test_cell_parameters(self):
        pass

    def test_init(self):
        cell = SingleCell()
        assert type(cell.present_herbivores) is list
        assert type(cell.present_carnivores) is list
        assert cell.get_fodder() == 0

    def test_age(self):
        herb = Herbivore(8, 3)
        assert herb.get_age() == 8

    def test_lowland_instance(self):
        lowland_default = Lowland()
        lowland_100 = Lowland()
        pass

    def test_animal_allocates(self):
        # ini_animal = [{'species': 'Dog',
        #                        'age': 5,
        #                        'weight': 20}]
        # Lowland().animals_allocate(ini_animal)
        # assert ValueError

        ini_animal = [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}]
        lowland = Lowland()
        animal = lowland.animals_allocate(ini_animal)
        liste = lowland.present_herbivores
        assert len(liste) == 1

        ini_animal = [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20} for _ in range(20)]
        lowland = Lowland()
        lowland.animals_allocate(ini_animal)
        assert len(lowland.present_herbivores) == 20

    def test_eat(self):
        for herb in Lowland().present_herbivores:
            herb_weight = herb.weight
            herb.eat()
            herb_weight_eaten = herb.weight
            assert herb_weight < herb_weight_eaten

    def test_procreation(self):
        lowland = Lowland()
        lowland.animals_allocate([{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20} for _ in range(20)])
        lowland.animals_allocate([{'species': 'Herbivore',
                                  'age': 5,
                                  'weight': 20} for _ in range(20)])

        num_carn = len(lowland.present_carnivores)
        for _ in range(100):
            lowland.procreation()
        num_carn_after = len(lowland.present_carnivores)

        assert num_carn_after > num_carn

        # carn_pro = len(lowland.present_carnivores)
        # assert num_carn < carn_pro


    def test_feed_herb(self):
        lowland = Lowland()
        lowland.present_herbivores.append(Herbivore())
        lowland.available_fodder = 10
        lowland.feed_herb()
        assert lowland.available_fodder == 0
    #
    def test_feed_carn_with_herb(self, ):
        lowland = Lowland()
        lowland.animals_allocate([{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}, {'species': 'Herbivore',
                       'age': 3,
                       'weight': 7}, {'species': 'Herbivore',
                       'age': 6,
                       'weight': 6}])
        lowland.animals_allocate([{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}, {'species': 'Carnivore',
                       'age': 4,
                       'weight': 15}, {'species': 'Carnivore',
                       'age': 5,
                       'weight': 25}])

        # available_herb = len(lowland.present_herbivores)
        # lowland.feed_carn_with_herb()
        # available_herb_after = len(lowland.present_herbivores)
        # assert available_herb > available_herb_after
        lowland.feed_carn_with_herb()

        sorted_phi_herb = [herb.phi for herb in lowland.present_herbivores]

        assert sorted_phi_herb[0] < sorted_phi_herb[1]








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



def test_procreation(): # Blir 50 < 50
    lowland = Lowland()
    pop_herb = [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(50)]
    len_pop_herb = len(pop_herb)
    lowland.animals_allocate(pop_herb)
    lowland.procreation()
    len_popHerb = len(pop_herb)
    assert len_pop_herb < len_popHerb

def test_procreation():
    lowland = Lowland()
    pop_herb = [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(50)]
    len_pop_herb = len(pop_herb)
    lowland.animals_allocate(pop_herb)
    lowland.procreation()
    len_popHerb = len(pop_herb)
    assert len_pop_herb < len_popHerb





        # mocker.patch('random.shuffle', return_value=5)
        #
        # herb = Herbivore(3, None)
        # assert herb.get_initial_weight_offspring() == 5
        # land = Lowland()
        # herb_weight = Herbivore().get_weight()
        # land.eat()
        # herb_weight_eaten = Herbivore().get_weight()
        # assert herb_weight < herb_weight_eaten



