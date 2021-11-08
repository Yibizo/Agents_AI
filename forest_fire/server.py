from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from model import ForestFire

colors = {'fine': '#00FF00', 'on fire': '#AA0000', 'burned out': '#000000'}

def forest_fire_portrayal(tree):
    
    if tree is None:
        return

    portrayal = {'Shape': 'rect', 'w': 0.7, 'h': 0.7, 'Filled': 'true', 'Layer': 0}
    (x, y) = tree.pos

    portrayal['x'] = x
    portrayal['y'] = y
    portrayal['Color'] = colors[tree.condition]

    return portrayal

canvas_element = CanvasGrid(forest_fire_portrayal, 100, 100, 500, 500)

model_params = {
    'height': 100,
    'width': 100,
    'density': UserSettableParameter('slider', 'Tree density', 0.6, 0.01, 1.0, 0.1)
}

server = ModularServer(
    ForestFire, [canvas_element], 'Forest Fire', model_params
)

server.launch()