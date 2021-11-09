from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import Model
from agent import RoombaAgent, TileAgent
from mesa.datacollection import DataCollector
import os, time

class RoomModel(Model):
    def __init__(self, total, height, width, stepLimit, density, timeLimit):
        self.stepLimit = stepLimit
        self.height = height
        self.width = width
        self.storedSteps = stepLimit
        self.numRoombas = total
        self.density = density
        self.timeLimit = timeLimit
        self.timeStart = time.time()
        self.grid = MultiGrid(height, width, False)
        self.schedule = RandomActivation(self)
        self.running = True

        self.datacollector = DataCollector(
            {
                # avoid delay
                'time': lambda m: time.time() - self.timeStart,
                # graphs
                'dirty': lambda m: self.countTiles(m, True),
                'clean': lambda m: self.countTiles(m, False),
                # results
                'clean percentage': lambda m: self.getCleanPercentage(m),
                'agent moves': lambda m: {agent.unique_id: agent.moves for agent in self.schedule.agents if isinstance(agent, RoombaAgent)}
            }
        )

        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                t = TileAgent((x,y), self)
                self.schedule.add(t)
                self.grid.place_agent(t, (x,y))

        for i in range(self.numRoombas):
            a = RoombaAgent(i+1, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1,1))

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

        self.stepLimit -= 1
        counter = 0

        # to not get delayed by loop searching for agents
        if time.time()-self.timeStart > self.timeLimit:
            self.finishSchedule()
            return

        for agent in self.schedule.agents:
            if isinstance(agent, TileAgent):
                counter += 1

        if counter == 0 or self.stepLimit == 1:
            self.finishSchedule()

    @staticmethod
    def countTiles(model, countDirty):
        area = model.height * model.width
        counter = 0 if countDirty else area
        # looks worse, more efficient than checking each loop for countDirty
        if countDirty:
            for agent in model.schedule.agents:
                if isinstance(agent, TileAgent):
                    counter += 1
        else:
            for agent in model.schedule.agents:
                if isinstance(agent, TileAgent):
                    counter -= 1
        
        return counter / area * 100

    @staticmethod
    def getCleanPercentage(model):
        counter = 0
        for agent in model.schedule.agents:
            if isinstance(agent, TileAgent):
                counter += 1
        
        return 100 - round(counter / (model.height * model.width), 3) * 100

    def finishSchedule(self):
        self.running = False
        dataFrame = self.datacollector.get_model_vars_dataframe()
        time = f'{round(dataFrame.iloc[-1, 2], 3)} seconds'
        cleanPercentage = f'{dataFrame.iloc[-1, 3]}%'
        agentMoves = '--- Agent Moves ---\n'
        tmpMoves = dataFrame.iloc[-1, 4]
        for agentId in tmpMoves:
            agentMoves += f'Agent {agentId}: {tmpMoves[agentId]} moves\n'
        tmp = 1
        while os.path.exists(f'data/data_{tmp}.txt'):
            tmp += 1
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
            file.write(f'Percentage of clean tiles: {cleanPercentage}\n')
            file.write(agentMoves)
        with open(f'data/data_{tmp}.txt') as file:
            print(file.read())