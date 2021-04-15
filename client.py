import pygame
from network import Network
from game import *

width = 1200
height = 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Uno")
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)


def draw_window(window, card_to_display, player_deck, player_number, draw_card, play_or_keep, choose_colour,
                current_colour, current_player):
    window.fill((255, 255, 255))
    window.blit(image_dictionary["background"], (0, 0))
    # if game.winner == "none":
    if True:
        for i in range(len(player_deck)):
            window.blit(pygame.transform.scale(find_image(player_deck[i]), (84, 129)), (50 + 84 * i, 600))
            # textsurface = myfont.render(player_deck[i].__str__(), False, (0, 0, 0))
            # window.blit(textsurface, (50, 85 + 35 * i))
        if card_to_display != "none":
            window.blit(find_image(card_to_display), (500, 200))
        if draw_card:
            textsurface = myfont.render('Draw Card', False, (0, 0, 0))
            window.blit(textsurface, (1000, 550))
        # elif game.winner == player_number:
        #
        #     textsurface = myfont.render('You win!', False, (0, 0, 0))
        # elif game.winner != player_number:
        #     textsurface = myfont.render('You lose!', False, (0, 0, 0))
        if play_or_keep:
            textsurface = myfont.render('Play it', False, (0, 0, 0))
            window.blit(textsurface, (1000, 590))
            textsurface = myfont.render('Keep it', False, (0, 0, 0))
            window.blit(textsurface, (1000, 625))
        if choose_colour:
            pygame.draw.rect(window, (237, 28, 36), (300, 300, 150, 150))  # red
            pygame.draw.rect(window, (80, 170, 68), (450, 300, 150, 150))  # green
            pygame.draw.rect(window, (0, 114, 188), (600, 300, 150, 150))  # blue
            pygame.draw.rect(window, (255, 222, 22), (750, 300, 150, 150))  # yellow
        if current_colour != "none":
            textsurface = myfont.render('Colour: ', False, (0, 0, 0))
            window.blit(textsurface, (1000, 210))
            pygame.draw.rect(window, colour02[current_colour], (1115, 210, 50, 50))
        if current_player != -1:
            textsurface = myfont.render('Turn: Player ' + str(current_player), False, (0, 0, 0))
            window.blit(textsurface, (1000, 160))
        textsurface = myfont.render("You are Player " + str(player_number), False, (0, 0, 0))
        window.blit(textsurface, (100, 550))
    pygame.display.update()


def get_card_played(pos, number_of_cards):
    if 0 < (pos[0] - 50) < 50 and 0 <= ((pos[1] - 85) // 35) < number_of_cards:
        return (pos[1] - 85) // 35


colours = {0: "red", 1: "green", 2: "blue", 3: "yellow"}
winner_list = {0: "winner", 1: "2nd", 2: "3rd", 3: "4th", 4: "5th", 5: "6th", 6: "7th", 7: "8th", 8: "9th", 9: "10th"}
colour02 = {"red": (237, 28, 36), "green": (80, 170, 68), "blue": (0, 114, 188), "yellow": (255, 222, 22)}


def main():
    run = True
    n = Network()
    info = n.get_number()
    player_number = info[0]
    player_deck = info[1:]
    others_card_number = []
    card_attempted = 'none'
    card_played = 'none'
    drew_card = False
    card_drawn_playable = False
    choose_colour = False
    can_play = True
    current_colour = 'none'
    current_player = -1
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 0 <= (pos[0] - 50) // 84 < len(player_deck) and 600 < pos[1] < 729 and not drew_card:
                    card_attempted = (pos[0] - 50) // 84
                    c = player_deck[card_attempted]
                    print(1)
                    player_deck, others_card_number, card_played, can_play, current_colour, current_player = n.send(
                        [player_number, card_attempted])
                    print(2)
                    if c.__str__() == card_played.__str__() and c.colour == "":
                        choose_colour = True
                    card_attempted = "none"
                if 1000 < pos[0] < 1100 and 550 < pos[1] < 600 and not drew_card:
                    # player_deck, others_card_number, card_played, card_drawn_playable
                    info = n.send([player_number, "draw card"])
                    card_drawn_playable = info[-3]
                    drew_card = True
                if choose_colour:
                    if 300 < pos[0] < 900 and 300 < pos[1] < 450:
                        colour_chosen = (pos[0] - 300) // 150
                        print(colours[colour_chosen])
                        n.send([player_number, colours[colour_chosen]])
                        choose_colour = False
                if card_drawn_playable and drew_card:
                    if 1000 < pos[0] < 1100 and 590 < pos[1] < 625:
                        c = player_deck[-1]
                        player_deck, others_card_number, card_played, can_play, current_colour, current_player = n.send(
                            [player_number, -1])
                        if c.__str__() == card_played.__str__() and c.colour == "":
                            choose_colour = True
                        card_drawn_playable = False
                        drew_card = False
                        can_play = True
                    elif 1000 < pos[0] < 1100 and 625 < pos[1] < 660:
                        n.send([player_number, "next player"])
                        card_drawn_playable = False
                        drew_card = False

                if not card_drawn_playable and drew_card:
                    n.send([player_number, "next player"])
                    print("got here")
                    drew_card = False
        information = n.send([player_number, card_attempted])
        player_deck = information[0]
        others_card_number = information[1]
        card_played = information[2]
        can_play = information[3]
        current_colour = information[4]
        current_player = information[5]
        # print(card_drawn_playable)
        draw_window(win, card_played, player_deck, player_number, not can_play, card_drawn_playable, choose_colour,
                    current_colour, current_player)


main()
