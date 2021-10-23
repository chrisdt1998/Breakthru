import numpy as np
import pygame

from board import Board

pygame.init()

class Random_AI:
    def __init__(self):
        pass

    @staticmethod
    def choose_move(piece, silver_array, gold_array, opp_arr):
        straight_moves = Board.straight_moves(piece, silver_array, gold_array)
        elim_moves = Board.elim_moves(piece, opp_arr)
        available_moves = np.concatenate([x for x in [elim_moves, straight_moves] if x.size > 0])
        move = np.random.randint(0, available_moves.shape[0])
        print("From ", available_moves.shape[0], "available moves, random move chosen is: ", available_moves[move])

        return available_moves[move]