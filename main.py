# Imports
import random
from disease_model.Agent import Agent
import numpy as np
from matplotlib import pyplot
import random as r





def infect_one_env(environment: list):
    for agent in environment:
        if (agent.status == "I") and (random.random() < agent.infect_prob):
            infect_nearby_agents(environment, agent.pos, agent.radius)

def infect_nearby_agents(env, infection_pos, infection_radius):
    for agent in env:
        if agent.status == "S":
            offset = tuple(np.subtract(infection_pos, agent.pos))
            distance = np.sqrt(offset[0]*offset[0] + offset[1]*offset[1])
            if distance < infection_radius:
                agent.status = "E"
                # Set something to track when to go form exposed to infected

        if (agent.status == "E") and (r.random() < agent.e2i_prob):
            agent.status = "I"


def recover_one_env(environment: list) -> None:
    for agent in environment:
        if (agent.status == "I") and (random.random() < agent.recover_prob):
            agent.status = "R"

def update_agent_positions_random(env, step_size, pos_limit) -> None:
    for agent in env:
        agent.random_move(pos_limit, step_size)

def count_status_one_env(env: list):
    num_I = 0
    num_S = 0
    num_E = 0
    num_R = 0
    for agent in env:
        if agent.status == "S": num_S = num_S + 1
        if agent.status == "E": num_E = num_E + 1
        if agent.status == "I": num_I = num_I + 1
        if agent.status == "R": num_R = num_R + 1

    return (num_S, num_E, num_I, num_R)



def timestep_one_env(env, step_size, env_size) -> None:
    update_agent_positions_random(env, step_size, env_size)
    infect_one_env(env)
    recover_one_env(env)

def main():
    # Constants
    ENVIRONMENT_COUNT = 1
    AGENT_COUNT_PER_ENV = 100
    TIMESTEPS = 500
    ENV_SIZE = 50
    AGENT_STEP_SIZE = 2

    # Initialization
    environment_list = []
    quarantine = []
    dead_agents = []
    
    for _ in range(ENVIRONMENT_COUNT):
        empty_environment = []
        environment_list.append(empty_environment)

    for environment in environment_list:
        for _ in range(AGENT_COUNT_PER_ENV):
            environment.append(Agent(pos=(ENV_SIZE*random.random(), ENV_SIZE*random.random())))

    for environment in environment_list:
        initial_infected = r.sample(environment, 10)
        for agent in initial_infected:
            agent.status = "I"



    for t in range(TIMESTEPS):
        pyplot.clf()
        print(f"step:{t}")
        for environment in environment_list:
            timestep_one_env(environment, AGENT_STEP_SIZE, ENV_SIZE)


        for agent in environment_list[0]:
            if agent.status == "I":
                pyplot.plot(agent.pos[0], agent.pos[1], "or")
            if agent.status == "S":
                pyplot.plot(agent.pos[0], agent.pos[1], "ob")
            if agent.status == "R":
                pyplot.plot(agent.pos[0], agent.pos[1], "og")
            if agent.status == "E":
                pyplot.plot(agent.pos[0], agent.pos[1], "oy")

        pyplot.xlim(0, ENV_SIZE)
        pyplot.ylim(0, ENV_SIZE)
        pyplot.pause(0.01)
        pyplot.show(block=False)




if __name__ == "__main__": 
    main()