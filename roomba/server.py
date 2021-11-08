from model import RoomModel, ObstacleAgent, TileAgent, RoombaAgent
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

dirtyStat = {True: '#3F1703', False: '#FFFFFF'}

def agent_portrayal(agent):
    portrayal = {"Filled": "true"}

    if (isinstance(agent, RoombaAgent)):
        portrayal['Shape'] = 'circle'
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.7

    if (isinstance(agent,ObstacleAgent)):
        portrayal['Shape'] = 'rect'
        portrayal['w'] = 1
        portrayal['h'] = 1
        portrayal['x'] = agent.pos[0]
        portrayal['y'] = agent.pos[1]
        portrayal["Color"] = '#3B3B3B'
        portrayal["Layer"] = 2
        # portrayal["r"] = 0.2

    elif (isinstance(agent, TileAgent)):
        portrayal['Shape'] = 'rect'
        portrayal['w'] = 0.3
        portrayal['h'] = 0.3
        portrayal['x'] = agent.pos[0]
        portrayal['y'] = agent.pos[1]
        portrayal['Color'] = dirtyStat[agent.isDirty]
        portrayal['Layer'] = 0
        # portrayal['r'] = 0.7
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

model_params = {
    'total': 5,
    'height': 10,
    'width': 10,
    'limit': 100,
    'density': UserSettableParameter('slider', 'Dirty Cell Density', 0.5, 0.01, 1.0, 0.1)
}

server = ModularServer(RoomModel,
                       [grid],
                       'Roomba Simulation Model',
                       model_params)
server.port = 8521 # The default
server.launch()