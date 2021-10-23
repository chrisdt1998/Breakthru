import numpy as np
import time
import pygame
from board import Board
from random_AI import Random_AI

pygame.init()

class Game:
    def __init__(self, game_board, length):
        self.game_board = game_board
        self.board = game_board.board
        self.gold_arr = game_board.gold_array
        self.silver_arr = game_board.silver_array
        self.player_turn = 'Gold'
        self.length = length

    def initialize_prints(self):
        print("Game started...")
        print("Gold player plays first.")
        print("Press n to skip first turn.")

    def is_in_arr(self, position, array):
        return np.argwhere(np.logical_and(array[:, 0] == position[0], array[:, 1] == position[1]))

    def run_player_turn(self, player, event, position, board, gold_array, silver_array, turn, available_moves, play, old_position=None):
        player_turn = {1: 'Gold', -1: 'Silver'}
        if player_turn[turn] == 'Gold':
            player_arr = gold_array
            opp_arr = silver_array
        else:
            player_arr = silver_array
            opp_arr = gold_array

        if position is None:
            if player == "Random":
                position = Random_AI.choose_move()
            else:
                position = (np.floor(np.array(event.pos) / self.length)).astype(int)
                position = position[::-1]
            if self.is_in_arr(position, player_arr).size > 0:
                print("check 1")
                if old_position is None or (old_position is not None and (old_position != position).any()):
                    print("check 2")
                    straight_moves = Board.straight_moves(position, silver_array, gold_array)

                    if play == 0:
                        elim_moves = Board.elim_moves(position, opp_arr)
                        available_moves = np.concatenate([x for x in [elim_moves, straight_moves] if x.size > 0])
                    else:
                        available_moves = straight_moves

                    self.game_board.update_board(self.length, board, available_moves)
                else:
                    position = None
            else:
                position = None

        else:
            if player == "Random":
                new_position = Random_AI.choose_move()
            else:
                new_position = np.floor(np.array(event.pos) / self.length).astype(int)
                new_position = new_position[::-1]
            if self.is_in_arr(new_position, available_moves).size > 0:
                old_position = new_position
                board, gold_array, silver_array, elimination = self.game_board.moveFunct(board, position, new_position,
                                                                                         gold_array, silver_array)
                available_moves = None
                self.game_board.update_board(self.length, board)

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