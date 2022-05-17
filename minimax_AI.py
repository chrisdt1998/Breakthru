import math
import numpy as np

class Minimax_AI:
    """
    This is a class which represents the MiniMax searching algorithm. The algorithm has been enhanced by Alpha-Beta
    pruning.
    """
    def __init__(self, game_board, player):
        """
        This method initalizes the class.
        :param game_board: Game board.
        :type game_board: nd.array
        :param player: Determines if the player is Gold or Silver.
        :type player: str
        """
        self.player = player
        self.Game_board = game_board
        self.node_count = 0

    def max_min_arrays(self, gold_array, silver_array):
        """
        This method decides which player array maximizes and which player array minimizes for the algorithm.
        :param gold_array: Array containing gold piece positions.
        :type gold_array: nd.array
        :param silver_array: Array containing silver piece positions.
        :type silver_array: nd.array
        :return: The max and min arrays.
        :rtype: nd.array
        """
        if self.player == 'Gold':
            return gold_array, silver_array
        elif self.player == 'Silver':
            return silver_array, gold_array

    def initialize_game(self, game):
        """
        Method to initialize the game object.
        :param game: Game object.
        :type game: object
        """
        self.Game = game

    def copy_arrays(self, board, gold_array, silver_array, old_position):
        """
        Method to copy arrays for when searching deeper into the recursion algorithm.
        :param board: Game board.
        :type board: nd.array
        :param gold_array: Array containing gold pieces.
        :type gold_array: nd.array
        :param silver_array: Array containing silver pieces.
        :type silver_array: nd.array
        :param old_position: Array containing old position.
        :type old_position: nd.array
        :return: Copied arrays
        :rtype: tuple
        """
        if old_position is not None:
            copy_old_position = old_position.copy()
        else:
            copy_old_position = None
        return board.copy(), gold_array.copy(), silver_array.copy(), copy_old_position

    def generate_moves(self, play, piece, opp_array, silver_array, gold_array):
        """
        This method generates the moves that a piece can make.
        :param play: If play is 1, then the player has already made one move and now cannot make an elimination move.
        :type play: int
        :param piece: Array containing the piece position.
        :type piece: nd.array
        :param opp_array: The array of the opposition pieces.
        :type opp_array: nd.array
        :param silver_array: Array containing silver pieces.
        :type silver_array: nd.array
        :param gold_array: Array containing gold pieces.
        :type gold_array: nd.array
        :return: Array of available moves the piece can make.
        :rtype: nd.array
        """
        straight_moves = self.Game_board.straight_moves(piece, silver_array, gold_array)
        if play != 1:
            elim_moves = self.Game_board.elim_moves(piece, opp_array)
            if straight_moves.shape[0] > 0 or elim_moves.shape[0] > 0:
                available_moves = np.concatenate([x for x in [elim_moves, straight_moves] if x.size > 0])
            else:
                available_moves = np.array([])
        else:
            available_moves = straight_moves
        return available_moves

    def remove_played_pawn(self, array, old_position):
        """
        This method removes a played piece.
        :param array: Array containg the piece.
        :type array: nd.array
        :param old_position: Position of the piece.
        :type old_position: nd.array
        :return: Returns the new array.
        :rtype: nd.array
        """
        if old_position is None:
            return array
        else:
            index = self.Game.is_in_arr(old_position, array)
            return np.delete(array, index, 0)

    def minimax(self, alpha, beta, depth, maximizing_player, board, gold_array, silver_array, turn, play, chosen_play, old_position):
        """
        This is the method that contains the MiniMax algorithm with Alpha-Beta enhancement. This method is used
        recursively up to the pre-determined depth point.
        :param alpha: Alpha value of the alpha-beta enhancement.
        :type alpha: int
        :param beta: Beta value of the alpha-beta enhancement.
        :type beta: int
        :param depth: Search depth.
        :type depth: int
        :param maximizing_player: Boolean containing if the turn is the maximizing player or not.
        :type maximizing_player: bool
        :param board: Game board.
        :type board: nd.array
        :param gold_array: Array containing gold pieces.
        :type gold_array: nd.array
        :param silver_array: Array containing silver pieces.
        :type silver_array: nd.array
        :param turn: 1 if it is Gold's turn, -1 if Silver's turn.
        :type turn: int
        :param play: If play is 1, then the player has already made one move and now cannot make an elimination move.
        :type play: int
        :param chosen_play: Array containing the move chosen.
        :type chosen_play: nd.array
        :param old_position: Array containng the old position.
        :type old_position: nd.array
        :return: Returns the reward and chosen move.
        :rtype: tuple
        """
        self.node_count += 1
        if depth == 0 or self.Game_board.winning_move(board) != 0:
            return self.Game_board.evaluate_board(board, self.player, silver_array, gold_array), chosen_play

        max_array, min_array = self.max_min_arrays(gold_array, silver_array)

        if maximizing_player:
            value = -math.inf
            max_array = self.remove_played_pawn(max_array, old_position)
            for piece in max_array:
                available_moves = self.generate_moves(play, piece, min_array, silver_array, gold_array)
                if available_moves.shape[0] > 0:
                    for move in available_moves:
                        # print(maximizing_player)
                        # if old_position is not None: print(np.array_equal(move, old_position), piece, move, old_position)

                        if old_position is None or not np.array_equal(move, old_position) or not np.array_equal(piece, old_position):
                            copy_board, copy_gold_array, copy_silver_array, copy_old_position = self.copy_arrays(board, gold_array, silver_array, old_position)

                            _, copy_board, copy_gold_array, copy_silver_array, new_turn, available_moves, _, copy_old_position = self.Game.run_player_turn(
                                piece, copy_board, copy_gold_array, copy_silver_array, turn, available_moves, play, new_position=move, sim=True, old_position=copy_old_position)

                            if turn != new_turn:
                                maximizing_player = False
                                copy_old_position = None
                            else:
                                maximizing_player = True
                                copy_old_position = move.copy()

                            value = max(value, self.minimax(alpha, beta, depth - 1, maximizing_player, copy_board, copy_gold_array, copy_silver_array, turn, play, chosen_play, copy_old_position)[0])

                            if value >= beta:
                                break
                            if value > alpha:
                                chosen_play = [piece, move]
                                alpha = value
            return value, chosen_play
        else:
            value = math.inf
            min_array = self.remove_played_pawn(min_array, old_position)
            for piece in min_array:
                available_moves = self.generate_moves(play, piece, max_array, silver_array, gold_array)
                if available_moves.shape[0] > 0:
                    for move in available_moves:
                        # print(maximizing_player)
                        # if old_position is not None: print(np.array_equal(move, old_position), piece, move, old_position)

                        if old_position is None or not np.array_equal(move, old_position) or not np.array_equal(piece, old_position):
                            copy_board, copy_gold_array, copy_silver_array, copy_old_position = self.copy_arrays(board, gold_array, silver_array, old_position)

                            _, copy_board, copy_gold_array, copy_silver_array, new_turn, available_moves, _, copy_old_position = self.Game.run_player_turn(
                                piece, copy_board, copy_gold_array, copy_silver_array, turn, available_moves, play, new_position=move, sim=True, old_position=copy_old_position)

                            if turn != new_turn:
                                maximizing_player = True
                                copy_old_position = None
                            else:
                                maximizing_player = False
                                copy_old_position = move.copy()

                            value = min(value, self.minimax(alpha, beta, depth - 1, maximizing_player, copy_board, copy_gold_array, copy_silver_array, turn, play, chosen_play, copy_old_position)[0])

                            if value <= alpha:
                                break
                            if value < beta:
                                chosen_play = [piece, move]
                                beta = value
            return value, chosen_play
