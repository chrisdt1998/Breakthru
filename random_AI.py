import numpy as np

class Random_AI:
    """
    This class represents the random AI, which just randomly chooses moves from the list of available moves with a bias
    to the elimination moves.
    """
    def __init__(self, Game_board):
        """
        This method initializes the random AI.
        :param Game_board: Game board
        :type Game_board: nd.array
        """
        self.Game_board = Game_board

    def choose_piece(self, player_arr, opp_arr, old_position):
        """
        This method chooses the move to play.
        :param player_arr: Array of the pieces that the Random AI can play.
        :type player_arr: nd.array
        :param opp_arr: Array of the pieces of the opposition player.
        :type opp_arr: nd.array
        :param old_position: Array containing the old position in the case that 2 moves are to be made.
        :type old_position: nd.array
        :return: The chosen move.
        :rtype: nd.array
        """
        pieces_in_elim_zone = []
        for piece in player_arr:
            elim_moves = self.Game_board.elim_moves(piece, opp_arr)
            if elim_moves.shape[0] > 0 and not np.array_equal(piece, old_position):
                pieces_in_elim_zone.append(piece)
        if len(pieces_in_elim_zone) > 0:
            move = np.random.randint(0, len(pieces_in_elim_zone))
            return pieces_in_elim_zone[move]
        else:
            move = np.random.randint(0, player_arr.shape[0])
            return player_arr[move]

    def choose_move(self, piece, silver_array, gold_array, opp_arr):
        """
        This method produces the arrays of possible moves that the piece can do. If elimination move is possible, it
        will only return the elimination moves.
        :param piece: The piece in question.
        :type piece: nd.array
        :param gold_array: Array containing gold pieces.
        :type gold_array: nd.array
        :param silver_array: Array containing silver pieces.
        :type silver_array: nd.array
        :param opp_arr: Array containing the positions of the opposition pieces.
        :type opp_arr: nd.array
        :return: All possible moves that the piece can make.
        :rtype: nd.array
        """
        elim_moves = self.Game_board.elim_moves(piece, opp_arr)
        if elim_moves.shape[0] > 0:
            move = np.random.randint(0, elim_moves.shape[0])
            return elim_moves[move]

        straight_moves = self.Game_board.straight_moves(piece, silver_array, gold_array)
        move = np.random.randint(0, straight_moves.shape[0])

        return straight_moves[move]
