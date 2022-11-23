import random

class Agent():

    def __init__(self, pos=(0, 0), rad=1, i_rate=0.1, r_rate=0.05, e2i_rate=0.5) -> None:

        self.parameters = {}    # If we want different paramters per agent?
        self.pos = pos
        self.radius = rad
        self.infect_rate = i_rate
        self.e2i_rate = e2i_rate
        self.recover_rate = r_rate

        self.S = True
        self.E = False
        self.I = False
        self.R = False

    def random_move(self, pos_limit, step_size):
        new_x = (self.pos[0] + (step_size*(random.random()-0.5)))%pos_limit
        new_y = (self.pos[1] + (step_size*(random.random())-0.5))%pos_limit
        self.pos = (new_x, new_y)

