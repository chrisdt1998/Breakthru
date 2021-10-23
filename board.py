import numpy as np
import pygame


class Board:
    def __init__(self, length):
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
        self.length = length
        self.window = pygame.display.set_mode((length * 11, length * 11))

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

    def update_board(self, available_moves=None):
        self.window.fill((0, 0, 0))

        for j in range(11):
            for i in range(11):
                if (i + j) % 2 == 0:
                    colour = (255, 255, 255)
                else:
                    colour = (0, 0, 0)

                if available_moves is not None and self.is_in_arr([j, i], available_moves).size > 0:
                    pygame.draw.rect(self.window, (0, 0, 255), (i * self.length, j * self.length, self.length, self.length))
                else:
                    pygame.draw.rect(self.window, colour, (i * self.length, j * self.length, self.length, self.length))

                if self.board[j][i] == 1:
                    pygame.draw.circle(self.window, (192, 192, 192), (i * self.length + 25, j * self.length + 25), 10)
                elif self.board[j][i] == 2:
                    pygame.draw.circle(self.window, (255, 223, 0), (i * self.length + 25, j * self.length + 25), 10)

                if self.board[j][i] == 3:
                    pygame.draw.circle(self.window, (255, 0, 0), (i * self.length + 25, j * self.length + 25), 15)

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

    @staticmethod
    def elim_moves(piece, array):
        x = array[np.logical_and(abs(np.full(array.shape[0], piece[0]) - array[:, 0]) == 1,
                                 abs(np.full(array.shape[0], piece[1]) - array[:, 1]) == 1)]

        return x

    @staticmethod
    def straight_moves(piece, silver_array, gold_array):
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

    def moveFunct(self, board, old_position, new_position, gold_array, silver_array):
        elimination = False

        # Update board
        board[new_position[0]][new_position[1]] = board[old_position[0]][old_position[1]]
        board[old_position[0]][old_position[1]] = 0

        arr_index = self.is_in_arr(new_position, gold_array)
        if arr_index.size > 0:
            gold_array = np.delete(gold_array, arr_index, 0)
            elimination = True
        else:
            arr_index = self.is_in_arr(new_position, silver_array)
            if arr_index.size > 0:
                silver_array = np.delete(silver_array, arr_index, 0)
                elimination = True

        arr_index = self.is_in_arr(old_position, gold_array)
        if arr_index.size > 0:
            gold_array[arr_index] = new_position
        else:
            arr_index = self.is_in_arr(old_position, silver_array)
            if arr_index.size > 0:
                silver_array[arr_index] = new_position

        return board, gold_array, silver_array, elimination

    def is_in_arr(self, position, array):
        return np.argwhere(np.logical_and(array[:, 0] == position[0], array[:, 1] == position[1]))
