from random import randint
from BoardClasses import Move
from BoardClasses import Board
import copy
import math

MINIMAX_DEPTH = 10
INFINITY = 10000

#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2

    def get_move(self,move):
            # make opponents move
            if len(move) != 0:
                self.board.make_move(move,self.opponent[self.color])
            # switch turn
            else:
                self.color = 1
            # find player 1 next move
            moves = self.board.get_all_possible_moves(self.color)
            alpha = -INFINITY
            beta = INFINITY
            result = self.move_ordering(self.color)
            for move in moves:
                for m in move:
                    limit = 0
                    self.board.make_move(m,self.color)
                    val = self.min_value(limit+1, alpha, beta)
                    if val > alpha:
                        alpha = val
                        result = m
                    self.board.undo()
            self.board.make_move(result,self.color)
            return result
            
    def max_value(self,limit, alpha, beta):
        if limit == MINIMAX_DEPTH or self.board.is_win(self.color) == self.color:
            return self.heuristic()
        #alpha = -INFINITY               # result = -infinity
        # move = self.move_ordering(self.color)
        # if not move:
        #     return alpha
        # self.board.make_move(move,self.color)
        # v = self.min_value(limit+1,alpha,beta)
        # self.board.undo()
        # if v >= beta:
        #     return INFINITY
        # alpha = max(alpha,v)
        val = -INFINITY
        moves = self.board.get_all_possible_moves(self.color)
        for move in moves:
            for m in move:
                self.board.make_move(m,self.color)
                val = max(val,self.min_value(limit+1,alpha,beta))
                self.board.undo()
                alpha = max(alpha,val)
                if alpha >= beta:
                    return val
        return val


    def min_value(self,limit, alpha, beta):
        if limit == MINIMAX_DEPTH or self.board.is_win(self.color) == self.opponent[self.color]:
            return self.heuristic()
        #beta = INFINITY               # result = infinity
        # move = self.move_ordering(self.opponent[self.color])
        # if not move:
        #     return beta
        # self.board.make_move(move,self.opponent[self.color])
        # v = self.max_value(limit+1,alpha,beta)
        # self.board.undo()
        # if alpha >= v:
        #     return -INFINITY
        # beta = min(beta,v)
        # return beta
        val = INFINITY
        moves = self.board.get_all_possible_moves(self.opponent[self.color])
        for move in moves:
            for m in move:
                self.board.make_move(m,self.opponent[self.color])
                val = min(val,self.max_value(limit+1, alpha,beta))
                self.board.undo()
                beta = min(beta,val)
                if alpha >= beta:   # pruning - go to next move (?)
                    return val
        return val


    def heuristic(self):
        black = 0
        white = 0
        #if (self.board.black_count+self.board.white_count) > (0.4* self.board.p * self.board.col):  # Decide between early game and mid,end game
        for row in range(self.board.row):
            for col in range(self.board.col):
                if self.board.board[row][col].color == "B":
                    if self.board.board[row][col].is_king:    # King = 10
                        black += self.board.row
                    else:
                        black += (5 + self.board.board[row][col].row - (0.5 * self.board.row))  # reg piece = 5 + rows on oponent side

                elif self.board.board[row][col].color == "W":
                    if self.board.board[row][col].is_king:    # King = 10
                        white += self.board.row
                    else:
                        white += (5 + (self.board.row*0.5) - self.board.board[row][col].row)    # reg piece = 5 + rows on oponent s
        if self.color == 1:
            return black-white
        else:
            return white-black        
       
                
    
    def move_ordering(self,player):
        best_move_value = -INFINITY if (player == self.color) else INFINITY
        moves = self.board.get_all_possible_moves(player)
        if moves:
            best_move = moves[0][0]
        else:
            return False
        for move in moves:
            for m in move:
                self.board.make_move(m,player)
                v = self.heuristic()
                if v > best_move_value if (player== self.color) else v < best_move_value:
                    best_move_value = v
                    best_move = m
                self.board.undo()
        return best_move

