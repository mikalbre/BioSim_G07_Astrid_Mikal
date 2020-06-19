# -*- coding: utf-8 -*-

"""
Simulation to test forced migration.

Square island of Lowland only, no death or birth, certain migration.
"""

__author__ = 'Hans Ekkehard Plesser, NMBU'


import textwrap
from biosim.simulation import BioSim
from biosim import animals

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    plt.ion()

    geogr = """\
               WWWWWWWWW
               WDDDDDDDW
               WDDDDDDDW
               WDDDDDDDW
               WDDDDDDDW
               WDDDDDDDW
               WDDDDDDDW
               WDDDDDDDW
               WWWWWWWWW"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (5, 5),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 50}
                          for _ in range(1000)]}]
    ini_carns = [{'loc': (5, 5),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 50}
                          for _ in range(1000)]}]

    animals.Herbivore.set_parameters({'mu': 1, 'omega': 0, 'gamma': 0,
                                      'a_half': 1000})
    animals.Carnivore.set_parameters({'mu': 1, 'omega': 0, 'gamma': 0,
                                      'F': 0, 'a_half': 1000})

    sim = BioSim(geogr, ini_herbs + ini_carns, seed=123456)
    sim.simulate(30, 1, 1)

    plt.show()
    input('Press ENTER')