# Victor Martinez Roman A01746361
# Mayra Fernanda Camacho Rodriguez A01378998

import numpy as np
import matplotlib.pyplot as plt
import mesa
import random

# Robot agent class
class RobotAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.vacuuming = False

    # Gets possible moves from 8 spaces around the agent
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore = True,
                include_center = False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    # Cleans an agent of type DirtyCell by setting isClean to True
    def clean(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            for i in cellmates:
                if isinstance(i, DirtyCell):
                    if i.isClean == False:
                        i.isClean = True
                        self.vacuuming = True

    def step(self):
        if self.vacuuming is False:
            self.move()
            self.clean()
        else:
            self.clean()
            self.vacuuming = False

# DirtyCell agent class
class DirtyCell(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.isClean = False

    def step(self):
        if self.isClean is False:
            pass

# CleaningRobots model class
class CleaningRobots(mesa.Model):

    def __init__(self, R, C, width, height):
        self.num_agentsR = R
        self.num_agentsC = C
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        
        # Create robots
        for i in range(self.num_agentsR):
            a = RobotAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (0, 0))
        
        self.num_agentsC += self.num_agentsR
        
        # Create cells
        for o in range(self.num_agentsR, self.num_agentsC):
            b = DirtyCell(o, self)
            self.schedule.add(b)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(b, (x, y))

        print("Initial dirty cells: " + str(self.num_agentsC))

        self.datacollector = mesa.DataCollector(
                agent_reporters={ "Steps": "pos" })

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

# Initial testing for plotting with matplotlib
if __name__ == '__main__':
    model = RobotModel(5, 10, 10)
    for i in range(10):
        model.step()

    agent_counts = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
        cell_content, x, y = cell
        agent_count = len(cell_content)
        agent_counts[x][y] = agent_count
    plt.imshow(agent_counts, interpolation = "nearest")
    plt.colorbar()

    plt.show()
