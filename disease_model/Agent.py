import random

class Agent():

    def __init__(self, pos=(0, 0), rad=1) -> None:
        self.parameters = {}    # If we want different paramters per agent?
        self.pos = pos
        self.radius = rad

        self.S = True
        self.E = False
        self.I = False
        self.R = False

    def random_move(self, pos_limit):
        new_x = (self.pos[0] + random.random())%pos_limit
        new_y = (self.pos[1] + random.random())%pos_limit
        self.pos = (new_x, new_y)

