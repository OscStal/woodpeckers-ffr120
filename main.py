# Imports
import random
from disease_model.Agent import Agent
from disease_model.Agent import updateAllAgents
from disease_model.Store import Store
import numpy as np
from matplotlib import pyplot
import random as r
# End


def infect_one_env(environment: list):
    for agent in environment:
        if (agent.status in "EI") and (random.random() < agent.infect_prob):
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

def kill_one_env(env: list):
    for agent in env:
        if (agent.status == "I") and (random.random() < agent.death_prob):
            agent.status == "D"

def update_agent_positions_random(env, pos_limit) -> None:
    for agent in env:
        agent.random_move(pos_limit, agent.step_size)

def count_status_one_env(env: list):
    num_I = 0
    num_S = 0
    num_E = 0
    num_R = 0
    num_D = 0
    for agent in env:
        if agent.status == "S": num_S += 1
        if agent.status == "E": num_E += 1
        if agent.status == "I": num_I += 1
        if agent.status == "R": num_R += 1
        if agent.status == "D": num_D += 1

    return (num_S, num_E, num_I, num_R, num_D)

def timestep_one_env(env, env_size, store) -> None:
    # env is list of the "Agent" object
    update_agent_positions_random(env, env_size)
    infect_one_env(env)
    recover_one_env(env)
    kill_one_env(env)
    store.update(env)

def create_environment(env_count, agent_per_env, env_size, n_initial_I):
    environment_list = []
    
    for _ in range(env_count):
        empty_environment = []
        environment_list.append(empty_environment)

    for environment in environment_list:
        for _ in range(agent_per_env):
            environment.append(Agent(pos=(env_size*random.random(), env_size*random.random())))

    if not n_initial_I: return environment_list
    for environment in environment_list:
        initial_infected = r.sample(environment, n_initial_I)
        for agent in initial_infected:
            agent.status = "I"

    return environment_list

def avg_customers(customer_history: list):
    return np.average(customer_history)

def get_resource_cash_distribution(env: list):
    resources = [agent.resources for agent in env]
    cash = [agent.cash for agent in env]
    return (resources, cash)



def run_simulation(
    env_count: int,
    agent_per_env: int,
    env_size: int,
    n_init_I: int,
    timesteps: int,
    infection_radius: int,
    infection_rate: float,
    recovery_rate: float
    ):

    environment_list = create_environment(env_count, agent_per_env, env_size, n_init_I)
    nS,nE,nI,nR,nD = (np.zeros((timesteps,)) for _ in range(5))

    for env in environment_list:
        for agent in env:
            agent.radius = infection_radius
            agent.infect_prob = infection_rate
            agent.recovery_prob = recovery_rate

    store = Store()
    for t in range(timesteps):
        for environment in environment_list:
            timestep_one_env(environment, env_size, store)

            # Save history of agent statuses across all timesteps
            (nS[t],nE[t],nI[t],nR[t],nD[t]) = count_status_one_env(environment)

        if (t > 20) and (nE[t-20] == 0) and (nI[t-20] == 0):
            # Stop simulation once noone is infected/exposed?
            break

    # Calculate average per 5 timesteps of store activity  
    ch = store.customers_history[:t]
    t_avg_history = []
    for i in range(len(ch)):
        if i%5==0 and i>0:
            t_avg_history.append(np.average(ch[i-5:i]))

    return {
        "t_steps" : t,
        "status_history": {
            "S": nS[:t],
            "E": nE[:t],
            "I": nI[:t],
            "R": nR[:t],
            "D": nD[:t],
        },
        "store":{
            "customers_history": store.customers_history[:t],
            "customer_history_averaged": t_avg_history,
            "customer_history_averaged_len": len(t_avg_history)
        }}

def main():
    ENVIRONMENT_COUNT = 1
    AGENT_COUNT_PER_ENV = 250
    TIMESTEPS = 250
    ENV_SIZE = 200
    INITIAL_INFECTED_PER_ENV = 5


    outputs: dict = run_simulation(
        env_count=ENVIRONMENT_COUNT,
        agent_per_env=AGENT_COUNT_PER_ENV,
        env_size=ENV_SIZE,
        n_init_I=INITIAL_INFECTED_PER_ENV,
        timesteps=TIMESTEPS,
        infection_radius=12,
        infection_rate=Agent.DEFAULT_I_RATE,
        recovery_rate=Agent.DEFAULT_R_RATE
        )


    # Plot stuff
    fig, subplots = pyplot.subplots(1, 2)
    subplots[0].set_xlabel("Time")
    subplots[0].set_ylabel("Number of agents in the environment")
    subplots[0].plot(np.arange(0, outputs.get("t_steps"), 1), outputs.get("status_history", {}).get("S"), label="Susceptible (Healthy)")
    n_alive = outputs.get("status_history", {}).get("S")[-1] + outputs.get("status_history", {}).get("R")[-1]
    alive_annotation = "Alive: " + str(n_alive/AGENT_COUNT_PER_ENV * 100) + "%"
    subplots[0].annotate(alive_annotation, xy=(outputs.get("t_steps"), outputs.get("status_history", {}).get("S")[-1]))
    subplots[0].plot(np.arange(0, outputs.get("t_steps"), 1), outputs.get("status_history", {}).get("I"), label="I")
    subplots[0].plot(np.arange(0, outputs.get("t_steps"), 1), outputs.get("status_history", {}).get("R"), label="R")
    subplots[0].plot(np.arange(0, outputs.get("t_steps"), 1), outputs.get("status_history", {}).get("D"), label="Dead")
    subplots[0].legend()
    
    subplots[1].set_xlabel("Average 5 timesteps")
    subplots[1].set_ylabel("Number of agents visiting the store per day")
    #subplots[1].plot(np.arange(0, outputs.get("t_steps"), 1), outputs.get("store", {}).get("customers_history"), label="Customers per day")
    subplots[1].plot(np.arange(0, outputs.get("store", {}).get("customer_history_averaged_len"), 1), outputs.get("store", {}).get("customer_history_averaged"), label="Customers per day")
    subplots[1].legend()
    pyplot.show()

