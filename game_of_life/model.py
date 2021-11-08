from mesa import Model
from mesa.space import Grid
from mesa.time import RandomActivation
from mesa.time import SimultaneousActivation

from agent import Cell

class Population(Model):

    def __init__(self, height=100, width=100, density=0.1):

        super().__init__()
        self.schedule = SimultaneousActivation(self)
        self.grid = Grid(height, width, torus=False)

        for (contents, x, y) in self.grid.coord_iter():
            
            new_cell = Cell((x, y), self, True) if self.random.random() < density else Cell((x, y), self, False)

            self.grid._place_agent((x, y), new_cell)
            self.schedule.add(new_cell)

        self.running = True

    def step(self):
        
        self.schedule.step()

        counter = 0
        for cell in self.schedule.agents:
            if cell.isAlive == True:
                counter += 1

        if counter == 0:
            self.running = False