import os
import numpy as np
import random
import math
import sys
import time
localpath = os.path.dirname(os.path.abspath(__file__))
print(localpath)
sys.path.append(f'{localpath}/libraries')
#print(sys.path)
import pygame
pygame.init()

## Lines 10-66 are for setting up the board, game window (UI) player turn etc.
is_gold_player = True
length = 50
number_of_silvers = 20
number_of_golds = 12
window = pygame.display.set_mode((length*11, length*11))
pygame.display.set_caption("Breakthru")
x_axis = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]

def is_gold_player_func(is_gold_player):
    if is_gold_player:
        player_turn = 1
        i = 1
    else:
        player_turn = -1
        i = -1
    return (player_turn, i)

(player_turn, i) = is_gold_player_func(is_gold_player)

def create_board():
    board = np.array([[0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,1,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,1,0,0,2,2,2,0,0,1,0],
        [0,1,0,2,0,0,0,2,0,1,0],
        [0,1,0,2,0,3,0,2,0,1,0],
        [0,1,0,2,0,0,0,2,0,1,0],
        [0,1,0,0,2,2,2,0,0,1,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,1,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0]])
    return board

board = create_board()

silver_array = np.array([1,3,1,4,1,5,1,6,1,7,3,1,3,9,4,1,4,9,5,1,5,9,6,1,6,9,7,1,7,9,9,3,9,4,9,5,9,6,9,7])
gold_array = np.array([5,5,3,4,3,5,3,6,4,3,4,7,5,3,5,7,6,3,6,7,7,4,7,5,7,6])

## Drawing the board using pygame for the UI
def draw_board_func(length, board):
    for j in range(11):
        for i in range(11):
            if (i+j)%2 == 0:
                colour = (255, 255, 255)
            else:
                colour = (0, 0, 0)
            pygame.draw.rect(window, colour, (i*length, j*length, length, length))
    for t in range(11):
        for s in range(11):
            if board[t][s] == 1:
                pygame.draw.circle(window, (192,192,192), (s*length + 25, t*length + 25), 10)
            elif board[t][s] == 2:
                pygame.draw.circle(window, (255,223,0), (s*length + 25, t*length + 25), 10)
            if board[t][s] == 3:
                pygame.draw.circle(window, (255,0,0), (s*length + 25, t*length + 25), 15)
    pygame.display.update()
    
## Lines 70 - 157 check for winning moves and evaluate states
## Function to check if winning move was made
def winning_move(board):
    winner = 0
    no_winner = 0
    for counter1 in range(11):
        for counter2 in range(11):
            if board[counter1][counter2] == 3:
                if (counter1 == 0 or counter1 == 10 or counter2 == 0 or counter2 == 10):
                    winner = 1
                    return winner
                no_winner = 1
                break
    if no_winner == 0:
        winner = -1
    return winner

