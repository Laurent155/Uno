import pygame
from player import *
import random


class Game:
    def __init__(self, player_list):
        self.turn_number = 0
        self.player_list = player_list
        self.winner = "none"
        self.game_going = True
        self.card_displayed = Card("none", "none")
        self.current_colour = 'none'
        self.increment = 1
        self.discard_pile = []

    def check_victory(self, player_number):
        if len(self.player_list[player_number].card_list) <= 1:
            return True
        else:
            return False

    def update_deck(self, d):
        if len(d < 70):
            random.shuffle(self.discard_pile)
            d = d + self.discard_pile

    def move_effect(self, player_number, card_attempted, d):
        if self.player_list[player_number].card_list[card_attempted].content == "reverse":
            self.increment *= -1
        elif self.player_list[player_number].card_list[card_attempted].content == "draw two":
            self.draw_one_card(player_number + self.increment, d)
            self.draw_one_card(player_number + self.increment, d)
        elif self.player_list[player_number].card_list[card_attempted].content == "skip":
            self.update_turn()
        elif self.player_list[player_number].card_list[card_attempted].content == "wild card":
            self.set_colour(player_number)
        elif self.player_list[player_number].card_list[card_attempted].content == "wild draw four":
            self.set_colour(player_number)
            self.draw_one_card(player_number + self.increment, d)
            self.draw_one_card(player_number + self.increment, d)
            self.draw_one_card(player_number + self.increment, d)
            self.draw_one_card(player_number + self.increment, d)

    def update_turn(self):
        self.turn_number += self.increment
        self.turn_number %= len(self.player_list)
        if self.card_displayed.colour != '':
            self.current_colour = self.card_displayed.colour

    def valid_move(self, player_number, card_attempted):
        if card_attempted == "draw card":
            return False
        if card_attempted == "next player":
            return False
        elif self.turn_number == player_number and card_attempted != "none":
            if self.current_colour == "none":
                return True
            elif self.player_list[player_number].card_list[card_attempted].colour == '':
                return True
            elif self.current_colour == self.player_list[player_number].card_list[card_attempted].colour:
                return True
            elif self.card_displayed.content == self.player_list[player_number].card_list[card_attempted].content:
                return True
        else:
            return False

    def valid_draw(self, player_number):
        return True

    def generate_reply(self, player_number, card_attempted):
        if card_attempted != "none":
            self.card_displayed = self.player_list[player_number].card_list[card_attempted]
            player_deck = self.player_list[player_number].card_list
            self.discard_pile.append(player_deck[card_attempted])
            del player_deck[card_attempted]
            others_card_number = []
            for i in self.player_list:
                others_card_number.append(len(i.card_list))
            reply = [player_deck, others_card_number, self.card_displayed]
            return reply
        elif card_attempted == "none" and self.card_displayed.colour == "none":
            player_deck = self.player_list[player_number].card_list
            others_card_number = []
            for i in self.player_list:
                others_card_number.append(len(i.card_list))
            reply = [player_deck, others_card_number, "none"]
            return reply
        elif card_attempted == "none" and self.card_displayed.colour != "none":
            player_deck = self.player_list[player_number].card_list
            others_card_number = []
            for i in self.player_list:
                others_card_number.append(len(i.card_list))
            reply = [player_deck, others_card_number, self.card_displayed]
            return reply

    def generate_reply02(self, player_number):
        if self.card_displayed.colour == "none":
            player_deck = self.player_list[player_number].card_list
            others_card_number = []
            for i in self.player_list:
                others_card_number.append(len(i.card_list))
            reply = [player_deck, others_card_number, "none"]
            return reply
        elif self.card_displayed.colour != "none":
            player_deck = self.player_list[player_number].card_list
            others_card_number = []
            for i in self.player_list:
                others_card_number.append(len(i.card_list))
            reply = [player_deck, others_card_number, self.card_displayed]
            return reply

    def draw_one_card(self, player_number, d):
        self.player_list[player_number].card_list.append(d[0])
        player_deck = self.player_list[player_number].card_list
        self.discard_pile.append(d[0])
        del d[0]
        others_card_number = []
        for i in self.player_list:
            others_card_number.append(len(i.card_list))
        reply = [player_deck, others_card_number, self.card_displayed]
        return reply

    def set_colour(self, player_number):
        pass


class Card:
    def __init__(self, colour, content):
        self.colour = colour
        self.content = content

    def __str__(self):
        return self.colour + " " + str(self.content)


deck = []


def add_card_to_deck(colour, content):
    card = Card(colour, content)
    deck.append(card)


def generate_deck():
    for i in range(0, 10):
        if i == 0:
            add_card_to_deck("red", i)
        else:
            add_card_to_deck("red", i)
            add_card_to_deck("red", i)
    for i in range(0, 10):
        if i == 0:
            add_card_to_deck("green", i)
        else:
            add_card_to_deck("green", i)
            add_card_to_deck("green", i)
    for i in range(0, 10):
        if i == 0:
            add_card_to_deck("yellow", i)
        else:
            add_card_to_deck("yellow", i)
            add_card_to_deck("yellow", i)
    for i in range(0, 10):
        if i == 0:
            add_card_to_deck("blue", i)
        else:
            add_card_to_deck("blue", i)
            add_card_to_deck("blue", i)
    add_card_to_deck("red", "draw two")
    add_card_to_deck("red", "draw two")
    add_card_to_deck("green", "draw two")
    add_card_to_deck("green", "draw two")
    add_card_to_deck("yellow", "draw two")
    add_card_to_deck("yellow", "draw two")
    add_card_to_deck("blue", "draw two")
    add_card_to_deck("blue", "draw two")

    add_card_to_deck("red", "skip")
    add_card_to_deck("red", "skip")
    add_card_to_deck("green", "skip")
    add_card_to_deck("green", "skip")
    add_card_to_deck("yellow", "skip")
    add_card_to_deck("yellow", "skip")
    add_card_to_deck("blue", "skip")
    add_card_to_deck("blue", "skip")

    add_card_to_deck("red", "reverse")
    add_card_to_deck("red", "reverse")
    add_card_to_deck("green", "reverse")
    add_card_to_deck("green", "reverse")
    add_card_to_deck("yellow", "reverse")
    add_card_to_deck("yellow", "reverse")
    add_card_to_deck("blue", "reverse")
    add_card_to_deck("blue", "reverse")

    add_card_to_deck("", "wild card")
    add_card_to_deck("", "wild card")
    add_card_to_deck("", "wild draw four")
    add_card_to_deck("", "wild draw four")


def shuffle():
    random.shuffle(deck)


def deal_card(d, number_of_players):
    player_list = []
    for i in range(number_of_players):
        player = Player(i, d[:7])
        player_list.append(player)
        d = d[7:]
    return player_list


generate_deck()
shuffle()
