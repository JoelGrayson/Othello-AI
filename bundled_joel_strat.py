import numpy as np

# <Utils
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
# >

# <Heuristic
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
# >

# <Constants
INFINITY=99999999999 #instead of float(-inf) so it is an int, not a float
NEGATIVE_INFINITY=-99999999999
PASS_MOVE=(-1, -1)
SIZE=8
NUM_SQUARES=SIZE*SIZE
max_depth=3 #variable
# >

def get_move(board, turn, time_left_seconds):
    # TODO: change depth based on time_left
    move: moveT=ab_prune(NEGATIVE_INFINITY, INFINITY, PASS_MOVE, turn, board, 0)['best_move'] #type: ignore
    return move

getMove=get_move #exported as camelCase

def number_of_blank_moves_left(board):
    return len(np.where(board==0)[0])

def ab_prune(
    alpha_score,
    beta_score,
    move,
    turn, #1 = black = max, -1 = white = min
    board,
    depth=0,
):
    # base case
    if check_terminal(board): #game over
        black_score, white_score=get_score(board)
        if black_score>white_score: #max wins
            return {'score': INFINITY-1, 'best_move': move }
        if white_score>black_score: #min wins
            return {'score': NEGATIVE_INFINITY+1, 'best_move': move }
        if white_score==black_score: #tie
            return { 'score': 0, 'best_move': move }
    
    all_moves=get_all_moves(board, turn)

    if len(all_moves)==0: #no legal moves
        return {
            "best_move": (-1, -1),
            "score": ab_prune(alpha_score, beta_score, move, -turn, board, depth+1)['score']
        }


    if depth>max_depth and number_of_blank_moves_left(board)>8: #exceeded depth and still have to recurse more (so use heuristic not continue calculating)
        return {
            "best_move": move,
            "score": heuristic(board)
        }

    # recursive step
    # best_move_score: move_scoreT={
    #     "best_move": None,
    #     "score": None
    # }
    # alpha or beta is score
    best_move=None

    for move in all_moves:
        new_board=board.copy()
        stones_to_flip=check_move(new_board, move[0], move[1], turn)
        for stone in stones_to_flip:
            new_board[stone]=turn
        new_board[move]=turn
        
        new_score=ab_prune(
            alpha_score,
            beta_score,
            move,
            -turn,
            new_board,
            depth+1
        )['score'] #type: ignore

        if turn==1: #max
            # custom max/min function
            if new_score>alpha_score: #type: ignore # better score
                best_move=move
                alpha_score=new_score
        if turn==-1: #min
            if new_score<beta_score: #type: ignore # better score
                best_move=move
                beta_score=new_score

        if alpha_score>beta_score: #pruning
            return {
                "best_move": best_move,
                "score": alpha_score if turn==1 else beta_score #undesriable
            }
    
    if turn==1:
        return {
            "best_move": best_move,
            "score": alpha_score
        }
    if turn==-1:
        return {
            "best_move": best_move,
            "score": beta_score
        }
    


def get_all_moves(board, turn):
    moves=[]
    for row in range(SIZE):
        for col in range(SIZE):
            if check_move(board, row, col, turn):
                moves.append((row, col))
    return moves
