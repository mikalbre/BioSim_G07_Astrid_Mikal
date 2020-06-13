from biosim.island import *
import pytest
#\n

def test_string_line_length():
    map_list = ['abc', 'def']
    assert check_length_of_string(map_list) is True


# def test_conditions_for_multiline_string1(geogr):
#
#     # geogr = """KWW\n WLW\n WWW"""
#     # island = CreateIsland(geogr)
#     # island.conditions_for_island_map_string(geogr)
#     # with pytest.raises(ValueError):
#     #     CreateIsland.conditions_for_island_map_string()
#
# def test_init():
#     pass

class TestCreateIsland:

    def test_init(self):
        pass

    def test_num_animals(self):
        pass

    def test_num_animals_per_species(self):
        pass

    def test_conditions_for_multiline_string(self):
        string = "WWW\nWWW\nWWW"
        list_string = CreateIsland.conditions_for_island_map_string(string)
        assert list_string == ['WWW', 'WWW', 'WWW']

    def test_make_map(self):
        pass

    def test_add_population(self):
        pass

    def test_new_year_reset(self):
        pass

    def test_year(self):
        pass

    def test_feed_animals(self):
        pass

    def test_procreation_animals(self):
        pass

    def test_aging_animals(self):
        pass

    def test_death_animals(self):
        pass

    def test_simulate_one_year(self):
        pass


