import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE  # .relative import, use a . when importing files from the same module
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []  # internal board representation as a 2d list
        self.red_left = self.white_left = 12  # set number of pieces for both sides
        self.red_kings = self.white_kings = 0  # set number of kings for both sides to 0
        self.create_board()  # create the board

    def draw_squares(self, win):  # function to draw the squares on the screen
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):  # draw a red square every two square_sizes
                pygame.draw.rect(win, WHITE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  # x, y, width, height

    def evaluate(self):  # calculate the score for the minimax algorithm
        piece_tv = self.white_left - self.red_left + (self.white_kings * 2 - self.red_kings * 2)
        return piece_tv

    def get_all_pieces(self, color):  # get all possible moves for red or white
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]  # swap the squares to move piece
        piece.move(row, col)  # move the piece

        if row == ROWS - 1 or row == 0:  # make the piece a king if it reaches the last row
            piece.make_king()
            if piece.color == WHITE:  # add the number of total white kings if piece is white
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):  # create internal representation of the board (2d list)
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))  # append white pieces at the first three rows
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))  # append red pieces at the last three rows
                    else:
                        self.board[row].append(0)  # append a zero as a blank piece
                else:
                    self.board[row].append(0)

    def clear_selected(self):
        for row in self.board:
            for piece in row:
                if piece != 0:
                    piece.selected = False

    def draw(self, win):  # draw all the pieces on the screen
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:  # return white as winner if there are no red pieces left
            return WHITE
        elif self.white_left <= 0:
            return RED

        return None  # return None if no one wins

    def filter_moves(self, moves):
        moves = {k: v for k, v in sorted(moves.items(), key=lambda x: len(x[1]), reverse=True)}

        new = {}
        big = 0
        for k, v in moves.items():

            if len(v) == 0:
                new[k] = v
            else:
                if len(v) > big:
                    big = len(v)
                    new[k] = v

        return new

    def get_valid_moves(self, piece):  # algorithm to figure out which moves are valid for the selected piece
        moves = {}  # dict to store valid moves (key = valid move, value = captured pieces)

        # get the left and right diagonals of the current piece
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        # check move up or move down based on the piece's color and if piece is king
        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))  # check upwards 2 rows for valid moves
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))

        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))  # check downwards 2 rows for valid moves
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=None):
        if skipped is None:
            skipped = []
        moves = {}
        last = []

        for r in range(start, stop, step):  # r = row, step = up or down
            if left < 0:  # if the left of the square is not in the board
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:  # if jumped once and no more pieces to jump
                    break
                elif skipped:  # if jumped once and can jump one more time
                    moves[(r, left)] = last + skipped
                else:  # if jumped once
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)

                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break

            elif current.color == color:  # break if the pieces are the same color
                break

            else:  # set last to current location if the current piece is a different color
                last = [current]

            left -= 1

        return self.filter_moves(moves)

    def _traverse_right(self, start, stop, step, color, right, skipped=None):
        if skipped is None:
            skipped = []
        moves = {}
        last = []

        for r in range(start, stop, step):  # r = row, step = up or down
            if right >= COLS:  # if the left of the square is not in the board
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)

                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break

            elif current.color == color:
                break

            else:
                last = [current]
            right += 1

        return self.filter_moves(moves)