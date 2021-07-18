import pygame
import sys
import time
import time
import random


from pygame import Surface, draw, display, event, key,mouse,cursors
from pygame.cursors import Cursor
from chess import *

from chess import *
from game import Game

def loader():
    loop = 0
    while True:
        lstr = " "

        for i in range(0, int(loop/2)):
            lstr += "▇"
        sys.stdout.write(lstr+" {0}%\r".format(loop))
        sys.stdout.flush()
        loop += 1
        wait = random.randint(100, 900)/1000
        time.sleep(wait)



class Chess(Game):
    currentItem = Empty()
    currentAction = False
    actions = []
    whiteAction = True
    showGridEffect = False
    showDeltatime = False
    showFps = False
    tile_count = 8
    grid=[]

    def __init__(self, args):
        size = int(500/8)*8
        Game.__init__(self, [size,size])
        self.tile_size = int(self.renderer.get_width()/self.tile_count)

        self.init_grid()
        self.process_args(args)
        display.set_caption("Chess game")

    def process_args(self, args):
        
        if len(args) > 1 and int(args[1])==1:
            self.showGridEffect = True

        if len(args) > 2 and int(args[2])==1:
            self.showDeltatime = True

        if len(args) > 3 and int(args[3])==1:
            self.showFps = True

    def draw_rect(self, x, y, tile_size):
        draw.line(self.renderer, (255, 255, 255), (x, y), (x+tile_size, y))
        draw.line(self.renderer, (255, 255, 255), (x, y), (x, y+tile_size))
        draw.line(self.renderer, (255, 255, 255),
                  (x+tile_size, y+tile_size), (x, y+tile_size))
        draw.line(self.renderer, (255, 255, 255),
                  (x+tile_size, y), (x+tile_size, y+tile_size))

    def init_grid(self):
        for i in range(0,self.tile_count):
            self.grid.append([])
            for k in range(0,self.tile_count):  
                  self.grid[i].append(Empty())

        self.grid[0][0] = Rook(True,[0,0])
        self.grid[1][0] = King(True,[1,0])
        self.grid[2][0] = Bishop(True,[2,0])
        self.grid[3][0] = King(True,[3,0])
        self.grid[4][0] = King(True,[4,0])
        self.grid[5][0] = Bishop(True,[5,0])
        self.grid[6][0] = King(True,[6,0])
        self.grid[7][0] = Rook(True,[7,0])

        for i in range(0,self.tile_count):
            self.grid[i][1] = King(True,[i,1])
        
    def draw_grid(self):
        self.renderer.fill((184, 139, 74))
        
        switch = False
        i = 0
        for x in range(0, self.tile_size*8, self.tile_size):
            for y in range(0, self.tile_size*8, self.tile_size):
                if i >= self.tile_count:
                    i = 0
                else:
                    switch = not switch
                i += 1

                if switch:
                    draw.rect(self.renderer, (227, 193, 111),pygame.Rect(x, y, self.tile_size, self.tile_size))

                if self.showGridEffect:
                    self.draw_rect(x,y,self.tile_size)
    
    def draw_chess(self):
        for i in range(0,self.tile_count):
            for k in range(0,self.tile_count):
                if not self.grid[i][k].type == ChessItemType.EMPTY:
                    c = int((10*int(self.grid[i][k].type[0]))/255)*255
                    draw.rect(self.renderer,(c,c,c),pygame.Rect(i*self.tile_size,k*self.tile_size,self.tile_size,self.tile_size))
        

    def mouse_coord(self):
        return [int(mouse.get_pos()[0]/self.tile_size)*self.tile_size,int(mouse.get_pos()[1]/self.tile_size)*self.tile_size]

    def draw(self):
        self.draw_grid()
        
        coord = self.mouse_coord()
        draw.rect(self.renderer,(190, 140,90),pygame.Rect(coord[0],coord[1],self.tile_size,self.tile_size))
        self.draw_rect(coord[0],coord[1],self.tile_size)
        
        self.draw_chess()
        if self.currentAction:
            self.draw_actions()

    def draw_actions(self):
        for act in self.actions:
            position = ((act.position[0]+1) * (self.tile_size) -self.tile_size/2, (act.position[1]+1)*(self.tile_size)-self.tile_size/2)
            draw.circle(self.renderer,(100,100,100),position,self.tile_size/8)
        


    def mouse_set_grid(self,item:ChessItem):
        coord=self.mouse_coord()
        self.grid[int(coord[0]/self.tile_size)][int(coord[1]/self.tile_size)] = item
    
    def mouse_get_grid(self):
        coord=self.mouse_coord()
        return self.grid[int(coord[0]/self.tile_size)][int(coord[1]/self.tile_size)]

    def update(self, deltatime):
        for evt in event.get():
            if evt.type == pygame.QUIT:
                    self.running = False
            if evt.type == pygame.MOUSEBUTTONDOWN:
                if not self.currentAction:
                    self.currentItem = self.mouse_get_grid()
                    if self.currentItem.type != ChessItemType.EMPTY:
                        self.currentAction =True
                        self.actions = self.currentItem.get_actions(self.grid)
                else:
                    i=0
                    index=-1
                    for act in self.actions:
                        pos = [act.position[0]*self.tile_size,act.position[1]*self.tile_size]
                        if pos == self.mouse_coord():
                            index=i
                            break
                        i+=1

                    if index != -1 and self.currentItem.type != ChessItemType.EMPTY:
                        g=self.currentItem.do_action(self.actions[index],self.grid)
                        if g != None:
                            self.grid = g
                        self.currentAction = False
                        self.actions = []
                        self.currentItem = Empty()
                    else:
                        # click out
                        self.currentAction = False
                        self.actions = []
                        self.currentItem = Empty()

        if self.showDeltatime:
            display.set_caption("Chess game - {0}".format(deltatime))


def main(argv):
    game = Chess(argv)
    game.start()


if __name__ == "__main__":
    main(sys.argv)
