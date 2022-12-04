# Pseudocode
```ts
const NEGATIVE_INFINITY
const INFINITY
let depth_limit //global but modifiable

type scoreT=int
type moveT=(int, int)
type move_scoreT={ score: scoreT | null, best_move: moveT | null }

heuristic()
    pass

get_all_moves(board, turn): moveT[]
    moves=[]
    for every square on the board:
        if can move there, add to moves
    return moves

get_move(board, turn, time_left): moveT
    change depth based on time_left
    return ab_prune(NEGATIVE_INFINITY, INFINITY, null, turn, board, 0).best_move

ab_prune(
    alpha_score: scoreT
    beta_score: scoreT
    move: moveT
    turn: 1 | -1, //1 = black = max, -1 = white = min
    board: numpy board
    depth: int
): move_scoreT
    all_moves=get_all_moves()
    
    // base case
    if check_terminal(board) //game is over
        if winner is max
            return INFINITY
        if winner is min
            return NEGATIVE_INFINITY
    
    if all_moves.length==0 //no legal moves
        return { best_move: (-1, -1), score: ab_prune(of other turn...).score }
    
    if depth>depth_limit: //depth limit exceeded
        return { best_move: move, heuristic(score) }
    
    // recursive step
    best_move_score: move_scoreT={
        best_move: null,
        score: null
    }
    for move in all_moves //loop over moves
        new_board=board moved to move //flip every stone
        score=ab_prune(
            alpha_score,
            beta_score,
            move,
            opposite turn,
            new_board,
            depth+1
        )
        if turn==1
            if score>best_move_score.score or best_move.best_move==null or best_move.score==null //better score
                best_move_score.best_move=move
                best_move_score.score=score
                alpha_score=score
        if turn==-1
            if score<best_move_score.score or best_move_score.score==null //better score
                best_move_score.best_move=move
                best_move_score.score=score
                beta_score=score

        if alpha_score>beta_score //pruning
            return best_move_score

    if turn==1
        return best_move_score
    if turn==-1
        return best_move_score

```


# Brainstorming
* Going up every level, the score is updated as the max of the children's scores
    * Alpha or beta are updated based on what the turn is

