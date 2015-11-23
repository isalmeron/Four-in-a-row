# Python Final Project
# Connect Four
#
# Irving Salmeron
# Juan Pablo Meouchi

import random, copy
from pprint import pprint

class Minimax(object):
    
    board = None
    colors = ["x", "o"]
    rows = 6
    cols = 7
    emptySpace = "."
    start_alpha = -1000

    fd = None
    
    def __init__(self, board):
        # copy the board to self.board
        self.board = [x[:] for x in board]

            
    def bestMove(self, depth, state, curr_player):
        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        # enumerate all legal moves
        legal_moves = {} # will map legal move states to their alpha values
        for col in range(self.cols):
            # if column i is a legal move...
            if self.isLegalMove(col, state):
                # make the move in column 'col' for curr_player as root for tree search
                temp = self.makeMove(state, col, curr_player)
                legal_moves[col] = self.search(depth-1, temp, opp_player)

        best_alpha = self.start_alpha
        best_move = None
        moves = legal_moves.items()
        random.shuffle(list(moves))
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move
        
        print "Alpha: ",best_alpha
        pprint(best_move)

        return best_move, best_alpha

    def bestMove2(self, depth, state, curr_player,rounds):
        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        # self.fd = open("legal_moves-%s.txt"%rounds,"a",1)
        # self.fd.write("Initial state\n")

        legal_moves = self.search2(depth, state, curr_player)

        #If a winner move then alpha=3000 if lose move alpha(beta) =-3000
        #Ensures it gets a value without an exception even if legal_moves its empty
        alpha = max(legal_moves) if legal_moves.__len__() > 0 else -99999999
        #It may be that alpha=0 cause it is not a legal move but gt the negative values
        if alpha == 0:
            alpha = min(legal_moves)
            for i in range(legal_moves.__len__()):
                if alpha != 0:
                    if self.isLegalMove(i,state):
                        if legal_moves[i] > alpha:
                            alpha = legal_moves[i]

        # self.fd.write("ALPHA: %s\n"%alpha)
        # pprint(legal_moves,self.fd)
        
        #Get the best moves found with best alpha        
        best_moves = []
        for c in range(legal_moves.__len__()):
            if legal_moves[c] == alpha and self.isLegalMove(c,state):
                best_moves.append(c)

        
        # self.fd.close()

        #If there are several moves with same alpha value choose a random one
        return random.choice(best_moves), alpha
        
    def search(self, depth, state, curr_player):
        # enumerate all legal moves from this state
        legal_moves = []

        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        # if this node (state) is a terminal node or depth == 0...
        if depth == 0 or self.gameIsOver(state):
            # return the heuristic value of node
            return self.value(state, curr_player)

        for i in range(self.cols):
            # if column i is a legal move...
            if self.isLegalMove(i, state):
                # make the move in column i for curr_player
                temp = self.makeMove(state, i, curr_player)
                legal_moves.append(temp)

        alpha = self.start_alpha
        for child in legal_moves:
            alpha = max(alpha, -self.search(depth-1, child, opp_player))

        return alpha

    def search2(self, depth, state, curr_player):

        # self.fd.write("DEPTH: %s\n"%depth)
        # pprint(state,self.fd)

        if depth == 0 or self.isBoardFull(state):
            return [self.value(state, curr_player)]

        legal_columns = [0]*self.cols

        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        for c in range(self.cols):
            if not self.isLegalMove(c, state):
                continue
            tempBoard = self.makeMove(state, c, curr_player)
            if self.gameIsOver(tempBoard):
                legal_columns[c] = 1000
                continue
            for ch in range(self.cols):
                if not self.isLegalMove(ch, tempBoard):
                    continue
                tempBoard2 = self.makeMove(tempBoard, ch, opp_player)
                if self.gameIsOver(tempBoard2):
                    legal_columns[c] = -1000
                    continue
                alpha = self.search2(depth-1, tempBoard2, curr_player)                
                legal_columns[c] += sum(alpha)

        #         self.fd.write("ALPHA: %s COL: %s CH: %s\n\n"%(legal_columns[c],c,ch))

        # self.fd.write("End Initial\nRETURN:\n")
        # pprint(legal_columns,self.fd)
        
        return legal_columns

    def isLegalMove(self, column, state):      
        for i in range(self.rows):
            if state[i][column] == self.emptySpace:
                return True
        
        # if we get here, the column is full
        return False

    def isBoardFull(self, state):
        #Check the top row for every column and if no empty space board if full
        for c in range(self.cols):
            if state[self.rows-1][c] == self.emptySpace:
                return False
        return True
    
    #Checks if there is any 4-in-a-row for every player
    def gameIsOver(self, state):
        if self.checkForStreak(state, self.colors[0], 4) >= 1:
            return True
        elif self.checkForStreak(state, self.colors[1], 4) >= 1:
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
    #Determine the alpha value (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 + 
    #(num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
    #3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
    def value(self, state, color):
        if color == self.colors[0]:
            o_color = self.colors[1]
        else:
            o_color = self.colors[0]
        
        my_fours = self.checkForStreak(state, color, 4)
        my_threes = self.checkForStreak(state, color, 3)
        my_twos = self.checkForStreak(state, color, 2)

        opp_fours = self.checkForStreak(state, o_color, 4)
        opp_threes = self.checkForStreak(state, o_color, 3)
        opp_twos = self.checkForStreak(state, o_color, 2)

        return (my_fours*10 + my_threes*5 + my_twos) - (opp_fours*10 + opp_threes*5 + opp_twos)
      

    #Functions to check and evaluate the current state to determine which one to chose
    def checkForStreak(self, state, color, streak):
        count = 0
        # for each piece in the board...
        for i in range(self.rows):
            for j in range(self.cols):
                if state[i][j].lower() == color.lower():
                    count += self.verticalStreak(i, j, state, streak)
                    
                    count += self.horizontalStreak(i, j, state, streak)
                    
                    count += self.diagonalCheck(i, j, state, streak)
        return count
            
    def verticalStreak(self, row, col, state, streak):
        consecutiveCount = 0
        for i in range(row, self.rows):
            if state[i][col].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break
    
        if consecutiveCount >= streak:
            return 1
        else:
            return 0
    
    def horizontalStreak(self, row, col, state, streak):
        consecutiveCount = 0
        for j in range(col, self.cols):
            if state[row][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= streak:
            return 1
        else:
            return 0
    
    def diagonalCheck(self, row, col, state, streak):

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
            
        if consecutiveCount >= streak:
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

        if consecutiveCount >= streak:
            total += 1

        return total