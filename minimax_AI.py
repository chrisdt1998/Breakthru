class AI:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.game_board = game.game_board

    ## Minimax algorithm containing alpha-beta minimax enahanced with Transition tables, iterative deepening and best first search.
    ## Lines 457-598
    def minimax(self, node, alpha, beta, depth, maximizing_player, board, gold_array, silver_array):
        if depth == 0 or self.game_board.winning_move(board) != 0:
            return self.game_board.evaluate_board(board)

        if maximizing_player:
            value = -math.inf

            for piece in array:
                available_moves =
                for move in available_moves:
                    board, gold_array, silver_array, elimination =
                    value = max(value, self.minimax(move, depth - 1, False))
                    if value >= beta:
                        break
                    alpha = max(alpha, value)
            return value, chosen_move
        else:
            value = math.inf
            for piece in array:
                available_moves =
                for move in available_moves:
                    value = min(value, self.minimax(move, depth - 1, True))
                    if value <= alpha:
                        break
                    beta = min(beta, value)
            return value, chosen_move