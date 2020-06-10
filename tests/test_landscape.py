from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Lowland, Highland, Desert, Water
import unittest
import pytest

def test_cell_parameters():
    pass

def test_init():
    pass

def test_age():
    herb = Herbivore(8, 3)
    assert herb.get_age() == 8

def test_lowland_instance():
    lowland_default = Lowland()
    lowland_100 = Lowland()

def test_animal_allocates():
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
                   'weight': 20}]
    lowland = Lowland()
    lowland.animals_allocate(ini_animal)
    assert len(lowland.present_herbivores) == 1













































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




