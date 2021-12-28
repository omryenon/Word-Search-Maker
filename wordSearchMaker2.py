# ===============================================================================
#  Word Search Constructor
# ===============================================================================
import sys
import  random
import copy

# ============================================================================
# get_arg() returns command line arguments.
# ============================================================================
def get_arg(index, default=None):
    '''Returns the command-line argument, or the default if not provided'''
    return sys.argv[index] if len(sys.argv) > index else default


# --------------------------------------------------------------------------------

class Grid:

    # ----------------------------------------------------------------------------
    # Grid:
    # A NUM_ROWS x NUM_COLS grid of characters
    # ----------------------------------------------------------------------------

    def __init__(self, nRows, nCols):
        self.NUM_ROWS = nRows
        self.NUM_COLS = nCols
        self.grid = [[" " for cols in range(nCols)] for rows in range(nRows)]

    def __getitem__(self, index):
        return self.grid[index]

    def __str__(self):
        # ========================================================================
        # Prints Puzzle
        # ========================================================================
        out = "+" + "---+" * self.NUM_ROWS + "\n"
        for i in range(self.NUM_ROWS):
            for j in range(self.NUM_COLS):
                out += "| " + self.grid[i][j] + " "
            out += "|" + "\n"
            out += "+" + "---+" * self.NUM_COLS + "\n"
        return out


# --------------------------------------------------------------------------------




class State:
    # ----------------------------------------------------------------------------
    # State:
    # represents the current state of the grid , and the word's bank
    # ----------------------------------------------------------------------------
    def __init__(self, grid, words):
        self.GRID = grid
        self.WORDS = words
        self.state = [grid, words]


    def __str__(self):
        out = "The Grid:\n"
        out += Grid.__str__(self.GRID)
        out += "Words left:"
        for i in range(len(self.WORDS)):
            out += self.WORDS[i]
            out += ", "
        return out

class Rule:
    # ----------------------------------------------------------------------------
    # Rule:
    # represents the location and direction of the word
    # ----------------------------------------------------------------------------
    def __init__(self, word, row, col, dh, dv):
        self.word = word
        self.row = row
        self.col = col
        self.dh = dh
        self.dv = dv
        self.rule = [word, row, col, dh, dv]

    def __str__(self):
        print(f' placed the word: "{self.word}" at: ({self.row}, {self.col}) , direction: ({self.dh}, {self.dv})')

    def applyRule(self,state):
        # creating new list without the word which we gonna place

        newWords = []
        for i in range(len(state.WORDS)):
            if state.WORDS[i] != self.word:
                newWords.append(state.WORDS[i])
        # deep copy of the grid
        newRows = state.GRID.NUM_ROWS
        newCols = state.GRID.NUM_COLS
        newGrid = Grid(newRows, newCols)
        for n in range(newRows):
            for m in range(newCols):
                newGrid[n][m] = state.GRID[n][m]
        # placing the current word in the grid
        currRow = self.row
        currCol = self.col
        for j in range(len(self.word)):
            newGrid[currRow][currCol] = self.word[j]
            currRow += self.dv
            currCol += self.dh
        # creating the new state
        newState = State(newGrid , newWords)
        return newState

    def precondition(self, state):
        # checking if writing the word on the gris is "out of bounds"
        if self.row + (self.dv * len(self.word)) < 0 :
            return False
        elif self.row + (self.dv * len(self.word)) > state.GRID.NUM_ROWS :
            return False
        elif self.col + (self.dh * len(self.word)) < 0 :
            return False
        elif self.col + (self.dh * len(self.word)) > state.GRID.NUM_COLS :
            return False
        else:
            # checking if writing the word on the grid is "overlap another word"
            currRow = self.row
            currCol = self.col
            for j in range(len(self.word) ):
                if(state.GRID[currRow][currCol] != " ") :
                    if(state.GRID[currRow][currCol]!= self.word[j]):
                        return False
                currRow += self.dv
                currCol += self.dh
        return True

# Global variables:
depthBound=0
verbose = False
failCounter=0
backtrackCalls=0
finalStateList=[]

def allCandidates(word, state):
    rulesList=[]
    for p in range(state.GRID.NUM_ROWS):
        for q in range(state.GRID.NUM_COLS):
            currRule1 = Rule(word, p, q, 0,1)
            if currRule1.precondition(state):
                rulesList.append(currRule1)
            currRule2 = Rule(word, p, q, 0,-1)
            if currRule2.precondition(state):
                rulesList.append(currRule2)
            currRule3 = Rule(word, p, q, 1,0)
            if currRule3.precondition(state):
                rulesList.append(currRule3)
            currRule4 = Rule(word, p, q, -1,0)
            if currRule4.precondition(state):
                rulesList.append(currRule4)
            currRule5 = Rule(word, p, q, 1,1)
            if currRule5.precondition(state):
                rulesList.append(currRule5)
            currRule6 = Rule(word, p, q, -1,-1)
            if currRule6.precondition(state):
                rulesList.append(currRule6)
            currRule7 = Rule(word, p, q, -1,1)
            if currRule7.precondition(state):
                rulesList.append(currRule7)
            currRule8 = Rule(word, p, q, 1,-1)
            if currRule8.precondition(state):
                rulesList.append(currRule8)
    return rulesList

