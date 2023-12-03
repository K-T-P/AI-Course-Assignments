import numpy as np

import evaluation
import game_functions as gf


class MCTS:
    def __init__(self, board, mode='ucb'):
        self.C_CONSTANT = 2  # You may change this parameter to scale the exploration term in the UCB formula.
        self.SD_SCALE_PARAM = 5  # You may change this parameter to scale the depth to which the agent searches.
        self.TM_SCALE_PARAM = 5  # You may change this parameter to scale the depth to which the agent searches.
        self.SCALER_PARAM = 200  # You may change this parameter to scale the depth to which the agent searches.
        self.UCB_SD_SCALE_PARAM = 5  # You may change this parameter to scale the depth to which the agent searches.
        self.UCB_TM_SCALE_PARAM = 5  # You may change this parameter to scale the depth to which the agent searches.
        self.UCB_SCALER_PARAM = 300  # You may change this parameter to scale the depth to which the agent searches.
        self.board = board
        self.mode = mode

    def get_search_params(self, move_number: int) -> (int, int):
        """
        Returns the depth to which the agent should search for the given move number.
        ...
        :type move_number: int
        :param move_number: The current move number.
        :return: The depth to which the agent should search for the given move number.
        """
        # TODO: Complete get_search_params function to return the depth to which the agent should search for the given move number.
        # Hint: You may want to use the self.SD_SCALE_PARAM, self.SL_SCALE_PARAM, and self.SCALER_PARAM parameters.
        # Hint: You may want to use the self.UCB_SPM_SCALE_PARAM, self.UCB_SL_SCALE_PARAM, and self.UCB_SCALER_PARAM parameters.
        # Hint: You may want to use the self.mode parameter to check which mode the agent is on.
        if self.mode=='ucb':
            search_depth=self.SD_SCALE_PARAM+ move_number//self.SCALER_PARAM
            total_move=self.TM_SCALE_PARAM+move_number//self.SCALER_PARAM
            return search_depth,total_move
        else:
            search_depth=self.UCB_SD_SCALE_PARAM+move_number//self.UCB_SCALER_PARAM
            total_move=self.UCB_TM_SCALE_PARAM+move_number//self.UCB_SCALER_PARAM
            return search_depth,total_move

    def ai_move(self, board, move_number):
        search_depth, total_moves = self.get_search_params(move_number)
        if self.mode == 'ucb':
            best_move = self.mcts_v2(board, total_moves * 4, search_depth)
        else:
            best_move = self.mcts_v0(board, total_moves, search_depth)
        return best_move

    @staticmethod
    def simulate_move(board: np.ndarray, search_depth: int) -> float:
        """
        Returns the score of the given board state.
        :param board: The board state for which the score is to be calculated.
        :param search_depth: The depth to which the agent should search for the given board state.
        :return: The score of the given board state.
        """
        # TODO: Complete simulate_move function to simulate a move and return the score of the given board state.
        # Hint: You may want to use the gf.random_move function to simulate a random move.
        # Hint: You may want to use the evaluation.evaluate_state function to score a board.
        # Hint: You may want to use the move_made returned from the gf.random_move function to check if a move was made.
        # Hint: You may want to use the gf.add_new_tile function to add a new tile to the board.
       # if 
        if gf.terminal_state or search_depth==0:
            return evaluation.evaluate_state(board)
        
        newBoard,flag,score1 = gf.random_move(np.copy(board))
        score2=0.0
        if not flag:
            gf.add_new_tile(newBoard)
            score2=evaluation.evaluate_state(newBoard)
        return score1+score2+MCTS.simulate_move(newBoard,search_depth-1)
        

    def ucb(self, moves: list, total_visits: int) -> np.ndarray:
        """
        Returns the UCB scores for the given moves.
        :param moves: The moves for which the UCB scores are to be calculated.
        :param total_visits: The total number of visits for all moves.
        :return: The UCB scores for the given moves.
        """
        # TODO: Complete ucb function to return the UCB scores for the given moves.
        # Hint: You may want to use the self.C_CONSTANT parameter to scale the exploration term in the UCB formula.
        # Hint: You may want to use np.inf to represent infinity.
        # Hint: You may want to use np.sqrt to calculate the square root of a number.
        # Hint: You may want to use np.log to calculate the natural logarithm of a number.
        move1_UCB, move2_UCB, move3_UCB, move4_UCB = 0.0,0.0,0.0,0.0
        if moves[0][2]:
            move1_UCB=moves[0][2]/total_visits + self.C_CONSTANT*np.sqrt(np.log(total_visits)/moves[0][2])
        else:
            move1_UCB=np.inf

        if moves[1][2]:
            move2_UCB=moves[1][2]/total_visits + self.C_CONSTANT*np.sqrt(np.log(total_visits)/moves[1][2])
        else:
            move2_UCB=np.inf

        if moves[2][2]:
            move3_UCB=moves[2][2]/total_visits + self.C_CONSTANT*np.sqrt(np.log(total_visits)/moves[2][2])
        else:
            move3_UCB=np.inf

        if moves[3][2]:
            move4_UCB=moves[3][2]/total_visits + self.C_CONSTANT*np.sqrt(np.log(total_visits)/moves[3][2])
        else:
            move4_UCB=np.inf

        return move1_UCB,move2_UCB,move3_UCB,move4_UCB

    def mcts_v0(self, board: np.ndarray, total_moves: int, search_depth: int):
        """
        Returns the best move for the given board state.
        ...
        :type search_depth: int
        :type total_moves: int
        :type board: np.ndarray
        :param board: The board state for which the best move is to be found.
        :param total_moves: The total number of moves to be simulated.
        :param search_depth: The depth to which the agent should search for the given board state.
        :return: Returns the best move for the given board state.
        """
        # TODO: Complete mcts_v0 function to return the best move for the given board state.
        # Hint: You may want to use the gf.get_moves function to get all possible moves.
        # Hint: You may want to use the gf.add_new_tile function to add a new tile to the board.
        # Hint: You may want to use the self.simulate_move function to simulate a move.
        # Hint: You may want to use the np.argmax function to get the index of the maximum value in an array.
        # Hint: You may want to use the np.zeros function to create an array of zeros.
        # Hint: You may want to use the np.copy function to create a copy of a numpy array.

        moves_scores=[ 0.0,0.0,0.0,0.0]
        index=0
        for func in gf.get_moves():
            newBoard,moveMade,score=func(np.copy(board))
            if not moveMade:
                moves_scores[index]=-1*np.inf
                index+=1
                continue
            moves_scores[index]+=score
            for i in range(self.TM_SCALE_PARAM):
                moves_scores[index]+=self.simulate_move(newBoard,search_depth-1)
            index+=1
        return gf.get_moves()[np.array(moves_scores).argmax()]

    def mcts_v2(self, board, total_moves, search_depth):
        """
        Returns the best move for the given board state.
        ...
        :type search_depth: int
        :type total_moves: int
        :type board: np.ndarray
        :param board: The board state for which the best move is to be found.
        :param total_moves: The total number of moves to be simulated.
        :param search_depth: The depth to which the agent should search for the given board state.
        :return: Returns the best move for the given board state.
        """
        # TODO: Complete mcts_v2 function to return the best move for the given board state.
        # Hint: You may want to use the gf.get_moves function to get all possible moves.
        # Hint: You may want to use the gf.add_new_tile function to add a new tile to the board.
        # Hint: You may want to use the self.simulate_move function to simulate a move.
        # Hint: You may want to use the np.argmax function to get the index of the maximum value in an array.
        # Hint: You may want to use the np.copy function to create a copy of a numpy array.
        # Hint: You may want to use the self.ucb function to get the UCB scores for the given moves.
        moves=[ [gf.get_moves()[0],0.0,0.0],
               [gf.get_moves()[1],0.0,0.0],
               [gf.get_moves()[2],0.0,0.0],
               [gf.get_moves()[3],0.0,0.0] ]
        for i in range(self.TM_SCALE_PARAM):
            scores=self.ucb(moves,total_moves)
            selected_move_index=np.array(scores).argmax()
            if moves[0][1]==np.inf:
                moves[0][1]=0.0
            if moves[1][1]==np.inf:
                moves[1][1]=0.0
            if moves[2][1]==np.inf:
                moves[2][1]=0.0
            if moves[3][1]==np.inf:
                moves[3][1]=0.0
            moves[0][1]+=scores[0]
            moves[1][1]+=scores[1]
            moves[2][1]+=scores[2]
            moves[3][1]+=scores[3]
            moves[selected_move_index][2]+=1
            newBoard,flag,score=gf.move(np.copy(board),selected_move_index)
            if not flag:
                moves[selected_move_index][1]=-1*np.inf
            else:
                moves[selected_move_index][1]+=MCTS.simulate_move(newBoard,search_depth-1)
            
        for i in range(4):
            temp1,moveMade,temp2=gf.move(np.copy(board),i)
            if not moveMade:
                moves[i][1]=-1*np.inf
        selectedMove=0
        for i in range(1,4):
            if moves[i][1]>moves[selectedMove][1]:
                selectedMove=i
        return gf.get_moves()[selectedMove]