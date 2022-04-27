import time
import numpy as np
from src.color import bg, fg, reset
import sys

class Screen:
    def __init__(self, height, width):
        self._width = width
        self._height = height
        ww = range(width)
        hh = range(height)
        self._board = np.array([['' for j in ww] for i in hh], dtype='object')
        print("\033[2J") 
    

    def clean(self):
        ww, hh = range(self._width), range(self._height)
        self._board = np.array([['' for j in ww] for i in hh], dtype='object')
        print("\033[0;0H")
        for i in hh:
            for j in ww:
                print(self._board[i][j], end='')
            print("")


    def render_screen(self):
        print("\033[0;0H")
        ww, hh = range(self._width), range(self._height)
        for i in hh:
            for j in ww:
                print(self._board[i][j], end='')
            print("")


    def reset_screen(self):
        ww, hh = range(self._width), range(self._height)
        self._board = np.array([[' ' for j in ww] for i in hh], dtype='object')

        for i in hh:
            for j in ww:
                if(i==0):
                    self._board[i][j] = bg.yellow+' '+reset
                elif(i == self._height - 1):
                    self._board[i][j] = bg.yellow+' '+reset
                
                elif(j==0 ):
                    self._board[i][j]=bg.yellow+' '+reset
                elif(j==self._width-1):
                    self._board[i][j]=bg.yellow+' '+reset


    def place_object(self, obj):
        pos, size, _ = obj.get_dimension()
        structure = obj.get_structure()
        for i in range(int(pos[1]), int(pos[1]) + int(size[1])):
            for j in range(int(pos[0]),int(pos[0]) + int(size[0])):
                self._board[i][j] = structure[i-int(pos[1])][j-int(pos[0])]


    def blink_screen(self):
        self.reset_screen()
        self.render_screen()
        time.sleep(0.1)


    def game_won(self):
        print("\033[2J") 
        print("\033[0;0H")
        message = '''


                    YOU WIN!! :)


                '''



        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")

        print(fg.green + message + reset)
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")

        sys.exit(0)

    def game_lost(self):
        print("\033[2J") # clear the screen!!
        print("\033[0;0H")
        message = '''


                    YOU LOST!! :(


                '''

        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print(fg.red + message + reset)
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")

        sys.exit(0)