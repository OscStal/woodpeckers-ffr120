# Imports
import random
from disease_model.Agent import Agent



def main():
    al = []
    for i in range(10):
        al.append(Agent(position=(random.random(), random.random())))
    for agent in al:
        print(agent.position)

if __name__ == "__main__": 
    main()