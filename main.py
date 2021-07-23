import os
import pygame
import sys
import time
import time
import random

from os import listdir
from os.path import isfile, join
from pygame import Surface, draw, display, event, key,mouse,cursors,image,transform
from pygame.cursors import Cursor
from chess import *
from copy import copy, deepcopy

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

    showAsInt = False
    showGridEffect = False
    showDeltatime = False
    showFps = False
    startWhiteTop = True


    enableTimer = -1
    currentTimerTime = 0

    tile_count = 8
    grid=[]
    images = []
    winsize = 700

    def __init__(self, args):
        self.process_args(args)
        size = int(self.winsize/8)*8
        Game.__init__(self, [size,size])
        self.tile_size = int(self.renderer.get_width()/self.tile_count)

        self.fill_grid()
        self.init_grid()
        self.chess_grid()
        self.load_images("white")
        self.load_images("black")
        
        display.set_caption("Chess game")

    def isChess(self, white=True, grid=[]):
        actions = []
        king_position = [0,0]
        for i in range(0,self.tile_count):
            for k in range(0,self.tile_count):
                if grid[i][k].type != ChessItemType.EMPTY and grid[i][k].white != white:
                   actions = actions + grid[i][k].get_actions(grid)
                elif  grid[i][k].type == ChessItemType.King and grid[i][k].white == white:
                    king_position = [i,k]
        
        for act in actions:
            if act.position == king_position:
                return True
        return False

    def process_args(self, args):
        
        if len(args) > 1 and int(args[1])==1:
            self.showGridEffect = True

        if len(args) > 2 and int(args[2])==1:
            self.showDeltatime = True

        if len(args) > 3 and int(args[3])==1:
            self.showFps = True
                      
        if len(args) >4 and int(args[4]) >= 200 and int(args[4]) <= 1080:
            self.winsize = int(args[4])

        if len(args) > 5 and int(args[5]) == 1:
            self.showAsInt=True

        if len(args) > 6 and int(args[6]) >= 30 and int(args[6]) <= 1000:
            self.fps_max(int(args[6]))

        if len(args) > 7 and int(args[7]) == 1:
            self.startWhiteTop = False

        if len(args) > 8 and int(args[8]) >= 30 and int(args[8]) <= 60*10:
            self.enableTimer = int(args[8])
    
    def load_images(self,dir):
        path = os.path.dirname(os.path.abspath(__file__))+"/assets/"+dir+"/"
        files = [f for f in listdir(path) if isfile(join(path, f))]
        files.sort()
        print("Load assets in {0}".format(path))
        for file in files:
            if file.endswith(".png"):
                print("[+] {0}".format(file))
                self.images.append(image.load(path+file))
        
    def draw_image(self,index,x,y):
        # self.renderer.blit(transform.scale(self.images[index],(self.tile_size,self.tile_size)),pygame.Rect(x*self.tile_size,y*self.tile_size,self.tile_size,self.tile_size))
        center_value = (self.tile_size-self.images[index].get_width())/2
        center = pygame.Rect(
            x*self.tile_size+center_value, y*self.tile_size+center_value, self.tile_size, self.tile_size)
        self.renderer.blit(self.images[index], center)
    def draw_rect(self, x, y, tile_size):
        draw.line(self.renderer, (255, 255, 255), (x, y), (x+tile_size, y))
        draw.line(self.renderer, (255, 255, 255), (x, y), (x, y+tile_size))
        draw.line(self.renderer, (255, 255, 255),
                  (x+tile_size, y+tile_size), (x, y+tile_size))
        draw.line(self.renderer, (255, 255, 255),
                  (x+tile_size, y), (x+tile_size, y+tile_size))

    def fill_grid(self):
        for i in range(0,self.tile_count):
            self.grid.append([])
            for k in range(0,self.tile_count):  
                  self.grid[i].append(Empty())

    def draw_grid(self):
        self.renderer.fill((184, 139, 74))
        i = 0
        switch = False
        for x in range(0, self.tile_count):
            for y in range(0, self.tile_count):
                if i >= self.tile_count:
                    i = 0
                else:
                    switch = not switch
                i += 1
                if switch:
                    draw.rect(self.renderer, (227, 193, 111), pygame.Rect(
                        x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size))

                    
    
    def init_grid(self):
        i=0
        switch = False
        for x in range(0, self.tile_count):
            for y in range(0, self.tile_count):
                if i >= self.tile_count:
                    i = 0
                else:
                    switch = not switch
                i += 1

                self.grid[x][y] = Empty(switch)

    def update_grid(self):
        i=0
        switch = False
        for x in range(0, self.tile_count):
            for y in range(0, self.tile_count):
                if i >= self.tile_count:
                    i = 0
                else:
                    switch = not switch
                i += 1
                if self.grid[x][y].type == ChessItemType.EMPTY:
                    self.grid[x][y] = Empty(switch)

    def draw_chess(self):
        for x in range(0,self.tile_count):
            for y in range(0,self.tile_count):
                if self.grid[x][y].type != ChessItemType.EMPTY:
                    # color=(255,255,255)
                    # if not self.grid[x][y].white:
                    #     color = (0,0,0)
                    # draw.rect(self.renderer,color,pygame.Rect(x*self.tile_size,y*self.tile_size,self.tile_size,self.tile_size))
                    
                    item_type = self.grid[x][y].type
                    image_id = 0
                    if item_type == ChessItemType.King:
                       image_id = 1
                    elif item_type == ChessItemType.Rook:
                        image_id = 5
                    elif item_type == ChessItemType.Knight:
                        image_id = 2
                    elif item_type == ChessItemType.Bishop:
                        image_id = 0
                    elif item_type == ChessItemType.Pawn:
                        image_id = 3
                    elif item_type == ChessItemType.Queen:
                        image_id = 4
                    if not self.grid[x][y].white:
                        image_id += 6
                    self.draw_image(image_id,x,y)
                        
                if self.showGridEffect:
                        self.draw_rect(x*self.tile_size, y*self.tile_size,self.tile_size)

    def chess_grid(self):
        self.grid[0][0] = Rook(self.startWhiteTop,[0,0])
        self.grid[1][0] = Knight(self.startWhiteTop,[1,0])
        self.grid[2][0] = Bishop(self.startWhiteTop,[2,0])
        self.grid[3][0] = King(self.startWhiteTop,[3,0])
        self.grid[4][0] = Queen(self.startWhiteTop,[4,0])
        self.grid[5][0] = Bishop(self.startWhiteTop,[5,0])
        self.grid[6][0] = Knight(self.startWhiteTop,[6,0])
        self.grid[7][0] = Rook(self.startWhiteTop,[7,0])

        self.grid[0][7] = Rook(not self.startWhiteTop, [0, 7])
        self.grid[1][7] = Knight(not self.startWhiteTop,[1,7])
        self.grid[2][7] = Bishop(not self.startWhiteTop,[2,7])
        self.grid[3][7] = King(not self.startWhiteTop, [3, 7])
        self.grid[4][7] = Queen(not self.startWhiteTop, [4, 7])
        self.grid[5][7] = Bishop(not self.startWhiteTop,[5,7])
        self.grid[6][7] = Knight(not self.startWhiteTop,[6,7])
        self.grid[7][7] = Rook(not self.startWhiteTop, [7, 7])

        for i in range(0,self.tile_count):
            self.grid[i][1] = Pwan(self.startWhiteTop,[i,1])
            self.grid[i][6] = Pwan(not self.startWhiteTop, [i, 6])

    def mouse_coord(self):
        return [int(mouse.get_pos()[0]/self.tile_size)*self.tile_size,int(mouse.get_pos()[1]/self.tile_size)*self.tile_size]

    

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

    def draw(self):
        self.draw_grid()
        coord = self.mouse_coord()
        draw.rect(self.renderer, (190, 140, 90), pygame.Rect(
            coord[0], coord[1], self.tile_size, self.tile_size))
        self.draw_rect(coord[0], coord[1], self.tile_size)

        
        self.draw_chess()
        if self.currentAction:
            self.draw_actions()

        

    def update(self, deltatime):
        for evt in event.get():
            if evt.type == pygame.QUIT:
                    self.running = False
            if evt.type == pygame.MOUSEBUTTONDOWN:
                if not self.currentAction:
                    self.currentItem = self.mouse_get_grid()
                    if self.currentItem.type != ChessItemType.EMPTY and self.whiteAction == self.currentItem.white:
                        self.currentAction =True
                        self.actions = self.currentItem.get_actions(self.grid)
                        if len(self.actions) == 0:
                            self.currentAction = False
                            self.actions = []
                            self.currentItem = Empty()
                else:
                    wasChess = self.isChess(self.whiteAction,self.grid)
                    i=0
                    index=-1
                    for act in self.actions:
                        pos = [act.position[0]*self.tile_size,act.position[1]*self.tile_size]
                        if pos == self.mouse_coord():
                            index=i
                            break
                        i+=1

                    if index != -1 and self.currentItem.type != ChessItemType.EMPTY:
                        last_grid = deepcopy(self.grid)
                        g=self.currentItem.do_action(self.actions[index],self.grid)
                        if wasChess and self.isChess(self.whiteAction,g):
                            # action invalid
                            self.grid = deepcopy(last_grid)
                        else:
                            # valid action
                            if g != None:
                                self.grid = g
                            self.whiteAction = not self.whiteAction

                        self.update_grid()
                        self.currentAction = False
                        self.actions = []
                        self.currentItem = Empty()
                    else:
                        #click out
                        self.currentAction = False
                        self.actions = []
                        self.currentItem = Empty()
        
        winTitle = "Chess game"
        
        if self.enableTimer != -1:
            winTitle += " Timer: {0}/{1}".format(
                int(self.currentTimerTime/1000) if self.showAsInt else self.currentTimerTime/1000, self.enableTimer)

            self.currentTimerTime += deltatime*10000
            if self.currentTimerTime >= self.enableTimer*1000:
                self.whiteAction = not self.whiteAction
                self.update_grid()
                self.currentAction = False
                self.actions = []
                self.currentItem = Empty()
                self.currentTimerTime = 0

        if self.showDeltatime:
            winTitle += " Deltatime: {0}".format(
                int(deltatime*10000) if self.showAsInt else deltatime)
        if self.showFps:
            fps = (1.0/deltatime if deltatime else 1)
            winTitle += " FPS: {0}".format(int(fps) if self.showAsInt else fps)
        display.set_caption(winTitle)


def main(argv):
    game = Chess(argv)
    game.start()


if __name__ == "__main__":
    main(sys.argv)
