from mesa import Agent
import random

class RoombaAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.direction = 0 #Frente 0, Derecha 1, Izquierda 2, Atras 3
        self.orientation = 3 #Derecha 0, Izquierda 1, Arriba 2, Abajo 3
        #El sentido toma en consideracion que las columnas crecen a la derecha y los renglones
        # crecen hacia arriba

    def isFreeMyDirection(self,listFreeSpaces,list_possible_steps):
        if (self.orientation == 0): #Derecha
            if(self.direction == 0): #Frente
                return listFreeSpaces[7],list_possible_steps[7]
            elif (self.direction == 1): #Derecha
                return listFreeSpaces[6],list_possible_steps[6]
            elif(self.direction == 2): #Izquierda
                return listFreeSpaces[8],list_possible_steps[8]
            elif(self.direction == 3): #Atras
                return listFreeSpaces[1],list_possible_steps[1]
            else:
                print('Error in self.direction')
                return False,(-1,-1)
        elif (self.orientation == 1): #Izquierda
            if(self.direction == 0): #Frente
                return listFreeSpaces[1],list_possible_steps[1]
            elif (self.direction == 1): #Derecha
                return listFreeSpaces[2],list_possible_steps[2]
            elif(self.direction == 2): #Izquierda
                return listFreeSpaces[0],list_possible_steps[0]
            elif(self.direction == 3): #Atras
                return listFreeSpaces[7],list_possible_steps[7]
            else:
                print('Error in self.direction')
                return False,(-1,-1)
        elif (self.orientation == 2): #Arriba
            if(self.direction == 0): #Frente
                return listFreeSpaces[5],list_possible_steps[5]
            elif (self.direction == 1): #Derecha
                return listFreeSpaces[8],list_possible_steps[8]
            elif(self.direction == 2): #Izquierda
                return listFreeSpaces[2],list_possible_steps[2]
            elif(self.direction == 3): #Atras
                return listFreeSpaces[3],list_possible_steps[3]
            else:
                print('Error in self.direction')
                return False,(-1,-1)
        elif (self.orientation == 3): #Abajo
            if(self.direction == 0): #Frente
                return listFreeSpaces[3],list_possible_steps[3]
            elif (self.direction == 1): #Derecha
                return listFreeSpaces[0],list_possible_steps[0]
            elif(self.direction == 2): #Izquierda
                return listFreeSpaces[6],list_possible_steps[6]
            elif(self.direction == 3): #Atras
                return listFreeSpaces[5],list_possible_steps[5]
            else:
                print('Error in self.direction')
                return False,(-1,-1)
        else:
            print('Error in self.orientation')
            return False,(-1,-1)

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, #8 conectado. Orden: arriba izquierda, centro, derecha; enmedio izquierda y derecha; abajo izquierda, centro, derecha
            include_center=True) # include own position
        
        myPosition = possible_steps[4]

        # verify free spaces around agent
        freeSpaces = []
        for pos in possible_steps:
            check = self.model.grid.get_cell_list_contents([pos]) # THIS IS A LIST, USE FIRST ELEMENT
            if len(check) == 1 and isinstance(check[0], TileAgent):
                freeSpaces.append(True)
            else:
                freeSpaces.append(False)

        #Movimiento tomando en consideración la dirección y si está libre ese espacio
        free,newPos = self.isFreeMyDirection(freeSpaces,possible_steps)
        if free:
            self.model.grid.move_agent(self,newPos)
            print(f'Moving from {myPosition} to {newPos} because it goes towards {self.direction}\n')
        else:
            print(f'Can\'t move in orientation {self.orientation}, tile occupied')
            newOrientation = random.randint(0,3)
            while (newOrientation == self.orientation):
                newOrientation = random.randint(0,3)
            self.orientation = newOrientation
            print(f'Changing orientation towards {self.orientation}\n')



    def step(self):
        check = self.model.grid.get_cell_list_contents([self.pos])
        if check[0].isDirty:
            check[0].isDirty = False
            print(f'Agent {self.unique_id}: cleaning tile {self.pos}')
        else:
            # random movement
            self.direction = random.randint(0,3)
            print(f'Agent {self.unique_id}: movement in direction {self.direction}')
            self.move()

class ObstacleAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    # def step(self):
    #     pass  


class TileAgent(Agent):
    def __init__(self, unique_id, model, isDirty):
        super().__init__(unique_id, model)
        self.isDirty = isDirty

    # def step(self):
    #     pass