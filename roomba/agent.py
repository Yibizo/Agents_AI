from mesa import Agent
import random

class RoombaAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.moves = 0

    def move(self):
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False) # don't include own position

        newStep = self.random.choice(possibleSteps)
        check = self.model.grid.get_cell_list_contents([newStep])

        if len(check) <= 1 and (len(check) == 0 or isinstance(check[0], TileAgent)):
            self.model.grid.move_agent(self, newStep)
            self.moves += 1
            print(f'Agent {self.unique_id}: moving towards tile {newStep}')
        else:
            print(f'Agent {self.unique_id}: can\'t move towards tile {newStep}, staying in tile {self.pos}')

    def step(self):
        check = self.model.grid.get_cell_list_contents([self.pos])
        if isinstance(check[0], TileAgent):
            print(f'Agent {self.unique_id}: cleaning tile {self.pos}')
            self.model.grid.remove_agent(check[0])
            self.model.schedule.remove(check[0])
        else:
            self.move()

class TileAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)