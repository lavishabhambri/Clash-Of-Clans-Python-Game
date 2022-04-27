import numpy as np
import os
from src.screen import Screen
from src.color import *

COLORS = [fg.green, fg.yellow, fg.red]
class Item:
    def __init__(self,pos,size,speed,max_size, health, damage):
        self._size = np.array(size)
        self._color = COLORS[0]
        self._pos = np.array(pos)
        self._structure = np.array([[]])
        self._speed = np.array(speed)
        self._max_size = np.array(max_size)
        self._health = health
        self._maxhealth = health
        self._damage = damage
        

    def get_dimension(self):
        return [self._pos,self._size, self._speed]

    def get_structure(self):
        return self._structure
    
    def color_change(self, symbol):
        if(self._health <= 0.5*self._maxhealth and self._health > 0.2*self._maxhealth): 
            self._structure = np.array([[COLORS[1]+ symbol +reset for j in range(self._size[0])] for i in range(self._size[1])], dtype='object') 
        elif(self._health <= 0.2*self._maxhealth and self._health > 0): 
            self._structure = np.array([[COLORS[2]+ symbol +reset for j in range(self._size[0])] for i in range(self._size[1])], dtype='object') 
            

    def decreaseHealth(self, damage, symbol):
        self._health = self._health - damage   
        if(self._health <= 0):
            self._health = 0
            self._size = [0,0]
            return
        self.color_change(symbol)

    

class TownHall(Item):
    def __init__(self,pos,size,speed,max_size,health, damage):
        super().__init__(pos,size,speed,max_size,health, damage)
        self._speed = speed
        self._size = [4,3]
        self._symbol = 'Î'
        self._health = health
        self._structure = np.array([[self._color+self._symbol+reset for j in range(self._size[0])] for i in range(self._size[1])], dtype='object') 


class WizardTower(Item):
    def __init__(self,pos,size,speed,max_size,health, damage):
        super().__init__(pos,size,speed,max_size,health, damage)
        self._speed = speed
        self._size = [4,3]
        self._symbol = 'W'
        self._health = health
        self._structure = np.array([[self._color+self._symbol+reset for j in range(self._size[0])] for i in range(self._size[1])], dtype='object') 



class Hut(Item):
    def __init__(self,pos,size,speed,max_size,health, damage):
        super().__init__(pos,size,speed,max_size,health, damage)
        self._speed = speed
        self._size = [4,3]
        self._symbol = 'Â'
        self._health = health
        self._structure = np.array([[self._color+self._symbol+reset for j in range(self._size[0])] for i in range(self._size[1])], dtype='object')
        

class Wall(Item):
    def __init__(self,pos,size,speed,max_size,health, damage):
        super().__init__(pos,size,speed,max_size,health,0)
        self._speed = speed
        self._size = [1,1]
        self._health = 100
        self._symbol = 'W'
        self._structure = np.array([[self._color+self._symbol+reset for j in range(self._size[0])] for i in range(self._size[1])], dtype='object')
        

class Cannon(Item):
    def __init__(self,pos,size,speed,max_size,health,rangeVal,damage):
        super().__init__(pos,size,speed,max_size,health, damage)
        self._speed = speed
        self._size = [1,1]
        self._symbol = 'C'
        self._structure = np.array([[self._color+self._symbol+reset for j in range(self._size[0])] for i in range(self._size[1])], dtype='object')
        self._rangeVal = rangeVal
        self._health = 250
        self._damage = damage
        

class SpawningPoint(Item):
    def __init__(self,pos,size,speed,max_size,health, damage):
        super().__init__(pos,size,speed,max_size,health, 0)
        self._speed = speed
        self._size = [1,1]
        self._symbol = 'S'
        self._structure = np.array([[fg.lightcyan+self._symbol+reset for j in range(self._size[0])] for i in range(self._size[1])], dtype='object')
        

class HealthBar(Item):
    def __init__(self,pos,size,speed,max_size,health, damage):
        super().__init__(pos,size,speed,max_size,health, 0)
        self._speed = speed
        self._size = size
        self._symbol = ' '
        self._health = health
        self._structure = np.array([[bg.green+self._symbol+reset for j in range(int(self._size[0]))] for i in range(int(self._size[1]))], dtype='object')

    def decreaseLength(self, maxHealth, health):
        self._size[0] = int((30 * health)/maxHealth)
        if(self._size[0] <= 0):
            self._size = [0,0]
        


