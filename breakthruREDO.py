import os
import numpy as np
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
        self.board = self.create_board()

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
    def update_board(self, length, board, available_moves=None):
        window.fill((0, 0, 0))

        for j in range(11):
            for i in range(11):
                if (i + j) % 2 == 0:
                    colour = (255, 255, 255)
                else:
                    colour = (0, 0, 0)

                if available_moves is not None and self.is_in_arr([j, i], available_moves).size > 0:
                    pygame.draw.rect(window, (0, 0, 255), (i * length, j * length, length, length))
                else:
                    pygame.draw.rect(window, colour, (i * length, j * length, length, length))

                if board[j][i] == 1:
                    pygame.draw.circle(window, (192, 192, 192), (i * length + 25, j * length + 25), 10)
                elif board[j][i] == 2:
                    pygame.draw.circle(window, (255, 223, 0), (i * length + 25, j * length + 25), 10)

                if board[j][i] == 3:
                    pygame.draw.circle(window, (255, 0, 0), (i * length + 25, j * length + 25), 15)



        pygame.display.update()

    def winning_move(self, board):
        x = np.argwhere(board > 2)
        winner = 0
        print('x=', x)
        if x.size > 0:
            if (x[0][0] == 0 or x[0][1] == 0) or (x[0][0] == 10 or x[0][1] == 10):
                winner = 1
                print("Gold player wins!")
                print("Game over.")
        else:
            winner = -1
            print("Silver player wins!")
            print("Game over.")

        return winner

    def elim_moves(self, piece, array):
        x = array[np.logical_and(abs(np.full(array.shape[0], piece[0]) - array[:, 0]) == 1,
                                 abs(np.full(array.shape[0], piece[1]) - array[:, 1]) == 1)]

        return x

    ## THIS FUNCTIONS NEED TO BE REDUCED BECAUSE THERE IS TOO MUCH REPITITIVE CODE
    def straight_moves(self, piece, silver_array, gold_array):
        print(piece)
        # Check right
        x = silver_array[np.logical_and(silver_array[:, 0] == piece[0], silver_array[:, 1] > piece[1])]
        x = np.vstack([x, gold_array[np.logical_and(gold_array[:, 0] == piece[0],
                                                         gold_array[:, 1] > piece[1])]])

        if x.size > 0:
            limit_right = x[np.argmin(x[:, 1])]
            right_moves = np.arange(piece[1] + 1, limit_right[1]).astype(int)
            right_moves = np.stack([np.full(limit_right[1] - piece[1] - 1, piece[0]), right_moves], axis=-1)
        else:
            limit_right = 11
            right_moves = np.arange(piece[1] + 1, limit_right).astype(int)
            right_moves = np.stack([np.full(limit_right - piece[1] - 1, piece[0]), right_moves], axis=-1)

        # Check left
        x = silver_array[np.logical_and(silver_array[:, 0] == piece[0], silver_array[:, 1] < piece[1])]
        x = np.vstack([x, gold_array[np.logical_and(gold_array[:, 0] == piece[0],
                                                         gold_array[:, 1] < piece[1])]])

        if x.size > 0:
            limit_left = x[np.argmax(x[:, 1])]
            left_moves = np.arange(limit_left[1] + 1, piece[1])
            left_moves = np.stack([np.full(piece[1] - limit_left[1] - 1, piece[0]), left_moves], axis=-1)
        else:
            limit_left = -1
            left_moves = np.arange(limit_left + 1, piece[1])
            left_moves = np.stack([np.full(piece[1] - limit_left - 1, piece[0]), left_moves], axis=-1)

        # Check down
        x = silver_array[np.logical_and(silver_array[:, 1] == piece[1], silver_array[:, 0] > piece[0])]
        x = np.vstack(
            [x, gold_array[np.logical_and(gold_array[:, 1] == piece[1], gold_array[:, 0] > piece[0])]])

        if x.size > 0:
            limit_down = x[np.argmin(x[:, 0])]
            down_moves = np.arange(piece[0] + 1, limit_down[0])
            down_moves = np.stack([down_moves, np.full(limit_down[0] - piece[0] - 1, piece[1])], axis=-1)
        else:
            limit_down = 11
            down_moves = np.arange(piece[0] + 1, limit_down)
            down_moves = np.stack([down_moves, np.full(limit_down - piece[0] - 1, piece[1])], axis=-1)

        # Check up
        x = silver_array[np.logical_and(silver_array[:, 1] == piece[1], silver_array[:, 0] < piece[0])]
        x = np.vstack([x, gold_array[np.logical_and(gold_array[:, 1] == piece[1],
                                                         gold_array[:, 0] < piece[0])]])

        if x.size > 0:
            limit_up = x[np.argmax(x[:, 0])]
            up_moves = np.arange(limit_up[0] + 1, piece[0])
            up_moves = np.stack([up_moves, np.full(piece[0] - limit_up[0] - 1, piece[1])], axis=-1)
        else:
            limit_up = -1
            up_moves = np.arange(limit_up + 1, piece[0])
            up_moves = np.stack([up_moves, np.full(piece[0] - limit_up - 1, piece[1])], axis=-1)

        if right_moves.size > 0 or left_moves.size > 0 or down_moves.size > 0 or up_moves.size > 0:
            return np.concatenate([x for x in [right_moves, left_moves, down_moves, up_moves] if x.size > 0])
        else:
            return np.array([])


    def moveFunct(self, board, old_position, new_position, g_copy, s_copy):
        elimination = False

        # Update board
        board[new_position[0]][new_position[1]] = board[old_position[0]][old_position[1]]
        board[old_position[0]][old_position[1]] = 0

        arr_index = self.is_in_arr(new_position, g_copy)
        if arr_index.size > 0:
            g_copy = np.delete(g_copy, arr_index, 0)
            elimination = True
        else:
            arr_index = self.is_in_arr(new_position, s_copy)
            if arr_index.size > 0:
                s_copy = np.delete(s_copy, arr_index, 0)
                elimination = True

        arr_index = self.is_in_arr(old_position, g_copy)
        if arr_index.size > 0:
            g_copy[arr_index] = new_position
        else:
            arr_index = self.is_in_arr(old_position, s_copy)
            if arr_index.size > 0:
                s_copy[arr_index] = new_position

        return board, g_copy, s_copy, elimination

    def is_in_arr(self, position, array):
        return np.argwhere(np.logical_and(array[:, 0] == position[0], array[:, 1] == position[1]))


