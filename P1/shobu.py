import numpy
import signal
import sys
import time
import timeit
import random

def signal_handler(sig, frame):
    print('\n\nExiting...')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


# =============================================================================
#  CONSTANTS
# =============================================================================

# white player homeboard (cima); has one black board and one white board
WHITE_HB = 0
# black player homeboard (baixo); has one black board and one white board
BLACK_HB = 1
BLACK_BOARD = 0  # black colored boards (left side boards)
WHITE_BOARD = 1  # white colored boards (right side boards)


class Board:
    def __init__(self):

        #Parameters for evaluation function
        self.points_per_piece = 100
        self.points_per_extra_piece = [100,200,300]
        self.points_per_extra_piece_turn = [40,30,20,10]
        
        # data structure
        self.boards = [[[['W', 'W', 'W', 'W'],
                         [' ', ' ', ' ', ' '],
                         [' ', ' ', ' ', ' '],
                         ['B', 'B', 'B', 'B']],

                        [['W', 'W', 'W', 'W'],
                         [' ', ' ', ' ', ' '],
                         [' ', ' ', ' ', ' '],
                         ['B', 'B', 'B', 'B']]],

                       [[['W', 'W', 'W', 'W'],
                         [' ', ' ', ' ', ' '],
                         [' ', ' ', ' ', ' '],
                         ['B', 'B', 'B', 'B']],

                        [['W', 'W', 'W', 'W'],
                         [' ', ' ', ' ', ' '],
                         [' ', ' ', ' ', ' '],
                         ['B', 'B', 'B', 'B']]]]
        
                               
    def displayHomeboard(self, color, color_string, row_number):

        print("   _______________________  |  _______________________ ")

        for row in range(4):
            print("  |     |     |     |     | | |     |     |     |     |")
            print(row_number, end=" ")  # row label

            for black_cell in range(4):  # print row from black board
                print("|  " + self.boards[color][BLACK_BOARD]
                      [row][black_cell] + "  ", end="")
            print("| | ", end="")
            for white_cell in range(4):  # print row from white board
                print("|  " + self.boards[color][WHITE_BOARD]
                      [row][white_cell] + "  ", end="")

            print("|\n  |_____|_____|_____|_____| | |_____|_____|_____|_____|", end="")
            if(row == 1):
                print("   " + color_string + "'s Homeboards", end="")
            print("")

            row_number += 1
        
        
    # displays board in a user friendly format
    def display(self):
        print("\n         Black Boards               White Boards      ")
        print("\n     A     B     C     D    |    E     F     G     H")
        self.displayHomeboard(WHITE_HB, "White", 1)
        print(" ___________________________|__________________________")
        self.displayHomeboard(BLACK_HB, "Black", 5)
    
    
    # returns the number of white and black pieces on each board
    def countNumPieces(self):
        score_num_pieces = []
        for homeboard in range(2):
            for board in range(2):
                num_black = numpy.count_nonzero(self.boards[homeboard][board] == "B")
                num_white = numpy.count_nonzero(self.boards[homeboard][board] == "W")
                score_num_pieces.append([num_white, num_black])
        return score_num_pieces
    
    
    # receives result from countNumPieces() and associates a score for each board, based on the difference of the number of pieces, using the hyperparemeters defined in the class constructor
    def calcDiffNumPieces(self, boards_num_pieces, player):
        
        individual_board_scores = []
        for board_num_pieces in boards_num_pieces:
            if(board_num_pieces[0] == 0): # 0 white pieces, black won
                score = -100000000
            elif(board_num_pieces[1] == 0): # 0 black pieces, white won
                score = 100000000
            else:
                # +/- points_per_piece
                score = (board_num_pieces[0] - board_num_pieces[1])*self.points_per_piece 
                
                # value white base on how many black pieces left
                if(board_num_pieces[1] == 1): # 1 black piece left
                    score += self.points_per_extra_piece[0]
                elif(board_num_pieces[1] == 2): # 2 black piece left
                    score += self.points_per_extra_piece[1]          
                elif(board_num_pieces[1] == 3): # 3 black piece left
                    score += self.points_per_extra_piece[2]
                
                # value black base on how many white pieces left
                if(board_num_pieces[0] == 1): # 1 white piece left
                    score -= self.points_per_extra_piece[0]
                elif(board_num_pieces[0] == 2): # 2 white piece left
                    score -= self.points_per_extra_piece[1]
                elif(board_num_pieces[0] == 3): # 3 white piece left
                    score -= self.points_per_extra_piece[2]
                
                # value player's turn
                if(player): # black to move
                    if(board_num_pieces[0] == 1): # 1 pieces left
                        score -= self.points_per_extra_piece_turn[0]
                    elif(board_num_pieces[0] == 2): # 2 piece left
                        score -= self.points_per_extra_piece_turn[1]
                    elif(board_num_pieces[0] == 3): # 3 pieces left
                        score -= self.points_per_extra_piece_turn[2] 
                    else: # 4 piece left
                        score -= self.points_per_extra_piece_turn[3]
                else: # white to move
                    if(board_num_pieces[0] == 1): # 1 pieces left
                        score += self.points_per_extra_piece_turn[0]
                    elif(board_num_pieces[0] == 2): # 2 piece left
                        score += self.points_per_extra_piece_turn[1]
                    elif(board_num_pieces[0] == 3): # 3 pieces left
                        score += self.points_per_extra_piece_turn[2]
                    else: # 4 piece left
                        score += self.points_per_extra_piece_turn[3]
                                             
            individual_board_scores.append(score)
        
        return individual_board_scores

      
    # evaluation function. evaluates each board based on the difference of the number of pieces and returns reduces the scores to a single value 
    def calcPoints(self, player):
              
        boards_num_pieces = self.countNumPieces()

        individual_board_scores = self.calcDiffNumPieces(boards_num_pieces, player)

        final_score = individual_board_scores[0]*abs(individual_board_scores[0]) + individual_board_scores[1]*abs(individual_board_scores[1]) + individual_board_scores[2]*abs(individual_board_scores[2]) + individual_board_scores[3]*abs(individual_board_scores[3]) 
  
        return final_score
        

    # checks if given board hasn't been played (path from given board state to the root)
    def isNotRepeated(self, repeated):
        for board in repeated:
            if(numpy.array_equal(self.boards, board.boards, equal_nan=False)):
                return False
        return True
        
    