class King(Item):
    def __init__(self,pos,size,speed,max_size,health,rangeVal,damage):
        super().__init__(pos,size,speed,max_size,health,damage)
        self._speed = speed
        self._size = [1,1]
        self._damage = 50
        self._health = 500
        self._symbol = 'K'
        self._structure = np.array([[fg.lightcyan +self._symbol+reset for j in range(self._size[0])] for i in range(self._size[1])], dtype='object')
        

    def move(self,ch,free_movement):
        print(free_movement)
        if( (ch=='w' or ch=='W') and free_movement[0] != 1):
            self._pos[1] = self._pos[1] - self._speed[1]
            if(self._pos[1] <= 1 or (self._pos[1]>1 and self._pos[1] <=1 )):
                self._pos[1] = 1

        elif((ch=='s' or ch=='S') and free_movement[2] != 1):
            self._pos[1] = self._pos[1] + self._speed[1]
            if(self._pos[1] >= self._max_size[1]-2):
                self._pos[1] = self._max_size[1]-2

        elif((ch=='d' or ch=='D') and free_movement[1] != 1):
            self._pos[0] = self._pos[0] + self._speed[0]
            if(self._pos[0]+self._size[0] >= self._max_size[0]-2):
                self._pos[0] = self._max_size[0] - self._size[0] - 2

        elif((ch=='a' or ch=='A') and free_movement[3] != 1):
            self._pos[0] = self._pos[0] - self._speed[0]
            if(self._pos[0] <= 2):
                self._pos[0] = 2

class ArcherQueen(Item):
    def __init__(self,pos,size,speed,max_size,health,rangeVal,damage):
        super().__init__(pos,size,speed,max_size,health,damage)
        self._speed = speed
        self._size = [1,1]
        self._damage = 50
        self._health = 500
        self._symbol = 'Q'
        self._structure = np.array([[fg.lightcyan +self._symbol+reset for j in range(self._size[0])] for i in range(self._size[1])], dtype='object')
        

    def move(self,ch,free_movement):
        
        print(free_movement)
        if( (ch=='w' or ch=='W') and free_movement[0] != 1):
            self._pos[1] = self._pos[1] - self._speed[1]
            if(self._pos[1] <= 1 or (self._pos[1]>1 and self._pos[1] <=1 )):
                self._pos[1] = 1

        elif((ch=='s' or ch=='S') and free_movement[2] != 1):
            self._pos[1] = self._pos[1] + self._speed[1]
            if(self._pos[1] >= self._max_size[1]-2):
                self._pos[1] = self._max_size[1]-2

        elif((ch=='d' or ch=='D') and free_movement[1] != 1):
            self._pos[0] = self._pos[0] + self._speed[0]
            if(self._pos[0]+self._size[0] >= self._max_size[0]-2):
                self._pos[0] = self._max_size[0] - self._size[0] - 2

        elif((ch=='a' or ch=='A') and free_movement[3] != 1):
            self._pos[0] = self._pos[0] - self._speed[0]
            if(self._pos[0] <= 2):
                self._pos[0] = 2



class Barbarian(Item):
    def __init__(self,pos,size,speed,max_size,health,rangeVal,damage):
        super().__init__(pos,size,speed,max_size,health,damage)
        self._speed = speed
        self._size = [1,1]
        self._damage = 20
        self._health = 250
        self._symbol = 'B'
        self._structure = np.array([[fg.lightcyan + self._symbol+reset for j in range(self._size[0])] for i in range(self._size[1])], dtype='object')
        self._isMoving = True
        
    def _move(self, closest_obj): 

        if(self._isMoving == False):
            return

        object_pos, object_size, object_speed = closest_obj[1].get_dimension()
        obj_x = object_pos[0]
        obj_y = object_pos[1]
        x_steps = self._pos[0] - obj_x
        y_steps = self._pos[1] - obj_y

        if (x_steps > 4): # left
            self._pos[0] -= self._speed[0]
            x_steps = self._pos[0] - obj_x
            
                        
        if (x_steps < -1): # right
            self._pos[0] += self._speed[0]
            x_steps = self._pos[0] - obj_x     

        if (y_steps > 2): # top
                self._pos[1] -= self._speed[1]
                y_steps = self._pos[1] - obj_y
                

        if (y_steps < 2): # bottom
                self._pos[1] += self._speed[1]
                y_steps = self._pos[1] - obj_y

