## Astrid og Mikal's BioSim Project

### Authors

- Astrid Sedal <astrised@nmbu.no>
- Mikal Breiteig <mibreite@nmbu.no>

### BioSim project for INF200 (Advanced Python Programming).
The project is a development of a population dynamic simulation, a project that has been created upon request from 
the Environmental Projection Agency of Pylandia. The development team consists of Astrid Hæve Sedal and Mikal Breiteig. 

Rossumøya is made out of Lowland, Highland, Desert and Water and is populated by the animals Herbivore and Carnivore. 
The animals can migrate through cells on the island, reproduce and eat of the course of a year. 

In the simulation the landscape and animals goes through an annual cycle.


The final output of the method is a visualization of the development of the ecosystem of the island, 
for the species Herbivore and Carnivore.


### The map of Rossumøya

Rossumøya is an island split into cells, where each cell either lowland, highland, desert or water. The island 
must be surrounded with water, a landscape type that is impassable for animals. Meaning that Herbivores and 
Carnivores cannot leave the island. In the beginning of each year the cells get replenish with fodder. 
Desert do not contain any fodder for the animal, but carnivores can prey on Herbivores here.


### The population on Rossumøya
Herbivores graze on Lowland and Highland with a given appetite F. The Herbivores eat randomly within each cell, and 
the resources can deplete and thus no fodder will be available for the animals.
Carnivores eat herbivores in either Lowland, Highland or Desert, but they have to be in the same cell as the prey. 
If there are multiple Herbivores and Carnivores in a cell, the Carnivore with the highest fitness will always first
try to eat the Herbivore with the lowest fitness of Herbivores.

### Movement of the animals
The animal can migrate to a new cell once a year. They can only migrate to one of the adjacent cells to their 
current position. The cell is randomly chosen, and they will move if the cell is of type passable. That means that 
if it randomly chose a water- cell, the animal will not migrate, and stay in the same cell for a whole new year.

