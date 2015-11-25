# Four-in-a-row
Four in a row game with minimax algorithm and alpha-beta prunning

Classes:

Play: Contains the main function that sets the Connect4 object and the players
Player: Contains the player object that holds the color, name, type of player and the move function which 
in case of being a human just sets the column as the color of player and for computer gets the best move 
by minimax algorithm.
Connect4: Contains the game main objects like the players, the board and its characteristics. Also contains the
methods to determine if game is over, who is the winner, printing the board and checking if a move is valid or not.
Minimax: Gets the best move by minimax algorithm with "alpha-beta" prunning (accustomed), uses a difficulty value as the depth of the tree to build.

HEURISTIC
The heuristic just looks for 4-in a row, 3-in a row and 2-in a row giving the following weights: 10, 5, 1 according
to calculate the best option determined by the depth value.

HOW TO:
python 2.7
:python play.py
:Select player type H:human C:computer
  :Select computer difficulty
:If human type the column number: 1-7
NOTE on the top of the board the last play of the computer is printed to keep track

Documents folder contains:
report.pdf: Report with justification and analysis of the application
The other files are papers used as reference to build the application.
