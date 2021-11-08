from mesa import Model
from mesa.space import Grid
from mesa.time import RandomActivation

from agent import Tree

class ForestFire(Model):

    def __init__(self, height=100, width=100, density=0.6):

        super().__init__()
        self.schedule = RandomActivation(self)
        self.grid = Grid(height, width, torus=False)

        for (contents, x, y) in self.grid.coord_iter():
            
            if self.random.random() < density:
                new_tree = Tree((x, y), self)

                if x == 0:
                    new_tree.condition = 'on fire'

                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)

        self.running = True

    def step(self):

        self.schedule.step()

        count = 0
        for tree in self.schedule.agents:
            if tree.condition == 'on fire':
                count += 1

        if count == 0:
            self.running = False