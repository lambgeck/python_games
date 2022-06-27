# Reversegam: a clone of Othello/Reversi.
import random
import sys
WIDTH = 8  # Board is 8 spaces wide.
HEIGHT = 8  # Board is 8 spaces tall.

def drawBoard(board):
    # Print the board passed to this function. Return None.
    print('  12345678')
    print(' +--------+')
    for y in range(HEIGHT):
        print(f'{y+1}|', end='')
        for x in range(WIDTH):
            print(board[x][y], end='')
        print(f'|{y+1}')
    print(' +--------+')
    print('  12345678')

def getNewBoard():
    # Creates a brand-new, blank board data structure.
    board = []
    for i in range(WIDTH):
        board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
    return board

def isValidMove(board, tile, x_start, y_start):
    # Returns False if the player's move on space x_start, y_start is invalid.
    # If it is a valid move, return a list of spaces that would become the player's if they made a move here.
    if board[x_start][y_start] != ' ' or not isOnBoard(x_start, y_start):
        return False
    if tile == 'X':
        other_tile = 'O'
    else:
        other_tile = 'X'
    tiles_to_flip = []

    for x_direction, y_direction in [[0, 1], [1, 1], [1, 0], [1, -1],
                                     [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = x_start, y_start
        x += x_direction  # First step in the x direction
        y += y_direction  # First step in the y direction
        while isOnBoard(x, y) and board[x][y] == other_tile:
            # Keep moving in this x and y direction.
            x += x_direction
            y += y_direction

            if isOnBoard(x,y) and board[x][y] == tile:
                ''' There are pieces to flip over. Go in the reverse
                    direction until we reach the original space, nothing
                    all the tiles along the way.'''
                while True:
                    x-= x_direction
                    y-= y_direction
                    if x == x_start and y == y_start:
                        break
                    tiles_to_flip.append([x, y])

    if len(tiles_to_flip) == 0:  # If no tiles were flipped, this is not a valid move.
        return False
    return tiles_to_flip

def isOnBoard(x, y):
    # Return True if the coordinates are located on the board.
    return x >= 0 and x <= WIDTH -1 and y >= 0 and y <= HEIGHT -1

def getBoardWithValidMoves(board, tile):
    # Return a new board with periods marking the valid moves the player can make.
    board_copy = getBoardCopy(board)

    for x, y in getValidMoves(board_copy, tile):
        board_copy[x][y] = '.'
    return board_copy

def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    valid_moves = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if isValidMove(board, tile, x, y) != False:
                valid_moves.append([x, y])
    return valid_moves

def getScoreOfBoard(board):
    '''Determine the score by counting the tiles.
    Return a dictionary with keys 'X' and 'O'.'''
    x_score = 0
    o_score = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[x][y] == 'X':
                x_score += 1
            if board[x][y] == 'O':
                o_score += 1
    return {'X': x_score, 'O': o_score}

def enterPlayerTile():
    '''Let the player enter which tile they want to be.
    Return a list with the player's tile as the first item
    and the computer's tile as the second item.'''
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()

    # The first element in the list is the player's tile.
    # The second element is the computer's tile.
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def whoGoesFirst():
    # Randomly choose who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def makeMove(board, tile, x_start, y_start):
    ''' Place the tile on the board at x_start, y_start
    and flip any of the opponent's pieces.
    Return False if this is an invalid move; True if it is valid.'''
    tiles_to_flip = isValidMove(board, tile, x_start, y_start)
    if tiles_to_flip == False:
        return False

    board[x_start][y_start] = tile
    for x, y in tiles_to_flip:
        board[x][y] = tile
    return True

def getBoardCopy(board):
    # Make a duplicate of the board list and return it.
    board_copy = getNewBoard()

    for x in range(WIDTH):
        for y in range(HEIGHT):
            board_copy[x][y] = board[x][y]
    return board_copy

def isOnCorner(x, y):
    # Return True if the position is in one of the four corners.
    return (x == 0 or x == WIDTH -1) and (y == 0 or y == HEIGHT -1)

def getPlayerMove(board, player_tile):
    ''' Let the player enter their move.
    Return the move as [x, y], or return the strings 'hints' or 'quit'.'''
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()

    while True:
        print('Enter your move, "quit" to end the game, or "hints" to toggle hints.')
        move = input().lower()
        if move == 'quit' or move == 'hints':
            return move

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, player_tile, x, y) == False:
                continue
            else:
                break
        else:
            print('That is not a valid move. Enter the column (1-8) and then the row(1-8).')
            print('For example, 81 will move on the top-right corner.')
    return [x, y]

def getComputerMove(board, computer_tile):
    ''' Given a board and the computer's tile, determine where to
    move and return that move as an [x,y] list.'''
    possible_moves = getValidMoves(board, computer_tile)
    random.shuffle(possible_moves)  # Randomize the order of the moves.

    # Always go for the corner if available.
    for x, y in possible_moves:
        if isOnCorner(x, y):
            return [x,y]

    # Find the highest-scoring move possible.
    best_score = -1
    for x, y in possible_moves:
        board_copy = getBoardCopy(board)
        makeMove(board_copy, computer_tile, x, y)
        score = getScoreOfBoard(board_copy)[computer_tile]
        if score > best_score:
            best_move = [x, y]
            best_score = score
        return best_move

def printScore(board, player_tile, computer_tile):
    scores = getScoreOfBoard(board)
    print(f'You: {scores[player_tile]} pts. | Computer: {scores[computer_tile]} pts.')

def playGame(player_tile, computer_tile):
    show_hints = False
    turn = whoGoesFirst()
    print(f'The {turn} will go first.')

    # Clear the board and place starting pieces.
    board = getNewBoard()
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'

    while True:
        player_valid_moves = getValidMoves(board, player_tile)
        computer_valid_moves = getValidMoves(board, computer_tile)
        # Check for a stalemate.
        if player_valid_moves == [] and computer_valid_moves == []:
            return board  # No one can move, so end the game.

        elif turn == 'player':  # Player's turn
            if player_valid_moves != []:
                if show_hints:
                    valid_moves_board = getBoardWithValidMoves(board, player_tile)
                    drawBoard(valid_moves_board)
                else:
                    drawBoard(board)
                printScore(board, player_tile, computer_tile)

                move = getPlayerMove(board, player_tile)
                if move == 'quit':
                    print('Thanks for playing!')
                    sys.exit()  # Terminates the program.
                elif move == 'hints':
                    show_hints = not show_hints
                    continue
                else:
                    makeMove(board, player_tile, move[0], move[1])
            turn = 'computer'

        elif turn == 'computer':  # Computer's turn
            if computer_valid_moves != []:
                drawBoard(board)
                printScore(board, player_tile, computer_tile)

                input('Press Enter to see the computer\'s move.')
                move = getComputerMove(board, computer_tile)
                makeMove(board, computer_tile, move[0], move[1])
            turn = 'player'

# Start the game loop.
print('Welcome to Reversegam!')
player_tile, computer_tile = enterPlayerTile()
while True:
    final_board = playGame(player_tile, computer_tile)

    # Display the final score.
    drawBoard(final_board)
    scores = getScoreOfBoard(final_board)
    print('X scored %s points. O scored %s points.' % (scores['X'], scores['O']))
    if scores[player_tile] > scores[computer_tile]:
        print(f'You beat the computer by {scores[player_tile] - scores[computer_tile]} points! Congratulations!')
    elif scores[player_tile] < scores[computer_tile]:
        print(f'You lost :( The computer beat you by {scores[computer_tile] - scores[player_tile]}.')
    else:
        print('The game was a tie!')

    print('Do you want to play again? (yes or no)')
    if not input().lower().startswith('y'):
        break


