# Python Final Project
# Connect Four
#
# Irving Salmeron

from connect4 import *

def main():
    
    connect4 = Connect4()
    connect4.printState()
    player1 = connect4.players[0]
    player2 = connect4.players[1]
    
    # win_counts = [0, 0, 0] # [p1 wins, p2 wins, ties]
    
    exit = False
    while not exit:
        while not connect4.finished:
            connect4.nextMove()
        
        connect4.checkBoard()
        connect4.printState()
        
        #Add tie counter
        # if connect4.winner == None:
        #     win_counts[2] += 1
        
        #Add win to player 1
        # elif connect4.winner == player1:
        #     win_counts[0] += 1

        #Add win to player 2
        # elif connect4.winner == player2:
        #     win_counts[1] += 1
        
        # printStats(player1, player2, win_counts)
        
        while True:
            play_again = str(raw_input("Would you like to play again? "))
            
            if play_again.lower().startswith('y'): 
                connect4 = Connect4(newgame=False)
                connect4.printState()
                break
            elif play_again.lower().startswith('n'):
                print("See you in 4")
                exit = True
                break
            else:
                print("Invalid, please try again"),
        
# def printStats(player1, player2, win_counts):
#     print("{0}: {1} wins, {2}: {3} wins, {4} ties".format(player1.name,
#         win_counts[0], player2.name, win_counts[1], win_counts[2]))
        
if __name__ == "__main__":
    main()
