
from .landscape import SingleCell, Highland, Lowland, Desert, Water, PassedBounds

class Island:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.top = PassedBounds()
        self.bottom = PassedBounds()
        self.left = PassedBounds()
        self.right = PassedBounds()
        self.num_years = 0

        map_params = {"H": Highland,
                      "L": Lowland,
                      "D": Desert,
                      "W": Water}





