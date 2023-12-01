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
                score+=(board[i,j])
            if board[i,j]==board[i+1,j]:
                score+=(board[i,j])
    for i in range(3):
        if board[3,i]==board[3,i+1]:
            score+=(board[3,i])
        if board[i,3]==board[i+1,3]:
            score+=(board[i,3])
    return score

def higherNumbers(board:np.ndarray):
    score=0.0
    for k in board.flatten():
        score+=k*k
    return score

def consistency(board:np.ndarray):
    """
    Return score of neighborhood
    Args:
        board : np.array ( np.ndarray ( shape (16) ) )
    Return:
        a float
    """    
    score1=0.0
    score2=0.0
    score3=0.0
    score4=0.0
    for i in range(4):
        for j in range(4):
            score1+=(3-i)*(3-j)*board[i,j]
    return score1

def evaluate_state(board: np.ndarray) -> float:
    """
    Returns the score of the given board state.
    :param board: The board state for which the score is to be calculated.
    :return: The score of the given board state.
    """
    # TODO: Complete evaluate_state function to return a score for the current state of the board
    # Hint: You may need to use the np.nonzero function to find the indices of non-zero elements.
    # Hint: You may need to use the gf.within_bounds function to check if a position is within the bounds of the board.

    return neighborhoob(board)#higherNumbers(board)+consistency(board)##+
