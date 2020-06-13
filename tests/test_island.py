from biosim.island import *
from biosim.landscape import *
import pytest
#\n

def test_string_line_length():
    map_list = ['abc', 'def']
    island = CreateIsland(map_list)
    assert island.check_length_of_string(map_list) is True


class TestCreateIsland:

    def test_init(self):
        pass

    def test_num_animals(self):
        pass

    def test_num_animals_per_species(self):
        pass

    def test_conditions_for_multiline_string(self):  # ALL GOOD
        string = "WWW\nWWW\nWWW"
        list_string = CreateIsland.condition_for_island_map_string(string)
        assert list_string == ['WWW', 'WWW', 'WWW']

        string = "WWWW\nWLWW\nWHLW\nWDLW\nWLLW\nWWWW\nWWWW"
        list_string = CreateIsland.condition_for_island_map_string(string)
        assert list_string == ['WWWW', 'WLWW', 'WHLW','WDLW', 'WLLW', 'WWWW', 'WWWW']

        string = "WWQ\nWWW\nWWW"
        with pytest.raises(ValueError):
            CreateIsland.condition_for_island_map_string(string)

        string = "AWC\nDWF"
        with pytest.raises(ValueError):
            CreateIsland.condition_for_island_map_string(string)




    def test_make_map(self):
        multi_string = "WWW"
        island = CreateIsland(multi_string)
        assert isinstance(island.map[(1, 1)], Water)

        multi_string = "WWW\nWLW\nWWW"
        island = CreateIsland(multi_string)
        assert isinstance(island.map[(2, 2)], Lowland)

        multi_string = "WWWW\nWDDW\nWHLW\nWWWW"
        island = CreateIsland(multi_string)
        assert isinstance(island.map[(2, 3)], Desert)
        assert isinstance(island.map[(3, 2)], Highland)
        assert isinstance(island.map[(4, 4)], Water)

    def test_add_population(self):
        multi_string = "WWW\nWDW\nWWW"
        test_island = CreateIsland(multi_string)
        assert test_island.map[(2, 2)].num_animals == 0
        test_island.add_population([{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}]}])
        for herb in test_island.map[(2, 2)].present_herbivores:
            assert herb.age == 5
            assert herb.weight == 20
        assert len(test_island.map[(2, 2)].present_herbivores) == 1

        with pytest.raises(ValueError):
            test_island.add_population([{'loc': (10, 10),
                                     'pop': [{'species': 'Herbivore',
                                              'age': 5,
                                              'weight': 20}]}])

        with pytest.raises(ValueError):
            test_island.add_population([{'loc': (1, 1), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}]}])

        with pytest.raises(ValueError):
            test_island.add_population([{'loc': (2, 3), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}]}])


    def test_new_year_reset(self):
        pass

    def test_year(self):
        pass

    def test_feed_animals(self):
        multi_string = "WWW\nWLW\nWWW"
        test_island = CreateIsland(multi_string)

    def test_procreation_animals(self):
        pass

    def test_aging_animals(self):
        pass

    def test_death_animals(self):
        pass

    def test_simulate_one_year(self):
        pass