def goal(state):
    if len(state.WORDS)==0:
        return True
    else:
        return False

# def flailWildly(state):
#     currState=state
#     while(True):
#         if goal(currState):
#             break
#         else:
#             CurrList = allCandidates(currState.WORDS[0], currState)
#             if(len(CurrList) > 0):
#                 x= random.randint(0,len(CurrList) -1)
#                 if CurrList[x].precondition(currState):
#                     CurrList[x].__str__()
#                     print(currState.__str__())
#                     currState = CurrList[x].applyRule(currState)
#
#                 else:
#                     break
#             else:
#                 print("Can't Place More Words!")
#                 break
#     print(currState.GRID)
#     print("ramaining words:")
#     print(currState.WORDS)

def backtrack(stateList):
    global backtrackCalls
    global failCounter
    global finalStateList
    currState = stateList[0]
    restList = stateList[1:]
    if goal(currState):
        return None
    ruleSet = allCandidates(currState.WORDS[0], currState)
    if (currState in restList):
        if verbose:
            print("FAILED-1")
            print("a cycle has occurred")
        failCounter+=1
        return "FAILED-1"
    elif len(ruleSet)==0:
        if verbose:
            print("FAILED-2")
            print("dead end - No solution possible from here")
        failCounter += 1
        return "FAILED-2"
    elif len(stateList) > depthBound:
        if verbose:
            print("FAILED-3")
            print("Passed the depth bound")
        failCounter += 1
        return "FAILED-3"
    elif ruleSet == None:
        if verbose:
            print("FAILED-4")
            print("There are not any possible moves")
        failCounter += 1
        return "FAILED-4"
    else:
        for r in ruleSet:
            # if r.precondition(currState):
            if verbose:
                print("Rule:")
                r.__str__()
            newState= r.applyRule(currState)
            if verbose:
                print("State:")
                print(newState.__str__())
            newStateList = [newState] + stateList
            backtrackCalls +=1
            path = backtrack(newStateList)
            if path and len(path) >0 and path[0] != "F" and path!=None :
                return path + [r]
            elif path==None :
                finalStateList = newStateList
                print("Goal achieved")
                path=[r]
                return path
        if verbose:
            print("FAILED-5")
            print("Nothing worked")
        failCounter += 1
        return "FAILED-5"



        

    






# --------------------------------------------------------------------------------
#  MAIN PROGRAM
# --------------------------------------------------------------------------------

if __name__ == '__main__':
    # ============================================================================
    # Read input from command line:
    #   python3 <this program>.py  NUM_ROWS NUM_COLS filename
    # where NUM_ROWS and NUM_COLS give the size of the grid to be filled,
    # and filename is a file of words to place in the grid, one word per line.
    # ============================================================================
    # Sample:
    #   python3 <this program>.py  12 12 wordfile1.txt
    # where wordfile1.txt contains these words on separate lines:
    #   ADMISSIBLE AGENT BACKTRACK CANNIBAL   DEADEND  GLOBAL   GRAPHSEARCH
    #   HEURISTIC  LISP  LOCAL     MISSIONARY OPTIMUM  RATIONAL SEARCH  SYMMETRY
    # ============================================================================

    NUM_ROWS = int(get_arg(1))
    NUM_COLS = int(get_arg(2))

    filename = get_arg(3)
    if get_arg(4)!=None:
        if get_arg(4)=="verbose":
            verbose = True
    with open(filename, 'r') as infile:
        theWords = [line.strip() for line in infile]

    # ============================================================================
    # Demonstration code for the Grid class:
    # Shows grid initialization, printing, and assignment to grid cells.
    # ============================================================================
    depthBound =len(theWords)
    grid = Grid(NUM_ROWS, NUM_COLS)
    initstate = State(Grid(NUM_ROWS, NUM_COLS), theWords)
    # making the initial statelist and calls
    stateList = [initstate]
    backtrackCalls+=1
    finalPath=backtrack(stateList)
    if finalPath[0] == "F":
        print(finalPath)
    else:
        print("---------Rules-----------------")
        finalPath.reverse()
        for r in finalPath:
            r.__str__()

        print("---------States-----------------")
        finalStateList.reverse()
        for s in finalStateList:
            print(s.__str__())

    print("Number of Failures:")
    print(failCounter)
    print("Number of backtrack calls:")
    print(backtrackCalls)





