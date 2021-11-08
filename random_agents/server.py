from model import RandomModel, ObstacleAgent, TileAgent
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

dirtyStat = {True: '#4F1E04', False: '#FFFFFF'}

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "red",
                 "r": 0.5}

    if (isinstance(agent,ObstacleAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.2

    if (isinstance(agent, TileAgent)):
        portrayal['Color'] = 'brown'
        portrayal['Layer'] = 0
        portrayal['r'] = 1
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(RandomModel,
                       [grid],
                       "Trafic Model",
                       {"N":1, "ancho":10, "alto":10})
server.port = 8521 # The default
server.launch()