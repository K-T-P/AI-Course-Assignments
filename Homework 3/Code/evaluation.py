import numpy as np
import math

import game_functions as gf


def consistency(board : np.ndarray):
    """
    Returns score of consistency.
    Args:
        board : np.array ( np.ndarray ( shape (16) ) )
    Return:
        a float
    """
    score=0.0
    shape=np.shape(board)[0]
   # maxNum=max(np.copy(board).flatten())
    for i in range(4):
    #    if board[0,0]==maxNum:
     #       score+=maxNum
        for j in range(shape-1):
            if board[0,j]>=board[0,j+1] and board[0,j+1]!=0.0:
                score+=2
            if board[j,0]>=board[j+1,0] and board[j+1,0]!=0.0:
                score+=2
        np.rot90(board)
    return score


def neighborhood(board:np.ndarray):
    """
    Return score of neighborhood
    Args:
        board : np.array ( np.ndarray ( shape (16) ) )
    Return:
        a float
    """    
    score=0.0
    shape=np.shape(board)
    for i in range(shape[0]-1):
        for j in range(shape[0]-1):
            if board[i,j]==board[i+1,j]:
                score+=(2*board[i,j])
            if board[i,j]==board[i,j+1]:
                score+=(2*board[i,j])
    return score

def evaluate_state(board: np.ndarray) -> float:
    """
    Returns the score of the given board state.
    :param board: The board state for which the score is to be calculated.
    :return: The score of the given board state.
    """
    # TODO: Complete evaluate_state function to return a score for the current state of the board
    # Hint: You may need to use the np.nonzero function to find the indices of non-zero elements.
    # Hint: You may need to use the gf.within_bounds function to check if a position is within the bounds of the board.

    return neighborhood(board)
