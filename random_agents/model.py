from mesa.time import RandomActivation
from mesa.space import MultiGrid # IMPORTANT CHANGE FROM SINGLE TO MULTI
from mesa import Model
from agent import RandomAgent, ObstacleAgent, TileAgent

class RandomModel(Model):
    """ Modelo para los autos """
    def __init__(self, N,ancho,alto):
        self.num_agents = N
        self.grid = MultiGrid(ancho,alto,False) #NO Es Toroidal
        self.schedule = RandomActivation(self)
        self.running = True #Para la visualizacion

        #Crear obstaculos en los limites del grid
        numObs = (ancho * 2) + (alto * 2 - 4)
        listaPosLimite = []
        #Las dos columnas límite
        for col in [0,ancho-1]:
            for ren in range(alto):
                listaPosLimite.append((col,ren))
        #Los dos renglones limite
        for col in range(1,ancho-1):
            for ren in [0,alto-1]:
                listaPosLimite.append((col,ren))
        print(listaPosLimite)

        for i in range(numObs):
            a = ObstacleAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, listaPosLimite[i])

        # tmp = ObstacleAgent(10000, self)
        # self.schedule.add(tmp)
        # self.grid.place_agent(tmp, (2,3))

        tmp = TileAgent(20000, self)
        self.schedule.add(tmp)
        self.grid.place_agent(tmp, (2,3))

        for i in range(self.num_agents):
            a = RandomAgent(i+1000, self) #La numeracion de los agentes empieza en el 1000
            self.schedule.add(a)
            # Add the agent to a random empty grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            while (not self.grid.is_cell_empty((x,y))):
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            # self.grid.place_agent(a, (x, y)) TODO:
            self.grid.place_agent(a, (2,2))

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