## Evaluation function
def evaluate_board(board, i, s_copy, g_copy):
    reward = 0
    ## Score the difference in number of pieces
    reward += i*int(len(s_copy) - len(g_copy) - 14)*100
    ## Checking for gold mothership in elimation zone from silver piece
    for counter1 in range(0,len(s_copy),2):
        if s_copy[counter1 + 1] + 1 < 11 and s_copy[counter1] + 1 < 11:
            if board[s_copy[counter1] + 1][s_copy[counter1 + 1] + 1] == 3:
                reward += i*200
        if s_copy[counter1] - 1 >= 0 and s_copy[counter1 + 1] + 1 < 11:
            if board[s_copy[counter1] - 1][s_copy[counter1 + 1] + 1] == 3:
                reward += i*200
        if s_copy[counter1] - 1 >= 0 and s_copy[counter1 + 1] - 1 >= 0:
            if board[s_copy[counter1] - 1][s_copy[counter1 + 1] - 1] == 3:
                reward += i*200
        if s_copy[counter1] + 1 < 11 and s_copy[counter1 + 1] - 1 >= 0:
            if board[s_copy[counter1] + 1][s_copy[counter1 + 1] - 1] == 3:
                reward += i*200
    ## Check if gold can make a winning move, silver should try block
    check1 = True
    check2 = True
    check3 = True
    check4 = True
    for counter in range(1,10):
        if g_copy[0] + counter < 11:
            if board[g_copy[0] + counter][g_copy[1]] != 0:
                check1 = False
            elif g_copy[0] + counter == 10 and check1 == True:
                reward += -i*200
        if g_copy[0] - counter >= 0:
            if board[g_copy[0] - counter][g_copy[1]] != 0:
                check2 = False
            elif g_copy[0] - counter == 0 and check2 == True:
                reward += -i*200
        if g_copy[1] + counter < 11:
            if board[g_copy[0]][g_copy[1] + counter] != 0:
                check3 = False
            elif g_copy[1] + counter == 10 and check3 == True:
                reward += -i*200
        if g_copy[1] - counter >= 0:
            if board[g_copy[0]][g_copy[1] - counter] != 0:
                check4 = False
            elif g_copy[1] - counter == 10 and check4 == True:
                reward += -i*200
    ## reward protectors of Gold ship - cumulative
    if g_copy[0] + counter < 11:
        if board[g_copy[0] + 2][g_copy[1] + 2] == 2:
            reward += -i*10
    if g_copy[0] - counter >= 0:
        if board[g_copy[0] - 2][g_copy[1] + 2] == 2:
            reward += -i*10
    if g_copy[1] + counter < 11:
        if board[g_copy[0] + 2][g_copy[1] - 2] == 2:
            reward += -i*10
    if g_copy[1] - counter >= 0:
        if board[g_copy[0] - 2][g_copy[1] - 2] == 2:
            reward += -i*10
    ## Award wining move with highest score
    no_winner = 0
    for counter1 in range(11):
        for counter2 in range(11):
            if board[counter1][counter2] == 3:
                if (counter1 == 0 or counter1 == 10 or counter2 == 0 or counter2 == 10):
                    reward += -i*100000
                no_winner = 1
                break
        else:
            continue
        break
    if no_winner == 0:
        reward += i*100000
    return reward

## Lines 161-422 are move functions for AI and human input. Move generation for AI is computed in lines 346-422
## This is the move function for the UI input moves.
def moveFunct(board, positionx, positiony, directionx, directiony, player_turn, i, g_copy, s_copy):
    valid_move = False
    x = positionx
    y = positiony
    elimination = False
    pawn = False
    gold = False
    piece_moved = board[x][y]
    if piece_moved == 3:
        gold = True
    piece_eliminated = board[x + directionx][y + directiony]
    if player_turn == i and (piece_moved == 2 or piece_moved == 3):
        ## Move function for gold piece
        if (directionx == 0 or directiony == 0) and piece_eliminated == 0 and elimination == False:
            board[x + directionx][y + directiony] = board[x][y]
            board[x][y] = 0
            valid_move = True
            pawn = True
            ## Change coordinates of piece moved
            for counter in range(0,len(g_copy),2):
                if g_copy[counter] == x and g_copy[counter + 1] == y:
                    g_copy[counter] = x + directionx
                    g_copy[counter + 1] = y + directiony
        ## Elimination function for gold piece
        else:
            if abs(directionx) == 1 and abs(directiony) == 1 and piece_eliminated == 1 and elimination == False and pawn == False:
                elimination = True
                board[x + directionx][y + directiony] = board[x][y]
                board[x][y] = 0
                valid_move = True
                ## Change coordinates of piece moved
                for counter in range(0,len(g_copy),2):
                    if g_copy[counter] == x and g_copy[counter + 1] == y:
                        g_copy[counter] = x + directionx
                        g_copy[counter + 1] = y + directiony
                        break
                ## Remove piece which was eliminated
                for counter in range(0,len(s_copy),2):
                    if s_copy[counter] == x + directionx and s_copy[counter + 1] == y + directiony:
                        s_copy = np.delete(s_copy, (counter, counter + 1))
                        break
    elif player_turn == -i and piece_moved == 1:
        ## Move function for silver piece
        if (directionx == 0 or directiony == 0) and piece_eliminated == 0 and elimination == False:
            pawn = True
            board[x + directionx][y + directiony] = board[x][y]
            board[x][y] = 0
            valid_move = True
            ## Change coordinates of piece moved
            for counter in range(0,len(s_copy),2):
                if s_copy[counter] == x and s_copy[counter + 1] == y:
                    s_copy[counter] = x + directionx
                    s_copy[counter + 1] = y + directiony
        ## Elimination function for silver piece
        else:
            if abs(directionx) == 1 and abs(directiony) == 1 and piece_eliminated != piece_moved and piece_eliminated != 0 and elimination == False and pawn == False:
                board[x + directionx][y + directiony] = board[x][y]
                board[x][y] = 0
                valid_move = True
                elimination = True
                ## Change coordinates of piece moved
                for counter in range(0,len(s_copy),2):
                    if s_copy[counter] == x and s_copy[counter + 1] == y:
                        s_copy[counter] = x + directionx
                        s_copy[counter + 1] = y + directiony
                        break
                ## Remove piece which was eliminated
                for counter in range(0,len(g_copy),2):
                    if g_copy[counter] == x + directionx and g_copy[counter + 1] == y + directiony:
                        g_copy = np.delete(g_copy, (counter, counter + 1))
                        break
    winner = winning_move(board)
    return valid_move, s_copy, g_copy, winner, elimination, gold

