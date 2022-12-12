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

def timestep_one_env(env, env_size, store, ca_perc) -> None:
    # env is list of the "Agent" object
    update_agent_positions_random(env, env_size)
    infect_one_env(env)
    recover_one_env(env)
    kill_one_env(env)
    store.update(env, ca_perc)

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

def get_max_EI(nE,nI):
    return np.max(nE+nI)



def run_simulation(
    env_count: int,
    agent_per_env: int,
    env_size: int,
    n_init_I: int,
    timesteps: int,
    infection_radius: int,
    infection_rate: float,
    recovery_rate: float,
    cash_assist_percentage: float
    ):

    environment_list = create_environment(env_count, agent_per_env, env_size, n_init_I)
    nS,nE,nI,nR,nD = (np.zeros((timesteps,)) for _ in range(5))
    resources, cash = np.zeros((timesteps,), dtype=list), np.zeros((timesteps,), dtype=list)

    for env in environment_list:
        for agent in env:
            agent.radius = infection_radius
            agent.infect_prob = infection_rate
            agent.recovery_prob = recovery_rate

    store = Store()
    for t in range(timesteps):
        for environment in environment_list:
            timestep_one_env(environment, env_size, store, cash_assist_percentage)

            # Save history of agent statuses across all timesteps
            (nS[t],nE[t],nI[t],nR[t],nD[t]) = count_status_one_env(environment)
            resources[t], cash[t] = get_resource_cash_distribution(environment)

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
        "max_infected_num" : get_max_EI(nE, nI),
        "max_infected_percent" : get_max_EI(nE, nI)/agent_per_env,
        "alive_at_end_num" : (nR[t-1] + nS[t-1]),
        "alive_at_end_percent" : (nR[t-1] + nS[t-1])/agent_per_env,
        "status_history": {
            "S": nS[:t],
            "E": nE[:t],
            "I": nI[:t],
            "R": nR[:t],
            "D": nD[:t],
            "resources" : resources,
            "cash" : cash,
        },
        "store":{
            "customers_history": store.customers_history[:t],
            "customer_history_averaged": t_avg_history,
            "customer_history_averaged_len": len(t_avg_history),
            "avg_customers" : avg_customers(store.customers_history[:t]),
        },
        }



def main():
    ENVIRONMENT_COUNT = 1
    AGENT_COUNT_PER_ENV = 500
    TIMESTEPS = 2000
    ENV_SIZE = 250
    INITIAL_INFECTED_PER_ENV = 40


    outputs: dict = run_simulation(
        env_count=ENVIRONMENT_COUNT,
        agent_per_env=AGENT_COUNT_PER_ENV,
        env_size=ENV_SIZE,
        n_init_I=INITIAL_INFECTED_PER_ENV,
        timesteps=TIMESTEPS,
        infection_radius=5,
        infection_rate=Agent.DEFAULT_I_RATE,
        recovery_rate=Agent.DEFAULT_R_RATE,
        cash_assist_percentage=0
        )


    # Plot stuff
    fig, subplots = pyplot.subplots(1, 2)
    subplots[0].set_xlabel("Time")
    subplots[0].set_ylabel("Number of agents in the environment")
    subplots[0].plot(np.arange(0, outputs.get("t_steps"), 1), outputs.get("status_history", {}).get("S"), label="Susceptible (Healthy)")
    n_alive = outputs.get("status_history", {}).get("S")[-1] + outputs.get("status_history", {}).get("R")[-1]
    alive_annotation = "Total Alive (S+R): " + str(n_alive/AGENT_COUNT_PER_ENV * 100) + "%"
    subplots[0].annotate(alive_annotation, xy=(outputs.get("t_steps"), outputs.get("status_history", {}).get("S")[-1]))
    subplots[0].plot(np.arange(0, outputs.get("t_steps"), 1), outputs.get("status_history", {}).get("I"), label="I")
    subplots[0].plot(np.arange(0, outputs.get("t_steps"), 1), outputs.get("status_history", {}).get("R"), label="R")
    subplots[0].plot(np.arange(0, outputs.get("t_steps"), 1), outputs.get("status_history", {}).get("D"), label="Dead")
    subplots[0].legend()
    
    subplots[1].set_xlabel("Time")
    subplots[1].set_ylabel("Number of agents visiting the store per 5 timesteps")
    #subplots[1].plot(np.arange(0, outputs.get("t_steps"), 1), outputs.get("store", {}).get("customers_history"), label="Customers per day")
    subplots[1].plot(np.arange(0, outputs.get("store", {}).get("customer_history_averaged_len")*10, 10), outputs.get("store", {}).get("customer_history_averaged"), label="Customers per day")
    subplots[1].legend()
    pyplot.show()



