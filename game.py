import pygame
from pygame import Surface, draw, display, event, key,mouse
import sys
import time
from pygame import cursors

from pygame.cursors import Cursor


class Game:
    current_time: float = 0
    last_time: float = 0
    renderer: Surface
    running: bool = True

    def __init__(self, size):
        pygame.init()
        self.renderer = display.set_mode(size)

    def start(self):
        while self.running:
            self.current_time = time.clock_gettime(
                time.CLOCK_PROCESS_CPUTIME_ID)
            deltatime = (self.current_time - self.last_time)
            self.last_time = self.current_time

            self.renderer.fill((0, 0, 0))

            self.update(deltatime)
            self.draw()

            display.flip()
            # time.sleep()

    def draw(self):
        pass

    def update(self, deltatime):
        pass


class ChessItemType:
    EMPTY=0,
    King=1,
    Queen=2,
    Rook=3,
    Bishop=4,
    Knight=5,
    Pawn=6

class ChessActionType:
    OVER_MOVE=2,
    MOVE=1,
    SKIP=0,
    NONE=-1

class ChessAction:
    position = [0,0]
    type:ChessActionType

    def __init__(self,position,type=ChessActionType.NONE):
        self.type = type
        self.position = position

class ChessItem:

    def __init__(self, type:ChessItemType, white:bool):
        self.white = white
        self.type = type
        self.position=[0,0]

    def get_actions(self,grid):
        pass
    def do_action(self,action:ChessAction,grid):
        grid[self.position[0]][self.position[1]] = Empty()
        grid[action.position[0]][action.position[1]] = self
        self.position = action.position
        return grid

class Empty(ChessItem):
    def __init__(self):
        ChessItem.__init__(self,ChessItemType.EMPTY,True)



class King(ChessItem):
    def __init__(self,white:bool):
        ChessItem.__init__(self,ChessItemType.King,white)

    def get_actions(self,grid):
        actions = []

        #actions.append(ChessAction(self.position))
        
        actions.append(ChessAction([self.position[0]+1,self.position[1]]))
        actions.append(ChessAction([self.position[0],self.position[1]+1]))
        actions.append(ChessAction([self.position[0]+1,self.position[1]+1]))
        actions.append(ChessAction([self.position[0]-1,self.position[1]+1]))
        actions.append(ChessAction([self.position[0]+1,self.position[1]-1]))
        actions.append(ChessAction([self.position[0]-1,self.position[1]]))
        actions.append(ChessAction([self.position[0],self.position[1]-1]))
        actions.append(ChessAction([self.position[0]-1,self.position[1]-1]))
        return actions


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
        self.grid[0][0] = King(True)
        
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

        if self.showDeltatime:
            display.set_caption("Chess game - {0}".format(deltatime))


def main(argv):
    game = Chess(argv)
    game.start()


if __name__ == "__main__":
    main(sys.argv)