import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE
from checkers.game import Game


FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()  # use pygame.time.Clock() create clock object to cap FPS
    game = Game(WIN)

    while run:
        clock.tick(FPS)  # limit FPS

        if game.winner() is not None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # terminate the main loop if the quit button is pressed
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:  # check for every mouse button press (LMB, RMB, etc)
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()  # close the application when the main loop ends


main()
