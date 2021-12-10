import numpy as np
import pygame
from game import Game
from board import Board
from random_AI import Random_AI
from minimax_AI import Minimax_AI

pygame.init()


class Player:
    pass





if __name__ == '__main__':

    ## Which player is the gold player and consequently, which player plays first
    is_gold_player = True
    ## Setting up the board
    length = 50
    number_of_silvers = 20
    number_of_golds = 12

    pygame.display.set_caption("Breakthru")
    x_axis = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
    Game_board = Board(length)
    Random_AI = Random_AI(Game_board)
    Minimax_AI = Minimax_AI(Game_board, 'Silver')

    player_1 = 'Human'
    # player_2 = 'Random'
    player_2 = 'MiniMax'
    search_depth = 4
    Game = Game(Game_board, length, Random_AI, Minimax_AI, search_depth, player_1, player_2)
    Minimax_AI.initialize_game(Game)
    Game.start()



