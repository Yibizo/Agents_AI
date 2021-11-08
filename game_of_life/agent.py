from mesa import Agent

class Cell(Agent):

    def __init__(self, pos, model, isAlive):

        super().__init__(pos, model)
        self.pos = pos
        self.isAlive = isAlive
        self.next = self.isAlive
        
    def step(self):

        self.next = self.isAlive
        counter = 0

        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.isAlive:
                counter += 1

        if self.isAlive and (counter <= 1 or counter >= 4):
            self.next = False

        elif not self.isAlive and counter == 3:
            self.next = True

    def advance(self):

        self.isAlive = self.next