def main2():
    ENVIRONMENT_COUNT = 1
    AGENT_COUNT_PER_ENV = 250
    TIMESTEPS = 250
    ENV_SIZE = 200
    INITIAL_INFECTED_PER_ENV = 20
    INFECTION_RADIUS = 4
    INFECTION_RATE = 0.8
    RECOVERY_RATE = 0.01

    NUM_POINTS = 19
    POINT_AVG = 5
    x_axis = range(1,20)
    NUM_POINTS = len(x_axis)

    avg_list = np.zeros((NUM_POINTS,))
    for idx, varying in enumerate(x_axis):
        print(idx)

        for _ in range(POINT_AVG):
            outputs: dict = run_simulation(
                env_count=ENVIRONMENT_COUNT,
                agent_per_env=AGENT_COUNT_PER_ENV,
                env_size=ENV_SIZE,
                n_init_I=INITIAL_INFECTED_PER_ENV,
                timesteps=TIMESTEPS,
                infection_radius=varying,
                infection_rate=INFECTION_RATE,
                recovery_rate=RECOVERY_RATE,
                # Add paramters here and in run_simulation as done for these above if other parameters need to be varied
                )

            avg_list[idx] += avg_customers(outputs.get("store", {}).get("customers_history"))
        avg_list[idx] = avg_list[idx]/POINT_AVG
    
    pyplot.plot(x_axis, avg_list, "ob")
    pyplot.xlabel("Infection Probability")
    pyplot.ylabel("Avg. Customers over a simulation")
    pyplot.show()
        




def test_disease():
    # Constants
    ENVIRONMENT_COUNT = 1
    AGENT_COUNT_PER_ENV = 200
    TIMESTEPS = 750
    ENV_SIZE = 100
    INITIAL_INFECTED_PER_ENV = 10

    # Initialization
    environment_list = create_environment(ENVIRONMENT_COUNT, AGENT_COUNT_PER_ENV, ENV_SIZE, INITIAL_INFECTED_PER_ENV)
    fig, (area, graph) = pyplot.subplots(1, 2)
    # End

    # Testing stuff
    num_s = np.zeros((TIMESTEPS, ))
    num_e = np.zeros((TIMESTEPS, ))
    num_i = np.zeros((TIMESTEPS, ))
    num_r = np.zeros((TIMESTEPS, ))

    for t in range(TIMESTEPS):
        print(t)
        # Clear plots between timesteps
        # area.clear()
        # graph.clear()

        for environment in environment_list:
            timestep_one_env(environment, ENV_SIZE)

            # Save S,E,I,R-amount every timestep
            (ss,ee,ii,rr) = count_status_one_env(environment)
            num_s[t] = ss
            num_e[t] = ee
            num_i[t] = ii
            num_r[t] = rr

        # for agent in environment_list[0]:
        #     if agent.status == "I":
        #         area.plot(agent.pos[0], agent.pos[1], "or")
        #     if agent.status == "S":
        #         area.plot(agent.pos[0], agent.pos[1], "ob")
        #     if agent.status == "R":
        #         area.plot(agent.pos[0], agent.pos[1], "og")

        # area.set_xlim(0, ENV_SIZE)
        # area.set_ylim(0, ENV_SIZE)

        # graph.plot(np.arange(0, t, 1), num_s[:t], label="S")
        # #pyplot.plot(np.arange(0, TIMESTEPS, 1), num_e, label="E")
        # graph.plot(np.arange(0, t, 1), num_i[:t], label="I")
        # graph.plot(np.arange(0, t, 1), num_r[:t], label="R")
        # graph.legend()
        
        # graph.set_title(f"Timestep: {t}")
        # pyplot.pause(0.01)
        # pyplot.show(block=False)
    pyplot.plot(np.arange(0, TIMESTEPS, 1), num_s, label="S")
    #pyplot.plot(np.arange(0, TIMESTEPS, 1), num_e, label="E")
    pyplot.plot(np.arange(0, TIMESTEPS, 1), num_i, label="I")
    pyplot.plot(np.arange(0, TIMESTEPS, 1), num_r, label="R")
    pyplot.legend()
    pyplot.show()




if __name__ == "__main__": 
    main()
