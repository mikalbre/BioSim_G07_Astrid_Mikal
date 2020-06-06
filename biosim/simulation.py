from animals import Herbivore


"""
    Set population
    initial year = 0
    increase year
    set_animal_parameters
    set_landscape_parameters
    simulate
    num_animals_per_species
    num_animals_on_island
"""
herb_list = []

num_animals = 5
for iterator in range(2):
    herb = Herbivore()
    herb_list.append(herb)
    print(herb_list)

for herb in herb_list:
    print("Age: ", herb.get_age(),
          "weight: ", herb.get_weight(),
          "fitness: ", herb.fitness_calculation())

for iterator in range(10):
    for herb in herb_list:
        herb.growing_older()
        herb.feeding(11)
        print("Age: ", herb.get_age(),
              "weight: ", herb.get_weight(),
              "fitness: ", herb.get_fitness())

    def randomise_list(self):
        random_list = self.present_herbivores.copy()
        np.random.shuffle(random_list)
        return random_list

    def animals_eat(self):  # herbivore feeding
        randomized_order = self.randomise_list()
        for herb in randomized_order:
            if self.available_fodder >= herb.get_F():
                self.available_fodder -= herb.eat()