## Move function for elimination move for the AI
def moveFunct_elim(b_copy, positionx, positiony, directionx, directiony, player_turn, i, g_copy, s_copy):
    valid_move = False
    x = positionx
    y = positiony
    piece_moved = b_copy[x][y]
    piece_eliminated = b_copy[x + directionx][y + directiony]
    if player_turn == i and (piece_moved == 2 or piece_moved == 3):
        if abs(directionx) == 1 and abs(directiony) == 1 and piece_eliminated != 2 and piece_eliminated != 3 and piece_eliminated != 0:
            b_copy[x + directionx][y + directiony] = b_copy[x][y]
            b_copy[x][y] = 0
            valid_move = True
            ## Change coordinate of piece moved
            for counter in range(0,len(g_copy),2):
                if g_copy[counter] == x and g_copy[counter + 1] == y:
                    g_copy[counter] = x + directionx
                    g_copy[counter + 1] = y + directiony
                    break
            ## Remove piece which was eliminated
            for counter in range(0,len(s_copy),2):
                if s_copy[counter] == x + directionx and s_copy[counter + 1] == y + directiony:
                    s_copy = np.delete(s_copy, (counter, counter + 1))
                    break
    elif player_turn == -i and piece_moved == 1:
        if abs(directionx) == 1 and abs(directiony) == 1 and piece_eliminated != piece_moved and piece_eliminated != 0:
            b_copy[x + directionx][y + directiony] = b_copy[x][y]
            b_copy[x][y] = 0
            valid_move = True
            ## Change coordinate of piece moved
            for counter in range(0,len(s_copy),2):
                if s_copy[counter] == x and s_copy[counter + 1] == y:
                    s_copy[counter] = x + directionx
                    s_copy[counter + 1] = y + directiony
                    break
            ## Remove piece which was eliminated
            for counter in range(0,len(g_copy),2):
                if g_copy[counter] == x + directionx and g_copy[counter + 1] == y + directiony:
                    g_copy = np.delete(g_copy, (counter, counter + 1))
                    break
    winner = winning_move(b_copy)
    return valid_move, s_copy, g_copy, b_copy, winner

