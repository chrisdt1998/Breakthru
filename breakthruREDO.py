import numpy as np
import time
import pygame

pygame.init()


class Player:
    pass





if __name__ == '__main__':
    game_board = Board()
    ## Which player is the gold player and consequently, which player plays first
    is_gold_player = True
    ## Setting up the board
    length = 50
    number_of_silvers = 20
    number_of_golds = 12

    pygame.display.set_caption("Breakthru")
    x_axis = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
    game = Game(game_board)
    game.start()



