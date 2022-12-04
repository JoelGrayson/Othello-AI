# ABOUT: used for testing
# Returns a random legal move

from utils import check_move
import random
SIZE=8

def get_all_moves(board, turn):
    moves=[]
    for row in range(SIZE):
        for col in range(SIZE):
            if check_move(board, row, col, turn):
                moves.append((row, col))
    return moves

def getMove(board, color, time_left):
    moves=get_all_moves(board, color)
    if moves==[]:
        return (-1, -1)
    return random.choice(moves)
