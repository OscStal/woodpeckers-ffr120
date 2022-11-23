import random

class Agent():

    DEFAULT_POS = (0, 0)
    DEFAULT_RADIUS = 1
    DEFAULT_I_RATE = 0.8
    DEFAULT_R_RATE = 0.02
    DEFAULT_E2I_RATE = 0.3

    def __init__(
        self, 
        pos=DEFAULT_POS, 
        rad=DEFAULT_RADIUS,
        i_rate=DEFAULT_I_RATE,
        r_rate=DEFAULT_R_RATE,
        e2i_rate=DEFAULT_E2I_RATE
        ) -> None:

        self.parameters = {}    # If we want different paramters per agent?
        self.pos = pos
        self.radius = rad
        self.infect_prob: float = i_rate   # Probability to infect nearby
        self.e2i_prob = e2i_rate    # Probability to go from exposed to infected
        self.recover_prob = r_rate  # Probability to recover

        self.S = True
        self.E = False
        self.I = False
        self.R = False

    def random_move(self, pos_limit, step_size):
        new_x = (self.pos[0] + (step_size*(random.random()-0.5)))%pos_limit
        new_y = (self.pos[1] + (step_size*(random.random())-0.5))%pos_limit
        self.pos = (new_x, new_y)

