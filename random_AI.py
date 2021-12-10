import numpy as np

class Random_AI:
    def __init__(self, Game_board):
        self.Game_board = Game_board

    def choose_piece(self, player_arr, opp_arr, old_position):
        # print(f"old_posi = {old_position}")
        pieces_in_elim_zone = []
        for piece in player_arr:
            elim_moves = self.Game_board.elim_moves(piece, opp_arr)
            # print(np.array_equal(piece, old_position), piece, old_position)
            if elim_moves.shape[0] > 0 and not np.array_equal(piece, old_position):
                pieces_in_elim_zone.append(piece)
        if len(pieces_in_elim_zone) > 0:
            move = np.random.randint(0, len(pieces_in_elim_zone))
            return pieces_in_elim_zone[move]
        else:
            move = np.random.randint(0, player_arr.shape[0])
            return player_arr[move]

    def choose_move(self, piece, silver_array, gold_array, opp_arr):
        # Prioritize elimination moves
        elim_moves = self.Game_board.elim_moves(piece, opp_arr)
        if elim_moves.shape[0] > 0:
            move = np.random.randint(0, elim_moves.shape[0])
            return elim_moves[move]

        straight_moves = self.Game_board.straight_moves(piece, silver_array, gold_array)

        # available_moves = np.concatenate([x for x in [elim_moves, straight_moves] if x.size > 0])
        move = np.random.randint(0, straight_moves.shape[0])

        return straight_moves[move]