def main2():
    ENVIRONMENT_COUNT = 1
    AGENT_COUNT_PER_ENV = 500
    TIMESTEPS = 2000
    ENV_SIZE = 250
    INITIAL_INFECTED_PER_ENV = 40
    INFECTION_RADIUS = 5
    INFECTION_RATE = Agent.DEFAULT_I_RATE
    RECOVERY_RATE = Agent.DEFAULT_R_RATE

    POINT_AVG = 8
    X1_AXIS = range(0,4)
    X1_POINTS = len(X1_AXIS)

    # https://stackoverflow.com/questions/9103166/multiple-axis-in-matplotlib-with-different-scales
    # https://matplotlib.org/3.1.0/gallery/subplots_axes_and_figures/two_scales.html
    fig, axs1 = pyplot.subplots()
    axs2 = axs1.twinx()
    axs3 = axs1.twinx()
    axs4 = axs1.twinx()

    avg1_list = np.zeros((X1_POINTS,))
    avg2_list = np.zeros((X1_POINTS,))
    avg3_list = np.zeros((X1_POINTS,))
    avg4_list = np.zeros((X1_POINTS,))


    for idx, varying in enumerate(X1_AXIS):
        print(f"{idx+1} of {X1_POINTS}")
        for _ in range(POINT_AVG):

            outputs: dict = run_simulation(
                env_count=ENVIRONMENT_COUNT,
                agent_per_env=AGENT_COUNT_PER_ENV,
                env_size=ENV_SIZE,
                n_init_I=INITIAL_INFECTED_PER_ENV,
                timesteps=TIMESTEPS,
                infection_radius=INFECTION_RADIUS,
                infection_rate=INFECTION_RATE,
                recovery_rate=RECOVERY_RATE,
                cash_assist_percentage=varying
                # Add paramters here and in run_simulation as done for these above if other parameters need to be varied
                )

            avg1_list[idx] += avg_customers(outputs.get("store", {}).get("customers_history"))
            avg2_list[idx] += outputs.get("alive_at_end_percent")
            avg3_list[idx] += outputs.get("max_infected_percent")
            avg4_list[idx] += outputs.get("t_steps")
        avg1_list[idx] = avg1_list[idx]/POINT_AVG
        avg2_list[idx] = avg2_list[idx]/POINT_AVG
        avg3_list[idx] = avg3_list[idx]/POINT_AVG
        avg4_list[idx] = avg4_list[idx]/POINT_AVG
    

    axs1.plot(X1_AXIS, avg1_list, "o-", color="tab:blue")
    axs1.set_xlabel("Infection Radius")
    axs1.set_ylabel("Average customers over an entire simulation", color="tab:blue")
    #axs1.tick_params(axis='y', labelcolor="tab:blue")

    axs2.plot(X1_AXIS, avg2_list, "s-", color="tab:red")
    axs2.set_ylabel("Percent alive at end of simulation", color="tab:red")
    #axs2.tick_params(axis='y', labelcolor="tab:red")

    axs3.plot(X1_AXIS, avg3_list, "^-", color="tab:green")
    axs3.set_ylabel("Max percent of population infected", color="tab:green")
    #axs3.tick_params(axis='y', labelcolor="tab:green")
    axs3.spines['right'].set_position(('outward', 50))

    axs4.plot(X1_AXIS, avg4_list, "H-", color="tab:brown")
    axs4.set_ylabel("Timesteps until disease gone", color="tab:brown")
    #axs4.tick_params(axis='y', labelcolor="tab:brown")
    axs4.spines['right'].set_position(('outward', 100))

    print(f"Avg.customers entire simulation: {avg1_list}")
    print(f"% alive end of simulation: {[100*v for v in avg3_list]}%")
    print(f"Max % infected during simulation: {[100*v for v in avg3_list]}%")

    fig.tight_layout()
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