# Move function of pawn or gold ship for AI
def moveFunct_pawn(b_copy, x1, y1, dx1, dy1, x2, y2, dx2, dy2, player_turn, i, g_copy, s_copy):
    valid_move_1 = False
    valid_move_2 = False
    valid_move = False
    g_piece = 0
    piece_moved_1 = b_copy[x1][y1]
    piece_moved_2 = b_copy[x2][y2]
    piece_eliminated_1 = b_copy[x1 + dx1][y1 + dy1]
    piece_eliminated_2 = b_copy[x2 + dx2][y2 + dy2]
    if player_turn == i and piece_moved_1 == 2 and piece_moved_2 == 2:
        if (dx1 == 0 or dy1 == 0) and piece_eliminated_1 == 0:
            b_copy[x1 + dx1][y1 + dy1] = b_copy[x1][y1]
            b_copy[x1][y1] = 0
            valid_move_1 = True
        if (dx2 == 0 or dy2 == 0) and piece_eliminated_2 == 0:
            b_copy[x2 + dx2][y2 + dy2] = b_copy[x2][y2]
            b_copy[x2][y2] = 0
            valid_move_2 = True
            ## Change coordinate of pieces moved
            for counter in range(0,len(g_copy),2):
                if g_copy[counter] == x1 and g_copy[counter + 1] == y1:
                    g_copy[counter] = x1 + dx1
                    g_copy[counter + 1] = y1 + dy1
                if g_copy[counter] == x2 and g_copy[counter + 1] == y2:
                    g_copy[counter] = x2 + dx2
                    g_copy[counter + 1] = y2 + dy2
    ## Only moving gold piece
    elif player_turn == i and (piece_moved_1 == 3 or piece_moved_2 == 3):
        if (dx1 == 0 or dy1 == 0) and piece_eliminated_1 == 0 and piece_moved_1 == 3:
            b_copy[x1 + dx1][y1 + dy1] = b_copy[x1][y1]
            b_copy[x1][y1] = 0
            valid_move_1 = True
            valid_move_2 = True
            g_piece = 1
            ## Change coordinate of mothership moved
            g_copy[0] = x1 + dx1
            g_copy[1] = y1 + dy1
        elif (dx2 == 0 or dy2 == 0) and piece_eliminated_2 == 0 and piece_moved_2 == 3:
            b_copy[x2 + dx2][y2 + dy2] = b_copy[x2][y2]
            b_copy[x2][y2] = 0
            valid_move_2 = True
            valid_move_1 = True
            g_piece = 2
            ## Change coordinate of mothership moved
            g_copy[0] = x2 + dx2
            g_copy[1] = y2 + dy2
    elif player_turn == -i and piece_moved_1 == 1 and piece_moved_2 == 1:
        if (dx1 == 0 or dy1 == 0) and piece_eliminated_1 == 0:
            b_copy[x1 + dx1][y1 + dy1] = b_copy[x1][y1]
            b_copy[x1][y1] = 0
            valid_move_1 = True
        if (dx2 == 0 or dy2 == 0) and piece_eliminated_2 == 0:
            b_copy[x2 + dx2][y2 + dy2] = b_copy[x2][y2]
            b_copy[x2][y2] = 0
            valid_move_2 = True
            ## Change coordinate of piece moved
            for counter in range(0,len(s_copy),2):
                if s_copy[counter] == x1 and s_copy[counter + 1] == y1:
                    s_copy[counter] = x1 + dx1
                    s_copy[counter + 1] = y1 + dy1
                if s_copy[counter] == x2 and s_copy[counter + 1] == y2:
                    s_copy[counter] = x2 + dx2
                    s_copy[counter + 1] = y2 + dy2
    if valid_move_1 is True and valid_move_2 is True:
        valid_move = True
    winner = winning_move(b_copy)
    return valid_move, s_copy, g_copy, b_copy, winner, g_piece

