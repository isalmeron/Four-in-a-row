# Python Final Project
# Connect Four
#
# Irving Salmeron
# Juan Pablo Meouchi

from connect4 import *

def main():
    
    g = Game()
    g.printState()
    player1 = g.players[0]
    player2 = g.players[1]
    
    win_counts = [0, 0, 0] # [p1 wins, p2 wins, ties]
    
    exit = False
    while not exit:
        while not g.finished:
            g.nextMove()
        
        g.findFours()
        g.printState()
        
        #Add tie counter
        if g.winner == None:
            win_counts[2] += 1
        
        #Add win to player 1
        elif g.winner == player1:
            win_counts[0] += 1

        #Add win to player 2
        elif g.winner == player2:
            win_counts[1] += 1
        
        printStats(player1, player2, win_counts)
        
        while True:
            play_again = str(raw_input("Would you like to play again? "))
            
            if play_again.lower().startswith('y'): 
                g = Game(newgame=False)
                g.printState()
                break
            elif play_again.lower().startswith('n'):
                print("Thanks for playing!")
                exit = True
                break
            else:
                print("I don't understand... "),
        
def printStats(player1, player2, win_counts):
    print("{0}: {1} wins, {2}: {3} wins, {4} ties".format(player1.name,
        win_counts[0], player2.name, win_counts[1], win_counts[2]))
        
if __name__ == "__main__":
    main()
