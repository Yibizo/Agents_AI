from mesa.time import RandomActivation
from mesa.space import MultiGrid # IMPORTANT CHANGE FROM SINGLE TO MULTI
from mesa import Model
from agent import RoombaAgent, ObstacleAgent, TileAgent
import os

class RoomModel(Model):
    def __init__(self, total, height, width, limit, density):
        self.limit = limit
        self.height = height
        self.width = width
        self.storedSteps = limit
        self.num_agents = total
        self.density = density
        self.grid = MultiGrid(height,width,False)
        self.schedule = RandomActivation(self)
        self.running = True

        # obstacles around grid
        numObs = (height * 2) + (width * 2 - 4)
        posLimitArr = []
        # columns
        for col in [0,height-1]:
            for row in range(width):
                posLimitArr.append((col,row))
        # rows
        for col in range(1,height-1):
            for row in [0,width-1]:
                posLimitArr.append((col,row))
        # print(posLimitArr)

        for i in range(numObs):
            a = ObstacleAgent(posLimitArr[i], self)
            self.schedule.add(a)
            self.grid.place_agent(a, posLimitArr[i])

        for (contents, x, y) in self.grid.coord_iter():
            if (x != 0 and x != width-1) and (y != 0 and y != height-1):
                t = TileAgent((x,y), self, True) if self.random.random() < density else TileAgent((x,y), self, False)
                self.schedule.add(t)
                self.grid.place_agent(t, (x,y))

        for i in range(self.num_agents):
            a = RoombaAgent(i+1, self)
            self.schedule.add(a)
            # Add the agent to a random empty grid cell
            # x = self.random.randrange(self.grid.width)
            # y = self.random.randrange(self.grid.height)
            # check = self.grid.get_cell_list_contents([(x,y)])
            # while (isinstance(check[0], ObstacleAgent)):
            #     x = self.random.randrange(self.grid.width)
            #     y = self.random.randrange(self.grid.height)
            #     check = self.grid.get_cell_list_contents([(x,y)])
            # self.grid.place_agent(a, (x, y))
            self.grid.place_agent(a, (1,1))

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.limit -= 1

        counter = 0
        for agent in self.schedule.agents:
            if isinstance(agent, TileAgent) and agent.isDirty:
                counter += 1

        if counter == 0 or self.limit == 1:
            self.running = False
            tmp = 1
            while os.path.exists(f'data/data_{tmp}.txt'):
                tmp += 1
            with open(f'data/data_{tmp}.txt', 'x') as file:
                file.write(f'=== Parameters ===\n')
                file.write(f'Height: {self.height}\n')
                file.write(f'Width: {self.width}\n')
                file.write(f'Number of Roombas: {self.num_agents}\n')
                file.write(f'Maximum number of steps: {self.storedSteps}\n')
                file.write(f'Dirty cell density: {self.density}\n\n')
                file.write(f'=== Results ===\n')
                file.write(f'Total steps taken: {self.storedSteps + 1 - self.limit}\n')
                file.write(f'Percentage of clean tiles: {100 - (round((counter / ((self.height-2) * (self.width-2))) * 100, 3))}%\n')
                for agent in self.schedule.agents:
                    if isinstance(agent, RoombaAgent):
                        file.write(f'Agent {agent.unique_id}: {agent.moves} moves taken\n')