## Produces list of viable elimination moves and pawn/mothership moves
def list_of_viable_moves(b_copy, array_type, g_player):
    c = array_type
    viable_move_array = np.array([])
    viable_elim_array = np.array([])
    ## Searching for possible elimination moves
    for j in range(0,len(c),2):
        if (c[j] + 1) < 11 and (c[j+1] + 1 < 11):
            if b_copy[c[j] + 1][c[j+1] + 1] != 0 and b_copy[c[j] + 1][c[j+1] + 1] != b_copy[c[j]][c[j+1]]:
                if g_player:
                    if b_copy[c[j] + 1][c[j+1] + 1] == 1:
                        viable_elim_array = np.append(viable_elim_array, [c[j], c[j + 1], c[j] + 1, c[j + 1] + 1])
                else: 
                    viable_elim_array = np.append(viable_elim_array, [c[j], c[j + 1], c[j] + 1, c[j + 1] + 1])
        if (c[j] - 1) >= 0 and (c[j+1] + 1 < 11):
            if b_copy[c[j] - 1][c[j+1] + 1] != 0 and b_copy[c[j] - 1][c[j+1] + 1] != b_copy[c[j]][c[j+1]]:
                if g_player:
                    if b_copy[c[j] - 1][c[j+1] + 1] == 1:
                        viable_elim_array = np.append(viable_elim_array, [c[j], c[j + 1], c[j] - 1, c[j + 1] + 1])
                else: 
                    viable_elim_array = np.append(viable_elim_array, [c[j], c[j + 1], c[j] - 1, c[j + 1] + 1])  
        if (c[j] + 1) < 11 and (c[j+1] - 1 >= 0):    
            if b_copy[c[j] + 1][c[j+1] - 1] != 0 and b_copy[c[j] + 1][c[j+1] - 1] != b_copy[c[j]][c[j+1]]:
                if g_player:
                    if b_copy[c[j] + 1][c[j+1] - 1] == 1:
                        viable_elim_array = np.append(viable_elim_array, [c[j], c[j + 1], c[j] + 1, c[j + 1] - 1])
                else: 
                    viable_elim_array = np.append(viable_elim_array, [c[j], c[j + 1], c[j] + 1, c[j + 1] - 1])
        if (c[j] - 1) >= 0 and (c[j+1] - 1 >= 0):
            if b_copy[c[j] - 1][c[j+1] - 1] != 0 and b_copy[c[j] - 1][c[j+1] - 1] != b_copy[c[j]][c[j+1]]:
                if g_player:
                    if b_copy[c[j] - 1][c[j+1] - 1] == 1:
                        viable_elim_array = np.append(viable_elim_array, [c[j], c[j + 1], c[j] - 1, c[j + 1] - 1])
                else: 
                    viable_elim_array = np.append(viable_elim_array, [c[j], c[j + 1], c[j] - 1, c[j + 1] - 1])
    ## Viable non-elimination moves.
    ## Searching eastward
    for j in range(0,len(c),2):      
        for t1 in range(1,10):
            if (t1 + c[j + 1]) < 11:
                if b_copy[c[j]][c[j + 1] + t1] == 0:
                    viable_move_array = np.append(viable_move_array, [c[j], c[j + 1], c[j], c[j + 1] + t1])
                else:
                    break
            else:
                break
    ## Searching westward
    for j in range(0,len(c),2):      
        for t1 in range(1,10):
            if (c[j + 1] - t1) >= 0:
                if b_copy[c[j]][c[j + 1] - t1] == 0:
                    viable_move_array = np.append(viable_move_array, [c[j], c[j + 1], c[j], c[j + 1] - t1])
                else:
                    break
            else: 
                break
    ## Searching southward
    for j in range(0,len(c),2):      
        for t1 in range(1,10):
            if (t1 + c[j]) < 11:
                if b_copy[c[j] + t1][c[j + 1]] == 0:
                    viable_move_array = np.append(viable_move_array, [c[j], c[j + 1], c[j] + t1, c[j + 1]])
                else: 
                    break
            else:
                break
    ## Searching northward
    for j in range(0,len(c),2):      
        for t1 in range(1,10):
            if (c[j] - t1) >= 0:
                if b_copy[c[j] - t1][c[j + 1]] == 0:
                    viable_move_array = np.append(viable_move_array, [c[j], c[j + 1], c[j] - t1, c[j + 1]])
                else:
                    break
            else:
                break
    return viable_elim_array, viable_move_array

##Lines 424-453 contain functions relating to the Transposition table
## Produces our hash table for each piece at each position on the board
hash_table = [[[random.randint(1,2**121 - 1) for i in range(3)]for j in range(11)]for k in range(11)]

## Produces the hash key for the the given state (board)
def hash_key(board):
    h = 0
    for i in range(11):
        for j in range(11):
            if board[i][j] != 0:
                piece = board[i][j] - 1
                h ^= hash_table[i][j][piece]
    return h

## Check if we have already explored this state. If so, return the corresponding best move, score, flag and depth
def TT_find(TT_key, TT):
    if len(TT) != 0:
        for i in range(0, len(TT), 5):
            if TT_key == TT[i]:
                #print("nice")
                return TT[i + 1], TT[i + 2], TT[i + 3], TT[i + 4]
    return 0, 0, 0, -1

## Adding new states into the TT
def TT_update(TT_key, TT, TT_move, TT_score, TT_flag, TT_depth):
    ## TT_flag is 0 for exact value, 1 for lower bound and 2 for upperbound
    ## TT_type represents the type of move made. 0: pawn, 1: elim
    array_add = [TT_key, TT_move, TT_score, TT_flag, TT_depth]
    TT.extend(array_add)
    return TT

