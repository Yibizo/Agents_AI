'''
Author: Diego Mejía Suárez

Modification Date: 09/11/21

Description: Program that contains server to run for the simulation to be viewed
'''

from model import RoomModel, TileAgent, RoombaAgent
from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule, BarChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

# colors for graphs
colorPercentage = {'dirty percentage': '#772105', 'clean percentage': '#AAAAAA'}

# function: define how to portray an agent according to its type
# parameters: Agent agent
# return: dictionary portrayal
def agent_portrayal(agent):
    portrayal = {'Filled': 'true'}

    # if agent given is a Roomba agent
    if (isinstance(agent, RoombaAgent)):
        portrayal['Shape'] = 'circle'
        portrayal['Color'] = '#0E8113'
        portrayal['Layer'] = 1
        portrayal['r'] = 0.7

    # if agent given is a Tile agent
    elif (isinstance(agent, TileAgent)):
        portrayal['Shape'] = 'rect'
        portrayal['w'] = 0.8
        portrayal['h'] = 0.8
        portrayal['x'] = agent.pos[0]
        portrayal['y'] = agent.pos[1]
        portrayal['Color'] = colorTiles['dirty']
        portrayal['Layer'] = 0

    return portrayal

# define grid proportions
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

# line chart to be graphed according to dirty vs. clean tile percentage
treeChart = ChartModule(
    [{'Label': label, 'Color': color} for (label, color) in colorPercentage.items()]
)

# bar chart to be graphed according to dirty vs. clean tile percentage
pieChart = PieChartModule(
    [{'Label': label, 'Color': color} for (label, color) in colorPercentage.items()]
)

# initialize parameters to be given to the model
model_params = {
    'total': UserSettableParameter(param_type='slider', name='Number of Roombas', value=3, min_value=1, max_value=30, step=1),
    'height': 10,
    'width': 10,
    'density': UserSettableParameter(param_type='slider', name='Dirty Cell Density', value=0.5, min_value=0.1, max_value=1.0, step=0.1),
    'stepLimit': UserSettableParameter(param_type='slider', name='Maximum Number of Steps', value=500, min_value=10, max_value=200, step=10),
    'timeLimit': UserSettableParameter(param_type='slider', name='Maximum Amount of Time', value=30, min_value=10, max_value=600, step=10)
}

# server variable that contains the model with its given parameters and the graphs
server = ModularServer(RoomModel,
                       [grid, treeChart, pieChart],
                       'Roomba Simulation Model',
                       model_params)
# define server port and launch the server
server.port = 8521
server.launch()