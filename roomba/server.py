from model import RoomModel, ObstacleAgent, TileAgent
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

dirtyStat = {True: '#3F1703', False: '#FFFFFF'}

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

    elif (isinstance(agent, TileAgent)):
        portrayal['Color'] = dirtyStat[agent.isDirty]
        portrayal['Layer'] = 0
        portrayal['r'] = 0.7
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

model_params = {
    'total': 3,
    'height': 10,
    'width': 10,
    'limit': 100,
    'density': UserSettableParameter('slider', 'Dirty Cell Density', 0.5, 0.01, 1.0, 0.1)
}

server = ModularServer(RoomModel,
                       [grid],
                       "Trafic Model",
                       model_params)
server.port = 8521 # The default
server.launch()