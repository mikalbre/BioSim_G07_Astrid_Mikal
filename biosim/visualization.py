# -*- coding: utf-8 -*-

__author__ = 'Astrid Sedal, Mikal Breiteig'
__email__ = 'astrised@nmbu.no, mibreite@nmbu.no'


from biosim.landscape import Lowland
import matplotlib.pyplot as plt
import numpy as np
np.random.seed(1)

listof = [{'species': 'Herbivore','age': 5,'weight': 20} for _ in range(50)]
listofcarns = [{'species': 'Carnivore','age': 5,'weight': 20} for _ in range(20)]

#create a Lowland Object
l = Lowland()
# place them in list in l
l.animals_allocate(listof)
l.animals_allocate(listofcarns)

#for i in l.herb_list:
 #   print(type(i))
#
# print(0, " Year End Herb numbers :-", len(l.herb_list))
# print(0, " Year End Carn numbers :-", len(l.carn_list))
#
#Making figure
fig = plt.figure(figsize=(8, 6.4))
plt.plot(0, len(l.present_herbivores),  '*-', color='g', lw=0.5)
plt.plot(0, len(l.present_carnivores),  '*-', color='r', lw=0.5)
plt.draw()
plt.pause(0.001)

count_herb = [len(l.present_herbivores)]
count_carn = [len(l.present_carnivores)]

for i in range(200):
    l.fodder_regrow()
    l.eat()
    l.procreation()
    l.animal_death()
    l.aging()

    count_herb.append(len(l.present_herbivores))
    count_carn.append(len(l.present_carnivores))

    # plotting
    plt.plot(list(range(i + 2)),  count_herb, '*-', color='g', lw=0.5)
    plt.plot(list(range(i + 2)), count_carn, '*-', color='r', lw=0.5)
    plt.draw()
    plt.pause(0.001)
