
class ChessItemType:
    EMPTY = 0,
    King = 1,
    Queen = 2,
    Rook = 3,
    Bishop = 4,
    Knight = 5,
    Pawn = 6,


class ChessValidAction:
    VALID = 0,
    INVALID = 1,
    VALIDE_ATTACK = 2


class ChessActionType:
    ATTACK = 2,
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

    def __init__(self, type: ChessItemType, white: bool, position):
        self.white = white
        self.type = type
        self.position = position

    def get_actions(self, grid):
        pass

    def loop_action(self,actions, start, end,index,index_value, grid,reverse=False):
        i = start
        if reverse:
            i = end
        while True:
            if reverse:
                if i < start:
                    break
            else:
                if i == end:
                    break
                
            position = [i, i]
            position[index] = index_value

            if self.position != position:
                res = self.valid_action(ChessAction(position), grid)
                if not res == ChessValidAction.INVALID:
                    self.add_action(position, actions, grid)
                    if res == ChessValidAction.VALIDE_ATTACK:
                        break
                else:
                    break
            if reverse:
                i-=1
            else:
                i+=1

    def valid_action(self, action, grid):
        if self.out_position(action.position):
            return ChessValidAction.INVALID

        item = grid[action.position[0]][action.position[1]]
        if item.type != ChessItemType.EMPTY:
            if item.white != self.white:
                return ChessValidAction.VALIDE_ATTACK
            else:
                return ChessValidAction.INVALID
        return ChessValidAction.VALID

    def out_position(self, position):
        if position[0] < 0 or position[0] > 7:
            return True
        if position[1] < 0 or position[1] > 7:
            return True
        return False

    def add_action(self, position, actions, grid):
        tmp = actions
        act = ChessAction(position)
        valid = self.valid_action(act, grid)

        if self.out_position(position):
            return tmp

        if valid == ChessValidAction.VALID:
            act.type = ChessActionType.MOVE
            tmp.append(act)
        elif valid == ChessValidAction.VALIDE_ATTACK:
            act.type = ChessActionType.ATTACK
            tmp.append(act)

        return tmp

    def do_action(self, action: ChessAction, grid):
        grid[self.position[0]][self.position[1]] = Empty()
        grid[action.position[0]][action.position[1]] = self
        self.position = action.position
        return grid


class Pwan(ChessItem):

    def __init__(self, white, position):
        self.first_move = False
        ChessItem.__init__(self, ChessItemType.Pawn, white, position)

    def get_actions(self, grid):
        actions = []
        add = (1 if self.white else -1)

        if self.valid_action(ChessAction([self.position[0], self.position[1]+add]), grid) == ChessValidAction.VALID:
            actions = self.add_action(
                [self.position[0], self.position[1]+add], actions, grid)

        if not self.first_move:
            if self.valid_action(ChessAction([self.position[0], self.position[1]+(add*2)]), grid) == ChessValidAction.VALID:
                actions = self.add_action(
                    [self.position[0], self.position[1]+(add*2)], actions, grid)

        list_try = [[self.position[0]+1, self.position[1]+add],
                    [self.position[0]-1, self.position[1]+add]]
        
        for i in list_try:
            if not self.out_position(i):
                if self.valid_action(ChessAction(i), grid) == ChessValidAction.VALIDE_ATTACK:
                    actions.append(ChessAction(i))

        return actions
    
    def do_action(self, action: ChessAction, grid):
        self.first_move = True
        grid[self.position[0]][self.position[1]] = Empty()
        grid[action.position[0]][action.position[1]] = self
        self.position = action.position
        return grid


class Knight(ChessItem):
    def __init__(self, white, position):
        ChessItem.__init__(self, ChessItemType.Knight, white, position)

    def get_actions(self, grid):
        actions = []
        list_try = [
            [self.position[0]+1, self.position[1]+2],
            [self.position[0]-1, self.position[1]+2],
            [self.position[0]+1, self.position[1]-2],
            [self.position[0]-1, self.position[1]-2],

            [self.position[0]+2, self.position[1]+1],
            [self.position[0]+2, self.position[1]-1],
            [self.position[0]-2, self.position[1]+1],
            [self.position[0]-2, self.position[1]-1]
                    ]
        for i in list_try:
            res = self.valid_action(ChessAction(i), grid)
            if res == ChessValidAction.VALIDE_ATTACK or res == ChessValidAction.VALID:
                actions.append(ChessAction(i))
        return actions


class Bishop(ChessItem):
    def __init__(self, white, position):
        ChessItem.__init__(self, ChessItemType.Bishop, white, position)

    def get_actions(self, grid):
        actions = []
        
        
            # act = ChessAction([self.position[0]+i, self.position[1]+i])
            # res = self.valid_action(act, grid)
            # if res == ChessValidAction.VALID or res == ChessValidAction.VALIDE_ATTACK:
            #     actions.append(act)
            #     if res == ChessValidAction.VALIDE_ATTACK:
            #         break
            # else:
            #     break
        return actions



class Rook(ChessItem):
    def __init__(self, white, position):
        ChessItem.__init__(self, ChessItemType.Rook, white, position)

    def get_actions(self, grid):
        actions = []
        self.loop_action(
            actions, self.position[0], 8, 1, self.position[1], grid)
        
        self.loop_action(
            actions, self.position[1], 8, 0, self.position[0], grid)

        self.loop_action(
            actions,  0, self.position[0], 1, self.position[1], grid,True)
        self.loop_action(
            actions, 0, self.position[1], 0, self.position[0], grid,True)
        

        return actions


class Empty(ChessItem):
    def __init__(self, white=True):
        ChessItem.__init__(self, ChessItemType.EMPTY, white, [0, 0])


class Queen(ChessItem):
    def __init__(self, white, position):
        ChessItem.__init__(self, ChessItemType.Queen, white, position)

    def get_actions(self, grid):
        actions = []
        self.loop_action(
            actions, self.position[0], 8, 1, self.position[1], grid)
        
        self.loop_action(
            actions, self.position[1], 8, 0, self.position[0], grid)

        self.loop_action(
            actions,  0, self.position[0], 1, self.position[1], grid,True)
        self.loop_action(
            actions, 0, self.position[1], 0, self.position[0], grid,True)
        

        return actions


class King(ChessItem):
    def __init__(self, white: bool, position):
        ChessItem.__init__(self, ChessItemType.King, white, position)

    def get_actions(self, grid):
        actions = []

        actions = self.add_action(
            [self.position[0]+1, self.position[1]], actions, grid)
        actions = self.add_action(
            [self.position[0], self.position[1]+1], actions, grid)
        actions = self.add_action(
            [self.position[0]+1, self.position[1]+1], actions, grid)
        actions = self.add_action(
            [self.position[0]-1, self.position[1]+1], actions, grid)
        actions = self.add_action(
            [self.position[0]+1, self.position[1]-1], actions, grid)
        actions = self.add_action(
            [self.position[0]-1, self.position[1]], actions, grid)
        actions = self.add_action(
            [self.position[0], self.position[1]-1], actions, grid)
        actions = self.add_action(
            [self.position[0]-1, self.position[1]-1], actions, grid)

        return actions
