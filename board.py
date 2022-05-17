import numpy as np
import pygame


class Board:
    """
    Class representing the board of the game.
    """
    def __init__(self, length=50):
        """
        Method to initialize the class.
        :param length: size of the board.
        :type length: int
        """
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
        self.board = self.create()
        self.length = length
        self.window = pygame.display.set_mode((length * 11, length * 11))

    def create(self):
        """
        Method to create the starting board.
        :return: board
        :rtype: nd.array
        """
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
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        return board

    def update(self, available_moves=None):
        """
        Method to update the board visualization after a move is done in pygame.
        :param available_moves: contains an array of possible moves from a piece if the piece has been clicked on.
        :type available_moves: nd.array
        """
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
        """
        Method to check if a winning move has been performed.
        :param board: current board.
        :type board: nd.array
        :return: 1 if gold player wins, -1 if silver player wins and 0 if neither wins.
        :rtype: int
        """
        x = np.argwhere(board > 2)
        winner = 0
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

    def evaluate_board(self, board, player, silver_arr, gold_arr):
        """
        Method to compute the score of a particular board composition.
        :param board: game board.
        :type board: nd.array
        :param player: Determines which player's turn it is.
        :type player: str
        :param silver_arr: array containing coordinates of silver pieces .
        :type silver_arr: nd.array
        :param gold_arr: array containing coordinates of gold pieces .
        :type gold_arr: nd.array
        :return: score
        :rtype: int
        """
        i = 1
        if player == 'Gold': i = -1
        reward = 0
        # Score the difference in number of pieces
        reward += i * int(len(silver_arr) - len(gold_arr) - 7) * 100
        # Checking for gold mothership in elimation zone from silver piece
        # TODO: change this to only look at the mother ship and look around it rather than looking at all silver pieces individually.
        for piece in silver_arr:
            if piece[0] + 1 < 11 and piece[1] + 1 < 11:
                if board[piece[0] + 1][piece[1] + 1] == 3:
                    reward += i * 200
            if piece[0] - 1 >= 0 and piece[1] + 1 < 11:
                if board[piece[0] - 1][piece[1] + 1] == 3:
                    reward += i * 200
            if piece[0] + 1 < 11 and piece[1] - 1 >= 0:
                if board[piece[0] + 1][piece[1] - 1] == 3:
                    reward += i * 200
            if piece[0] - 1 >= 0 and piece[1] - 1 >= 0:
                if board[piece[0] - 1][piece[1] - 1] == 3:
                    reward += i * 200

        ## Check if gold can make a winning move, silver should try block
        check1 = True
        check2 = True
        check3 = True
        check4 = True
        for counter in range(1, 10):
            if gold_arr[0][0] + counter < 11:
                if board[gold_arr[0][0] + counter][gold_arr[0][1]] != 0:
                    check1 = False
                elif gold_arr[0][0] + counter == 10 and check1 is True:
                    reward += -i * 200
            if gold_arr[0][0] - counter >= 0:
                if board[gold_arr[0][0] - counter][gold_arr[0][1]] != 0:
                    check2 = False
                elif gold_arr[0][0] - counter == 0 and check2 is True:
                    reward += -i * 200
            if gold_arr[0][1] + counter < 11:
                if board[gold_arr[0][0]][gold_arr[0][1] + counter] != 0:
                    check3 = False
                elif gold_arr[0][1] + counter == 10 and check3 is True:
                    reward += -i * 200
            if gold_arr[0][1] - counter >= 0:
                if board[gold_arr[0][0]][gold_arr[0][1] - counter] != 0:
                    check4 = False
                elif gold_arr[0][1] - counter == 10 and check4 is True:
                    reward += -i * 200

        ## Award wining move with highest score
        no_winner = 0
        for c1 in range(11):
            for c2 in range(11):
                if board[c1][c2] == 3:
                    if c1 == 0 or c1 == 10 or c2 == 0 or c2 == 10:
                        reward += -i * 100000
                    no_winner = 1
                    break
            else:
                continue
            break

        if no_winner == 0:
            reward += i * 100000

        return reward


    def elim_moves(self, piece, array):
        """
        Method which outputs the positions of pieces that are within elimination range from the piece
        :param piece: The piece in question.
        :type piece: nd.array
        :param array: list of all opposition pieces.
        :type array: nd.array
        :return: array containing pieces in elimination range.
        :rtype: nd.array
        """
        x = array[np.logical_and(abs(np.full(array.shape[0], piece[0]) - array[:, 0]) == 1,
                                 abs(np.full(array.shape[0], piece[1]) - array[:, 1]) == 1)]

        return x

    def straight_moves(self, piece, silver_array, gold_array):
        """
        Method to compute the possible straight moves that the piece can make.
        :param piece: The piece in question.
        :type piece: nd.array
        :param silver_array: Array of all silver pieces.
        :type silver_array: nd.array
        :param gold_array: Array of all gold pieces.
        :type gold_array: nd.array
        :return: array of all possible straight moves.
        :rtype: nd.array
        """
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
        """
        This method performs the movement of a position from the original position to it's new position and updates
        the board, silver array and gold array.
        :param board: Game board.
        :type board: nd.array
        :param old_position: Initial position of piece.
        :type old_position: nd.array
        :param new_position: New position of piece.
        :type new_position: nd.array
        :param silver_array: Array of all silver pieces.
        :type silver_array: nd.array
        :param gold_array: Array of all gold pieces.
        :type gold_array: nd.array
        :return: The new board, gold_array and silver_array arrays as well as the elimination boolean.
        :rtype: tuple
        """
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
        """
        This method checks if a position is contained within an array.
        :param position: Position of piece in question
        :type position: nd.array
        :param array: Array in question
        :type array: nd.array
        :return: True if is in the array otherwise False.
        :rtype: bool
        """
        return np.argwhere(np.logical_and(array[:, 0] == position[0], array[:, 1] == position[1]))
