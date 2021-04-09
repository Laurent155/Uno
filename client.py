import pygame
from network import Network
from game import *


width = 800
height = 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Uno")
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)


def draw_window(window, game, player_number):
    window.fill((255, 255, 255))
    if game.winner == "None":
        textsurface = myfont.render('Your cards are: ', False, (0, 0, 0))
        window.blit(textsurface, (300, 320))
        for i in range(len(game.player_list[player_number].card_list)):
            textsurface = myfont.render(str(game.player_list[player_number].card_list[i]), False, (0, 0, 0))
            window.blit(textsurface, (320 + i * 25, 370))
    elif game.winner == player_number:

        textsurface = myfont.render('You win!', False, (0, 0, 0))
    elif game.winner != player_number:
        textsurface = myfont.render('You lose!', False, (0, 0, 0))

    pygame.display.update()


def main():
    run = True
    n = Network()
    info = n.get_number()
    player_number = info[0]
    player_deck = info[1:]
    print(player_number, player_deck)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                updated_deck = player_deck + ["new card"]
                g = n.send(Player(player_number, updated_deck))

        g = n.send(Player(player_number, player_deck))
        print(g.winner)
        draw_window(win, g, player_number)


main()
