from biosim.island import CreateIsland

def test_check_line_length():
    lines = ['WWW', 'WLW', 'WWW']
    assert CreateIsland.conditions_for_island_map_string(lines) is True


def test_init(string, ini_herb):
    island = CreateIsland(string, ini_herb)
    assert hasattr(island, 'map')
