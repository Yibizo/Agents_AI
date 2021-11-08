from mesa import Agent

class Tree(Agent):

    def __init__(self, pos, model):

        super().__init__(pos, model)
        self.pos = pos
        # tree state: fine, on fire, burned out
        self.condition = 'fine'
        
    def step(self):

        if self.condition == 'on fire':
            # search neighbours of agent
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                if neighbor.condition == 'fine':
                    neighbor.condition = 'on fire'
            self.condition = 'burned out'