from .constants import *


class Piece:
    PADDING = 14  # padding to calculate radius
    OUTLINE = 3  # outline for the drawn circle

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False  # set to True if promoted to king
        self.selected = False

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):  # calculate x and y pos based on row and column the piece is in
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2  # set coords to center of square with + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        if self.selected:  # if piece is selected, draw highlight
            pygame.draw.circle(win, GREEN, (self.x, self.y), radius + self.OUTLINE + 3)

        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)  # draw a bigger circle to use as outline
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)  # draw smaller circle that overlaps the bigger one to create outline
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))  # center the crown

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):  # create repr for piece object
        return str(self.color)  # return color of piece
