# Imports
import random
from disease_model.Agent import Agent
import numpy as np
from matplotlib import pyplot



# Idk if we wanna do it like this
def timestep() -> None:
    # Position update for every agent
    # Infect people
    # Recover people
    pass

def infect_one_env(environment: list):
    for agent in environment:
        if (agent.S or agent.E) and (random.random() < agent.infect_rate):
            infect_nearby_agents(environment, agent.pos, agent.radius)

def infect_nearby_agents(env, infection_pos, infection_radius):
    for agent in env:
        if agent.S:
            offset = tuple(np.subtract(infection_pos, agent.pos))
            distance = np.sqrt(offset[0]*offset[0] + offset[1]*offset[1])
            if distance < infection_radius:
                agent.E = True
                agent.S = False
                # Set something to track when to go form exposed to infected

def recover_one_env(environment: list) -> None:
    for agent in environment:
        if agent.I and (random.random() < agent.recover_rate):
            agent.I = False
            agent.R = True

def update_agent_positions(env, step_size, pos_limit) -> None:
    for agent in env:
        agent.random_move(pos_limit, step_size)



def main():
    ENVIRONMENT_COUNT = 1
    AGENT_COUNT = 100
    TIMESTEPS = 1000

    env_size = 100
    environment = np.zeros((ENVIRONMENT_COUNT, AGENT_COUNT), dtype=object)
    environment = []
    for _ in range(AGENT_COUNT):
        environment.append(Agent(pos=(env_size*random.random(), env_size*random.random())))





    for t in range(TIMESTEPS):
        for agent in environment:
            agent.random_move(env_size)
            pyplot.plot(agent.pos[0], agent.pos[1], "o")
        pyplot.show()

if __name__ == "__main__": 
    main()