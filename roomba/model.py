from mesa.time import RandomActivation
from mesa.space import MultiGrid # IMPORTANT CHANGE FROM SINGLE TO MULTI
from mesa import Model
from agent import RoombaAgent, ObstacleAgent, TileAgent

class RoomModel(Model):
    def __init__(self, total, height, width, limit, density):
        self.limit = limit
        self.num_agents = total
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
            a = ObstacleAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, posLimitArr[i])

        tilesArr = []

        for col in range(1, height-1):
            for row in range(1, width-1):
                tilesArr.append((col, row))

        for i in range(len(tilesArr)):
            t = TileAgent(1000+i, self, True) if self.random.random() < density else TileAgent(i+40000, self, False)
            self.schedule.add(t)
            self.grid.place_agent(t, tilesArr[i])

        for i in range(self.num_agents):
            a = RoombaAgent(2000+i, self)
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