# Word-Search-Maker

In this game there is a bank of words and a grid of MxN.
The goal: place all the words in the grid. 

# wordSearchMaker
The algorithm takes one word at a time from the bank (in order), checks all the options for its location, chooses a location at random and places the word in it. The game ends when all the words have been placed or when the next word cannot be placed.

# wordSearchMaker2
This is an improved version of wordSearchMaker.
The algorithm checks if the goal is achieved, or any possible fail that prevents us continue keep searching for a solution in a specific branch. Otherwise, continues do deeper at the search tree and update 3 global variables each iteration.

# Read input from command line:
    #   python3 <this program>.py  NUM_ROWS NUM_COLS filename
    #   where <this program> can be either wordSearchMaker or wordSearchMaker2,
    #   NUM_ROWS and NUM_COLS give the size of the grid to be filled,
    #   and filename is a file of words to place in the grid, one word per line.

 A documentation with Description and several Outputs is attached
