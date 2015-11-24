# Python Final Project
# Connect Four
#
# Irving Salmer4n
# Juan Pablo Meouchi

import random
import os
import time
from player import Player

class Connect4(object):
    
    board = None
    rows = 6
    cols = 7
    rounds = None
    finished = None
    winner = None
    turn = None
    #Player type list
    players = [None, None]

    players_name = ["Kasparov", "Karpov", "Deep Blue", "Rybka"]
    game_name = "Four in a Row"

    colors = ["x", "o"]
    emptySpace = "."
    
    def __init__(self,newgame=True):
        self.rounds = 1
        self.finished = False
        self.winner = None
        
        self.printWelcome()
        
        #Set players color and computer difficulty which is the depth for the minimax
        if newgame:
            self.setPlayers()
        
        self.turn = self.players[0]
        # self.turn = random.choice(self.players)
        #Init board with rows*cols spaces
        # self.board = [[self.emptySpace]*self.cols]*self.rows
        self.board = []
        for i in range(self.rows):
            self.board.append([])
            for j in range(self.cols):
                self.board[i].append(self.emptySpace)


    def setPlayers(self):

        for p in range(self.players.__len__()):
            print("Should Player %s be a Human or a Computer?"%(p+1))

            while self.players[p] == None:
                choice = str(raw_input("Type 'H' or 'C': "))
                if choice.lower().startswith("h"):
                    self.players[p] = Player(self.players_name[p], self.colors[p],"Human")
                elif choice.lower().startswith("c"):
                    diffic = int(raw_input("Enter difficulty (1 - 4) "))
                    if 1<= diffic <= 4:
                        self.players[p] = Player(self.players_name[p+2], self.colors[p],"Computer", diffic)
                else:
                    print "Invalid choice, please try again"

            print "{0} will be {1}".format(self.players[0].name, self.colors[0])


    def switchTurn(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]

        # increment the round number
        self.rounds += 1

    def nextMove(self):
        player = self.turn

        #6 rows * 7 columns are the possible turns giving a DRAW
        if self.rounds > self.rows*self.cols:
            self.finished = True
            return
        
        # returns the column the player chose
        move = player.move(self.board,self.rounds)

        for i in range(self.rows):
            #Find empty space to put the tile
            if self.board[i][move] == self.emptySpace:
                self.board[i][move] = player.color
                self.switchTurn()
                self.checkWinMove()
                self.printState(move,player)
                return
        print("Invalid move")
        return
    
    def checkWinMove(self):

        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != self.emptySpace:
                     #Check vertical four-in a row
                    if self.checkVertical(i, j):
                        self.finished = True
                        return
                    
                     #Check horizontal four-in a row
                    if self.checkHorizontal(i, j):
                        self.finished = True
                        return
                    
                    #Check diagonal four-in a row
                    diag_fours, slope = self.checkDiagonal(i, j)
                    if diag_fours:
                        self.finished = True
                        return
        
    def checkVertical(self, row, col):
        tiles = 0
    
        for i in range(row, self.rows):
            if self.board[i][col].lower() == self.board[row][col].lower():
                tiles += 1
            else:
                break
    
        if tiles >= 4:
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]
            return True
    
        return False
    
    def checkHorizontal(self, row, col):
        tiles = 0
        
        for j in range(col, self.cols):
            if self.board[row][j].lower() == self.board[row][col].lower():
                tiles += 1
            else:
                break

        if tiles >= 4:
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]
            return True

        return False
    
    def checkDiagonal(self, row, col):
        count = 0
        direction = None

        tiles = 0
        j = col
        for i in range(row, self.rows):
            if j > self.rows:
                break
            if self.board[i][j].lower() == self.board[row][col].lower():
                tiles += 1
            else:
                break
            j += 1
            
        if tiles >= 4:
            count += 1
            direction = 1
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        tiles = 0
        j = col
        for i in range(row, -1, -1):
            if j > self.rows:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                tiles += 1
            else:
                break
            j += 1 # increment column when row is decremented

        if tiles >= 4:
            count += 1
            direction = -1
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        if count == 2:
            direction = 0
        if count > 0:
            return True, direction
        
        return False, direction
    
    def checkBoard(self):
    
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != self.emptySpace:
                    # check if a vertical four-in-a-row starts at (i, j)
                    if self.checkVertical(i, j):
                        self.markWinner(i, j, 0)
                    
                    # check if a horizontal four-in-a-row starts at (i, j)
                    if self.checkHorizontal(i, j):
                        self.markWinner(i, j, 1)
                    
                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    # also, get the slope of the four if there is one
                    diag_fours, slope = self.checkDiagonal(i, j)
                    if diag_fours:
                        self.markWinner(i, j, 2, slope)
    
    def markWinner(self, row, col, direction, slope=None):
        
        if direction == 0:
            for i in range(4):
                self.board[row+i][col] = self.board[row+i][col].upper()
        
        elif direction == 1:
            for i in range(4):
                self.board[row][col+i] = self.board[row][col+i].upper()
        
        elif direction == 2:
            if slope == 1 or slope == 0:
                for i in range(4):
                    self.board[row+i][col+i] = self.board[row+i][col+i].upper()
        
            elif slope == -1 or slope == 0:
                for i in range(4):
                    self.board[row-i][col+i] = self.board[row-i][col+i].upper()
        
        else:
            print("Error - Cannot enunciate four-of-a-kind")
    
    def printState(self,move=None,player=None):
        self.printWelcome(move,player)
        print "Round: ",self.rounds

        for i in range(5, -1, -1):
            print "\t",
            for j in range(self.cols):
                print "| " + str(self.board[i][j]),
            print "|"
        print "\t  _   _   _   _   _   _   _ "
        print "\t  1   2   3   4   5   6   7 "

        if self.finished:
            print "Game Over!"
            if self.winner != None:
                print str(self.winner.name) + " is the winner"
            else:
                print "It's a DRAW"
                

    def printWelcome(self,col=None,player=None):
        # do cross-platform clear screen
        os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
        #Welcome message to game
        print "\t\tWelcome to {0}!".format(self.game_name)
        print "\t\tBy Irving and Juan Pablo.\n\n"

        if player != None:
            if player.type.lower().startswith("c"):
                print "%s moved in : %s\n"%(player.name,(col+1))