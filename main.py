# Imports
import random
from disease_model.Agent import Agent
import numpy as np
from matplotlib import pyplot
import random as r



# Idk if we wanna do it like this
def timestep(env, step_size, env_size) -> None:
    update_agent_positions(env, step_size, env_size)
    infect_one_env(env)
    recover_one_env(env)
    pass

def infect_one_env(environment: list):
    for agent in environment:
        if (agent.I) and (random.random() < agent.infect_prob):
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

        if agent.E and r.random() < agent.e2i_prob:
            agent.E = False
            agent.I = True


def recover_one_env(environment: list) -> None:
    for agent in environment:
        if agent.I and (random.random() < agent.recover_prob):
            agent.I = False
            agent.R = True

def update_agent_positions(env, step_size, pos_limit) -> None:
    for agent in env:
        agent.random_move(pos_limit, step_size)



def main():
    ENVIRONMENT_COUNT = 1
    AGENT_COUNT = 50
    TIMESTEPS = 500
    ENV_SIZE = 100
    STEP_SIZE = 5

    environment = []
    for _ in range(AGENT_COUNT):
        environment.append(Agent(pos=(ENV_SIZE*random.random(), ENV_SIZE*random.random())))
    agents = random.sample(environment, 5)
    for agent in agents:
        agent.S = False
        agent.I = True

    for t in range(TIMESTEPS):
        pyplot.clf()
        print(f"step:{t}")
        timestep(environment, STEP_SIZE, ENV_SIZE)
        for agent in environment:
            if agent.I:
                pyplot.plot(agent.pos[0], agent.pos[1], "or")
            if agent.S:
                pyplot.plot(agent.pos[0], agent.pos[1], "ob")
            if agent.R:
                pyplot.plot(agent.pos[0], agent.pos[1], "og")
            if agent.E:
                pyplot.plot(agent.pos[0], agent.pos[1], "oy")
            
        pyplot.pause(0.05)
        pyplot.xlim([0, 100])
        pyplot.ylim([0, 100])
        pyplot.show(block=False)




if __name__ == "__main__": 
    main()