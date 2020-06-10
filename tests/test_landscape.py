from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Lowland, Highland, Desert, Water
import unittest

def test_cell_parameters():
    pass

def test_init():
    pass

def test_age():
    herb = Herbivore(8,3)
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