class GameLogic:
    def __init__(self):
        self.board = Board()
        self.player = 1  # white=0, black=1
        
        self.boards_history = [] #boards that have already been played, in order to avoid them
        
        self.playerColor = None
        self.difficulty = None # 1.Easy 2.Medium 3.Hard
        self.difficultyWhite = None
        self.difficultyBlack = None
        self.cntComWhiteMove = 0 #number or computer white moves
        self.cntComBlackMove = 0

    # =============================================================================
    #  AUX FUNTIONS
    # =============================================================================

    # 1 - 1 = 0; 1 - 0 = 1
    def switch_01(self, number):
        return 1 - number

    def parseInt(self, x):
        try:
            int_x = int(x)
            return int_x
        except ValueError:
            return None


    # receives user's input in the selection of a passive piece; returns given piece coordinates  
    def parseInput(self, cell_input):

        if(len(cell_input) != 2):
            return None, None, None, None

        row = cell_input[0]
        col = cell_input[1]

        int_row = self.parseInt(row)
        if(int_row is None or int_row < 1 or int_row > 8):
            return None, None, None, None

        if(int_row <= 4):
            player_side = WHITE_HB
        else:
            player_side = BLACK_HB

        row_index = (int_row - 1) % 4

        if(col == 'A' or col == 'a'):
            return player_side, BLACK_BOARD, row_index, 0
        elif(col == 'B' or col == 'b'):
            return player_side, BLACK_BOARD, row_index, 1
        elif(col == 'C' or col == 'c'):
            return player_side, BLACK_BOARD, row_index, 2
        elif(col == 'D' or col == 'd'):
            return player_side, BLACK_BOARD, row_index, 3

        elif(col == 'E' or col == 'e'):
            return player_side, WHITE_BOARD, row_index, 0
        elif(col == 'F' or col == 'f'):
            return player_side, WHITE_BOARD, row_index, 1
        elif(col == 'G' or col == 'g'):
            return player_side, WHITE_BOARD, row_index, 2
        elif(col == 'H' or col == 'h'):
            return player_side, WHITE_BOARD, row_index, 3
        else:
            return None, None, None, None
        
        
    # receives piece board position; returns respective coordinates
    def parseOutput(self, homeboard, color_side, row, col):
        
        row_output = row + 1
        if(homeboard == 1):
            row_output += 4
        col_output = self.colIndexToLetter(color_side, col)
        return str(row_output)+str(col_output)
            
    
    # translates column board position to column coordinate
    def colIndexToLetter(self, color_side, col_index):
        if(color_side == 0):
            if(col_index == 0):
                return 'A'
            elif(col_index == 1):
                return 'B'
            elif(col_index == 2):
                return 'C'
            elif(col_index == 3):
                return 'D'
            else:
                return None
        elif(color_side == 1):
            if(col_index == 0):
                return 'E'
            elif(col_index == 1):
                return 'F'
            elif(col_index == 2):
                return 'G'
            elif(col_index == 3):
                return 'H'
            else:
                return None
        else:
            return None


    # prints arrows, representing a movement offset
    def displayArrow(self, arrow, n_arrows):
        for i in range(n_arrows):
            print(arrow, end="")
        print("")


    # displays given movement offset in an arrow format
    def displayOffset(self, row_offset, col_offset):

        n_arrows = max(abs(row_offset), abs(col_offset))

        if(row_offset < 0):  # up
            if(col_offset < 0):  # left
                self.displayArrow("↖", n_arrows)
            elif(col_offset > 0):  # right
                self.displayArrow("↗", n_arrows)
            else:  # up
                self.displayArrow("↑", n_arrows)
        elif(row_offset > 0):  # down
            if(col_offset < 0):  # left
                self.displayArrow("↙", n_arrows)
            elif(col_offset > 0):  # right
                self.displayArrow("↘", n_arrows)
            else:  # up
                self.displayArrow("↓", n_arrows)
        else:  # sides
            if(col_offset < 0):  # left
                self.displayArrow("←", n_arrows)
            else:  # right
                self.displayArrow("→", n_arrows)


    # =============================================================================
    #  PASSIVE MOVE
    # =============================================================================

    # receives input from user to select desired piece; returns piece board position

    def selectPiece(self, color, piece, other_piece):
        while(True):
            
            print("\n[type HINT for a hint]")
            cell_input = input("Select a " + color + " piece from your homeboard (<row><column>): ")
            
            # if user enters 'HINT', calls minimax with depth 2 to get a hint
            if(str(cell_input).upper() == 'HINT'):
                maximizing = False
                if(color == 'white'):
                    maximizing = True
                best_move = self.minimax(self.board, self.boards_history, 2, 2, -sys.maxsize, sys.maxsize, maximizing, self.player, piece, other_piece)
                
                # displays hint
                self.displayMove(best_move[1], best_move[2], best_move[3], "Hint: ")
            
            else:
                player_side, color_side, row_index, col_index = self.parseInput(cell_input)
    
                if(color_side is None or row_index is None or col_index is None):
                    print("INVALID INPUT")
                    continue
    
                if(player_side != self.player):
                    print("CHOOSE A PIECE FROM ONE OF YOUR HOMEBOARDS")
                else:
                    if((self.player == 0 and self.board.boards[WHITE_HB][color_side][row_index][col_index] == 'W') or
                       (self.player == 1 and self.board.boards[BLACK_HB][color_side][row_index][col_index] == 'B')):
                        return color_side, row_index, col_index
                    else:
                        print("CHOOSE A PIECE OF YOUR COLOR")


    # displays board with an 'x' in the available passive move options; returns options

    def legalPassiveMoves(self, board, homeboard, color_side, row_index, col_index, is_human):

        if(is_human): # for user readibility
            aux_board = Board()
            aux_board.boards = numpy.copy(board.boards)
        options = []

        for i in range(row_index - 2, row_index + 3):  # 2 rows behind, 2 rows ahead
            if(i < 0 or i > 3):
                continue
            for j in range(col_index - 2, col_index + 3):  # 2 cols behind, 2 cols ahead
                if(j < 0 or j > 3):
                    continue

                # skips any cell that doesnt satisfy an * format
                if(((i == row_index - 2 or i == row_index + 2) and (j == col_index - 1 or j == col_index + 1)) or
                   (((i == row_index - 1 or i == row_index + 1) and (j == col_index - 2 or j == col_index + 2)))):
                    continue

                # skips options that need to jump over pieces
                if(i == row_index - 2 or i == row_index + 2 or
                   j == col_index - 2 or j == col_index + 2):
                    middle_i = int((row_index + i)/2)
                    middle_j = int((col_index + j)/2)
                    if(board.boards[homeboard][color_side][middle_i][middle_j] != ' '):
                        continue
                
                # if cell is empty, add board coordinates as an option
                if(board.boards[homeboard][color_side][i][j] == ' '):
                    options.append([i, j])
                    if(is_human): # for user readibility
                        aux_board.boards[homeboard][color_side][i][j] = 'x' 
                    

        if(is_human): # for user readibility
            aux_board.display()

        return options


    # displays passive move options, lets user select desired one; returns desired move offset from piece cell (or 0 if player wants to re-select piece option)
    def passiveMoveOptions(self, options, color_side, row_index, col_index):

        print("\nPassive move options:")
        print("0: re-select piece")
        counter = 1

        if(self.player):  # black player => black homeboard => row in [5,6,7,8]
            board_offset = 5
        else:  # white player => white homeboard => row in [1,2,3,4]
            board_offset = 1

        for option in options:
            print(str(counter)+": " + str(option[0]+board_offset) +
                  str(self.colIndexToLetter(color_side, option[1])))
            counter += 1

        while(True):
            selected_option = input("Select an option (<option_number>):")
            parsed_selected_option = self.parseInt(selected_option)

            if(parsed_selected_option is None or parsed_selected_option < 0 or parsed_selected_option > len(options)):
                print("INVALID INPUT")

            # if option selected, return [row_offset, col_offset]
            elif(parsed_selected_option != 0):
                target_row = options[parsed_selected_option-1][0]
                target_col = options[parsed_selected_option-1][1]
                return [target_row-row_index, target_col-col_index]

            # re-select piece option
            else:
                return None


    # passive move function; returns passive selected piece, the move offset and the color side it was choosen from

    def passiveMove(self, color, piece, other_piece):
        while(True):
            
            self.board.display()

            print("\n> > "+color+" player's turn:")

            print("\n> Passive Move:")

            color_side, row_index, col_index = self.selectPiece(color.lower(),piece, other_piece)

            options = self.legalPassiveMoves(self.board, self.player, color_side, row_index, col_index, True)

            offset = self.passiveMoveOptions(
                options, color_side, row_index, col_index)

            if(offset is not None):
                break

        return offset, color_side, [row_index, col_index]



    # =============================================================================
    #  AGRESSIVE MOVE
    # =============================================================================

    # receives cell board postition and passive move offset, checks if it's possible; returns True/False

    def verifyDirection(self, board, player_side, color_side, row, col, offset, piece, other_piece):

        if(row + offset[0] not in [0, 1, 2, 3] or col + offset[1] not in [0, 1, 2, 3]):
            # print(row + offset[0], col + offset[1])
            return False  # out of board move

        v_dir = 0
        h_dir = 0

        if(offset[0] != 0):
            v_dir = int(offset[0] / abs(offset[0]))
        if(offset[1] != 0):
            h_dir = int(offset[1] / abs(offset[1]))

        n_iter = max(abs(offset[0]), abs(offset[1]))

        pushing = False

        for i in range(1, n_iter + 1):
            if(board.boards[player_side][color_side][row + i*v_dir][col + i*h_dir] == piece):
                return False  # cannot push own piece
            if(board.boards[player_side][color_side][row + i*v_dir][col + i*h_dir] == other_piece):
                pushing = True  # found other color piece to push
            if(pushing):  # pushing a piece. Check that the next cell doesnt have a piece (is empty or out of board)
                # if inside board
                if(row + (i+1)*v_dir in [0, 1, 2, 3] and col + (i+1)*h_dir in [0, 1, 2, 3]):
                    # if not empty
                    if(board.boards[player_side][color_side][row + (i+1)*v_dir][col + (i+1)*h_dir] != " "):
                        return False

        return True


    # receives passive move offset and returns all possible options for the agressive move

    def legalAgressiveMoves(self, board, offset, other_color, piece, other_piece):

        options1 = []
        options2 = []

        for row in range(4):
            for col in range(4):
                if(board.boards[0][other_color][row][col] == piece): 
                    if(self.verifyDirection(board, 0, other_color, row, col, offset, piece, other_piece)): # searches for agressive moves in white homeboard 
                        options1.append([row, col])
                if(board.boards[1][other_color][row][col] == piece):
                    if(self.verifyDirection(board, 1, other_color, row, col, offset, piece, other_piece)): # searches for agressive moves in black homeboard 
                        options2.append([row, col])

        return [options1, options2]


    # gets all legal moves and returns four lists with passive and agressive for a given player

    def getLegalMoves(self, gameboard, repeated, player):

        #start_time = timeit.default_timer()

        moves = []
        
        for homeboard in range(2):
            for board in range(2):
                for row in range(4):
                    for col in range(4):
                        
                        # If black player and black piece on black HB
                        if(player == 1 and gameboard.boards[homeboard][board][row][col] == "B" and homeboard == 1): 
                            passive_moves = self.legalPassiveMoves(gameboard ,homeboard, board, row, col, False) # get passive options
                            for passive_move in passive_moves:
                                offset = [passive_move[0]-row, passive_move[1]-col] # calculate movement offset
                                other_color = self.switch_01(board)
                                agressive_moves = self.legalAgressiveMoves(gameboard, offset, other_color, "B", "W") # for each passive option, get agressive options
                                
                                # agressive moves on white homeboard
                                for agressive_move in agressive_moves[0]:
                                    aux_board = Board()
                                    aux_board.boards = numpy.copy(gameboard.boards)
                                    self.updateBoard([homeboard,board,row,col], [0,other_color,agressive_move[0],agressive_move[1]], offset, "B", "W", aux_board)
                                    if(aux_board.isNotRepeated(repeated)): # if does not result in a repeated board, add as an option
                                        moves.append([[homeboard,board,row,col], [0,other_color,agressive_move[0],agressive_move[1]], offset])
                                
                                # agressive moves on black homeboard
                                for agressive_move in agressive_moves[1]:
                                    aux_board = Board()
                                    aux_board.boards = numpy.copy(gameboard.boards)
                                    self.updateBoard([homeboard,board,row,col], [1,other_color,agressive_move[0],agressive_move[1]], offset, "B", "W", aux_board)
                                    if(aux_board.isNotRepeated(repeated)): # if does not result in a repeated board, add as an option
                                        moves.append([[homeboard,board,row,col], [1,other_color,agressive_move[0],agressive_move[1]], offset])
                        
                        #If white player and white piece on white HB
                        elif(player == 0 and gameboard.boards[homeboard][board][row][col] == "W" and homeboard == 0): 
                            passive_moves = self.legalPassiveMoves(gameboard ,homeboard, board, row, col, False) # get passive options
                            for passive_move in passive_moves:
                                offset = [passive_move[0]-row, passive_move[1]-col] # calculate movement offset
                                other_color = self.switch_01(board)
                                agressive_moves = self.legalAgressiveMoves(gameboard, offset, other_color, "W", "B") # for each passive option, get agressive options
                                
                                # agressive moves on white homeboard
                                for agressive_move in agressive_moves[0]:
                                    aux_board = Board()
                                    aux_board.boards = numpy.copy(gameboard.boards)
                                    self.updateBoard([homeboard,board,row,col], [0,other_color,agressive_move[0],agressive_move[1]], offset, "W", "B", aux_board)
                                    if(aux_board.isNotRepeated(repeated)): # if does not result in a repeated board, add as an option
                                        moves.append([[homeboard,board,row,col], [0,other_color,agressive_move[0],agressive_move[1]], offset])
                                 
                                # agressive moves on black homeboard
                                for agressive_move in agressive_moves[1]:
                                    aux_board = Board()
                                    aux_board.boards = numpy.copy(gameboard.boards)
                                    self.updateBoard([homeboard,board,row,col], [1,other_color,agressive_move[0],agressive_move[1]], offset, "W", "B", aux_board)
                                    if(aux_board.isNotRepeated(repeated)): # if does not result in a repeated board, add as an option
                                        moves.append([[homeboard,board,row,col], [1,other_color,agressive_move[0],agressive_move[1]], offset])


        return moves


    # displays agressive move options and lets player choose one; returns selected piece (or 0 if player wants to re-select passive move)

    def agressiveMoveOptions(self, color_side, options):

        print("\nAgressive move options:")

        if(options == [[], []]):
            print("\nNo valid agressive moves. Please select a new passive move.")
            time.sleep(3)
            return None, None

        print("0: re-select passive move")
        counter = 1
        for option in options[0]:
            print(str(counter)+": " +
                  str(option[0]+1) + str(self.colIndexToLetter(color_side, option[1])))
            counter += 1

        split = counter

        for option in options[1]:
            print(str(counter)+": " +
                  str(option[0]+5) + str(self.colIndexToLetter(color_side, option[1])))
            counter += 1

        while(True):
            selected_option = input("Select an option (<option_number>):")
            parsed_selected_option = self.parseInt(selected_option)

            if(parsed_selected_option is None or parsed_selected_option < 0 or parsed_selected_option > (len(options[0]) + len(options[1]))):
                print("INVALID INPUT")

            # if option selected, return selected cell coords
            elif(parsed_selected_option != 0):
                # if selected option < split, move is in white's homeboards
                if(parsed_selected_option < split):
                    return options[0][parsed_selected_option-1], 0
                else:  # else, move is in black's homeboards
                    return options[1][parsed_selected_option-split], 1

            # re-select passive move
            else:
                return None, None


    # agressive move function; returns agressive selected piece and the color side it was choosen from

    def agressiveMove(self, offset, other_color, piece, other_piece):

        self.board.display()        

        print("\n> Agressive Move:")

        print("\nSelected movement: ", end="")
        self.displayOffset(offset[0], offset[1])

        options = self.legalAgressiveMoves(self.board, offset, other_color, piece, other_piece)

        selected, player_side = self.agressiveMoveOptions(other_color, options)

        if(selected is None):
            return None, None  # re-select passive Move
        else:
            return selected, player_side


    # receives selected passive and agressive pieces, the move offset and the player and enemy player's pieces; returns True if an enemy piece was pushed out of the board, else False


    def updateBoard(self, passive_piece, agressive_piece, offset, piece, other_piece, board):
            
        
        # clear original passive_piece location
        board.boards[passive_piece[0]][passive_piece[1]][passive_piece[2]][passive_piece[3]] = ' '
        # relocate passive_piece
        board.boards[passive_piece[0]][passive_piece[1]][passive_piece[2] + offset[0]][passive_piece[3] + offset[1]] = piece

        # clear original agressive_piece location
        board.boards[agressive_piece[0]][agressive_piece[1]][agressive_piece[2]][agressive_piece[3]] = ' '

        v_dir = 0
        h_dir = 0

        if(offset[0] != 0):
            v_dir = int(offset[0] / abs(offset[0]))
        if(offset[1] != 0):
            h_dir = int(offset[1] / abs(offset[1]))

        n_iter = max(abs(offset[0]), abs(offset[1]))

        pushing = False

        for i in range(1, n_iter + 1):
            if(board.boards[agressive_piece[0]][agressive_piece[1]][agressive_piece[2] + i*v_dir][agressive_piece[3] + i*h_dir] == other_piece):
                pushing = True  # is pushing other color piece

            if(i == n_iter):  # if in last cell of the offset, place the piece
                board.boards[agressive_piece[0]][agressive_piece[1]][agressive_piece[2] + i*v_dir][agressive_piece[3] + i*h_dir] = piece
            else:  # else, clean the path
                board.boards[agressive_piece[0]][agressive_piece[1]][agressive_piece[2] + i*v_dir][agressive_piece[3] + i*h_dir] = ' '

        if(pushing):  # if there's enemy piece to be pushed
            # if destiny location is in board, update it
            if(agressive_piece[2] + offset[0] + v_dir in [0, 1, 2, 3] and agressive_piece[3] + offset[1] + h_dir in [0, 1, 2, 3]):
                board.boards[agressive_piece[0]][agressive_piece[1]][agressive_piece[2] + offset[0] + v_dir][agressive_piece[3] + offset[1] + h_dir] = other_piece
            else:
                return True  # enemy piece was pushed out of board => check for winners

        return False  # no enemy piece was pushed out of the board => no need to check for winners


    # displays given move in a user friendly format

    def displayMove(self, passive_piece, agressive_piece, offset, message):
        passive_output = self.parseOutput(passive_piece[0],passive_piece[1],passive_piece[2],passive_piece[3])
        agressive_output = self.parseOutput(agressive_piece[0],agressive_piece[1],agressive_piece[2],agressive_piece[3])
        
        print("\n"+ message + passive_output + " and " + agressive_output + " with ", end="")
        self.displayOffset(offset[0], offset[1])
       
        
    # makes move for a player 
       
    def playerMove(self, color, piece, other_piece):
        while(True):
            offset, color_side, passive_selected = self.passiveMove(color,piece, other_piece)
    
            other_color = self.switch_01(color_side) # change color_side, since agressive move must be made in opposite color_side
    
            agressive_selected, player_side = self.agressiveMove(offset, other_color, piece, other_piece)
    
            if(agressive_selected is not None and player_side is not None):
                break
            
        self.displayMove([self.player, color_side, passive_selected[0], passive_selected[1]],
                         [player_side, other_color, agressive_selected[0], agressive_selected[1]],
                         offset, "Moved ")
            
        return self.updateBoard([self.player, color_side, passive_selected[0], passive_selected[1]],
                                [player_side, other_color, agressive_selected[0], agressive_selected[1]],
                                offset, piece, other_piece, self.board)


    # makes move for the computer 

    def computerMove(self, color, piece, other_piece):
        
        
        print("\n> > Computer's turn (" +color+ "):")
        
        maximizing = False
        if(color == 'White'):
            maximizing = True
            self.cntComWhiteMove += 1
            if self.difficultyWhite == 0 or self.difficulty == 0: #Super Easy
                legal_moves = self.getLegalMoves(self.board,[],0)
                length = len(legal_moves) - 1
                if length < 0:
                    print ("Black Won, white has no moves")
                    sys.exit(0)
                index = random.randrange(0,length)
                best_move = legal_moves[index]
                return self.updateBoard(best_move[0], best_move[1], best_move[2], piece, other_piece, self.board)
            elif self.difficultyWhite == 1 or self.difficulty == 1: #Easy
                depth = 1
            elif self.difficultyWhite == 2 or self.difficulty == 2: #Medium
                depth = 2
            elif self.difficultyWhite == 3 or self.difficulty == 3: #Hard
                depth = 3
            elif self.difficultyWhite == 4 or self.difficulty == 4: #Dynamic Hard
                depth = 2
                if self.cntComWhiteMove > 5:
                    depth = 3
        else:
            self.cntComBlackMove += 1
            if self.difficultyBlack == 0 or self.difficulty == 0: #Super Easy
                legal_moves = self.getLegalMoves(self.board,[],1)
                length = len(legal_moves) - 1
                if length < 0:
                    print ("White Won, black has no moves")
                    sys.exit(0)
                index = random.randrange(0,length)
                best_move = legal_moves[index]
                return self.updateBoard(best_move[0], best_move[1], best_move[2], piece, other_piece, self.board)
            elif self.difficultyBlack == 1 or self.difficulty == 1: #Easy
                depth = 1
            elif self.difficultyBlack == 2 or self.difficulty == 2: #Medium
                depth = 2
            elif self.difficultyBlack == 3 or self.difficulty == 3: #Hard
                depth = 3
            elif self.difficultyBlack == 4 or self.difficulty == 4: #Dynamic Hard
                depth = 2
                if self.cntComBlackMove > 5:
                    depth = 3
 
        best_move = self.minimax(self.board, self.boards_history, depth, depth, -sys.maxsize, sys.maxsize, maximizing, self.player, piece, other_piece)
        
        self.displayMove(best_move[1], best_move[2], best_move[3], "Moved ")
        
        return self.updateBoard(best_move[1], best_move[2], best_move[3], piece, other_piece, self.board)


    # makes a move for the player or the computer
    
    def makeMove(self, color, piece, other_piece):
        if(self.mode == 1): #PvP         
            return self.playerMove(color, piece, other_piece)
                
        elif(self.mode == 2): # PvC
        
            # Player move               
            if(self.player == self.playerColor):
                return self.playerMove(color, piece, other_piece)  
            else:
                return self.computerMove(color, piece, other_piece)
                

        else: # CvC
            return self.computerMove(color, piece, other_piece)


    # makes a turn for a player/computer, adds resulting board to the game history; returns if any piece was pushed of the board in the turn

    def turn(self):

        if(self.player):
            color = 'Black'
            piece = "B"
            other_piece = "W"
        else:
            color = 'White'
            piece = "W"
            other_piece = "B"

        enemyPushedOff = self.makeMove(color, piece, other_piece)

        aux_board = Board()
        aux_board.boards = numpy.copy(self.board.boards)
        
        self.boards_history.append(aux_board)

        return  enemyPushedOff



    # checks for a winner in a board; if winner, returns the winning color, else false

    def isThereWinnerInBoard(self, i, j):

        whites = 0
        blacks = 0
        for row in range(4):
            for col in range(4):
                if(self.board.boards[i][j][row][col] == 'W'):  # found a white piece
                    whites += 1
                elif(self.board.boards[i][j][row][col] == 'B'):  # found a black piece
                    blacks += 1
                if(whites != 0 and blacks != 0):  # board with both pieces, no winner on this board
                    return False

        # if function reaches here, there is a winner
        if(whites != 0):
            return "WHITE"
        else:
            return "BLACK"


    # checks for a winner in all boards

    def isThereWinner(self):
        for i in range(2):
            for j in range(2):
                winner = self.isThereWinnerInBoard(i, j)
                if(winner):
                    return winner
        return False


    # choose gamemode and difficulty

    def menu(self):
        
        while(True):
            print("\n=====================================================================")
            print("====                                                             ====")
            print("====                           SHOBU                             ====")
            print("====                                                             ====")
            print("=====================================================================")
            print("====                                                             ====")
            print("===                            MENU                               ===")
            print("==                                                                 ==")
            print("=        1. Player VS Player               2.Player VS CPU          =")
            print("=                                                                   =")
            print("=        3. CPU VS CPU                     4. Instructions          =")
            print("==                                                                 ==")
            print("=====================================================================")

            mode = 0
            while(True):
                mode = input("\nChoose an option: ")
                parsed_input = self.parseInt(mode)
                if(not(parsed_input is None or parsed_input < 1 or parsed_input > 4)):
                    break
                print("INVALID INPUT")
                
            if(parsed_input == 4):
                print("\n=====================================================================")
                print("====                 SHOBU INSTRUCTIONS                          ====")
                print("=====================================================================")
                print("\nShobu is a turn based game, where each turn is comprised of two moves: first one Passive move and then one Aggressive move.\n\nThe passive move must be played on one of the player’s two homeboards. The player chooses one of their colour pieces and moves it into any direction inside the board, up two spaces, without pushing or jumping over any piece.\n\nThe aggressive move must be made in the same direction and number of spaces as the passive move, on one of the opposite colour boards as the one chosen in the passive move. Additionally, the aggressive move can push, at most, one piece, of the opponent colour. If a piece is pushed off the board, that piece is removed from the game.\n\nThe game’s objective is to remove all opponent pieces from one board. First one to do so wins the game.")
                print("\nAt any time you can hit Ctrl+C to exit the game. Have fun!")
            else:           
                self.mode = parsed_input
                break
        
        if(self.mode == 2):
            playerColor = 0
            while(True):            
                print("\n   1.White                                          2.Black   ")
                playerColor = input("\nChoose your Color: ")
                parsed_input = self.parseInt(playerColor)
                if(not(parsed_input is None or parsed_input < 1 or parsed_input > 2)):
                    break
                print("INVALID INPUT")
            self.playerColor = parsed_input - 1
            

            difficulty = -1
            while(True):
                print("\n 0.Super Easy     1.Easy         2.Medium          3.Hard         4.Dynamic Hard")
                difficulty = input("\nChoose difficulty for Computer: ")
                parsed_input = self.parseInt(difficulty)
                if(not(parsed_input is None or parsed_input < 0 or parsed_input > 4)):
                    break
                print("INVALID INPUT")
                    
            self.difficulty = parsed_input

        if(self.mode == 3):
            difficultyWhite = -1
            while(True):
                print("\n 0.Super Easy     1.Easy         2.Medium          3.Hard         4.Dynamic Hard")
                difficultyWhite = input("\nChoose difficulty for White: ")
                parsed_input = self.parseInt(difficultyWhite)
                if(not(parsed_input is None or parsed_input < 0 or parsed_input > 4)):
                    break
                    
            self.difficultyWhite = parsed_input

            difficultyBlack = -1
            while(True):
                print("\n 0.Super Easy     1.Easy         2.Medium          3.Hard         4.Dynamic Hard")
                difficultyBlack = input("\nChoose difficulty for White: ")
                parsed_input = self.parseInt(difficultyBlack)
                if(not(parsed_input is None or parsed_input < 0 or parsed_input > 4)):
                    break
                    
            self.difficultyBlack = parsed_input


    # game main function. calls turn function on loop until there's a winner

    def run(self):
        sum=0
        
        while(True):
            
            if(self.mode==3 or (self.mode==2 and self.player != self.playerColor)):
                self.board.display()
            
            start_time = timeit.default_timer()
            
            if(self.turn()):
                winner = self.isThereWinner()
                if(winner):
                    break
            
            self.player = self.switch_01(self.player)
            
            elapsed = timeit.default_timer() - start_time
            print("\n| Elapsed Time on This Turn: ", elapsed)
            sum+= elapsed
            print("\n=====================================================================")
            
        print("\n=====================================================================")
        self.board.display()
        print("\nGAME OVER! WINNER IS: " + winner)
        print("\nTotal Time: ", sum)

    
    # def sortMoves(self, board, repeated, turn, piece, other_piece):       
    #     moves = self.getLegalMoves(board, repeated, turn)
    #     move_scores = []
    #     for move in moves:
    #         updated_board = Board()
    #         updated_board.boards = numpy.copy(board.boards)
    #         self.updateBoard(move[0], move[1], move[2], piece, other_piece, updated_board)
    #         move_score = board.calcPoints(turn)    
    #         move_scores.append([move, move_score])
    #     if turn == 1:
    #         sorted_moves = sorted(move_scores, key= lambda move_score : move_score[1]) #ascending order, for black
    #     else:
    #         sorted_moves = sorted(move_scores, key= lambda move_score : move_score[1], reverse=True)
    #     return sorted_moves


    # minimax function 

    def minimax(self, board, repeated, depth_size, depth, alpha, beta, maximizing, turn, piece, other_piece):
        
        
        if depth == 0:
            return  [board.calcPoints(turn), None, None, None]
        
        moves = self.getLegalMoves(board, repeated, turn)      
        if len(moves) < 0:
            if turn:
                print ("Black Won, white has no moves")
            else:
                print ("White Won, black has no moves")
            sys.exit(0)  
        turn = self.switch_01(turn) # change player pov
        
        # white to play (wants to maximize score)
        if maximizing: 
            best = [-sys.maxsize, None, None, None] 
            for move in moves:
                updated_board = Board()
                updated_board.boards = numpy.copy(board.boards)
                self.updateBoard(move[0], move[1], move[2], piece, other_piece, updated_board)
                repeated.append(updated_board)     
                score = self.minimax(updated_board, repeated, depth_size, depth-1,alpha,beta,False,turn, other_piece, piece)
                repeated.pop()
                if(score[0] > best[0] or (score[0] == best[0] and random.randrange(0,4) == 3)): # score value > best value
                    if(depth == depth_size):
                        best = [score[0], move[0], move[1], move[2]]
                    else:
                        best[0] = score[0]
                alpha = max(alpha,best[0])
                if(alpha >= beta):
                    break    
                
        # black to play (wants to minimize score)
        else: 
            best = [sys.maxsize, None, None, None] 
            for move in moves:
                updated_board = Board()
                updated_board.boards = numpy.copy(board.boards)
                self.updateBoard(move[0], move[1], move[2], piece, other_piece, updated_board)
                repeated.append(updated_board)
                score = self.minimax(updated_board, repeated, depth_size, depth-1,alpha,beta,True,turn, other_piece, piece)
                repeated.pop()
                if(score[0] < best[0] or (score[0] == best[0] and random.randrange(0,4) == 3)): # score value < best value
                    if(depth == depth_size):
                        best = [score[0], move[0], move[1], move[2]]
                    else:
                        best[0] = score[0]
                beta = min(beta,best[0])
                
                if(beta <= alpha):
                    break
                
                    
        return best


def main():
    game = GameLogic()
    game.menu()
    game.run()


main()