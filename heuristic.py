import numpy as np

square_weights = np.array([ #University of Washington othello board values
    [20, -3, 11, 8, 8, 11, -3, 20], 
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [11, -4, 2, 2, 2, 2, -4, 11], 
    [8, 1, 2, -3, -3, 2, 1, 8],
    [8, 1, 2, -3, -3, 2, 1, 8], 
    [11, -4, 2, 2, 2, 2, -4, 11],
    [-3, -7, -4, 1, 1, -4, -7, -3], 
    [20, -3, 11, 8, 8, 11, -3, 20]
])


def heuristic(board):
    multiplied=square_weights*board
    return multiplied.sum()



def parity_heuristic(board): #exported
    # parity: number of black - number of white stones
	return board.sum()
