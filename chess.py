class ChessItemType:
    EMPTY = 0,
    King = 1,
    Queen = 2,
    Rook = 3,
    Bishop = 4,
    Knight = 5,
    Pawn = 6


class ChessActionType:
    OVER_MOVE = 2,
    MOVE = 1,
    SKIP = 0,
    NONE = -1


class ChessAction:
    position = [0, 0]
    type: ChessActionType

    def __init__(self, position, type=ChessActionType.NONE):
        self.type = type
        self.position = position


class ChessItem:

    def __init__(self, type: ChessItemType, white: bool,position):
        self.white = white
        self.type = type
        self.position = position

    def get_actions(self, grid):
        pass

    def do_action(self, action: ChessAction, grid):
        grid[self.position[0]][self.position[1]] = Empty()
        grid[action.position[0]][action.position[1]] = self
        self.position = action.position
        return grid


class Bishop(ChessItem):
    def __init__(self, white,position):
        ChessItem.__init__(self, ChessItemType.Bishop, white,position)

    def get_actions(self, grid):
        actions = []
        
        return actions

class Rook(ChessItem):
    def __init__(self, white,position):
        ChessItem.__init__(self, ChessItemType.Rook, white,position)

    def get_actions(self, grid):
        actions = []
        for i in range(0,8):
            actions.append(ChessAction([i,self.position[1]]))
            actions.append(ChessAction([self.position[0],i]))  
            
        return actions


class Empty(ChessItem):
    def __init__(self):
        ChessItem.__init__(self, ChessItemType.EMPTY, True,[0,0])


class King(ChessItem):
    def __init__(self, white: bool,position):
        ChessItem.__init__(self, ChessItemType.King, white,position)

    def get_actions(self, grid):
        actions = []

        # actions.append(ChessAction(self.position))

        actions.append(ChessAction([self.position[0]+1, self.position[1]]))
        actions.append(ChessAction([self.position[0], self.position[1]+1]))
        actions.append(ChessAction([self.position[0]+1, self.position[1]+1]))
        actions.append(ChessAction([self.position[0]-1, self.position[1]+1]))
        actions.append(ChessAction([self.position[0]+1, self.position[1]-1]))
        actions.append(ChessAction([self.position[0]-1, self.position[1]]))
        actions.append(ChessAction([self.position[0], self.position[1]-1]))
        actions.append(ChessAction([self.position[0]-1, self.position[1]-1]))
        return actions
