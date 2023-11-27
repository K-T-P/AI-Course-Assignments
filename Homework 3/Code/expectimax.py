import numpy as np

import evaluation
import game_functions as gf


class Expectimax:
    def __init__(self, board):
        self.DEPTH_BASE_PARAM = 1 # You may change this parameter to scale the depth to which the agent searches.
        self.SCALER_PARAM = 400 # You may change this parameter to scale depth to which the agent searches.
        self.board = board

    def get_depth(self, move_number):
        """
        Returns the depth to which the agent should search for the given move number.
        ...
        :type move_number: int
        :param move_number: The current move number.
        :return: The depth to which the agent should search for the given move number.
        """
        # TODO: Complete get_depth function to return the depth to which the agent should search for the given move number.
        # Hint: You may need to use the DEPTH_BASE_PARAM constant.
        
        raise NotImplementedError("Get depth not implemented yet.")

    def ai_move(self, board, move_number):
        depth = self.get_depth(move_number)
        score, action = self.expectimax(board, depth, 1)
        return action

    def expectimax(self, board: np.ndarray, depth: int, turn: int):
        """
        Returns the best move for the given board state and turn.
        ...
        :type turn: int
        :type depth: int
        :type board: np.ndarray
        :param board: The board state for which the best move is to be found.
        :param depth: Depth to which agent takes actions for each move
        :param turn: The turn of the agent. 1 for AI, 0 for computer.
        :return: Returns the best move and score we can obtain by taking it, for the given board state and turn.
        """
        
        
        # TODO: Complete expectimax function to return the best move and score for the given board state and turn.
        # Hint: You may need to implement minimizer_node and maximizer_node functions.
        # Hint: You may need to use the evaluation.evaluate_state function to score leaf nodes.
        # Hint: You may need to use the gf.terminal_state function to check if the game is over.
        if turn:
            return self.maximizer_node(board,depth)
        else:
            return self.chance_node(board,depth)
        

    def maximizer_node(self, board: np.ndarray, depth: int):
        """
        Returns the best move for the given board state and turn.
        ...
        :type depth: int
        :type board: np.ndarray
        :param board: The board state for which the best move is to be found.
        :param depth: Depth to which agent takes actions for each move
        :return: Returns the move with highest score, for the given board state.
        """
        
        # TODO: Complete maximizer_node function to return the move with highest score, for the given board state.
        # Hint: You may need to use the gf.get_moves function to get all possible moves.
        # Hint: You may need to use the gf.add_new_tile function to add a new tile to the board.
        # Hint: You may need to use the np.copy function to create a copy of the board.
        # Hint: You may need to use the np.inf constant to represent infinity.
        # Hint: You may need to use the max function to get the maximum value in a list.
        v= -1*np.inf
        board_copy=np.copy(board)
        bestMove=None
        for func in gf.get_moves():
            score=func(np.copy(board_copy))[2]
            if score>v:
                bestMove=func
                v=score
        func(board)
        gf.add_new_tile(board)
        return func,v
        
        #raise NotImplementedError("Maximizer node not implemented yet.")

    def chance_node(self, board: np.ndarray, depth: int):
        """
        Returns the expected score for the given board state and turn.
        ...
        :type depth: int
        :type board: np.ndarray
        :param board: The board state for which the expected score is to be found.
        :param depth: Depth to which agent takes actions for each move
        :return: Returns the expected score for the given board state.
        """
        
        # TODO: Complete chance_node function to return the expected score for the given board state.
        # Hint: You may need to use the gf.get_empty_cells function to get all empty cells in the board.
        # Hint: You may need to use the gf.add_new_tile function to add a new tile to the board.
        # Hint: You may need to use the np.copy function to create a copy of the board.
        
        score=0.0
        emptyCells=gf.get_empty_cells(board)
        size=len(emptyCells)
        for i,j in emptyCells:
            board_copy=np.copy(board)
            board_copy[i,j]=2.0
            score+=(0.9*self.expectimax(board_copy)/size)
            board_copy=np.copy(board)
            board_copy[i,j]=4.0
            score+=(0.1*self.expectimax(board_copy)/size)
        
        return score,None
        
