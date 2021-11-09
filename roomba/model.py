'''
Author: Diego Mejía Suárez

Modification Date: 09/11/21

Description: Program that contains the model of the Roomba simulation to be visualized within the server
'''

from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import Model
from agent import RoombaAgent, TileAgent
from mesa.datacollection import DataCollector
import os, time

# Room model class that contains a cell grid with all acting agents
class RoomModel(Model):
    # function: initializer function to create a new agent
    # parameters: Model self, int total, int height, int width, int stepLimit, float density, int timeLimit
    # return: None
    def __init__(self, total, height, width, stepLimit, density, timeLimit):
        self.stepLimit = stepLimit
        self.height = height
        self.width = width
        self.storedSteps = stepLimit
        self.numRoombas = total
        self.density = density
        self.timeLimit = timeLimit
        self.timeStart = None
        self.grid = MultiGrid(height, width, False)
        self.schedule = RandomActivation(self)
        self.running = True

        # data to be collected and registered
        self.datacollector = DataCollector(
            {
                # register first to avoid delay 
                'time': lambda m: time.time() - self.timeStart,
                # value to graph
                'dirty percentage': lambda m: self.getCleanPercentage(m, True),
                # value to graph
                'clean percentage': lambda m: self.getCleanPercentage(m, False),
                # track all agent moves
                'agent moves': lambda m: {agent.unique_id: agent.moves for agent in self.schedule.agents if isinstance(agent, RoombaAgent)}
            }
        )

        # loop through the generated grid to create Tile agents according to given density
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                t = TileAgent((x,y), self)
                self.schedule.add(t)
                self.grid.place_agent(t, (x,y))

        # create Roomba agents according to number given
        for i in range(self.numRoombas):
            a = RoombaAgent(i+1, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1,1))

    # function: function that gets executed whenever a step is concluded within the model
    # parameters: Model self
    # return: None
    def step(self):
        # register until simulation starts
        if not self.timeStart:
            self.timeStart = time.time()

        # advance schedule steps
        self.schedule.step()
        # collect all defined data
        self.datacollector.collect(self)

        # track current step number
        self.stepLimit -= 1
        counter = 0

        # to not get delayed by loop searching for agents
        # if time limit is reached
        if time.time()-self.timeStart > self.timeLimit:
            self.finishSchedule()
            return

        # search for existing Tile agents
        for agent in self.schedule.agents:
            if isinstance(agent, TileAgent):
                counter += 1

        # if not Tile agents are found or step limit is reached
        if counter == 0 or self.stepLimit == 1:
            self.finishSchedule()

    # function: calculate percentage of either dirty or clean tiles within the model
    # parameters: Model model, bool countDirty
    # return float percentage
    @staticmethod
    def getCleanPercentage(model, countDirty):
        area = model.height * model.width
        counter = 0 if countDirty else area
        if countDirty:
            for agent in model.schedule.agents:
                if isinstance(agent, TileAgent):
                    counter += 1
        else:
            for agent in model.schedule.agents:
                if isinstance(agent, TileAgent):
                    counter -= 1

        return round(counter / (model.height * model.width) * 100, 3)

    # function: stop model schedule, track and print collected data so far
    # parameters: Model self
    # return: None
    def finishSchedule(self):
        # stop the simulation
        self.running = False
        # get dataframe of data collected
        dataFrame = self.datacollector.get_model_vars_dataframe()

        # assign dataframe values to variables
        time = f'{round(dataFrame.iloc[-1, 0], 3)} seconds'
        dirtyPercentage = f'{round(dataFrame.iloc[-1, 1], 3)}%'
        cleanPercentage = f'{round(dataFrame.iloc[-1, 2], 3)}%'
        agentMoves = '--- Agent Moves ---\n'
        tmpMoves = dataFrame.iloc[-1, 3]
        for agentId in tmpMoves:
            agentMoves += f'Agent {agentId}: {tmpMoves[agentId]} moves\n'

        # search for next data file to create
        tmp = 1
        while os.path.exists(f'data/data_{tmp}.txt'):
            tmp += 1

        # create and write text within the data file
        with open(f'data/data_{tmp}.txt', 'x') as file:
            file.write(f'\n=== Parameters ===\n')
            file.write(f'Height: {self.height}\n')
            file.write(f'Width: {self.width}\n')
            file.write(f'Number of Roombas: {self.numRoombas}\n')
            file.write(f'Dirty cell density: {self.density}\n')
            file.write(f'Maximum number of steps: {self.storedSteps}\n')
            file.write(f'Maximum amount of time: {self.timeLimit}\n\n')
            file.write(f'=== Results ===\n')
            file.write(f'Total steps taken: {self.storedSteps + 1 - self.stepLimit}\n')
            file.write(f'Total time taken: {time}\n')
            file.write(f'Percentage of dirty tiles: {dirtyPercentage}\n')
            file.write(f'Percentage of clean tiles: {cleanPercentage}\n')
            file.write(agentMoves)

        # print text from data file
        with open(f'data/data_{tmp}.txt') as file:
            print(file.read())