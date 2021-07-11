import os
import numpy as np
import random
import math
import sys
import time
localpath = os.path.dirname(os.path.abspath(__file__))
print(localpath)
sys.path.append('/Users/chris/Uni/Maastrict University/1.1 period/ISG/Breakthru project - C. DU TOIT/libraries')
#print(sys.path)
import pygame

#import importlib.util

pygame.init()


class Board():
    def __init__(self):
        silver_array = np.array([
                                [1, 1, 1, 1, 1, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 9, 9, 9, 9, 9],
                                [3, 4, 5, 6, 7, 1, 9, 1, 9, 1, 9, 1, 9, 1, 9, 3, 4, 5, 6, 7]
                                ])
        self.silver_array = silver_array.transpose()
        gold_array = np.array([
                                [5, 3, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 7],
                                [5, 4, 5, 6, 3, 7, 3, 7, 3, 7, 4, 5, 6]
                                ])
        self.gold_array = gold_array.transpose()

    def create_board(self):
        board = np.array([
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 2, 2, 2, 0, 0, 1, 0],
                        [0, 1, 0, 2, 0, 0, 0, 2, 0, 1, 0],
                        [0, 1, 0, 2, 0, 3, 0, 2, 0, 1, 0],
                        [0, 1, 0, 2, 0, 0, 0, 2, 0, 1, 0],
                        [0, 1, 0, 0, 2, 2, 2, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        return board

    ## Updating the board visual using pygame for the UI
    def update_board(self, length, board):
        window.fill((0, 0, 0))
        for j in range(11):
            for i in range(11):
                if (i + j) % 2 == 0:
                    colour = (255, 255, 255)
                else:
                    colour = (0, 0, 0)

                pygame.draw.rect(window, colour, (i * length, j * length, length, length))

                if board[j][i] == 1:
                    pygame.draw.circle(window, (192, 192, 192), (i * length + 25, j * length + 25), 10)
                elif board[j][i] == 2:
                    pygame.draw.circle(window, (255, 223, 0), (i * length + 25, j * length + 25), 10)

                if board[j][i] == 3:
                    pygame.draw.circle(window, (255, 0, 0), (i * length + 25, j * length + 25), 15)

        pygame.display.update()

    ## Evaluation function
    def evaluate_board(self, board, i, s_copy, g_copy):
        reward = 0
        ## Score the difference in number of pieces
        reward += i * int(len(s_copy) - len(g_copy) - 7) * 100

        ## Checking for gold mothership in elimation zone from silver piece
        for j in range(0, s_copy.shape[0], 2):
            if s_copy[j][0] + 1 < 11 and s_copy[j][1] + 1 < 11:
                if board[s_copy[j][0] + 1][s_copy[j][1] + 1] == 3:
                    reward += i * 200

            if s_copy[j][0] - 1 >= 0 and s_copy[j][1] + 1 < 11:
                if board[s_copy[j][0] - 1][s_copy[j][1] + 1] == 3:
                    reward += i * 200

            if s_copy[j][0] - 1 >= 0 and s_copy[j][1] - 1 >= 0:
                if board[s_copy[j][0] - 1][s_copy[j][1] - 1] == 3:
                    reward += i * 200

            if s_copy[j][0] + 1 < 11 and s_copy[j][1] - 1 >= 0:
                if board[s_copy[j][0] + 1][s_copy[j][1] - 1] == 3:
                    reward += i * 200

        ## Check if gold can make a winning move, silver should try block
        ## Needs to be redone
        x = np.argwhere(board > 2)
        if x.size > 0:
            check = [True, True, True, True]
            for counter in range(1, 10):
                if g_copy[0][0] + counter < 11:
                    if board[g_copy[0][0] + counter][g_copy[0][1]] != 0:
                        check[0] = False
                    elif g_copy[0][0] + counter == 10 and check[0] == True:
                        reward += -i * 200

                if g_copy[0][0] - counter >= 0:
                    if board[g_copy[0][0] - counter][g_copy[1][0]] != 0:
                        check[1] = False
                    elif g_copy[0][0] - counter == 0 and check[1] == True:
                        reward += -i * 200

                if g_copy[1][0] + counter < 11:
                    if board[g_copy[0][0]][g_copy[1][0] + counter] != 0:
                        check[2] = False
                    elif g_copy[1][0] + counter == 10 and check[2] == True:
                        reward += -i * 200

                if g_copy[1][0] - counter >= 0:
                    if board[g_copy[0][1]][g_copy[1][0] - counter] != 0:
                        check[3] = False
                    elif g_copy[1][0] - counter == 10 and check[3] == True:
                        reward += -i * 200

            ## reward protectors of Gold ship - cumulative
            if g_copy[0][0] + counter < 11:
                if board[g_copy[0][0] + 2][g_copy[1][0] + 2] == 2:
                    reward += -i * 10

            if g_copy[0][0] - counter >= 0:
                if board[g_copy[0][0] - 2][g_copy[1][0] + 2] == 2:
                    reward += -i * 10

            if g_copy[1][0] + counter < 11:
                if board[g_copy[0][0] + 2][g_copy[1][0] - 2] == 2:
                    reward += -i * 10

            if g_copy[1][0] - counter >= 0:
                if board[g_copy[0][0] - 2][g_copy[1][0] - 2] == 2:
                    reward += -i * 10

        ## Award wining move with highest score
        if x.size > 0:
            if (x[0] or x[1] == 0) or (x[0] or x[1] == 10):
                reward += -i * 100000
        else:
            reward += i * 100000

        return reward

    def winning_move(self, board):
        x = np.argwhere(board > 2)
        winner = 0
        if x.size > 0:
            if (x[0] or x[1] == 0) or (x[0] or x[1] == 10):
                winner = 1
        else:
            winner = -1

        return winner

    def elim_moves(self, piece, array):
        x = array[np.logical_and(abs(np.full(array.shape[0], piece[0]) - array[:, 0]) == 1,
                                 abs(np.full(array.shape[0], piece[1]) - array[:, 1]) == 1)]

        return x

    ## THIS FUNCTIONS NEED TO BE REDUCED BECAUSE THERE IS TOO MUCH REPITITIVE CODE
    def straight_moves(self, piece):
        # Check right
        x = self.silver_array[np.logical_and(self.silver_array[:, 0] == piece[0], self.silver_array[:, 1] > piece[1])]
        x = np.vstack([x, self.gold_array[np.logical_and(self.gold_array[:, 0] == piece[0], self.gold_array[:, 1] > piece[1])]])

        limit_right = x[np.argmin(x[:, 1])]
        right_moves = np.arange(piece[1] + 1, limit_right[1])
        right_moves = np.stack([np.full(limit_right[1] - piece[1] - 1, piece[0]), right_moves], axis=-1)
        print(right_moves)

        # Check left
        x = self.silver_array[np.logical_and(self.silver_array[:, 0] == piece[0], self.silver_array[:, 1] < piece[1])]
        x = np.vstack([x, self.gold_array[np.logical_and(self.gold_array[:, 0] == piece[0], self.gold_array[:, 1] < piece[1])]])

        limit_left = x[np.argmax(x[:, 1])]
        left_moves = np.arange(limit_left[1] + 1, piece[1])
        left_moves = np.stack([np.full(piece[1] - limit_left[1] - 1, piece[0]), left_moves], axis=-1)
        print(left_moves)

        # Check down
        x = self.silver_array[np.logical_and(self.silver_array[:, 1] == piece[1], self.silver_array[:, 0] > piece[0])]
        x = np.vstack(
            [x, self.gold_array[np.logical_and(self.gold_array[:, 1] == piece[1], self.gold_array[:, 0] > piece[0])]])

        limit_right = x[np.argmin(x[:, 0])]
        right_moves = np.arange(piece[0] + 1, limit_right[0])
        right_moves = np.stack([np.full(limit_right[0] - piece[0] - 1, piece[1]), right_moves], axis=-1)
        print(right_moves)

        # Check left
        x = self.silver_array[np.logical_and(self.silver_array[:, 1] == piece[1], self.silver_array[:, 0] < piece[0])]
        x = np.vstack([x, self.gold_array[np.logical_and(self.gold_array[:, 1] == piece[1], self.gold_array[:, 0] < piece[0])]])

        limit_left = x[np.argmax(x[:, 0])]
        left_moves = np.arange(limit_left[0] + 1, piece[0])
        left_moves = np.stack([np.full(piece[0] - limit_left[0] - 1, piece[1]), left_moves], axis=-1)
        print(left_moves)

    def moveFunct(self, board, position, direction, new_position, g_copy, s_copy, valid_moves):
        # Input arrays and board because we don't want to edit the main ones when searching for a move
        # Check move is in valid_moves
        # If move piece is also in opposition array then we have an elimination
        # Update the board and arrays
        if new_position not in valid_moves:
            print("Move not legal, try again...")
        else:
            board[new_position[0]][new_position[1]] = board[position[0]][position[1]]
            board[position[0]][position[1]] = 0
            if new_position in g_copy:



class Player():
    pass

class AI():
    pass

class Game():
    def __init__(self, board, gold_arr, silver_arr):
        self.board = board
        self.gold_arr = gold_arr
        self.silver_arr = silver_arr
        self.player_turn = 'Gold'

    def initialize_prints(self):
        print("Game started...")
        print("Gold player plays first.")
        print("Press n to skip first turn.")

    def start(self):
        running = True
        self.initialize_prints()
        ## Game loop
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        print("Gold player skips first turn.")
                        player_turn = 'Silver'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if player_turn == 'Gold':
                            if first_click:
                                ## Make first_click true if the first click clicks on a piece
                                position = np.around(np.array(event.pos)/length)
                                if position[0] in self.gold_arr[0] and position[1] in self.gold_arr[1]:
                                    first_click = False
                            elif first_click == False:
                                first_click = True
                                new_position = np.around(np.array(event.pos)/length)
                                direction = new_position - position
                                valid_move, silver_array, gold_array, winner, elimination, gold = moveFunct(board, position, direction, new_position, player_turn, i, gold_array, silver_array)

                                if valid_move:
                                    self.board.draw_board_func(length, board)
                                    print(int(11 - position[0]), x_axis[position[1]], "->", int(11 - new_position[0]), x_axis[new_position[1]])
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
                            best_move = [0, 0]
                            ## Iterative deepening where we keep computing until 10seconds is done or depth of 10 is reached
                            while end - start < 10 and depth <= 10:
                                end = time.time()
                                chosen_move, minimax_score = minimax(board, silver_array, gold_array, depth, -math.inf, math.inf, i, True, TT, best_move)
                                ## choosing best_move as last chosen move as best move for best first search
                                best_move = chosen_move
                                depth += 1
                            print("depth search = ", depth - 1)
                            print("nodes visited = ", leafs)
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

if __name__ == '__main__':
    new_board = Board()
    board = new_board.create_board()
    ## Which player is the gold player and consequently, which player plays first
    is_gold_player = True
    ## Setting up the board
    length = 50
    number_of_silvers = 20
    number_of_golds = 12
    window = pygame.display.set_mode((length * 11, length * 11))
    pygame.display.set_caption("Breakthru")
    x_axis = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]



