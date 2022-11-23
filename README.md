# AtomicObject---Othello
This was project was aimed at creating an Othello player using SDKs from Atomic Object

## Run The Project
1. Open the Othello_Game_Server directory in Command Line or Terminal.
2. To start the Othello server, type: `java -jar othello.jar --p1-type remote --p2-type random --wait-for-ui`
3. Using a new terminal, switch to the AtomicObject---Othello folder
4. Type `python client.py` to start the AI player

## client.py
This is my attempt at creating an Othello player AI. The AI is searches among the pieces it has on the board, and attempts to find the longest line of 
opponent pieces to convert into its own pieces. The AI is weighted to attain any of the four corners of the board.
