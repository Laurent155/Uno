import pygame
from player import *


class Game:
    def __init__(self, player_list):
        self.turn_number = 0
        self.player_list = player_list
        self.winner = "None"
        self.game_going = True

    def check_victory(self, deck):
        pass

    def update_player_deck(self, player_number, deck):
        self.player_list[player_number].card_list = deck

    def update_turn(self, increment):
        self.turn_number += increment

    def valid_move(self, player):
        if self.turn_number == player.number:
            return True