class Player():
    pass

class AI():
    pass

class Game():
    def __init__(self, game_board):
        self.game_board = game_board
        self.board = game_board.board
        self.gold_arr = game_board.gold_array
        self.silver_arr = game_board.silver_array
        self.player_turn = 'Gold'

    def initialize_prints(self):
        print("Game started...")
        print("Gold player plays first.")
        print("Press n to skip first turn.")

    def run_player_turn(self, event, position, board, gold_array, silver_array, turn, available_moves, play, old_position=None):
        player_turn = {1: 'Gold', -1: 'Silver'}
        if player_turn[turn] == 'Gold':
            player_arr = gold_array
            opp_arr = silver_array
        else:
            player_arr = silver_array
            opp_arr = gold_array

        if position is None:
            position = (np.floor(np.array(event.pos) / length)).astype(int)
            position = position[::-1]
            if self.game_board.is_in_arr(position, player_arr).size > 0:
                print("check 1")
                if old_position is None or (old_position is not None and (old_position != position).any()):
                    print("check 2")
                    straight_moves = self.game_board.straight_moves(position, silver_array, gold_array)

                    if play == 0:
                        elim_moves = self.game_board.elim_moves(position, opp_arr)
                        available_moves = np.concatenate([x for x in [elim_moves, straight_moves] if x.size > 0])
                    else:
                        available_moves = straight_moves

                    self.game_board.update_board(length, board, available_moves)
                else:
                    position = None
            else:
                position = None

        else:
            new_position = np.floor(np.array(event.pos) / length).astype(int)
            new_position = new_position[::-1]
            if self.game_board.is_in_arr(new_position, available_moves).size > 0:
                old_position = new_position
                board, gold_array, silver_array, elimination = self.game_board.moveFunct(board, position, new_position,
                                                                                         gold_array, silver_array)
                available_moves = None
                self.game_board.update_board(length, board)
                print(int(11 - position[0]), x_axis[position[1]], "->", int(11 - new_position[0]),
                      x_axis[new_position[1]])

                print((new_position == gold_array[0]).all())
                if play == 1 or (new_position == gold_array[0]).all() or elimination:
                    print("Next turn")
                    turn = turn * -1
                    play = 0
                else:
                    play = 1

                position = None

            elif (new_position == position).all():
                position = None
                available_moves = None

        return position, board, gold_array, silver_array, turn, available_moves, play, old_position

    def start(self):
        running = True
        turn = 1
        position = None
        available_moves = None
        old_position = None
        play = 0
        self.initialize_prints()
        self.game_board.update_board(50, self.board)

        ## Game loop
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        print("Gold player skips first turn.")
                        turn = -1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        position, self.board, self.gold_arr, self.silver_arr, turn, available_moves, play, old_position = self.run_player_turn(
                            event, position, self.board, self.gold_arr, self.silver_arr, turn, available_moves, play, old_position)
                        self.game_board.update_board(50, self.board, available_moves)
                        if self.game_board.winning_move(self.board) != 0:
                            time.sleep(10)
                            running = False



        pygame.quit()

if __name__ == '__main__':
    game_board = Board()
    ## Which player is the gold player and consequently, which player plays first
    is_gold_player = True
    ## Setting up the board
    length = 50
    number_of_silvers = 20
    number_of_golds = 12
    window = pygame.display.set_mode((length * 11, length * 11))
    pygame.display.set_caption("Breakthru")
    x_axis = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
    game = Game(game_board)
    game.start()



