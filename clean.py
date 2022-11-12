# Victor Martinez Roman A01746361
# Mayra Fernanda Camacho Rodriguez A01378998

from mesa.visualization.modules import ChartModule
from robot import *
import mesa
import random

# Visualize agents and it respective color code
def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}
    if isinstance(agent, DirtyCell):
        if agent.isClean:
            portrayal["Color"] = "red"
        else:
            portrayal["Color"] = "grey"
    if isinstance(agent, RobotAgent):
        portrayal["Color"] = "blue"
    return portrayal

# Serves as a dice to generate random size grid
def diceSize():
    return random.randint(3, 12)

x = diceSize()
y = diceSize()

# Instanciate grid and chart
grid = mesa.visualization.CanvasGrid(agent_portrayal, x, y, 500, 500)
chart = ChartModule([{ "Label": "Steps",
                      "Color": "Black" }],
                    data_collector_name = 'datacollector')

# Start mesa server
server = mesa.visualization.ModularServer(
        CleaningRobots,
        [grid, chart],
        "Cleaning robots",
        {"R": diceSize(),
         "C": diceSize(),
         "width": x,
         "height": y})
server.port = 8521
server.launch()
