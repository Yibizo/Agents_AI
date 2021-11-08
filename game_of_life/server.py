from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from model import Population

colors = {True: '#000000', False: '#FFFFFF'}

def cell_population_portrayal(cell):

    portrayal = {'Shape': 'rect', 'w': 0.7, 'h': 0.7, 'Filled': 'true', 'Layer': 0}
    (x, y) = cell.pos

    portrayal['x'] = x
    portrayal['y'] = y
    portrayal['Color'] = colors[cell.isAlive]

    return portrayal

canvas_element = CanvasGrid(cell_population_portrayal, 100, 100, 500, 500)

model_params = {
    'height': 100,
    'width': 100,
    'density': UserSettableParameter('slider', 'Cell density', 0.1, 0.01, 1.0, 0.1)
}

server = ModularServer(
    Population, [canvas_element], 'Game of Life', model_params
)

server.launch()