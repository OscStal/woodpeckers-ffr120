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
    AGENT_COUNT_PER_ENV = 200
    TIMESTEPS = 100
    ENV_SIZE = 100
    AGENT_STEP_SIZE = 2

    # Initialization
    environment_list = []
    
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
    # End initialization

    # Figure setup
    fig, (area, graph) = pyplot.subplots(1, 2)
    # End

    # Testing stuff
    num_s = np.zeros((TIMESTEPS, ))
    num_e = np.zeros((TIMESTEPS, ))
    num_i = np.zeros((TIMESTEPS, ))
    num_r = np.zeros((TIMESTEPS, ))

    for t in range(TIMESTEPS):
        area.clear()
        graph.clear()
        for environment in environment_list:
            timestep_one_env(environment, AGENT_STEP_SIZE, ENV_SIZE)

            (ss,ee,ii,rr) = count_status_one_env(environment)
            num_s[t] = ss
            num_e[t] = ee
            num_i[t] = ii
            num_r[t] = rr

        for agent in environment_list[0]:
            if agent.status == "I":
                area.plot(agent.pos[0], agent.pos[1], "or")
            if agent.status == "S":
                area.plot(agent.pos[0], agent.pos[1], "ob")
            if agent.status == "R":
                area.plot(agent.pos[0], agent.pos[1], "og")

        area.set_xlim(0, ENV_SIZE)
        area.set_ylim(0, ENV_SIZE)

        graph.plot(np.arange(0, t, 1), num_s[:t], label="S")
        #pyplot.plot(np.arange(0, TIMESTEPS, 1), num_e, label="E")
        graph.plot(np.arange(0, t, 1), num_i[:t], label="I")
        graph.plot(np.arange(0, t, 1), num_r[:t], label="R")
        graph.legend()
        
        graph.set_title(f"Timestep: {t}")
        pyplot.pause(0.01)
        pyplot.show(block=False)
    pyplot.show()




if __name__ == "__main__": 
    main()