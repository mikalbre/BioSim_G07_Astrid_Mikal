from biosim.island import *
from biosim.landscape import *
import pytest



# def test_string_line_length():  # NOT WORKING
#     string = """abc\ndef\nghi"""
#     island = CreateIsland(string, pop)
#     assert island.check_length_of_string(string) is True


class TestCreateIsland:

    def test_init(self):
        pass

    # def test_string_line_length(self):
    #     string = """abc\ndef\nghi"""
    #     island = CreateIsland(string)
    #     assert island.check_length_of_string(string) is True

    def test_num_animals(self):
        pass

    def test_num_animals_per_species(self):
        pass

    def test_conditions_for_multiline_string(self):  # ALL GOOD

        string = "WWWW\nWWW\nWWWW"
        with pytest.raises(ValueError):
            CreateIsland.condition_for_island_map_string(string)

        string = "WWWWW\nRWWWW\nWWWWH\nWWWWW"
        with pytest.raises(ValueError):
            CreateIsland.condition_for_island_map_string(string)

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
        multi_string = "WWW\nWLW\nWWW"
        pop = [{'loc': (2, 2),
                'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}]}]
        island = CreateIsland(multi_string, pop)
        assert isinstance(island.map[(1, 1)], Water)

        multi_string = "WWW\nWLW\nWWW"
        island = CreateIsland(multi_string, pop)
        assert isinstance(island.map[(2, 2)], Lowland)

        multi_string = "WWWW\nWDDW\nWHLW\nWWWW"
        island = CreateIsland(multi_string, pop)
        assert isinstance(island.map[(2, 3)], Desert)
        assert isinstance(island.map[(3, 2)], Highland)
        assert isinstance(island.map[(4, 4)], Water)

    def test_add_population(self):
        multi_string = "WWW\nWDW\nWWW"
        pop = [{'loc': (2, 2),
               'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}]}]
        test_island = CreateIsland(multi_string, pop)

        for herb in test_island.map[(2, 2)].present_herbivores:
            assert herb.age == 5
            assert herb.weight == 20
        assert len(test_island.map[(2, 2)].present_herbivores) == 1

        pop = [{'loc': (10, 10),
                'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}]}]

        with pytest.raises(ValueError):
            CreateIsland(multi_string, pop)

        pop = [{'loc': (1, 1),
                'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}]}]
        with pytest.raises(ValueError):
            CreateIsland(multi_string, pop)

        pop = [{'loc': (2, 3),
                'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}]}]
        with pytest.raises(ValueError):
            CreateIsland(multi_string, pop)

    def test_new_year_reset(self):
        multi_string = "WWW\nWDW\nWWW"
        pop = [{'loc': (2, 2),
                'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}]}]
        test_island = CreateIsland(multi_string, pop)

        test_island.simulate_one_year()

    def test_year(self):
        pass

    def test_feed_animals(self):
        multi_string = "WWW\nWLW\nWWW"
        pop = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}]}]
        test_island = CreateIsland(multi_string, pop)
        test_island.feed_animal()
        assert test_island.map[(2, 2)].present_herbivores[0].weight > 20

    def test_procreation_animals(self):
        multi_string = "WWW\nWLW\nWWW"
        pop = [{'loc': (2, 2),
                'pop': [{'species': 'Carnivore', 'age': 7, 'weight': 80}
                        for _ in range(20)]}]
        test_island = CreateIsland(multi_string, pop)

        num_carns = test_island.num_animals_per_species["Carnivore"]
        assert num_carns == 20
        for _ in range(200):
            test_island.procreation_animals()
        num_carns_after = test_island.num_animals_per_species["Carnivore"]
        assert num_carns < num_carns_after

    def test_add_migrated_herb_to_new_cell(self):
        multi_string = "WWW\nWLW\nWWW"
        pop = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}]}]
        test_island = CreateIsland(multi_string, pop)
        loc = (2, 2)
        assert test_island.map[loc].num_herbivores == 1
        test_island.add_migrated_herb_to_new_cell(loc, Herbivore())
        assert test_island.map[loc].num_herbivores == 2
        test_island.add_migrated_herb_to_new_cell(loc, Herbivore())
        assert test_island.map[loc].num_herbivores == 3
        test_island.add_migrated_herb_to_new_cell((2, 3), Herbivore())
        assert test_island.map[(2, 3)].num_herbivores == 1

    def test_add_migrated_carn_to_new_cell(self):
        multi_string = "WWW\nWLW\nWWW"
        pop = [{'loc': (2, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20}]}]
        test_island = CreateIsland(multi_string, pop)
        loc = (2, 2)
        assert test_island.map[loc].num_carnivores == 1
        test_island.add_migrated_carn_to_new_cell(loc, Carnivore())
        assert test_island.map[loc].num_carnivores == 2
        test_island.add_migrated_carn_to_new_cell(loc, Carnivore())
        assert test_island.map[loc].num_carnivores == 3

    def test_migration_neighboring_cells(self):
        multi_string = "WWWW\nWLWW\nWWWW"
        pop = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}]}]
        test_island = CreateIsland(multi_string, pop)
        loc = (2, 2)
        neighbor_cells = test_island.migration_neighboring_cells(loc)
        assert isinstance(neighbor_cells, list)

    def test_migrate_animals(self):
        """
        Checks if animal movs to correct cells, and that they do not move to cells that is
        not adjacent to the current cell.
        """

        multi_string = "WWWW\nWLHW\nWHWW\nWWWW"
        pop = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}
                                       for _ in range(30)]}]
        test_island = CreateIsland(multi_string, pop)

        assert test_island.map[(2, 2)].num_animals == 30  # Center- Lowland
        assert test_island.map[(2, 3)].num_animals == 0  # East - Water
        assert test_island.map[(3, 2)].num_animals == 0  # South - Lowland
        assert test_island.map[(1, 2)].num_animals == 0  # North - Water
        assert test_island.map[(2, 1)].num_animals == 0  # West - Water

        for i in range(25):
            test_island.simulate_one_year()

        assert test_island.map[(2, 2)].num_animals != 30  # Center
        assert test_island.map[(2, 3)].num_animals > 5  # East
        assert test_island.map[(3, 2)].num_animals > 5  # South
        assert test_island.map[(1, 2)].num_animals == 0  # North
        assert test_island.map[(2, 1)].num_animals == 0  # West
        assert test_island.map[(1, 3)].num_animals == 0  # North- east
        assert test_island.map[(1, 1)].num_animals == 0  # North- west
        assert test_island.map[(3, 3)].num_animals == 0  # South- east
        assert test_island.map[(3, 1)].num_animals == 0  # South- west

    def test_aging_animals(self):
        multi_string = "WWW\nWLW\nWWW"
        pop = [{'loc': (2, 2),
               'pop': [{'species': 'Carnivore', 'age': 7, 'weight': 80}]}]
        test_island = CreateIsland(multi_string, pop)

        test_island.aging_animals()
        for carn in test_island.map[(2, 2)].present_carnivores:
            assert carn.age == 8

    def test_death_animals(self):
        multi_string = "WWW\nWLW\nWWW"
        pop = [{'loc': (2, 2),
                'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 2}
                                                            for _ in range(50)]}]
        test_island = CreateIsland(multi_string, pop)

        num_animals_before = test_island.num_animals
        for _ in range(15):
            test_island.death_animals()
        num_animals_after = test_island.num_animals
        print(num_animals_before, num_animals_after)
        assert num_animals_before > num_animals_after

    def test_simulate_one_year(self):
        pass


