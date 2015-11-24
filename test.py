from minimax import *

def printState(board):
	for i in range(5, -1, -1):
	    print "\t",
	    for j in range(7):
	        print "| " + str(board[i][j]),
	    print "|"
	print "\t  _   _   _   _   _   _   _ "
	print "\t  1   2   3   4   5   6   7 "

board = [["x","x","x",".","o",".","."]
		,[".","o",".",".",".",".","."]
		,[".","o",".",".",".",".","."]
		,[".",".",".",".",".",".","."]
		,[".",".",".",".",".",".","."]
		,[".",".",".",".",".",".","."]]
printState(board)
m = Minimax(board)

print m.findColumn(1, board, "o", 6)

board = [["x","x","x",".","o",".","."]
		,[".","o","x",".",".",".","."]
		,[".","o",".",".",".",".","."]
		,[".","o",".",".",".",".","."]
		,[".",".",".",".",".",".","."]
		,[".",".",".",".",".",".","."]]

printState(board)
m = Minimax(board)

print m.findColumn(1, board, "o", 8)