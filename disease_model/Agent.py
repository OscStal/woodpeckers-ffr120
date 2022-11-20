class Agent():

    def __init__(self, position=(0, 0)) -> None:
        self.parameters = {}    # If we want different paramters per agent?
        self.position = position

        self.S = True
        self.E = False
        self.I = False
        self.R = False
        

