import random
import numpy as np

class Agent():

    DEFAULT_POS = (0, 0)
    DEFAULT_RADIUS = 4
    DEFAULT_I_RATE = 0.8
    DEFAULT_R_RATE = 0.02
    DEFAULT_E2I_RATE = 0.3
    DEFAULT_D_RATE = 0
    DEFAULT_STEP_SIZE = 2.5

    def __init__(
        self, 
        pos=DEFAULT_POS, 
        rad=DEFAULT_RADIUS,
        i_rate=DEFAULT_I_RATE,
        r_rate=DEFAULT_R_RATE,
        e2i_rate=DEFAULT_E2I_RATE,
        d_rate=DEFAULT_D_RATE,
        step_size=DEFAULT_STEP_SIZE
        ) -> None:

        # Misc, optional, etc parameters can be added to this dict
        self.parameters = {}

        # Disease related paramteres
        self.pos = pos
        self.step_size = step_size
        self.radius = rad
        self.infect_prob = i_rate   # Probability to infect nearby
        self.e2i_prob = e2i_rate    # Probability to go from exposed to infected
        self.recover_prob = r_rate  # Probability to recover
        self.death_prob = d_rate
        self.in_quarantine = False
        self.status = "S"

        # Economy related parameters
        self.resources = np.random.normal(8, 0.5)
        self.resource_minimum = 5
        self.daily_resource_decrease_rate = np.random.normal(0.2, 0.01)
        self.cash = (np.random.normal(5, 0.5))
        self.daily_salary = np.random.normal(1, 0.1)


    def random_move(self, pos_limit, step_size):
        new_x = (self.pos[0] + (step_size*(random.random()-0.5)))%pos_limit
        new_y = (self.pos[1] + (step_size*(random.random()-0.5)))%pos_limit
        self.pos = (new_x, new_y)

    # def buy(self, resourceCost):
    #     self.cash -= resourceCost
    #     self.resources = 8

    def buy(self, resourceCost): 
        nItemsPurchased = random.randint(1, int(self.cash / resourceCost))
        self.resources += nItemsPurchased
        self.cash -= resourceCost * nItemsPurchased

    def updateCash(self):
        self.cash += self.daily_salary

    def updateResources(self):
        self.resources -= self.daily_resource_decrease_rate
            
    def update(self):
        self.updateCash()
        self.updateResources()
        if(self.resources<0):
            self.status = "D"

def updateAllAgents(all_agents):
    for agent in all_agents:
        agent.update()

