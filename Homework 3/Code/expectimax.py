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
        return self.DEPTH_BASE_PARAM+move_number//self.SCALER_PARAM

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

        Return : score as float and action
        """
        
        
        # TODO: Complete expectimax function to return the best move and score for the given board state and turn.
        # Hint: You may need to implement minimizer_node and maximizer_node functions.
        # Hint: You may need to use the evaluation.evaluate_state function to score leaf nodes.
        # Hint: You may need to use the gf.terminal_state function to check if the game is over.
        if gf.terminal_state(board):
            return evaluation.evaluate_state(board),None
        if depth==0:
            return evaluation.evaluate_state(board),None
        if turn:
            bestMove,bestScore=self.maximizer_node(board,depth-1)
            return bestScore,bestMove
        else:
            coefficient=(16-np.count_nonzero(board)+0.0)/4.0
            return coefficient*self.chance_node(board,depth),None
        

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
        
        bestScore= -1*np.inf
        bestMove=None
        
        for func in gf.get_moves():
            newBoard,moveMade,score1=func(np.copy(board))
            if not moveMade:
                continue
            newBoardScore=evaluation.evaluate_state(newBoard)
            score2=self.expectimax(newBoard,depth,0)
            if score1*2+score2[0]>bestScore:
                bestMove=func
                bestScore=(score1*2+score2[0]+newBoardScore)
        
        return bestMove,bestScore

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
        board_copy=np.copy(board)
        size=np.shape(board)[0]
        num=0.0
        for i in range(size):
            for j in range(size):
                if not board[i,j]:
                    num+=1
                    board_copy[i,j]=2.0
                    score+=(0.9*self.expectimax(board_copy,depth,1)[0])
                    board_copy[i,j]=0.0
                    board_copy[i,j]=4.0
                    score+=(0.1*self.expectimax(board_copy,depth,1)[0])
                    board_copy[i,j]=0.0
        return score/num
        
