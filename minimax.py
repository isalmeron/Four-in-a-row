# Python Final Project
# Connect Four
#
# Irving Salmeron

import random, copy
from pprint import pprint

class Minimax(object):
    
    board = None
    colors = ["x", "o"]
    rows = 6
    cols = 7
    emptySpace = "."
    start_alpha = -99999999

    fd = None
    
    def __init__(self, board):
        # copy the board to self.board
        self.board = [x[:] for x in board]

    def findColumn(self, depth, state, curr_player,rounds):
        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        # self.fd = open("legal_moves-%s.txt"%rounds,"a",1)
        # self.fd.write("Initial state\n")

        legal_moves = self.search(depth, state, curr_player)

        #If a winner move then alpha=1000 if lose move alpha(beta) =-1000
        #Ensures it gets a value without an exception even if legal_moves its empty
        alpha = max(legal_moves) if legal_moves.__len__() > 0 else -start_alpha
        #It may be that alpha=0 cause it is not a legal move but gt the negative values
        if alpha == 0:
            alpha = min(legal_moves)
            for i in range(legal_moves.__len__()):
                if alpha != 0:
                    if self.isValid(i,state):
                        if legal_moves[i] > alpha:
                            alpha = legal_moves[i]

        # self.fd.write("ALPHA: %s\n"%alpha)
        # pprint(legal_moves,self.fd)
        
        #Get the best moves found with best alpha        
        best_moves = []
        for c in range(legal_moves.__len__()):
            if legal_moves[c] == alpha and self.isValid(c,state):
                best_moves.append(c)

        # self.fd.write("BEST MOVE:\n")
        # pprint(best_moves,self.fd)
        # self.fd.close()

        #If there are several moves with same alpha alphaValue choose a random one
        return random.choice(best_moves), alpha
        
    def search(self, depth, state, curr_player):

        # self.fd.write("DEPTH: %s\n"%depth)
        # pprint(state,self.fd)

        if depth == 0 or self.isBoardFull(state):
            return [self.alphaValue(state, curr_player)]

        legal_columns = [0]*self.cols

        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        for c in range(self.cols):
            if not self.isValid(c, state):
                continue
            tempBoard = self.makeMove(state, c, curr_player)
            if self.endGame(tempBoard):
                legal_columns[c] = start_alpha
                break
            for ch in range(self.cols):
                if not self.isValid(ch, tempBoard):
                    continue
                tempBoard2 = self.makeMove(tempBoard, ch, opp_player)
                if self.endGame(tempBoard2):
                    legal_columns[c] = -start_alpha
                    break
                alpha = self.search(depth-1, tempBoard2, curr_player)      

                if sum(alpha)>89999999:
                    legal_columns[c] = start_alpha
                else:
                    legal_columns[c] += sum(alpha)

                # self.fd.write("ALPHA: %s COL: %s CH: %s\n\n"%(legal_columns[c],c,ch))

        # self.fd.write("End Initial\nRETURN:\n")
        # pprint(legal_columns,self.fd)
        
        return legal_columns

    def isValid(self, column, state):      
        for i in range(self.rows):
            if state[i][column] == self.emptySpace:
                return True
        return False

    def isBoardFull(self, state):
        #Check the top row for every column and if no empty space board if full
        for c in range(self.cols):
            if state[self.rows-1][c] == self.emptySpace:
                return False
        return True
    
    #Checks if there is any 4-in-a-row for every player
    def endGame(self, state):
        if self.checkBoard(state, self.colors[0], 4) >= 1:
            return True
        elif self.checkBoard(state, self.colors[1], 4) >= 1:
            return True
        else:
            return False
        
    #Sets a column as marked by the color(player)
    def makeMove(self, state, column, player):
        temp = [x[:] for x in state]
        for i in range(self.rows):
            if temp[i][column] == self.emptySpace:
                temp[i][column] = player
                return temp
    #Determine the alpha value (num of 4-in-a-rows)*1000 + (num of 3-in-a-rows)*5 + 
    #(num of 2-in-a-rows) - (num of opponent 4-in-a-rows)*1000 - (num of opponent
    #3-in-a-rows)*5 - (num of opponent 2-in-a-rows)
    def alphaValue(self, state, color):
        if color == self.colors[0]:
            o_color = self.colors[1]
        else:
            o_color = self.colors[0]
        # my_fours = 0
        # opp_fours = 0
        my_fours = self.checkBoard(state, color, 4)
        my_threes = self.checkBoard(state, color, 3)
        my_twos = self.checkBoard(state, color, 2)

        opp_fours = self.checkBoard(state, o_color, 4)
        opp_threes = self.checkBoard(state, o_color, 3)
        opp_twos = self.checkBoard(state, o_color, 2)

        return (my_fours*100 + my_threes*5 + my_twos) - (opp_fours*1000 + opp_threes*5 + opp_twos)
      

    #Functions to check and evaluate the current state to determine which one to chose
    def checkBoard(self, state, color, tileCount):
        count = 0
        # for each piece in the board...
        for i in range(self.rows):
            for j in range(self.cols):
                if state[i][j].lower() == color.lower():
                    count += self.checkVertical(i, j, state, tileCount)
                    
                    count += self.checkHorizontal(i, j, state, tileCount)
                    
                    count += self.checkDiagonal(i, j, state, tileCount)
        return count
            
    def checkVertical(self, row, col, state, tileCount):
        consecutiveCount = 0
        for i in range(row, self.rows):
            if state[i][col].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break
    
        if consecutiveCount >= tileCount:
            return 1
        else:
            return 0
    
    def checkHorizontal(self, row, col, state, tileCount):
        consecutiveCount = 0
        for j in range(col, self.cols):
            if state[row][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= tileCount:
            return 1
        else:
            return 0
    
    def checkDiagonal(self, row, col, state, tileCount):

        total = 0
        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in range(row, self.rows):
            if j > self.rows:
                break
            elif state[i][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented
            
        if consecutiveCount >= tileCount:
            total += 1

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > self.rows:
                break
            elif state[i][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented

        if consecutiveCount >= tileCount:
            total += 1

        return total