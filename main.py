# Imports
import random
from disease_model.Agent import Agent
import numpy as np
from matplotlib import pyplot



def main():
    ENVIRONMENT_COUNT = 1
    AGENT_COUNT = 100
    TIMESTEPS = 1000

    env_size = 100
    environment = np.zeros((ENVIRONMENT_COUNT, AGENT_COUNT), dtype=object)
    for i in range(AGENT_COUNT):
        environment[0, i] = Agent(pos=(env_size*random.random(), env_size*random.random()))

    for t in range(TIMESTEPS):
        for agent in environment[0]:
            agent.random_move(env_size)
            pyplot.plot(agent.pos[0], agent.pos[1], "o")
        pyplot.show()

if __name__ == "__main__": 
    main()