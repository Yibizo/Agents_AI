'''
Author: Diego Mejía Suárez

Modification Date: 09/11/21

Description: Program that contains a Roomba and Tile agent to be used within the simulation
'''

from mesa import Agent
import random

# Roomba agent class that moves around the model randomly and removes "dirty" Tile agent
class RoombaAgent(Agent):
    # function: initializer function to create a new agent
    # parameters: Agent self, int unique_id, Model model
    # return: None
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.moves = 0

    # function: decide a new position for the agent to move in, if possible
    # parameters: Agent self
    # return: None
    def move(self):
        # list of possible positions, not including its own
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)

        newStep = self.random.choice(possibleSteps)
        check = self.model.grid.get_cell_list_contents([newStep])

        # move if cell is empty or if cell only has a Tile agent
        if len(check) <= 1 and (len(check) == 0 or isinstance(check[0], TileAgent)):
            self.model.grid.move_agent(self, newStep)
            self.moves += 1
            print(f'Agent {self.unique_id}: moving towards tile {newStep}')
        # don't move if step isn't possible
        else:
            print(f'Agent {self.unique_id}: can\'t move towards tile {newStep}, staying in tile {self.pos}')

    # function: function that gets executed whenever the agent takes a step in the model
    # parameters: Agent self
    # return: None
    def step(self):
        check = self.model.grid.get_cell_list_contents([self.pos])
        # if Tile agent is found, stay in place and remove it
        if isinstance(check[0], TileAgent):
            print(f'Agent {self.unique_id}: cleaning tile {self.pos}')
            self.model.grid.remove_agent(check[0])
            self.model.schedule.remove(check[0])
        # decide where to move next
        else:
            self.move()

# Tile agent class that gets created to represent dirty tiles to be removed
class TileAgent(Agent):
    # function: initializer function to create a new agent
    # parameters: Agent self, int unique_id, Model model
    # return: None
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)