from model import RoomModel, TileAgent, RoombaAgent
from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

colorTiles = {'dirty': '#3F1703', 'clean': '#AAAAAA'}

def agent_portrayal(agent):
    portrayal = {'Filled': 'true'}

    if (isinstance(agent, RoombaAgent)):
        portrayal['Shape'] = 'circle'
        portrayal['Color'] = 'red'
        portrayal['Layer'] = 1
        portrayal['r'] = 0.7

    # if (isinstance(agent,ObstacleAgent)):
    #     portrayal['Shape'] = 'rect'
    #     portrayal['w'] = 1
    #     portrayal['h'] = 1
    #     portrayal['x'] = agent.pos[0]
    #     portrayal['y'] = agent.pos[1]
    #     portrayal['Color'] = '#3B3B3B'
    #     portrayal['Layer'] = 2
    #     # portrayal['r'] = 0.2

    elif (isinstance(agent, TileAgent)):
        portrayal['Shape'] = 'rect'
        portrayal['w'] = 0.3
        portrayal['h'] = 0.3
        portrayal['x'] = agent.pos[0]
        portrayal['y'] = agent.pos[1]
        portrayal['Color'] = '#3F1703'
        portrayal['Layer'] = 0
        # portrayal['r'] = 0.7
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

treeChart = ChartModule(
    [{'Label': label, 'Color': color} for (label, color) in colorTiles.items()]
)

pieChart = PieChartModule(
    [{'Label': label, 'Color': color} for (label, color) in colorTiles.items()]
)

model_params = {
    'total': UserSettableParameter(param_type='slider', name='Number of Roombas', value=2, min_value=1, max_value=30, step=1),
    'height': 10,
    'width': 10,
    'density': UserSettableParameter(param_type='slider', name='Dirty Cell Density', value=0.5, min_value=0.1, max_value=1.0, step=0.1),
    'stepLimit': UserSettableParameter(param_type='slider', name='Maximum Number of Steps', value=500, min_value=10, max_value=1000, step=10),
    'timeLimit': UserSettableParameter(param_type='slider', name='Maximum Amount of Time', value=10, min_value=1, max_value=60, step=1)
}

server = ModularServer(RoomModel,
                       [grid, treeChart, pieChart],
                       'Roomba Simulation Model',
                       model_params)
server.port = 8521 # The default
server.launch()