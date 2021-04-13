import pygame
from player import *
import random
from os import listdir
from os.path import isfile, join

# loading the images into a dictionary

files = [f[:-4] for f in listdir(r"C:\Users\Jerome159\Desktop\Tech\Python Projects\Uno\image") if
         isfile(join(r"C:\Users\Jerome159\Desktop\Tech\Python Projects\Uno\image", f))]

image_dictionary = {}
for x in files:
    image_dictionary[x] = pygame.image.load(
        r"C:\Users\Jerome159\Desktop\Tech\Python Projects\Uno\image\{0}.png".format(x))

image_dictionary["background"] = pygame.transform.scale(image_dictionary["background"], (1200, 800))


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
        self.players_in_game = [i for i in range(len(self.player_list))]
        self.winners = []

    def check_victory(self, player_number):
        if len(self.player_list[player_number].card_list) <= 1:
            self.winners.append(player_number)
            self.players_in_game.remove(player_number)
            return True
        else:
            return False

    def update_deck(self, d):
        if len(d < 100):
            random.shuffle(self.discard_pile)
            d = d + self.discard_pile

    def move_effect(self, player_number, card_attempted, d):
        if self.player_list[player_number].card_list[card_attempted].content == "reverse":
            self.increment *= -1
        elif self.player_list[player_number].card_list[card_attempted].content == "draw_two":
            self.draw_one_card(player_number + self.increment, d)
            self.draw_one_card(player_number + self.increment, d)
        elif self.player_list[player_number].card_list[card_attempted].content == "skip":
            self.update_turn()
        elif self.player_list[player_number].card_list[card_attempted].content == "wild_card":
            self.find_previous_player()
        elif self.player_list[player_number].card_list[card_attempted].content == "wild_draw_four":
            self.draw_one_card(player_number + self.increment, d)
            self.draw_one_card(player_number + self.increment, d)
            self.draw_one_card(player_number + self.increment, d)
            self.draw_one_card(player_number + self.increment, d)
            self.find_previous_player()

    def update_turn(self):
        self.find_next_player()
        if self.card_displayed.colour != '':
            self.current_colour = self.card_displayed.colour

    def valid_move(self, player_number, card_attempted):
        if card_attempted == "draw card":
            return False
        if card_attempted == "next player":
            return False
        if card_attempted in ["red", "green", "blue", "yellow"]:
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

    def find_next_player(self):
        if self.players_in_game:
            ind = self.players_in_game.index(self.turn_number)
            ind += 1
            ind %= len(self.players_in_game)
            self.turn_number = self.players_in_game[ind]

    def find_previous_player(self):
        if self.players_in_game:
            ind = self.players_in_game.index(self.turn_number)
            ind -= 1
            ind %= len(self.players_in_game)
            self.turn_number = self.players_in_game[ind]


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
    add_card_to_deck("red", "draw_two")
    add_card_to_deck("red", "draw_two")
    add_card_to_deck("green", "draw_two")
    add_card_to_deck("green", "draw_two")
    add_card_to_deck("yellow", "draw_two")
    add_card_to_deck("yellow", "draw_two")
    add_card_to_deck("blue", "draw_two")
    add_card_to_deck("blue", "draw_two")

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

    add_card_to_deck("", "wild_card")
    add_card_to_deck("", "wild_card")
    add_card_to_deck("", "wild_draw_four")
    add_card_to_deck("", "wild_draw_four")


def find_image(card):
    if isinstance(card.content, int) or card.colour == "":
        return image_dictionary[card.colour + str(card.content)]
    else:
        return image_dictionary[card.colour + "_" + str(card.content)]


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
