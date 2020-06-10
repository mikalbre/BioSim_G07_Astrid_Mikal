from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Lowland, Highland, Desert, Water
import unittest
import numpy as np
np.random.seed(1)

class TestSingleClass:
    def test_cell_parameters(self):
        pass

    def test_init(self):
        pass

    def test_age(self):
        herb = Herbivore(8,3)
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
        ini_animal = [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}]
        lowland = Lowland()
        lowland.animals_allocate(ini_animal)
        self.carn = Lowland().present_carnivores
        self.herb = len(self.carn)
        Lowland().procreation()
        self.herb_pro = len(self.carn)
        assert self.herb < self.herb_pro

        # for carn in Lowland().present_carnivores:
        #     carn_weight = carn.weight
        #     carn.eat()
        #     carn_weight_eaten = carn.weight
        # assert carn_weight < carn_weight_eaten

        # mocker.patch('random.shuffle', return_value=5)
        #
        # herb = Herbivore(3, None)
        # assert herb.get_initial_weight_offspring() == 5
        # land = Lowland()
        # herb_weight = Herbivore().get_weight()
        # land.eat()
        # herb_weight_eaten = Herbivore().get_weight()
        # assert herb_weight < herb_weight_eaten



