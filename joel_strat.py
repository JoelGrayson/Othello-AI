import numpy as np
from utils import check_move, check_terminal, get_score
from heuristic import heuristic

# <Typing
from typing import List, Tuple, Dict, Literal
scoreT=int
moveT=Tuple[int, int]
move_scoreT=Dict[Literal['score'] | Literal['best_move'], scoreT | moveT | None]
    # { score: scoreT | null, best_move: moveT | null }
    # need to use type: ignore whenever accessing dict's key ∵ of unknown typeof key
turnT=Literal[-1] | Literal[1]
boardT=np.ndarray
# >

# <Constants
INFINITY=99999999999 #instead of float(-inf) so it is an int, not a float
NEGATIVE_INFINITY=-99999999999
PASS_MOVE=(-1, -1)
SIZE=8
NUM_SQUARES=SIZE*SIZE
max_depth=4 #variable
# >

def get_move(board, turn, time_left_seconds) -> moveT:
    # TODO: change depth based on time_left
    move: moveT=ab_prune(NEGATIVE_INFINITY, INFINITY, PASS_MOVE, turn, board, 0)['best_move'] #type: ignore
    return move

getMove=get_move #exported as camelCase

def ab_prune(
    alpha_score: scoreT,
    beta_score: scoreT,
    move: moveT,
    turn: turnT, #1 = black = max, -1 = white = min
    board: boardT,
    depth: int=0,
) -> move_scoreT:
    all_moves=get_all_moves(board, turn)

    # base case
    if check_terminal(board): #game over
        black_score, white_score=get_score(board)
        if black_score>white_score: #max wins
            return {'score': INFINITY, 'best_move': move }
        if white_score>black_score: #min wins
            return {'score': NEGATIVE_INFINITY, 'best_move': move }
        if white_score==black_score: #tie
            return { 'score': 0, 'best_move': move }
    
    if len(all_moves)==0: #no legal moves
        return {
            "best_move": (-1, -1),
            "score": ab_prune(alpha_score, beta_score, move, -turn, board, depth+1)['score']
        }

    if depth>=max_depth: #exceeded depth
        return {
            "best_move": move,
            "score": heuristic(board)
        }

    # recursive case
    best_move_score: move_scoreT={
        "best_move": None,
        "score": None
    }

    for move in all_moves:
        new_board=board.copy()
        stones_to_flip=check_move(new_board, move[0], move[1], turn)
        for stone in stones_to_flip:
            new_board[stone]=turn
        
        new_score: scoreT=ab_prune(
            alpha_score,
            beta_score,
            move,
            -turn,
            new_board,
            depth+1
        )['score'] #type: ignore

        if turn==1: #max
            if best_move_score['score']==None or new_score>best_move_score['score']: #type: ignore
                # better score
                best_move_score['score']=new_score
                best_move_score['best_move']=move
                alpha_score=new_score
        if turn==-1: #min
            if best_move_score['score']==None or new_score<best_move_score['score']: #type: ignore
                # better score
                best_move_score['score']=new_score
                best_move_score['best_move']=move
                beta_score=new_score

        if alpha_score>beta_score: #pruning
            return best_move_score
    
    if turn==1:
        return best_move_score
    if turn==-1:
        return best_move_score
    


def get_all_moves(board, turn):
    moves: List[moveT]=[]
    for row in range(SIZE):
        for col in range(SIZE):
            if check_move(board, row, col, turn):
                moves.append((row, col))
    return moves