class Archer(Item):
    def __init__(self,pos,size,speed,max_size,health,rangeVal,damage):
        super().__init__(pos,size,speed,max_size,health,damage)
        self._speed = speed
        self._size = [1,1]
        self._damage = 10
        self._health = 125
        self._symbol = 'A'
        self._structure = np.array([[fg.lightcyan + self._symbol+reset for j in range(self._size[0])] for i in range(self._size[1])], dtype='object')
        self._isMoving = True
        
    def _move(self, closest_obj): 

        if(self._isMoving == False):
            return
        object_pos, object_size, object_speed = closest_obj[1].get_dimension()
        obj_x = object_pos[0]
        obj_y = object_pos[1]
        x_steps = self._pos[0] - obj_x
        y_steps = self._pos[1] - obj_y

        if (x_steps > 4): # left
            self._pos[0] -= self._speed[0]
            x_steps = self._pos[0] - obj_x
            
                        
        if (x_steps < -1): # right
            self._pos[0] += self._speed[0]
            x_steps = self._pos[0] - obj_x     

        if (y_steps > 2): # top
                self._pos[1] -= self._speed[1]
                y_steps = self._pos[1] - obj_y
                

        if (y_steps < 2): # bottom
                self._pos[1] += self._speed[1]
                y_steps = self._pos[1] - obj_y

    
class Balloon(Item):
    def __init__(self,pos,size,speed,max_size,health,rangeVal,damage):
        super().__init__(pos,size,speed,max_size,health,damage)
        self._speed = speed
        self._size = [1,1]
        self._damage = 40
        self._health = 250
        self._symbol = 'O'
        self._structure = np.array([[fg.lightcyan + self._symbol+reset for j in range(self._size[0])] for i in range(self._size[1])], dtype='object')
        self._isMoving = True
        
    def _move(self, closest_obj): 
        if(closest_obj[1]._symbol == 'C'):
            object_pos, object_size, object_speed = closest_obj[1].get_dimension()
            obj_x = object_pos[0]
            obj_y = object_pos[1]
            x_steps = self._pos[0] - obj_x
            y_steps = self._pos[1] - obj_y

            if (x_steps > 1): # left
                self._pos[0] -= self._speed[0]
                x_steps = self._pos[0] - obj_x
                
                            
            if (x_steps < 0): # right
                if(self._pos[0] + self._speed[0] > self._pos[0] - obj_x):
                    self._pos[0] += self._speed[0]/2
                else:
                    self._pos[0] += self._speed[0]
                x_steps = self._pos[0] - obj_x     

            if (y_steps > 1): # top
                    self._pos[1] -= self._speed[1]
                    y_steps = self._pos[1] - obj_y
                    
            if (y_steps < 1): # bottom
                    self._pos[1] += self._speed[1]
                    y_steps = self._pos[1] - obj_y 
        else:
            object_pos, object_size, object_speed = closest_obj[1].get_dimension()
            obj_x = object_pos[0]
            obj_y = object_pos[1]
            x_steps = self._pos[0] - obj_x
            y_steps = self._pos[1] - obj_y

            if (x_steps > 2): # left
                self._pos[0] -= self._speed[0]
                x_steps = self._pos[0] - obj_x
                
                            
            if (x_steps < 0): # right
                self._pos[0] += self._speed[0]
                x_steps = self._pos[0] - obj_x     

            if (y_steps > 2): # top
                    self._pos[1] -= self._speed[1]
                    y_steps = self._pos[1] - obj_y
                    

            if (y_steps < 2): # bottom
                    self._pos[1] += self._speed[1]
                    y_steps = self._pos[1] - obj_y
        
        