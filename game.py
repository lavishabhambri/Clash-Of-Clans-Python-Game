from asyncio import constants
from re import A, S
from select import select
import sys
import json
from tkinter.tix import Tree
from src.input import input_to
import os
import numpy as np
import time
from src.Objects import Barbarian, Archer, Balloon , Cannon, Hut, King, ArcherQueen, SpawningPoint, TownHall, WizardTower, Wall, HealthBar
from src.screen import Screen
import src.input
from src.color import *
from src.input import Get



# todo 
# 5. check all points from doc are implemented or not
# 6. Implement bonus of queen

KEYS = ['a','s','w','d']

class Game:
    def __init__(self):
        rows, cols = os.popen('stty size', 'r').read().split()

        if(int(rows) < 32 or int(cols) < 128):
            print("Expand terminal size!")
            sys.exit(0)
        self._margin = int(0.4*(int(rows)))
        
        self._floor = int(0.1*(int(rows)))-4
        self._width = int(cols) - self._margin
        self._height = int(rows) - self._floor-4
        self._time = time.time()
        self._screen = Screen(self._height, self._width)
        self._level = 0

        self._maxWizardTower = 2
        self._maxCannon = 2

        self.make_layout()
        self.free_movement = [0,0,0,0]
        self.previous_movement = [0,0,0,0]

        # For replay
        self._iteration = 0
        self._isReplay = False
        self._dictionary = {}
        self._replayName = ""
        self._lastMove = ''

        # For Winning
        self._win = True
        self._Loose = True
   
        self._maxBarbarians = 10
        self._currentBarbarians = 0

        self._maxArchers = 10
        self._currentArchers = 0

        self._maxBalloons = 10
        self._currentBalloons = 0

        self._balloonChasingCannon = True
        self._numDeadCannonWizard = 0

        


    def make_layout(self):
        size = 13
        left = size * 2 - 5
        top = 5        

        self._townhall = TownHall([int(self._width/2)-6, self._height/2],[13,1],[0,0], [self._width,self._height], 1000, 20)
        self._huts = []
        self._huts.append(Hut([int(self._width/2)+1, self._height/2-8],[1,1],[0,0], [self._width,self._height], 500, 10))
        self._huts.append(Hut([int(self._width/2)-20, self._height/2-4],[1,1],[0,0], [self._width,self._height], 500, 10))
        self._huts.append(Hut([int(self._width/2)-10, self._height/2+5],[1,1],[0,0], [self._width,self._height], 500, 10))
        self._huts.append(Hut([int(self._width/2)+19, self._height/2+7],[1,1],[0,0], [self._width,self._height], 500, 10))
        self._huts.append(Hut([int(self._width/2)+12, self._height/2-3],[1,1],[0,0], [self._width,self._height], 500, 10))

        self._wizardTowers = []
        self._wizardTowers.append(WizardTower([int(self._width/2), self._height/2 + 3],[13,1],[0,0], [self._width,self._height], 1000, 50))
        self._wizardTowers.append(WizardTower([int(self._width/2) - 12, self._height/2 - 3],[13,1],[0,0], [self._width,self._height], 1000, 50))


        self._walls = []

        # horizontal walls
        for i in range(80):
            self._walls.append(Wall([int(self._width/2) + 40 - i, self._height- 8],[1,1],[0,0], [self._width,self._height], 100, 0))
            self._walls.append(Wall([int(self._width/2) + 40 - i,  10],[1,1],[0,0], [self._width,self._height], 100, 0))

        # vertical walls
        for i in range(31):
            self._walls.append(Wall([int(self._width/2) - 40, 10 + i],[1,1],[0,0], [self._width,self._height], 100, 0))
            self._walls.append(Wall([int(self._width/2) + 40 , 10 + i],[1,1],[0,0], [self._width,self._height], 100, 0))    
        

        self._cannons = []
        self._cannons.append(Cannon([int(self._width/2) - 5, self._height/2 + 4],[1,1],[0,0], [self._width,self._height], 250, 5, 15))
        self._cannons.append(Cannon([int(self._width/2)-25, self._height/2 - 6],[1,1],[0,0], [self._width,self._height], 250, 5, 15))


        self._spawningpoints = []
        self._spawningpoints.append(SpawningPoint([self._width - 23, self._height - 13],[1,1],[0,0], [self._width,self._height], 250, 0))
        self._spawningpoints.append(SpawningPoint([13, self._height/2],[1,1],[0,0], [self._width,self._height], 250, 0))
        self._spawningpoints.append(SpawningPoint([self._width - 35, 5],[1,1],[0,0], [self._width,self._height], 250, 0))

        
        if(kingKey == 'o' or kingKey == 'O'):
            self._king = King([int(self._width/2)-21, self._height/2 - 21],[13,1],[1,1], [self._width,self._height], 500, 1, 50)
        else:
            self._king = ArcherQueen([int(self._width/2)-21, self._height/2 - 21],[13,1],[1,1], [self._width,self._height], 500, 1, 40)
            
        self._barbarians = []
        self._archers = []
        self._balloons = []
        self._healthBar = HealthBar([self._width - 45, self._height-3],[int(30), 1],[0,0], [self._width,self._height], self._king._health, 0)


        if(self._level == 1 or self._level == 2):
            self._maxCannon += 1
            self._maxWizardTower += 1
            self._cannons.append(Cannon([int(self._width/2) + 25, self._height/2],[1,1],[0,0], [self._width,self._height], 250, 5, 15))
            self._wizardTowers.append(WizardTower([int(self._width/2) + 25, self._height/2 - 6],[13,1],[0,0], [self._width,self._height], 1000, 50))

        if(self._level == 2):
            self._maxCannon += 1
            self._maxWizardTower += 1
            self._cannons.append(Cannon([int(self._width/2) + 15, self._height/2 + 6],[1,1],[0,0], [self._width,self._height], 250, 5, 15))
            self._wizardTowers.append(WizardTower([int(self._width/2) + 10, self._height/2 + 10],[13,1],[0,0], [self._width,self._height], 1000, 50))
            





    def closestObjectForTroop(self, Player, huts, townhall): # wall, townhall, building
        player_pos,player_size,player_speed = Player.get_dimension()
        x = player_pos[0]
        y = player_pos[1]

        distances = []
        for hut in huts:
            hut_pos,hut_size,hut_speed = hut.get_dimension()
            x_h = hut_pos[0]
            y_h = hut_pos[1]
            d = abs(x_h - x) + abs(y_h - y)
            distances.append([d, hut])


        townhall_pos, townhall_size, townhall_speed = townhall.get_dimension()
        x_t = townhall_pos[0]
        y_t = townhall_pos[1]
        d = abs(x_t - x) + abs(y_t - y)
        distances.append([d, townhall])
        distances  = sorted(distances, key=lambda x: x[0])
        return distances


    def closestObjectForBalloon(self, Player, cannons, wizardTowers): # wall, townhall, building
        player_pos,player_size,player_speed = Player.get_dimension()
        x = player_pos[0]
        y = player_pos[1]

        distances = []
        for cannon in cannons:
            cannon_pos,cannon_size,cannon_speed = cannon.get_dimension()
            x_h = cannon_pos[0]
            y_h = cannon_pos[1]
            d = abs(x_h - x) + abs(y_h - y)
            distances.append([d, cannon])


        for wizardTower in wizardTowers:
            wizardTower_pos, wizardTower_size, wizardTower_speed = wizardTower.get_dimension()
            x_t = wizardTower_pos[0]
            y_t = wizardTower_pos[1]
            d = abs(x_t - x) + abs(y_t - y)
            distances.append([d, wizardTower])
        
        distances  = sorted(distances, key=lambda x: x[0])
        return distances    
    

    def closestNonAttackingBuildingForBalloon(self, Player, huts, townHall): # wall, townhall, building
        player_pos,player_size,player_speed = Player.get_dimension()
        x = player_pos[0]
        y = player_pos[1]

        distances = []
        for hut in huts:
            hut_pos,hut_size,hut_speed = hut.get_dimension()
            x_h = hut_pos[0]
            y_h = hut_pos[1]
            d = abs(x_h - x) + abs(y_h - y)
            distances.append([d, hut])

        
        townHall_pos, townHall_size, townHall_speed = townHall.get_dimension()
        x_t = townHall_pos[0]
        y_t = townHall_pos[1]
        d = abs(x_t - x) + abs(y_t - y)
        distances.append([d, townHall])
        
        distances  = sorted(distances, key=lambda x: x[0])
        return distances    


    def spawn_barbarian(self, ch):
        if(ch == 'r' or ch == 'R'):
            spawn_pos,spawn_size,spawn_speed = self._spawningpoints[0].get_dimension()
            self._barbarians.append(Barbarian([int(spawn_pos[0])-1, int(spawn_pos[1]) - 1],[13,1],[1,1], [self._width,self._height], 1000, 0, 50))

        if(ch == 't' or ch == 'T'):
            spawn_pos,spawn_size,spawn_speed = self._spawningpoints[1].get_dimension()
            self._barbarians.append(Barbarian([int(spawn_pos[0])-1, int(spawn_pos[1]) - 1],[13,1],[1,1], [self._width,self._height], 1000, 0, 50))

        if(ch == 'y' or ch == 'Y'):
            spawn_pos,spawn_size,spawn_speed = self._spawningpoints[2].get_dimension()
            self._barbarians.append(Barbarian([int(spawn_pos[0])-1, int(spawn_pos[1]) - 1],[13,1],[1,1], [self._width,self._height], 1000, 0, 50))


    def spawn_archers(self, ch):
        if(ch == 'u' or ch == 'U'):
            spawn_pos,spawn_size,spawn_speed = self._spawningpoints[0].get_dimension()
            self._archers.append(Archer([int(spawn_pos[0])-1, int(spawn_pos[1]) - 1],[13,1],[2,2], [self._width,self._height], 500, 7, 25))

        if(ch == 'i' or ch == 'I'):
            spawn_pos,spawn_size,spawn_speed = self._spawningpoints[1].get_dimension()
            self._archers.append(Archer([int(spawn_pos[0])-1, int(spawn_pos[1]) - 1],[13,1],[2,2], [self._width,self._height], 500, 7, 25))

        if(ch == 'o' or ch == 'O'):
            spawn_pos,spawn_size,spawn_speed = self._spawningpoints[2].get_dimension()
            self._archers.append(Archer([int(spawn_pos[0])-1, int(spawn_pos[1]) - 1],[13,1],[2,2], [self._width,self._height], 500, 7, 25))


    def spawn_balloons(self, ch):
        if(ch == 'j' or ch == 'J'):
            spawn_pos,spawn_size,spawn_speed = self._spawningpoints[0].get_dimension()
            self._balloons.append(Balloon([int(spawn_pos[0])-1, int(spawn_pos[1]) - 1],[13,1],[2,2], [self._width,self._height], 500, 0, 100))

        if(ch == 'k' or ch == 'K'):
            spawn_pos,spawn_size,spawn_speed = self._spawningpoints[1].get_dimension()
            self._balloons.append(Balloon([int(spawn_pos[0])-1, int(spawn_pos[1]) - 1],[13,1],[2,2], [self._width,self._height], 500, 0, 100))

        if(ch == 'l' or ch == 'L'):
            spawn_pos,spawn_size,spawn_speed = self._spawningpoints[2].get_dimension()
            self._balloons.append(Balloon([int(spawn_pos[0])-1, int(spawn_pos[1]) - 1],[13,1],[2,2], [self._width,self._height], 500, 0, 100))



    def handle_keyboard_interrupt(self, replay = False, ch = None):
        if replay == False:
            get = Get()
            ch = input_to(get.__call__)
        else:
            time.sleep(0.1)

        if ch in KEYS:
            self._lastMove = ch
            self.free_movement = [0,0,0,0]
            self._dictionary[self._iteration] = ch
            
            # calling collision function
            self.handle_collisions()
            self._king.move(ch,self.free_movement)
        
        if(ch == ' '):
            if(kingKey == 'o' or kingKey == 'O'):
                self.damage_object()
            else:
                self.damage_object_by_queen()
            self._dictionary[self._iteration] = ch
            
        if(ch =='q'):
            # For replay, store in dictionary
            self._dictionary[self._iteration] = ch
            with open('sample.txt', 'w') as convert_file:
                convert_file.write(json.dumps(self._dictionary))
            sys.exit()
        
        if(ch == 'r' or ch =='R' or ch =='t' or ch =='T' or ch =='y' or ch =='Y'):
            self._dictionary[self._iteration] = ch
            if (self._currentBarbarians + 1 <= self._maxBarbarians):
                self._currentBarbarians += 1
                self.spawn_barbarian(ch)

        if(ch == 'u' or ch =='U' or ch =='i' or ch =='I' or ch =='o' or ch =='O'):
            self._dictionary[self._iteration] = ch
            if (self._currentArchers + 1 <= self._maxArchers):
                self._currentArchers += 1
                self.spawn_archers(ch)  

        if(ch == 'j' or ch =='J' or ch =='k' or ch =='K' or ch =='l' or ch =='L'):
            self._dictionary[self._iteration] = ch
            if (self._currentBalloons + 1 <= self._maxBalloons):
                self._currentBalloons += 1
                self.spawn_balloons(ch)        
        
        if (ch == 'g' or ch == 'G'):
            self.rageSpell()
            self.place_items()
        
        if (ch == 'h' or ch == 'H'):
            self.healSpell()
            self.place_items()
        

    def returnPos(self, w, h):
        return self._screen

       
    def place_items(self):
        self._screen.place_object(self._townhall)

        self._screen.place_object(self._king)    

        for hut in self._huts:
            self._screen.place_object(hut)
        
        for wall in self._walls:
            self._screen.place_object(wall)

        for cannon in self._cannons:
            self._screen.place_object(cannon)

        for points in self._spawningpoints:
            self._screen.place_object(points)   

        for barbarian in self._barbarians:
            self._screen.place_object(barbarian) 

        for archer in self._archers:
            self._screen.place_object(archer)   

        for balloon in self._balloons:
            self._screen.place_object(balloon)  

        for wizardTower in self._wizardTowers:
            self._screen.place_object(wizardTower)       

        self._screen.place_object(self._healthBar)

    def damage_king(self):
        # Townhall is defensive 
        self._king.decreaseHealth(self._townhall._damage, self._king._symbol)
        self._healthBar.decreaseLength(self._king._maxhealth, self._king._health )

    # def damage_troop(self, barbarian):
    #     barbarian.decreaseHealth(self._townhall._damage, 'B')
    # damaging health of archer by townhall --> extend for wizard tower

    def damage_troop(self, player):
        player.decreaseHealth(self._townhall._damage, player._symbol)


    def damage_object(self):
        # collision with huts
        for hut in self._huts:
            self.damageHouseHealth(self._king, hut, "HUT", "KING")
        
        # collision with townhall
        self.damageHouseHealth(self._king, self._townhall, "TOWN_HALL", "KING")

        # collision with wizardToward
        for wizardTower in self._wizardTowers:
            self.damageHouseHealth(self._king, wizardTower, "WIZARD_TOWER", "KING")

        # collision with cannon
        for cannon in self._cannons:
            self.damageWallHealth(self._king, cannon, "C", "KING")

        # # collision of balloons with cannons
        for balloon in self._balloons:
            cannonAlive = True
            cannonDead = 0
            for cannon in self._cannons:
                if(cannon._health <= 0):
                    cannonDead += 1
                    continue
                self.damageWallHealth(balloon, cannon, "C", "Balloon")
            
            # self.damageHouseHealth(balloon, self._wizardTower, "Wizard_Tower", "Balloon")

            if(cannonDead == len(self._cannons)):
                for hut in self._huts:
                    self.damageHouseHealth(balloon, hut, "HUT", "Balloon")    
        
                

        # collision with walls
        for wall in self._walls:
            self.damageWallHealth(self._king, wall, "W", "KING")

        for hut in self._huts:
            for b in self._barbarians:
                self.damageHouseHealth(b, hut, "HUT", "BARBARIAN")
        
        # collision with townhall
        for b in self._barbarians:
            self.damageHouseHealth(b, self._townhall, "TOWN_HALL", "BARBARIAN")

    def damage_object_by_queen(self):
        # collision with huts
        for hut in self._huts:
            self.damageHouseByQueen(self._king, hut, "HUT", "KING")
        
        # collision with townhall
        self.damageHouseByQueen(self._king, self._townhall, "TOWN_HALL", "KING")

        # collision with wizardToward
        for wizardTower in self._wizardTowers:
            self.damageHouseByQueen(self._king, wizardTower, "WIZARD_TOWER", "KING")

        # collision with cannon
        for cannon in self._cannons:
            self.damageHouseByQueen(self._king, cannon, "C", "KING")
     
        # collision with walls
        for wall in self._walls:
            self.damageHouseByQueen(self._king, wall, "W", "KING")


    ################ Damage ################################
    def damageHouseHealth(self ,player, object, nameObject, namePlayer):

        if(player._symbol == 'Q'):
            return

        player_pos,player_size,player_speed = player.get_dimension()
        object_pos,object_size,object_speed = object.get_dimension()

        symbol = 'Â'
        if(nameObject == "TOWN_HALL"):
            symbol = 'Î'
        if(nameObject == "WIZARD_TOWER"):
            symbol = 'W'

        if((player_pos[0] - 1 > object_pos[0] - object_size[0]/2) and (player_pos[0] < object_pos[0] + object_size[0]/2 + 2)):

            # top collision   
            if(self.free_movement[0] == 1):         
                if((player_pos[1] - 2 <= object_pos[1] + object_size[1]/2) and (player_pos[1] > object_pos[1])):
                    object.decreaseHealth(player._damage, symbol)
    
            # bottom collision    
            if(self.free_movement[2] == 1):        
                if((player_pos[1] >= object_pos[1] - object_size[1]/2) and (player_pos[1] < object_pos[1])):
                    object.decreaseHealth(player._damage,symbol)

        
        if((player_pos[1] - 1 > object_pos[1] - object_size[1]/2) and (player_pos[1] - 1 < object_pos[1] + object_size[1]/2)):

            # right collision
            if(self.free_movement[1] == 1):
                if((player_pos[0] - 1 >= object_pos[0] - object_size[0]/2) and (player_pos[0] - 2 < object_pos[0] - object_size[0]/2)):
                    object.decreaseHealth(player._damage,symbol)
                    

            # left collision
            if(self.free_movement[3] == 1):
                if((player_pos[0] - 2 <= object_pos[0] + object_size[0]/2) and (player_pos[0] > object_pos[0] + object_size[0]/2)):
                    object.decreaseHealth(player._damage, symbol)
             

    def damageWallHealth(self ,player, object, nameObject, namePlayer):
        if(player._symbol == 'Q'):
            return

        player_pos,player_size,player_speed = player.get_dimension()
        object_pos,object_size,object_speed = object.get_dimension()

        symbol = 'W'
        if(nameObject == "C"):
            symbol = 'C'

        # top collision            
        if((player_pos[1] - 1 == object_pos[1]) and (player_pos[0] == object_pos[0])):
            object.decreaseHealth(player._damage, symbol)

        # bottom collision            
        if((player_pos[1] + 1 == object_pos[1]) and (player_pos[0] == object_pos[0])):
            object.decreaseHealth(player._damage, symbol)

        # right collision
        if((player_pos[0] + 1 == object_pos[0]) and (player_pos[1] == object_pos[1])):
            object.decreaseHealth(player._damage, symbol)

        # left collision
        if((player_pos[0] - 1 == object_pos[0]) and (player_pos[1] == object_pos[1])):
            object.decreaseHealth(player._damage, symbol)



  ############################## ATTACK BY QUEEN ################################### 
    def damageHouseByQueen(self ,player, object, nameObject, namePlayer):

        player_pos,player_size,player_speed = player.get_dimension()
        object_pos,object_size,object_speed = object.get_dimension()

        symbol = 'Â'
        if(nameObject == "TOWN_HALL"):
            symbol = 'Î'
        if(nameObject == "WIZARD_TOWER"):
            symbol = 'W'
        if(nameObject == "C"):
            symbol = 'C'
        if(nameObject == "W"):
            symbol == "W"

        if(self._lastMove == 'd' or self._lastMove == 'D'):
            if((player_pos[0] + 5 >= object_pos[0]) and (player_pos[0] + 3 <= object_pos[0])):
                if((player_pos[1] - 5 <= object_pos[1] - object_size[1]/2) and (player_pos[1] + 5 > object_pos[1] + object_size[1]/2)):
                    object.decreaseHealth(player._damage, symbol)
    
        if(self._lastMove == 'a' or self._lastMove == 'A'):
            if((player_pos[0] - 5 - 3 <= object_pos[0]) and (player_pos[0] - 3 >= object_pos[0])):
                if((player_pos[1] - 5 <= object_pos[1] - object_size[1]/2) and (player_pos[1] + 5 > object_pos[1] + object_size[1]/2)):
                    object.decreaseHealth(player._damage, symbol)

        if(self._lastMove == 'w' or self._lastMove == 'W'):
            if((player_pos[1] - 5 -3 <= object_pos[1]) and (player_pos[1] - 3 >= object_pos[1])):
                if((player_pos[0] - 5 <= object_pos[0]) and (player_pos[0] + 5 >= object_pos[0])):
                    object.decreaseHealth(player._damage, symbol)
    
        if(self._lastMove == 's' or self._lastMove == 'S'):
            if((player_pos[1] + 5 + 3 >= object_pos[1]) and (player_pos[1] + 3 <= object_pos[1])):
                if((player_pos[0] - 5 <= object_pos[0]) and (player_pos[0] + 5 >= object_pos[0])):
                    object.decreaseHealth(player._damage, symbol)

    

    ################ COLLISIONS ################################
    def detectDirection(self ,player, object, nameObject, namePlayer):

        player_pos,player_size,player_speed = player.get_dimension()
        object_pos,object_size,object_speed = object.get_dimension()

        if((player_pos[0] - 1 > object_pos[0] - object_size[0]/2) and (player_pos[0] < object_pos[0] + object_size[0]/2 + 2)):

            # top collision            
            if((player_pos[1] - 2 <= object_pos[1] + object_size[1]/2) and (player_pos[1] > object_pos[1])):
                self.free_movement[0] = 1
                if (nameObject == "TOWN HALL" and namePlayer == "KING"):
                    self.damage_king()
                

            # bottom collision            
            if((player_pos[1] >= object_pos[1] - object_size[1]/2) and (player_pos[1] < object_pos[1])):
                self.free_movement[2] = 1
                if (nameObject == "TOWN HALL" and namePlayer == "KING"):
                    self.damage_king()
                
        
        if((player_pos[1] - 1 > object_pos[1] - object_size[1]/2) and (player_pos[1] - 1 < object_pos[1] + object_size[1]/2)):

            # right collision
            if((player_pos[0] - 1 >= object_pos[0] - object_size[0]/2) and (player_pos[0] - 2 < object_pos[0] - object_size[0]/2)):
                self.free_movement[1] = 1
                if (nameObject == "TOWN HALL" and namePlayer == "KING"):
                    self.damage_king()
            

            # left collision
            if((player_pos[0] - 2 <= object_pos[0] + object_size[0]/2) and (player_pos[0] > object_pos[0] + object_size[0]/2)):
                self.free_movement[3] = 1
                if (nameObject == "TOWN HALL" and namePlayer == "KING"):
                    self.damage_king()

        return self.free_movement    


    def detectDirectionTroop(self ,player, object, nameObject, namePlayer):

        player_pos,player_size,player_speed = player.get_dimension()
        object_pos,object_size,object_speed = object.get_dimension()
        if((player_pos[0] - 1 > object_pos[0] - object_size[0]/2) and (player_pos[0] < object_pos[0] + object_size[0]/2 + 2)):

            # top collision            
            if((player_pos[1] - 2 <= object_pos[1] + object_size[1]/2) and (player_pos[1] > object_pos[1])):
                object.decreaseHealth(player._damage, object._symbol)
                if (nameObject == "TOWN HALL"):
                    self.damage_troop(player)
                if (object._health <= 0):
                    player._isMoving = True
                else:
                    player.isMoving = False

            # bottom collision            
            if((player_pos[1] >= object_pos[1] - object_size[1]/2) and (player_pos[1] < object_pos[1])):
                object.decreaseHealth(player._damage, object._symbol)
                if (nameObject == "TOWN HALL"):
                    self.damage_troop(player)
                if (object._health <= 0):
                    player._isMoving = True
                else:
                    player.isMoving = False
                
        if((player_pos[1] - 1 > object_pos[1] - object_size[1]/2) and (player_pos[1] - 1 < object_pos[1] + object_size[1]/2)):

            # right collision
            if((player_pos[0] - 1 >= object_pos[0] - object_size[0]/2) and (player_pos[0] - 2 < object_pos[0] - object_size[0]/2)):
                object.decreaseHealth(player._damage, object._symbol)
                if (nameObject == "TOWN HALL"):
                    self.damage_troop(player)
                if (object._health <= 0):
                    player._isMoving = True
                else:
                    player.isMoving = False

            # left collision
            if((player_pos[0] - 2 <= object_pos[0] + object_size[0]/2) and (player_pos[0] > object_pos[0] + object_size[0]/2)):
                object.decreaseHealth(player._damage, object._symbol)
                if (nameObject == "TOWN HALL"):
                    self.damage_troop(player)
                if (object._health <= 0):
                    player._isMoving = True
                else:
                    player.isMoving = False



    
    def detectDirectionWithWall(self ,player, object, nameObject, namePlayer):

        player_pos,player_size,player_speed = player.get_dimension()
        object_pos,object_size,object_speed = object.get_dimension()
        
        if(player_speed[0] == 2):
            if (object_size[0] == 0):
                return self.free_movement
            # top collision            
            if((player_pos[1] - 2 == object_pos[1] or player_pos[1] - 1 == object_pos[1]) and (player_pos[0] == object_pos[0])):
                self.free_movement[0] = 1

            # bottom collision            
            if((player_pos[1] + 2 == object_pos[1] or player_pos[1] + 1 == object_pos[1]) and (player_pos[0] == object_pos[0])):
                self.free_movement[2] = 1
        
            # right collision
            if((player_pos[0] + 2 == object_pos[0] or player_pos[0] + 1 == object_pos[0]) and (player_pos[1] == object_pos[1])):
                self.free_movement[1] = 1

            # left collision
            if((player_pos[0] - 2 == object_pos[0] or player_pos[0] - 1 == object_pos[0]) and (player_pos[1] == object_pos[1])):
                self.free_movement[3] = 1
            
            return self.free_movement


        if (object_size[0] == 0):
            return self.free_movement
        # top collision            
        if((player_pos[1] - 1 == object_pos[1]) and (player_pos[0] == object_pos[0])):
            self.free_movement[0] = 1

        # bottom collision            
        if((player_pos[1] + 1 == object_pos[1]) and (player_pos[0] == object_pos[0])):
            self.free_movement[2] = 1
    
        # right collision
        if((player_pos[0] + 1 == object_pos[0]) and (player_pos[1] == object_pos[1])):
            self.free_movement[1] = 1

        # left collision
        if((player_pos[0] - 1 == object_pos[0]) and (player_pos[1] == object_pos[1])):
            self.free_movement[3] = 1

        return self.free_movement

    def detectDirectionWithWallTroop(self ,player, object, nameObject, namePlayer):

        player_pos,player_size,player_speed = player.get_dimension()
        object_pos,object_size,object_speed = object.get_dimension()

        if (object_size[0] == 0):
            return

        if(player_speed[0] == 2):
            # top collision            
            if((player_pos[1] - 2 == object_pos[1] or player_pos[1] - 1 == object_pos[1]) and (player_pos[0] == object_pos[0])):
                object.decreaseHealth(player._damage, object._symbol)
                if (object._health <= 0):
                    player._isMoving = True
                else:
                    player.isMoving = False

            # bottom collision            
            if((player_pos[1] + 2 == object_pos[1] or player_pos[1] + 1 == object_pos[1]) and (player_pos[0] == object_pos[0])):
                object.decreaseHealth(player._damage, object._symbol)
                if (object._health <= 0):
                    player._isMoving = True
                else:
                    player.isMoving = False
        
            # right collision
            if((player_pos[0] + 2 == object_pos[0] or player_pos[0] + 1 == object_pos[0]) and (player_pos[1] == object_pos[1])):
                object.decreaseHealth(player._damage, object._symbol)
                if (object._health <= 0):
                    player._isMoving = True
                else:
                    player.isMoving = False

            # left collision
            if((player_pos[0] - 2 == object_pos[0] or player_pos[0] - 1 == object_pos[0]) and (player_pos[1] == object_pos[1])):
                object.decreaseHealth(player._damage, object._symbol)
                if (object._health <= 0):
                    player._isMoving = True
                else:
                    player.isMoving = False
            
            return


        # top collision            
        if((player_pos[1] - 1 == object_pos[1]) and (player_pos[0] == object_pos[0])):
            object.decreaseHealth(player._damage, object._symbol)
            if (object._health <= 0):
                player._isMoving = True
            else:
                player.isMoving = False

        # bottom collision            
        if((player_pos[1] + 1 == object_pos[1]) and (player_pos[0] == object_pos[0])):
            object.decreaseHealth(player._damage, object._symbol)
            if (object._health <= 0):
                player._isMoving = True
            else:
                player.isMoving = False
    
        # right collision
        if((player_pos[0] + 1 == object_pos[0]) and (player_pos[1] == object_pos[1])):
            object.decreaseHealth(player._damage, object._symbol)
            if (object._health <= 0):
                player._isMoving = True
            else:
                player.isMoving = False

        # left collision
        if((player_pos[0] - 1 == object_pos[0]) and (player_pos[1] == object_pos[1])):
            object.decreaseHealth(player._damage, object._symbol)
            if (object._health <= 0):
                player._isMoving = True
            else:
                player.isMoving = False


    def detectDirectionWithWallTroopForBalloon(self ,player, object, nameObject, namePlayer):

        player_pos,player_size,player_speed = player.get_dimension()
        object_pos,object_size,object_speed = object.get_dimension()

        if (object_size[0] == 0):
            return

        # top collision            
        if((player_pos[1] - 1 == object_pos[1]) and (player_pos[0] == object_pos[0])):
            object.decreaseHealth(player._damage, object._symbol)
            if (object._health <= 0):
                player._isMoving = True
            else:
                player.isMoving = False

        # bottom collision            
        if((player_pos[1] + 1 == object_pos[1]) and (player_pos[0] == object_pos[0])):
            object.decreaseHealth(player._damage, object._symbol)
            if (object._health <= 0):
                player._isMoving = True
            else:
                player.isMoving = False
    
        # right collision
        if((player_pos[0] + 1 == object_pos[0]) and (player_pos[1] == object_pos[1])):
            object.decreaseHealth(player._damage, object._symbol)
            if (object._health <= 0):
                player._isMoving = True
            else:
                player.isMoving = False

        # left collision
        if((player_pos[0] - 1 == object_pos[0]) and (player_pos[1] == object_pos[1])):
            object.decreaseHealth(player._damage, object._symbol)
            if (object._health <= 0):
                player._isMoving = True
            else:
                player.isMoving = False




    
    def handle_collision_players(self, player, playerName, huts, townhall, walls, cannons, wizardTowers):
        # collision with huts
        for hut in huts:
            arr1 = self.detectDirection(player, hut, "HUT", playerName)
            for i in range(4):
                if (arr1[i] == 1):
                    self.free_movement[i] = 1

        for wizardTower in wizardTowers:
            arr5 = self.detectDirection(player, wizardTower, "WIZARDTOWER", playerName)
            for i in range(4):
                if (arr5[i] == 1):
                    self.free_movement[i] = 1
        
        #collision with townhall
        arr2 = self.detectDirection(player, townhall, "TOWN HALL", playerName)

        for wall in walls:
            arr3 = self.detectDirectionWithWall(player, wall, "WALL", playerName)
            for i in range(4):
                if (arr3[i] == 1):
                    self.free_movement[i] = 1

        for cannon in cannons:
            arr4 = self.detectDirectionWithWall(player, cannon, "CANNON", playerName)
            for i in range(4):
                if (arr4[i] == 1):
                    self.free_movement[i] = 1

        # make seperate function to detect collision with walls and cannon
        for i in range(4):
            if(arr2[i]):
                self.free_movement[i] = 1


    def handle_collision_Troops(self,player, playerName, huts, townhall, walls, cannons, wizardTowers):
        if (player._size[0] != 0):
            # collision with huts
        
            if(player._symbol == 'O'):
                numDeadCount = 0
                for cannon in cannons:
                    if(cannon._size[0] == 0):
                        numDeadCount += 1

                    self.detectDirectionWithWallTroopForBalloon(player, cannon, "CANNON", playerName)

                for wizardTower in wizardTowers:
                    if(wizardTower._size[0] == 0):
                        numDeadCount += 1
                    if (wizardTower._size[0] != 0):
                        self.detectDirectionTroop(player, wizardTower, "WIZARDTOWER", playerName)

                self._numDeadCannonWizard = numDeadCount   

                if(self._numDeadCannonWizard == len(self._cannons) + len(self._wizardTowers)):
                    self._balloonChasingCannon = False
                    for hut in huts:
                        if (hut._size[0] != 0):
                            self.detectDirectionTroop(player, hut, "HUT", playerName)

                    self.detectDirectionTroop(player, townhall, "TOWN HALL", playerName)        
                return            

            for wizardTower in wizardTowers:
                if (wizardTower._size[0] != 0):
                    self.detectDirectionTroop(player, wizardTower, "WIZARDTOWER", playerName)

            for hut in huts:
                if (hut._size[0] != 0):
                    self.detectDirectionTroop(player, hut, "HUT", playerName)
                    
            #collision with townhall
            self.detectDirectionTroop(player, townhall, "TOWN HALL", playerName)
            
            for wall in walls:
                self.detectDirectionWithWallTroop(player, wall, "WALL", playerName)

            for cannon in cannons:
                self.detectDirectionWithWallTroop(player, cannon, "CANNON", playerName)
       
    def handle_collisions(self):
        self.handle_collision_players(self._king,"KING", self._huts, self._townhall, self._walls, self._cannons, self._wizardTowers)
        
    def checkBarbarianCollision(self):
        for b in self._barbarians:
            self.handle_collision_Troops(b,"BARBARIAN", self._huts, self._townhall, self._walls, self._cannons, self._wizardTowers)

    def checkBalloonCollision(self):
        for b in self._balloons:
            self.handle_collision_Troops(b,"BALLOON", self._huts, self._townhall, self._walls, self._cannons, self._wizardTowers)

    def checkArcherCollision(self):
        for a in self._archers:
            self.handle_collision_Troops(a,"ARCHER", self._huts, self._townhall, self._walls, self._cannons, self._wizardTowers)

    def checkPositionForCannon(self, player):
        for i in range(len(self._cannons)):
            pos,size,spped = self._cannons[i].get_dimension()
            if(self._cannons[i]._health <= 0):
                return
            x = pos[0]
            y = pos[1]
            player_pos,player_size,player_speed = player.get_dimension()
            x_p = player_pos[0]
            y_p = player_pos[1]

            if (x_p < x + 6 and x_p > x - 6):
                if (y_p < y + 6 and y_p > y - 6):
                    player.decreaseHealth(self._cannons[0]._damage, player._symbol)
                    if (player._symbol == 'K' or player._symbol == 'Q'):
                        self._healthBar.decreaseLength(self._king._maxhealth, self._king._health )


    def checkPositionTowerShoot(self, player):
        for i in range(2):
            pos,size,spped = self._wizardTowers[i].get_dimension()
            if(self._wizardTowers[i]._health <= 0):
                return
            x = pos[0]
            y = pos[1]
            player_pos,player_size,player_speed = player.get_dimension()
            x_p = player_pos[0]
            y_p = player_pos[1]

            if (x_p < x + 6 and x_p > x - 6):
                if (y_p < y + 6 and y_p > y - 6):
                    player.decreaseHealth(self._cannons[0]._damage, player._symbol)
                    if (player._symbol == 'K' or player._symbol == 'Q'):
                        self._healthBar.decreaseLength(self._king._maxhealth, self._king._health )


    def checkPositionForArcher(self, building):
        for i in range(self._currentArchers):
            if(self._archers[i]._health <= 0):
                continue
            pos,size,spped = self._archers[i].get_dimension()
            x = pos[0]
            y = pos[1]
            building_pos,building_size,building_speed = building.get_dimension()
            x_p = building_pos[0]
            y_p = building_pos[1]
            if (x_p < x + 7 and x_p > x - 7):
                if (y_p < y + 7 and y_p > y - 7):
                    building.decreaseHealth(self._archers[0]._damage, building._symbol)


    def cannonFire(self):
        self.checkPositionForCannon(self._king)
        for b in self._barbarians:
            self.checkPositionForCannon(b)
        for a in self._archers:
            self.checkPositionForCannon(a)

    def TroopShootingByTower(self, wizardTower, troops): # wall, townhall, building
        pos,size,spped = wizardTower.get_dimension()
        if(wizardTower._health <= 0):
            return False
        x = pos[0]
        y = pos[1]

        for troop in  troops:
            if(troop._health <= 0):
                continue
            troop_pos,troop_size,troop_speed = troop.get_dimension()
            x_p = troop_pos[0]
            y_p = troop_pos[1]

            if (x_p < x + 6 and x_p > x - 6):
                if (y_p < y + 6 and y_p > y - 6):
                    troop.decreaseHealth(self._wizardTowers[0]._damage, troop._symbol)
                    self.callTowerHitRange(troop, self._barbarians, self._archers, self._balloons)
                    return True
        return False
                
    def KingShootingByTower(self, wizardTower, King): # wall, townhall, building
        pos,size,spped = wizardTower.get_dimension()
        if(wizardTower._health <= 0):
            return False
        x = pos[0]
        y = pos[1]

        if(King._health <= 0):
            return False
        troop_pos,troop_size,troop_speed = King.get_dimension()
        x_p = troop_pos[0]
        y_p = troop_pos[1]

        if (x_p < x + 6 and x_p > x - 6):
            if (y_p < y + 6 and y_p > y - 6):
                King.decreaseHealth(self._wizardTowers[0]._damage, King._symbol)
                self._healthBar.decreaseLength(King._maxhealth, King._health )
                return True
        
        return False
        

     
    def shootTroopInTowerHitRange(self, player, hittedPlayer):
        pos,size,spped = hittedPlayer.get_dimension()
        if(hittedPlayer._health <= 0):
            return
        x = pos[0]
        y = pos[1]
        player_pos,player_size,player_speed = player.get_dimension()
        x_p = player_pos[0]
        y_p = player_pos[1]

        if (x_p <= x + 3 and x_p >= x - 3):
            if (y_p < y + 3 and y_p > y - 3):
                player.decreaseHealth(hittedPlayer._damage, player._symbol)

    def callTowerHitRange(self, hittedPlayer , barbarians, archers, balloons):
        for b in barbarians:
            self.shootTroopInTowerHitRange(b, hittedPlayer)
        for a in archers:
            self.shootTroopInTowerHitRange(a, hittedPlayer)
        for b in balloons:
            self.shootTroopInTowerHitRange(b, hittedPlayer)

    def wizardTowerFire(self):
        isTowerShooting = False # so that no two troop can be damaged by entering area of damage

        for i in range(2):
            isTowerShooting = self.TroopShootingByTower(self._wizardTowers[i], self._balloons)
            if(isTowerShooting == False):
                isTowerShooting = self.TroopShootingByTower(self._wizardTowers[i], self._barbarians)
            if(isTowerShooting == False):
                isTowerShooting = self.KingShootingByTower(self._wizardTowers[i], self._king)
            if(isTowerShooting == False):
                isTowerShooting = self.TroopShootingByTower(self._wizardTowers[i], self._archers)



    def archerFire(self):
        self.checkPositionForArcher(self._townhall)
        for h in self._huts:
            self.checkPositionForArcher(h)
        for wizardTower in self._wizardTowers:
            self.checkPositionForArcher(wizardTower)

    # Rage spell
    def rageSpell(self):
        if self._king._size[0] != 0:
            self._king._damage *= 2
            self._king._speed *= 2
        
        for barbarian in self._barbarians:
            if barbarian._size[0] != 0:
                barbarian._damage *= 2
                barbarian._speed *= 2

    def healSpell(self):
        if self._king._size[0] != 0:
            self._king._health *= 1.5
            if (self._king._health > self._king._maxhealth):
                self._king._health = self._king._maxhealth
            
        for barbarian in self._barbarians:
            if barbarian._size[0] != 0:
                barbarian._health *= 1.5
                if (barbarian._health > barbarian._maxhealth):
                    barbarian._health = barbarian._maxhealth


    def checkWin(self):
        if self._townhall._size[0] != 0:
            self._win = False

        for hut in self._huts:
            if hut._size[0] != 0:
                self._win = False

    
    def checkLoose(self):
        if self._king._size[0] != 0:
            self._Loose = False

        for b in self._barbarians:
            if b._size[0] != 0:
                self._Loose = False

    def level_up(self):

        self._currentBarbarians = 0
        self._currentArchers = 0
        self._currentBalloons = 0

        self._level = self._level+1
        if(self._level <= 2):
            self.make_layout()
        else:
            if(self._win):
                self._screen.game_won()
            else:
                self._screen.game_lost()
            sys.exit(0)

    def run(self):
        # For replay
        n = len(sys.argv)
        if (n == 2):
            self._isReplay = True
            self._replayName = sys.argv[1]
            fd = open(self._replayName, 'r')
            self._dictionary = json.load(fd)
            fd.close()

        while 1:
            self._screen.clean()
            if self._isReplay == True:
                if str(self._iteration) in self._dictionary.keys():
                    ch = self._dictionary[str(self._iteration)]
                    self.handle_keyboard_interrupt(self._isReplay, ch)
                else:
                    self.handle_keyboard_interrupt(self._isReplay)

            else:
                self.handle_keyboard_interrupt(self._isReplay)


            self._screen.reset_screen()

            for b in self._barbarians:
                distances = self.closestObjectForTroop(b, self._huts, self._townhall)
                for i in distances:
                    obj_pos, obj_size, obj_speed = i[1].get_dimension()
                    if(obj_size[0] != 0):
                        b._move(i)  
                        break
                        

            for a in self._archers:
                distances = self.closestObjectForTroop(a, self._huts, self._townhall)
                for i in distances:
                    obj_pos, obj_size, obj_speed = i[1].get_dimension()
                    if(obj_size[0] != 0):
                        a._move(i)  
                        break 
            
            for b in self._balloons:
                balloonDistances = self.closestObjectForBalloon(b, self._cannons, self._wizardTowers)
                for i in balloonDistances:
                    obj_pos, obj_size, obj_speed = i[1].get_dimension()
                    if(obj_size[0] != 0):
                        b._move(i)  
                        break 
            
            if(self._balloonChasingCannon == False):
                for b in self._balloons:
                    balloonDistances = self.closestNonAttackingBuildingForBalloon(b, self._huts, self._townhall)
                    for i in balloonDistances:
                        obj_pos, obj_size, obj_speed = i[1].get_dimension()
                        if(obj_size[0] != 0):
                            b._move(i)  
                            break 

            self.wizardTowerFire()
            self.checkBarbarianCollision()
            self.checkArcherCollision()
            self.checkBalloonCollision()
            self.cannonFire()
            self.archerFire()
            self.place_items()
            self._screen.render_screen()
            self._iteration += 1
            self._win = True
            self._Loose = True
            self.checkWin()
            self.checkLoose()
            if self._win == True:
                if(self._level <= 2):
                    self.level_up()
                else:
                    self._screen.game_won()
            if self._Loose == True:
                self._screen.game_lost()

kingKey = input("Press 'o' for King and 'p' for Archer Queen. Then press Enter\n")

game = Game()

if(kingKey == 'o' or kingKey == 'O'):
    isKing = True
else:
    isKing = False
game.run()
    

    
