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
        for num in game.player_list[player_number].card_list:
            textsurface = myfont.render(str(num), False, (0, 0, 0))
        window.blit(textsurface, (300, 370))
    elif game.winner == player_number:

        textsurface = myfont.render('You win!', False, (0, 0, 0))
    elif game.winner != player_number:
        textsurface = myfont.render('You lose!', False, (0, 0, 0))

    pygame.display.update()
