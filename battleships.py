#A battleships game for one player, to be played via a terminal.
#The computer places ships randomly on the board.
#Your goal is to sink the computer's battleships in the smallest number of steps.

#Tested with Python v3.6.0.



from random import randint

#If changing these constants, ensure it is possible for the number of SHIPS
#chosen to fit within the board of chosen WIDTH and HEIGHT, given that ships
#occupy one tile only, and cannot touch each other horizontally or vertically.
WIDTH = 4   
HEIGHT = 3 
SHIPS = 3
EMPTY = "."
HIT = "X"
MISS = "O"




#-------------------------------------------------------------------------#
#  FUNCTIONS                                                              #
#-------------------------------------------------------------------------#



# Continues to ask for user input until an integer is entered.
# INPUT:  prompt (string)
# RETURN: integer
def getInteger( prompt ):
    while True:
        try:
            num = int( input( prompt ) )
        except ValueError:
            continue
        return num

        
        
# Asks the user for input, and converts this to a string with any
# leading and trailing blank spaces removed.
# INPUT:  prompt (string)
# RETURN: stripped string
def getString( prompt ):
    line = input( prompt )
    return line.strip()

    
    
# Gets a valid user input firing column for board of given WIDTH.
# Note that columns are displayed as letters to the player.
# USES:   getString()
# INPUT:  None
# RETURN: user input column (string)
def getCol():
    while True:
        col = getString( "Enter firing column: " )
        if len(col) != 1 or col < "A" or col > chr( (WIDTH-1) + ord("A") ):
            continue
        return col

        
        
# Gets a valid user input firing row for board of given HEIGHT.
# Note that rows are displayed as numbers to the player.
# USES:   getInteger()
# INPUT:  None
# RETURN: user input row (integer)
def getRow():
    while True:
        row = getInteger( "Enter firing row: " )
        if row == 0 or row > HEIGHT:
            continue
        return row

        
        
# Gets a valid user input coordinate pair, and converts the row and
# column coordinate to their coresponding list element numbers.
# USES:   getCol(), getRow()
# INPUT:  visible board (list)
# RETURN: firing row (integer), firing column (integer)
def getCoords( board ):
    while True:
        col = getCol()
        row = getRow()
        firecol = ord(col) - ord("A")
        firerow = row - 1
        if not board[firerow][firecol] == EMPTY:
            print( "This space has already been tried." )
            continue
        return firerow, firecol


        
# For given firing coordinate list element numbers, updates the visible board
# and prints text to the terminal to reflect whether a ship has been hit or not.
# INPUT:  visible board (list), ship location board (list),
#         firing row (integer), firing column (integer)
# RETURN: None
def updateBoard(board, shipboard, firerow, firecol):
    if shipboard[firerow][firecol] == True:
        board[firerow][firecol] = HIT
        print( "You sunk my battleship!" )
    else:
        board[firerow][firecol] = MISS
        print( "Splash..." )     


        
# Prints the board visible to the player.
# INPUT:  visible board (list)
# RETURN: None
def displayBoard( board ):
    print( "  ", end="" )
    for col in range(WIDTH):   
        print( " " + chr(ord("A")+col), end="" )
    print()
    for row in range(HEIGHT):
        print( "{:>2}".format(row+1), end="" )
        for col in range(WIDTH):
            print( " " + board[row][col][0], end="" )
        print()

        
        
# To be called at the beginning of the game only. Places the ships randomly
# on the invisible shipboard such that they do not touch horizontally or vertically.
# Ships are 1 tile long.
# INPUT:  ship location board (list)
# RETURN: None 
def placeShips( shipboard ):
    for i in range(SHIPS):
        while True:
            x = randint(0, HEIGHT-1)
            y = randint(0, WIDTH-1)
            if shipboard[x][y] == True:
                continue
                
            #Ships cannot touch horizontally or vertically:
            if x > 0 and shipboard[x-1][y] == True:
                continue
            if x < HEIGHT-1 and shipboard[x+1][y] == True:
                continue
            if y > 0 and shipboard[x][y-1] == True:
                continue
            if y < WIDTH-1 and shipboard[x][y+1] == True:
                continue
                
            shipboard[x][y] = True
            break

            
            
# To be called at the end of each game loop.
# Determines from the visible board if the player has won.
# INPUT:  visible board (list)
# RETURN: 1 if winner, 0 if not winner
def isWinner( board ):
    sunkcount = 0
    for row in board:
        for tile in row:
            if tile == HIT:
                sunkcount += 1
    if sunkcount == SHIPS:
        return 1
    return 0
    
    
    


#-------------------------------------------------------------------------#
#  MAIN PROGRAM                                                           #
#-------------------------------------------------------------------------#



print( "Welcome to Battleships!" )
print()

#Construct boards:
board = [] #visible to player
shipboard = [] #invisible to player (keeps track of ship locations)
for row in range(HEIGHT):
    board.append(WIDTH * [EMPTY])
    shipboard.append(WIDTH * [False])
   
#Initialise boards:   
placeShips(shipboard)
displayBoard(board)

#Game loop:
turns = 0
while True:
    firerow, firecol = getCoords( board )
    updateBoard( board, shipboard, firerow, firecol )
    print()
    displayBoard( board )
    print()
    turns += 1
    if isWinner( board ):
        print( "You sunk every battleship in", turns, "turns!" )
        break

        
        
        
        