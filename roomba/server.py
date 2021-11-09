from model import RoomModel, TileAgent, RoombaAgent
from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

colorTiles = {'dirty': '#772105', 'clean': '#AAAAAA'}

def agent_portrayal(agent):
    portrayal = {'Filled': 'true'}

    if (isinstance(agent, RoombaAgent)):
        portrayal['Shape'] = 'circle'
        portrayal['Color'] = '#0E8113'
        portrayal['Layer'] = 1
        portrayal['r'] = 0.7

    elif (isinstance(agent, TileAgent)):
        portrayal['Shape'] = 'rect'
        portrayal['w'] = 0.8
        portrayal['h'] = 0.8
        portrayal['x'] = agent.pos[0]
        portrayal['y'] = agent.pos[1]
        portrayal['Color'] = colorTiles['dirty']
        portrayal['Layer'] = 0

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
    'timeLimit': UserSettableParameter(param_type='slider', name='Maximum Amount of Time', value=10, min_value=1, max_value=600, step=1)
}

server = ModularServer(RoomModel,
                       [grid, treeChart, pieChart],
                       'Roomba Simulation Model',
                       model_params)
server.port = 8521 # The default
server.launch()