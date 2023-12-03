import numpy as np
import math

import game_functions as gf


def neighborhoob(board : np.ndarray):
    """
    Returns score of consistency.
    Args:
        board : np.array ( np.ndarray ( shape (16) ) )
    Return:
        a float
    """
    score=0.0
    for i in range(3):
        for j in range(3):
            if board[i,j]==board[i,j+1]:
                score+=(2*board[i,j])
            if board[i,j]==board[i+1,j]:
                score+=(2*board[i,j])
    for i in range(3):
        if board[3,i]==board[3,i+1]:
            score+=(2*board[3,i])
        if board[i,3]==board[i+1,3]:
            score+=(2*board[i,3])
    return score

def consistency(board:np.ndarray):
    """
    Return score of neighborhood
    Args:
        board : np.array ( np.ndarray ( shape (16) ) )
    Return:
        a float
    """    
    
    scores = [0.0 for i in range(4)]
    for k in range(4):
        for i in range(3):
            for j in range(3):
                if board[i,j]>board[i,j+1]:
                    scores[k]+=board[i,j]
                if board[i,j]>board[i+1,j]:
                    scores[k]+=board[i,j]
        np.rot90(board)
    return scores

def evaluate_state(board: np.ndarray) -> float:
    """
    Returns the score of the given board state.
    :param board: The board state for which the score is to be calculated.
    :return: The score of the given board state.
    """
    # TODO: Complete evaluate_state function to return a score for the current state of the board
    # Hint: You may need to use the np.nonzero function to find the indices of non-zero elements.
    # Hint: You may need to use the gf.within_bounds function to check if a position is within the bounds of the board.

    if 2048 in board:
        return np.inf
    return neighborhoob(board) # 0 * consistency(board) 