## Minimax algorithm containing alpha-beta minimax enahanced with Transition tables, iterative deepening and best first search.
## Lines 457-598
def minimax(board1, s_arr, g_arr, depth, alpha, beta, i, maximizingPlayer, TT, best_move):
    global leafs
    leafs += 1
    old_beta = beta
    old_alpha = alpha
    ## Get hash key for the board and check if we have already seen this board
    TT_key = hash_key(board1)
    TT_move, TT_score, TT_flag, TT_depth = TT_find(TT_key, TT)
    ## TT_flag is 0 for exact value, 1 for lower bound and 2 for upperbound
    ## If state is found and depth of TT search is deeper then return flag values
    if TT_depth >= depth:
        if TT_flag == 0:
            return TT_move, TT_score
        elif TT_flag == 1:
            alpha = max(alpha, TT_score)
        elif TT_flag == 2:
            beta = min(beta, TT_score)
        if alpha >= beta:
            return TT_move, TT_score
    ## Evaluate the state if depth is reached
    if depth == 0: 
        return (None, evaluate_board(board1, i, s_arr, g_arr))
    ## Produce viable moves for the state given
    if i == 1:
        if maximizingPlayer:
            AI_elim, AI_moves = list_of_viable_moves(board1, s_arr, False)
        else:
            p_elim, p_moves = list_of_viable_moves(board1, g_arr, True)
    else:
        if maximizingPlayer:
            AI_elim, AI_moves = list_of_viable_moves(board1, g_arr, True)
        else:
            p_elim, p_moves = list_of_viable_moves(board1, s_arr, False)
    ## Maximizing player
    if maximizingPlayer:
        value = -math.inf
        chosen_move = np.array([])
        ## First do best move from previous iteration in iterative deepening
        if len(best_move) != 2:
            b_copy = board1.copy()
            g_copy = gold_array.copy()
            s_copy = silver_array.copy()
            if len(best_move) == 4:
                valid_move = moveFunct_elim(b_copy, int(best_move[0]), int(best_move[1]), int(best_move[2] - best_move[0]), int(best_move[3] - best_move[1]), player_turn, i, g_copy, s_copy)[0]
                if valid_move:
                    new_score = minimax(b_copy, s_copy, g_copy, depth-1, alpha, beta, i, False, TT, best_move)[1]
                    if new_score > value:
                        value = new_score
                        chosen_move = np.array([best_move[0], best_move[1], best_move[2], best_move[3]])
                    alpha = max(alpha, value)
            else:
                valid_move = moveFunct_pawn(b_copy, int(best_move[0]), int(best_move[1]), int(best_move[2] - best_move[0]), int(best_move[3] - best_move[1]), int(best_move[4]), int(best_move[5]), int(best_move[6] - best_move[4]), int(best_move[7] - best_move[5]), player_turn, i, g_copy, s_copy)[0]
                if valid_move:
                    new_score = minimax(b_copy, s_copy, g_copy, depth-1, alpha, beta, i, False, TT, best_move)[1]
                    if new_score > value:
                        value = new_score
                        chosen_move = np.array([best_move[0], best_move[1], best_move[2], best_move[3], best_move[4], best_move[5], best_move[6], best_move[7]])
                    alpha = max(alpha, value)
        ## Then simulate viable elimination moves
        for move in range(0,len(AI_elim)-4,4):
            b_copy = board1.copy()
            g_copy = gold_array.copy()
            s_copy = silver_array.copy()
            valid_move = moveFunct_elim(b_copy, int(AI_elim[move]), int(AI_elim[move + 1]), int(AI_elim[move + 2] - AI_elim[move]), int(AI_elim[move + 3] - AI_elim[move + 1]), player_turn, i, g_copy, s_copy)[0]
            if valid_move:
                new_score = minimax(b_copy, s_copy, g_copy, depth-1, alpha, beta, i, False, TT, best_move)[1]
                if new_score > value:
                    value = new_score
                    chosen_move = np.array([AI_elim[move], AI_elim[move + 1], AI_elim[move + 2], AI_elim[move + 3]])
                alpha = max(alpha, value)
                ## Pruning criteria
                if alpha >= beta:
                    break
        ## Then simulate viable pawn and mothership moves
        for move in range(0, len(AI_moves) - 8, 4):
            for move2 in range(move + 4, len(AI_moves) - 4, 4):
                if (AI_moves[move] != AI_moves[move2] or AI_moves[move + 1] != AI_moves[move2 + 1]) and (AI_moves[move + 2] !=  AI_moves[move2 + 2] or AI_moves[move + 3] != AI_moves[move2 + 3]):
                    b_copy = board1.copy()
                    g_copy = gold_array.copy()
                    s_copy = silver_array.copy()
                    valid_move = moveFunct_pawn(b_copy, int(AI_moves[move]), int(AI_moves[move + 1]), int(AI_moves[move + 2] - AI_moves[move]), int(AI_moves[move + 3] - AI_moves[move + 1]), int(AI_moves[move2]), int(AI_moves[move2 + 1]), int(AI_moves[move2 + 2] - AI_moves[move2]), int(AI_moves[move2 + 3] - AI_moves[move2 + 1]), player_turn, i, g_copy, s_copy)[0]
                    if valid_move:
                        new_score = minimax(b_copy, s_copy, g_copy, depth-1, alpha, beta, i, False, TT, best_move)[1]
                        if new_score > value:
                            value = new_score
                            chosen_move = np.array([AI_moves[move], AI_moves[move + 1], AI_moves[move + 2], AI_moves[move + 3], AI_moves[move2], AI_moves[move2 + 1], AI_moves[move2 + 2], AI_moves[move2 + 3]])
                        alpha = max(alpha, value)
                        ## Pruning criteria
                        if alpha >= beta:
                            break
            else:
                continue
            break
    ## Minimizing player
    else: 
        value = math.inf
        chosen_move = np.array([])
        ## Simulate viable elimination moves
        for move in range(0,len(p_elim)-4,4):
            b_copy = board1.copy()
            g_copy = gold_array.copy()
            s_copy = silver_array.copy()
            valid_move = moveFunct_elim(b_copy, int(p_elim[move]), int(p_elim[move + 1]), int(p_elim[move + 2] - p_elim[move]), int(p_elim[move + 3] - p_elim[move + 1]), player_turn, i, g_copy, s_copy)[0]
            if valid_move:
                new_score = minimax(b_copy, s_copy, g_copy, depth-1, alpha, beta, i, True, TT, best_move)[1]
                if new_score < value:
                    value = new_score
                    chosen_move = np.array([p_elim[move], p_elim[move + 1], p_elim[move + 2], p_elim[move + 3]])
                beta = min(beta, value)
                ## Pruning criteria
                if beta <= alpha:
                    break
        ## Simulate viable pawn and mothership moves
        for move in range(0, len(p_moves) - 8, 4):
            for move2 in range(move + 4, len(p_moves) - 4, 4):
                if (p_moves[move] != p_moves[move2] or p_moves[move + 1] != p_moves[move2 + 1]) and (p_moves[move + 2] !=  p_moves[move2 + 2] or p_moves[move + 3] != p_moves[move2 + 3]):
                    b_copy = board1.copy()
                    g_copy = gold_array.copy()
                    s_copy = silver_array.copy()
                    valid_move = moveFunct_pawn(b_copy, int(p_moves[move]), int(p_moves[move + 1]), int(p_moves[move + 2] - p_moves[move]), int(p_moves[move + 3] - p_moves[move + 1]), int(p_moves[move2]), int(p_moves[move2 + 1]), int(p_moves[move2 + 2] - p_moves[move2]), int(p_moves[move2 + 3] - p_moves[move2 + 1]), player_turn, i, g_copy, s_copy)[0]
                    if valid_move:
                        new_score = minimax(b_copy, s_copy, g_copy, depth-1, alpha, beta, i, True, TT, best_move)[1]
                        if new_score < value:
                            value = new_score
                            chosen_move = np.array([p_moves[move], p_moves[move + 1], p_moves[move + 2], p_moves[move + 3], p_moves[move2], p_moves[move2 + 1], p_moves[move2 + 2], p_moves[move2 + 3]])
                        beta = min(beta, value)
                        ## Pruning criteria
                        if beta <= alpha:
                            break
            else:
                continue
            break
    ## Storing flag type, state hash-key, best move, score of that move and depth of the search into transition table
    if value <= old_alpha:
        TT_flag = 1
    elif value >= old_beta:
        TT_flag = 2
    else: 
        TT_flag = 0
        #print(TT_key, TT, TT_move, value, TT_flag, depth)
    if TT_depth <= depth:
        TT_move = chosen_move
        TT = TT_update(TT_key, TT, TT_move, value, TT_flag, depth)
    return chosen_move, value

