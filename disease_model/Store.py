import random

class Store():
    DEFAULT_NUMBER_OF_CUSTOMERS = 0
    DEFAULT_COST_OF_RESOURCE = 4
    
    def __init__(self) -> None:
        self.resource_cost = self.DEFAULT_COST_OF_RESOURCE
        self.customers = 0
        self.customers_history = []

    def update(self, all_agents: list):
        self.number_of_customers = 0
        for agent in all_agents:
            if agent.cash >= self.resource_cost:
                agent.buy(self.resource_cost)
                self.number_of_customers += 1
            else:
                continue
        self.customers_history.append(self.number_of_customers)