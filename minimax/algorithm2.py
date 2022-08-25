from copy import deepcopy
import pygame
from checkers.constants import RED, WHITE


# algorithm that takes a board object, and evaluates and returns a new board with the best outcome for the ai
def minimax(position, depth, alpha, beta, max_player,
            game):  # position = board, max_player = minimize or maximize the score
    if depth == 0 or position.winner() is not None:  # if the algorithm has reached the last layer or there is a winner
        return position.evaluate(), position

    if max_player:  # if maximize score
        maxEval = float(
            '-inf')  # set maxEval to negative infinity so that the next score will be larger than it and be taken
        best_move = None
        for move in get_all_moves(position, WHITE, game):  # for every possible move
            evaluation = minimax(move, depth - 1, alpha, beta, False, game)[0]  # evaluate that move by recursively calling minimax
            maxEval = max(maxEval, evaluation)  # update maxEval by comparing it with the evaluation of the new move
            alpha = max(alpha, evaluation)
            if maxEval == evaluation:  # if found best move, set best move to this move
                best_move = move
            if beta <= alpha:
                break

        return maxEval, best_move

    else:  # if minimize score
        minEval = float('inf')  # set maxEval to infinity so that the next score will be smaller than it and be taken
        best_move = None
        for move in get_all_moves(position, RED, game):  # for every possible move
            evaluation = minimax(move, depth - 1, alpha, beta, True, game)[0]  # evaluate that move by recursively calling minimax
            minEval = min(minEval, evaluation)  # update minEval by comparing it with the evaluation of the new move
            beta = min(beta, evaluation)
            if minEval == evaluation:  # if found best move, set best move to this move
                best_move = move
            if beta <= alpha:
                break

        return minEval, best_move


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])  # move the piece to the new square
    if skip:  # if we skipped(captured) over a piece
        board.remove(skip)
    return board


def get_all_moves(board, color, game):
    moves = []  # new board if we move the piece to a certain location
    for piece in board.get_all_pieces(color):  # get every piece for this color
        valid_moves = board.get_valid_moves(piece)  # and get every valid move for the pieces of that color
        for move, skip in valid_moves.items():  # move coords, skipped(captured) piece
            draw_moves(game, board, piece)
            temp_board = deepcopy(board)  # make a deep copy of the board
            temp_piece = temp_board.get_piece(piece.row, piece.col)  # make a temp piece with the copy of the board
            new_board = simulate_move(temp_piece, move, temp_board, game,
                                      skip)  # return a new board that have made a move onto
            moves.append(new_board)
    return moves


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    # pygame.time.delay(100)
