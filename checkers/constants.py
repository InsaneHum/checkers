import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8  # how may rows and cols in the checkerboard
SQUARE_SIZE = WIDTH // ROWS  # size of each square

# rgb
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)


CROWN = pygame.transform.scale((pygame.image.load('crown.png')), (45, 25))  # load and resize the image
