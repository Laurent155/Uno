import pygame
from network import Network
from game import *

width = 800
height = 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Uno")
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)


def draw_window(window, card_to_display, player_deck, player_number):
    window.fill((255, 255, 255))
    # if game.winner == "none":
    if True:
        textsurface = myfont.render('Your cards are: ', False, (0, 0, 0))
        window.blit(textsurface, (50, 50))
        for i in range(len(player_deck)):
            textsurface = myfont.render(player_deck[i].__str__(), False, (0, 0, 0))
            window.blit(textsurface, (50, 85 + 35 * i))
        if card_to_display != "none":
            textsurface = myfont.render(card_to_display.__str__(), False, (0, 0, 0))
            window.blit(textsurface, (500, 200))
    # elif game.winner == player_number:
    #
    #     textsurface = myfont.render('You win!', False, (0, 0, 0))
    # elif game.winner != player_number:
    #     textsurface = myfont.render('You lose!', False, (0, 0, 0))

    pygame.display.update()


def get_card_played(pos, number_of_cards):
    if 0 < (pos[0] - 50) < 50 and 0 <= ((pos[1] - 85) // 35) < number_of_cards:
        return (pos[1] - 85) // 35


def main():
    run = True
    n = Network()
    info = n.get_number()
    player_number = info[0]
    player_deck = info[1:]
    others_card_number = []
    card_attempted = 'none'
    card_played = 'none'
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 0 < (pos[0] - 50) < 50 and 0 <= ((pos[1] - 85) // 35) < len(player_deck):
                    card_attempted = (pos[1] - 85) // 35
                    player_deck, others_card_number, card_played = n.send([player_number, card_attempted])
                    card_attempted = "none"

        information = n.send([player_number, card_attempted])
        player_deck = information[0]
        others_card_number = information[1]
        card_played = information[2]
        draw_window(win, card_played, player_deck, player_number)


main()
