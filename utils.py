# check_move, score, check_terminal
SIZE=8

#returns if the game is over
def check_terminal(board, check=[-1,1]) -> bool:
    for t in check: # check both players if necessary
        for i in range(SIZE):
            for j in range(SIZE):
                # only run checkMove if spot is empty
                # since checkMove is expensive
                if board[i,j] == 0:
                    if check_move(board, i, j, t):
                        return False
    return True

def get_score(board):
    score_black = 0
    score_white = 0

    # loop through board, count stones
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r,c] == 1:
                score_black += 1
            elif board[r,c] == -1:
                score_white += 1
    return (score_black, score_white)


def check_move(board,row, col, turn):
    # position is not empty
    if board[row, col] != 0:
        return []
    stonesToFlip = []
    rows,cols = board.shape

    # 8 directions
    #			  down	  up	  right	  left	  dr 	  dl	   ur		ul  
    directions = [(1,0), (-1, 0), (0,1), (0,-1), (1, 1), (1, -1), (-1,1), (-1, -1)]
    for d in directions:
        flank = False
        r = row + d[0] # first position we're checking
        c = col + d[1] # in the current direction

        # temporary list of positions to flip
        # don't know if accurate until we find that the stones are surrounded
        tempflips = []
        # while we're still on the board

        while r >= 0 and r < rows and c >= 0 and c < cols:
            # first we should find stones of opponts color
            if board[r,c] == -turn:
                flank = True
                tempflips.append((r,c))# opponent stones we might flip

            # then a stone of our color, so the line is surrounded
            elif board[r,c] == turn:
                if flank: # found stones of opponent color surrounded by our color
                    stonesToFlip += tempflips
                    break 

                else: # if no stones of opponents color
                    break # break without adding any stones

            else: # found a blank spot when expecting something else
                break # break without adding any stones

            r += d[0] # next 
            c += d[1] # position

        # if we reached the end of the loop without finding flanked stones, no stones are added
    # We've searched all directions
    return stonesToFlip
