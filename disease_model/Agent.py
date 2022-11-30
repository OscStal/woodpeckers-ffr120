import random

class Agent():

    DEFAULT_POS = (0, 0)
    DEFAULT_RADIUS = 4
    DEFAULT_I_RATE = 0.9
    DEFAULT_R_RATE = 0.01
    DEFAULT_E2I_RATE = 0.5
    DEFAULT_D_RATE = 0

    def __init__(
        self, 
        pos=DEFAULT_POS, 
        rad=DEFAULT_RADIUS,
        i_rate=DEFAULT_I_RATE,
        r_rate=DEFAULT_R_RATE,
        e2i_rate=DEFAULT_E2I_RATE,
        d_rate=DEFAULT_D_RATE
        ) -> None:

        # Misc, optional, etc parameters can be added to this dict
        self.parameters = {}

        # Disease related paramteres
        self.pos = pos
        self.radius = rad
        self.infect_prob = i_rate   # Probability to infect nearby
        self.e2i_prob = e2i_rate    # Probability to go from exposed to infected
        self.recover_prob = r_rate  # Probability to recover
        self.death_prob = d_rate
        self.in_quarantine = False
        self.status = "S"

        # Economy related parameters
        self.resources = 0
        self.resource_minimum = 4
        self.cash = 0
        self.salary = 0


    def random_move(self, pos_limit, step_size):
        new_x = (self.pos[0] + (step_size*(random.random()-0.5)))%pos_limit
        new_y = (self.pos[1] + (step_size*(random.random()-0.5)))%pos_limit
        self.pos = (new_x, new_y)


    def buy(self, resourceCost):
        self.cash -= resourceCost 
        self.resources += 1

    def updateCash(self):
        self.cash += self.salary/30

    def updateResources(self):
        self.resources -= 1
            
    def update(self):
        self.updateCash()
        self.updateResources()
        if(self.resources<0):
            self.status = "D"

def updateAllAgents(self, all_agents):
    for agent in all_agents:
        agent.update()