## Lines 602-711 contain the game loop aswell and some initializing
## Initializing variables
running = True
turn = 0
positionx = 0
positiony = 0
directiony = 0
directionx = 0
first_click = True
play_2 = False
TT = []
print("Welcome")
print("Press G if AI is the gold player and S if AI is the silver player")
window.fill((0,0,0))
draw_board_func(length, board)

## Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        ## Deciding which player is which and if gold player skips turn
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                is_gold_player = False
                player_turn, i = is_gold_player_func(is_gold_player)
                print("AI is the gold player.")
            elif event.key == pygame.K_s:
                is_gold_player = True
                player_turn, i = is_gold_player_func(is_gold_player)
                print("AI is now the silver player")
                print("Did the opposition skip their first turn? Press n.")
            if event.key == pygame.K_n:
                player_turn = -1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:   
                ## Human input. Click once on piece to select piece. Second click on location you want to move the piece
                ## If there is no piece where you have first clicked, click again to unselect and then re-click on the piece you want to click on.
                ## If move is illegal, redo your turn
                if player_turn == 1:
                    if first_click:
                        first_click = False
                        (positiony, positionx) = event.pos
                        (positiony, positionx) = (int(positiony/length), int(positionx/length))
                    elif first_click == False:
                        first_click = True
                        (new_position_y, new_position_x) = event.pos
                        (new_position_y, new_position_x) = (int(new_position_y/length), int(new_position_x/length))
                        directionx = new_position_x - positionx
                        directiony = new_position_y - positiony
                        valid_move, silver_array, gold_array, winner, elimination, gold = moveFunct(board, positionx, positiony, directionx, directiony, player_turn, i, gold_array, silver_array)
                        if valid_move:
                            window.fill((0,0,0))
                            draw_board_func(length, board)
                            print(int(11 - positionx), x_axis[positiony], "->", int(11 - new_position_x), x_axis[new_position_y])
                            if play_2 or elimination or gold:
                                player_turn *= -1
                                if winner != 0:
                                    player_turn = 0
                                    if winner == 1:
                                        print("Gold player wins!")
                                    else:
                                        print("Silver player wins!")
                                elif i == 1:
                                    print("Silver player's turn")
                                else:
                                    print("Gold player's turn")
                                play_2 = False
                            elif play_2 == False:
                                play_2 = True
                ## AI player's turn. Output if given by chosen move
                if player_turn == -1:
                    leafs = 0
                    start = time.time()
                    end = 0
                    depth = 1
                    best_move = [0,0]
                    ## Iterative deepening where we keep computing until 10seconds is done or depth of 10 is reached
                    while end - start < 5 and depth <= 10:
                        end = time.time()
                        chosen_move, minimax_score = minimax(board, silver_array, gold_array, depth, -math.inf, math.inf, i, True, TT, best_move)
                        ## choosing best_move as last chosen move as best move for best first search
                        best_move = chosen_move
                        depth += 1
                    print("depth search = ", depth - 1)
                    print("nodes visited = ", leafs)
                    print("Size of TT = ", len(TT))
                    ## If move was an elimination move
                    if len(chosen_move) == 4:
                        valid_move, silver_array, gold_array, board, winner = moveFunct_elim(board, int(chosen_move[0]), int(chosen_move[1]), int(chosen_move[2] - chosen_move[0]), int(chosen_move[3] - chosen_move[1]), player_turn, i, gold_array, silver_array)
                        print(x_axis[int(chosen_move[1])], int(11 - chosen_move[0]), "->", x_axis[int(chosen_move[3])], int(11 - chosen_move[2]))
                    ## If move was a pawn/mothership move
                    else:
                        valid_move, silver_array, gold_array, board, winner, g_piece = moveFunct_pawn(board, int(chosen_move[0]), int(chosen_move[1]), int(chosen_move[2] - chosen_move[0]), int(chosen_move[3] - chosen_move[1]), int(chosen_move[4]), int(chosen_move[5]), int(chosen_move[6] - chosen_move[4]), int(chosen_move[7] - chosen_move[5]), player_turn, i, gold_array, silver_array)
                        if g_piece == 1:
                            print(x_axis[int(chosen_move[1])], int(11 - chosen_move[0]), "->", x_axis[int(chosen_move[3])], int(11 - chosen_move[2]))
                        elif g_piece == 2:
                            print(x_axis[int(chosen_move[5])], int(11 - chosen_move[4]), "->", x_axis[int(chosen_move[7])], int(11 - chosen_move[6]))
                        else:
                            print(x_axis[int(chosen_move[1])], int(11 - chosen_move[0]), "->", x_axis[int(chosen_move[3])], int(11 - chosen_move[2]), "and", x_axis[int(chosen_move[5])], int(11 - chosen_move[4]), "->", x_axis[int(chosen_move[7])], int(11 - chosen_move[6]))
                    if valid_move:
                        window.fill((0,0,0))
                        draw_board_func(length, board)
                        player_turn *= -1
                        if winner != 0:
                            player_turn = 0
                            if winner == 1:
                                print("Gold player wins!")
                            else:
                                print("Silver player wins!")
                        elif i == 1:
                            print("Gold player's turn")
                        else:
                            print("Silver player's turn")

pygame.quit()
