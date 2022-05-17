import numpy as np
import pygame
import math

pygame.init()

class Game:
    """
    This class represents the core of the game. It contains methods that run each players turn when it is their
    respective turn.
    """
    def __init__(self, game_board, length, Random_AI, Minimax_AI, depth, player_gold, player_silver):
        """
        This method initializes the class.
        :param game_board: Game board.
        :type game_board: nd.array
        :param length: Size of the board.
        :type length: int
        :param Random_AI: Class object for the Random_AI.
        :type Random_AI: object
        :param Minimax_AI: Class object for the Minimax_AI.
        :type Minimax_AI: object
        :param depth: Search depth for minimax.
        :type depth: int
        :param player_gold: Determines what is playing player_gold i.e. Human, Minimax or Random.
        :type player_gold: str
        :param player_silver: Determines what is playing player_silver i.e. Human, Minimax or Random.
        :type player_silver: str
        """
        self.Random_AI = Random_AI
        self.Minimax_AI = Minimax_AI
        self.Game_board = game_board
        self.board = game_board.board
        self.gold_arr = game_board.gold_array
        self.silver_arr = game_board.silver_array
        self.player_turn = 'Gold'
        self.length = length
        self.players = {1: player_gold, -1: player_silver}
        self.clock = pygame.time.Clock()
        self.depth = depth

    def initialize_prints(self):
        """
        Method to show that the game is starting up.
        :return:
        :rtype:
        """
        print("Game started...")
        print("Gold player plays first.")
        print("Press n to skip first turn.")


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

    def run_player_turn(self, position, board, gold_array, silver_array, turn, available_moves, play,
                        old_position=None, event=None, new_position=None, sim=False):
        """
        Method to run the player turn. Each player gets either 2 movement turns, or 1 elimination turn or 1 move of the
        mothership (only in the case of gold).
        :param position: Array containing the position of piece.
        :type position: nd.array
        :param board: Game board.
        :type board: nd.array
        :param gold_array: Array containing gold pieces.
        :type gold_array: nd.array
        :param silver_array: Array containing silver pieces.
        :type silver_array: nd.array
        :param turn: 1 if it is Gold's turn, -1 if Silver's turn.
        :type turn: int
        :param available_moves: nd.array containing all possible moves of a particular node.
        :type available_moves: nd.array
        :param play: If 0, the move has no restrictions. If 1, the next move can only be a movement move of a pawn.
        :type play: int
        :param old_position: Old position of the piece such that the same piece is not moved twice.
        :type old_position: nd.array
        :param event: Event containing the input from the human player.
        :type event: pygame.event
        :param new_position: New position of piece.
        :type new_position: nd.array
        :param sim: Used to simulated. TBD.
        :type sim: bool
        :return: Returns the same variables for recursion purposes.
        :rtype: tuple
        """
        player = self.players[turn]
        player_turn = {1: 'Gold', -1: 'Silver'}
        if player_turn[turn] == 'Gold':
            player_arr = gold_array
            opp_arr = silver_array
        else:
            player_arr = silver_array
            opp_arr = gold_array

        if position is None and sim is False and player != "MiniMax":
            if player == "Random":
                position = self.Random_AI.choose_piece(player_arr, opp_arr, old_position)
            else:
                position = (np.floor(np.array(event.pos) / self.length)).astype(int)
                position = position[::-1]
            if self.is_in_arr(position, player_arr).size > 0:
                if old_position is None or (old_position is not None and (old_position != position).any()):
                    straight_moves = self.Game_board.straight_moves(position, silver_array, gold_array)

                    if play == 0:
                        elim_moves = self.Game_board.elim_moves(position, opp_arr)
                        available_moves = np.concatenate([x for x in [elim_moves, straight_moves] if x.size > 0])
                    else:
                        available_moves = straight_moves

                    self.Game_board.update(available_moves)
                else:
                    position = None
            else:
                position = None

        else:
            if player == "Random":
                new_position = self.Random_AI.choose_move(position, silver_array, gold_array, opp_arr)
            if player == 'MiniMax':
                if sim is False:
                    _, [position, new_position] = self.Minimax_AI.minimax(-math.inf, math.inf, self.depth, True, board, gold_array, silver_array, turn, play, [], old_position)
                    print(f"piece moved from {position} to {new_position}. Number of nodes: {self.Minimax_AI.node_count}")
                else:
                    new_position = new_position
            if player == 'Human':
                if sim:
                    new_position = new_position
                else:
                    new_position = np.floor(np.array(event.pos) / self.length).astype(int)
                    new_position = new_position[::-1]

            if (player == "MiniMax" and sim is False) or self.is_in_arr(new_position, available_moves).size > 0:
                old_position = new_position
                board, gold_array, silver_array, elimination = self.Game_board.moveFunct(board, position, new_position,
                                                                                         gold_array, silver_array)

                if sim is False:
                    available_moves = None
                    self.Game_board.update()

                if play == 1 or (new_position == gold_array[0]).all() or elimination:
                    # print("Next turn")
                    turn = turn * -1
                    play = 0
                else:
                    play = 1

                position = None

            elif np.array_equal(new_position, position):
                position = None
                available_moves = None

        return position, board, gold_array, silver_array, turn, available_moves, play, old_position

    def start(self):
        """
        This is the main method to start the game.
        """
        running = True
        turn = 1
        position = None
        available_moves = None
        old_position = None
        play = 0
        self.initialize_prints()
        self.Game_board.update()
        # Game loop
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        print("Gold player skips first turn.")
                        turn = -1

                if play == 0:
                    old_position = None

                if self.players[turn] == 'Human':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            position, self.board, self.gold_arr, self.silver_arr, turn, available_moves, play, old_position = self.run_player_turn(
                                position, self.board, self.gold_arr, self.silver_arr, turn, available_moves, play, old_position, event)
                            self.Game_board.update(available_moves)
                            if self.Game_board.winning_move(self.board) != 0:
                                print("Close game when you are ready...")
                                # pygame.time.wait(10000)
                                # running = False
                elif self.players[turn] == 'Random':
                    position, self.board, self.gold_arr, self.silver_arr, turn, available_moves, play, old_position = self.run_player_turn(
                        position, self.board, self.gold_arr, self.silver_arr, turn, available_moves, play,
                        old_position, None)
                    self.Game_board.update(available_moves)
                    pygame.time.wait(1000)
                    if self.Game_board.winning_move(self.board) != 0:
                        print("Close game when you are ready...")
                        # pygame.time.wait(10000)
                        # running = False
                elif self.players[turn] == 'MiniMax':
                    position, self.board, self.gold_arr, self.silver_arr, turn, available_moves, play, old_position = self.run_player_turn(
                        position, self.board, self.gold_arr, self.silver_arr, turn, available_moves, play,
                        old_position, sim=False)
                    print(old_position)
                    self.Game_board.update(available_moves)
                    if self.Game_board.winning_move(self.board) != 0:
                        print("Close game when you are ready...")
                        # pygame.time.wait(10000)
                        # running = False


        pygame.quit()