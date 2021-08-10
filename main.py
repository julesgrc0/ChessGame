import os
import pygame
import sys
import time
import time
import random
import datetime

from os import listdir
from os.path import isfile, join
from pygame import Surface, draw, display, event, key,mouse,cursors,image,transform,font
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
    showMove = True
    showChess = True
    showTurn = True

    chessKing = [-1,-1]

    currentMove = [-1, -1]
    lastcurrentMove = [-1,-1]

    enableTimer = -1
    currentTimerTime = 0

    tile_count = 8
    grid=[]
    images = []
    winsize = 700
    winTitle = "Chess game"
    gameStop = False

    currentChoose = False
    choosePosition = [-1,-1]

    def __init__(self, args):
        self.process_args(args)
        size = int(self.winsize/8)*8
        Game.__init__(self, [size,size])
        icon = image.load(os.path.dirname(os.path.abspath(
            __file__))+os.sep+"assets"+os.sep+"icon.png").convert_alpha()
        display.set_icon(icon)
        self.tile_size = int(self.renderer.get_width()/self.tile_count)

        self.fontpath = os.path.dirname(os.path.abspath(
            __file__))+os.sep+"assets"+os.sep+"font.ttf"
        self.font = pygame.font.SysFont(self.fontpath, 72)
        
        self.fill_grid(self.grid)
        self.init_grid(self.grid)
        self.chess_grid()
        self.load_images("white")
        self.load_images("black")
        
        display.set_caption("Chess game")

    def MatchEnd(self, white=True, grid=[]):
        if self.isChess(white,grid):
            possibilities = []
            tmp_grid = deepcopy(grid)
            
            for i in range(0,self.tile_count):
                for k in range(0,self.tile_count):
                    if tmp_grid[i][k].type != ChessItemType.EMPTY and tmp_grid[i][k].white == white:
                        possibilities.append([tmp_grid[i][k].get_actions(tmp_grid),tmp_grid[i][k]])
           
            for act in possibilities:
                for action in act[0]:
                    act[1].do_action(action,tmp_grid)
                    if not self.isChess(white,tmp_grid):
                        return False
                    tmp_grid = deepcopy(grid)
            return True
        return False

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
                self.chessKing = king_position
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

        if len(args) > 9 and int(args[9]) ==1:
            self.winTitle = ""

        if len(args) > 10 and int(args[10]) ==1:
            self.showMove = False

        if len(args) > 11 and int(args[11]) ==1:
            self.showChess = False
        if len(args) > 12 and int(args[12]) ==1:
            self.showTurn = False
    
    def load_images(self,dir):
        path = os.path.dirname(os.path.abspath(__file__))+os.sep+"assets"+os.sep+dir+os.sep
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

    def fill_grid(self,grid):
        for i in range(0,self.tile_count):
            grid.append([])
            for k in range(0,self.tile_count):  
                  grid[i].append(Empty())

    def draw_grid(self):
        back = (184, 139, 74)
        case =  (227, 193, 111)
        if not self.startWhiteTop:
            back = case
            case = (184, 139, 74)
        self.renderer.fill(back)
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
                    draw.rect(self.renderer, case, pygame.Rect(
                        x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size))

                    
    
    def init_grid(self,grid):
        i=0
        switch = False
        for x in range(0, self.tile_count):
            for y in range(0, self.tile_count):
                if i >= self.tile_count:
                    i = 0
                else:
                    switch = not switch
                i += 1

                grid[x][y] = Empty(switch)

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

    def draw_chess(self,grid):
        for x in range(0,self.tile_count):
            for y in range(0,self.tile_count):
                if grid[x][y].type != ChessItemType.EMPTY:
                    # color=(255,255,255)
                    # if not self.grid[x][y].white:
                    #     color = (0,0,0)
                    # draw.rect(self.renderer,color,pygame.Rect(x*self.tile_size,y*self.tile_size,self.tile_size,self.tile_size))
                    
                    item_type = grid[x][y].type
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
                    if not grid[x][y].white:
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
            self.grid[i][1] = Pwan(self.startWhiteTop,self.startWhiteTop,[i,1])
            self.grid[i][6] = Pwan(
                not self.startWhiteTop, self.startWhiteTop, [i, 6])

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
        if self.gameStop:
            self.draw_grid()
            if self.showChess:
                draw.rect(self.renderer, (161, 18, 13), pygame.Rect(
                    self.chessKing[0]*self.tile_size, self.chessKing[1]*self.tile_size, self.tile_size, self.tile_size))
            self.draw_chess(self.grid)

            
            txt = self.font.render("White Win" if not self.whiteAction else "Black Win", True, (255,255,255) if not self.whiteAction else (0,0,0))
            w, h = self.renderer.get_size()
            self.renderer.blit(txt,txt.get_rect(center=(w/2, h/2)))
        else:    
            self.draw_grid()
            if not self.currentChoose:
                coord = self.mouse_coord()
                draw.rect(self.renderer, (190, 140, 90), pygame.Rect(
                    coord[0], coord[1], self.tile_size, self.tile_size))
                self.draw_rect(coord[0], coord[1], self.tile_size)
                
                if self.showMove:
                    draw.rect(self.renderer, (217, 162, 13), pygame.Rect(
                    self.currentMove[0]*self.tile_size, self.currentMove[1]*self.tile_size, self.tile_size, self.tile_size))
                    draw.rect(self.renderer, (161, 121, 13), pygame.Rect(
                    self.lastcurrentMove[0]*self.tile_size, self.lastcurrentMove[1]*self.tile_size, self.tile_size, self.tile_size))
                if self.showChess:
                    draw.rect(self.renderer, (161, 18, 13), pygame.Rect(
                        self.chessKing[0]*self.tile_size, self.chessKing[1]*self.tile_size, self.tile_size, self.tile_size))
                    
                self.draw_chess(self.grid)
                if self.currentAction:
                    self.draw_actions()
            else:
                tmp = []
                self.fill_grid(tmp)
                self.init_grid(tmp)
                tmp[0][0] = Rook(not self.currentAction,[0,0])
                tmp[1][0] = Knight(not self.currentAction,[1,0])
                tmp[2][0] = Bishop(not self.currentAction,[2,0])
                tmp[3][0] = Queen(not self.currentAction,[3,0])
                self.draw_chess(tmp)


                
    def write_info(self):
        f = open("info.log", "w+")
        lines = ["Date "+str(datetime.datetime.now()), "",
                 os.path.dirname(os.path.abspath(__file__))+os.sep+"assets"+os.sep, ""]
        lines += [
            "Empty  0",
            "King  1",
            "Queen  2",
            "Rook  3",
            "Bishop  4",
            "Knight  5",
            "Pawn  6",
        ]
        lines.append("")
        for x in range(0, self.tile_count):
            l = ""
            for y in range(0, self.tile_count):
                l += str(self.grid[y][x].type[0]) + " "
            lines.append(l)
        lines.append("")
        lines += [
                "whiteAction "+str(self.whiteAction),
                "showAsInt "+str(self.showAsInt),
                "showGridEffect "+str(self.showGridEffect),
                "showDeltatime "+str(self.showDeltatime),
                "showFps "+str(self.showFps ),
                "showMove"+str(self.showMove),
                "startWhiteTop "+str(self.startWhiteTop ),
                "enableTimer "+str(self.enableTimer)+" s",
                "currentTimerTime "+str(self.currentTimerTime)+" ms",
                "currentMove "+str(self.currentMove),
                "lastcurrentMove "+str(self.lastcurrentMove),
                ]
        for line in lines:
            f.write(line+"\n")
        f.close()

    def update(self, deltatime):
        for evt in event.get():
            if evt.type == pygame.QUIT:
                    self.running = False
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_ESCAPE:
                    self.running = False
                if evt.key == pygame.K_i:
                    self.write_info()
            if evt.type == pygame.MOUSEBUTTONDOWN:
                if self.currentChoose:
                    coord = self.mouse_coord()
                    position = [int(coord[0]/self.tile_size),int(coord[1]/self.tile_size)]
                    white = self.grid[self.choosePosition[0]][self.choosePosition[1]].white
                    x = position[0]
                    if x == 0 or x == 7:
                        self.grid[self.choosePosition[0]][self.choosePosition[1]] = Rook(white,self.choosePosition)
                    elif x == 1 or x == 6:
                        self.grid[self.choosePosition[0]][self.choosePosition[1]] = Knight(white,self.choosePosition)
                    elif x ==2 or x == 5:
                        self.grid[self.choosePosition[0]][self.choosePosition[1]] = Bishop(white,self.choosePosition)
                    elif x ==3 or x==4:
                         self.grid[self.choosePosition[0]][self.choosePosition[1]] = Queen(white,self.choosePosition)

                    
                    self.choosePosition = [-1,-1]
                    self.currentChoose = False
                else:
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
                            tmpCurrentMove = self.currentItem.position
                            last_grid = deepcopy(self.grid)
                            g=self.currentItem.do_action(self.actions[index],self.grid)
                            if wasChess and self.isChess(self.whiteAction,g):
                                # action invalid
                                self.grid = deepcopy(last_grid)
                            else:
                                if not self.isChess(self.whiteAction,g): 
                                    self.chessKing = [-1,-1]
                                    self.currentTimerTime = 0
                                    # valid action
                                    if g != None:
                                        self.grid = g
                                        if self.currentItem.type == ChessItemType.Pawn and self.currentItem.chooseActive:
                                            self.currentChoose = True
                                            self.choosePosition = self.currentItem.position
                                    self.whiteAction = not self.whiteAction
                                    self.currentMove = self.currentItem.position
                                    self.lastcurrentMove = tmpCurrentMove

                                    # update chessKing position
                                    self.isChess(self.whiteAction, self.grid)
                                    if self.MatchEnd(self.whiteAction,self.grid):
                                        self.gameStop = True
                                else:
                                    self.grid = deepcopy(last_grid)

                            self.update_grid()
                            self.currentAction = False
                            self.actions = []
                            self.currentItem = Empty()
                        else:
                            
                            #click out
                            self.currentAction = False
                            self.actions = []
                            self.currentItem = Empty()
        if not self.gameStop:
            tmpTitle = self.winTitle
            if self.showTurn:
                tmpTitle += " "+("White" if self.whiteAction else "Black")
            if self.enableTimer != -1:
                tmpTitle += " Timer: {0}/{1}".format(
                    int(self.currentTimerTime/1000) if self.showAsInt else self.currentTimerTime/1000, self.enableTimer)

                self.currentTimerTime += deltatime*1000
                if self.currentTimerTime >= self.enableTimer*1000:
                    self.whiteAction = not self.whiteAction
                    self.update_grid()
                    self.currentAction = False
                    self.actions = []
                    self.currentItem = Empty()
                    self.currentTimerTime = 0

            if self.showDeltatime:
                tmpTitle += " Deltatime: {0}".format(
                    int(deltatime*10000) if self.showAsInt else deltatime)
            if self.showFps:
                fps = (1.0/deltatime if deltatime else 1)
                tmpTitle += " FPS: {0}".format(int(fps) if self.showAsInt else fps)
            display.set_caption(tmpTitle)
        else:
             display.set_caption("Chess game - {0}".format("White Win" if not self.whiteAction else "Black Win"))


def main(argv):
    game = Chess(argv)
    game.start()


if __name__ == "__main__":
    main(sys.argv)
