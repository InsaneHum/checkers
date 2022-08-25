import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from .board import Board


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):  # function to refresh the screen
        self.board.draw(self.win)  # draw the board
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()  # update the screen

    def _init(self):  # make a private method _init that initializes the game
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def reset(self):  # function to reset the game
        self._init()

    def select(self, row, col):  # function to handle selection of pieces
        if self.selected:  # if a piece is selected
            result = self._move(row, col)  # try to move the piece to where we pressed
            if not result:  # if not a valid square
                self.selected = None  # reset current selection
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0:
            if piece.color == RED:
                self.board.clear_selected()
                piece.selected = True  # highlight the selected piece

        if piece != 0 and piece.color == self.turn:  # if the selected piece is not a placeholder and is the current turn of the player
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def winner(self):
        return self.board.winner()

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:  # if the selected square is empty and the move is valid
            self.board.move(self.selected, row, col)  # move the piece to the selected square
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()  # change the turn
        else:
            return False  # return false if the square is not valid

        return True  # return true if the square is valid

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):  # change the player's turn
        self.valid_moves = []  # reset the valid moves
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):  # return the board object
        return self.board

    def ai_move(self, board):  # return the board which the AI has made its move on to update the screen
        self.board = board
        self.change_turn()
