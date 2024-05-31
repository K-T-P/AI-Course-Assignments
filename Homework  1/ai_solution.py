import copy
import heapq
from math import floor,sqrt


class GameSolution:
    """
    A class for solving the Water Sort game and finding solutions(normal, optimal).

    Attributes:
        ws_game (Game): An instance of the Water Sort game which implemented in game.py file.
        moves (List[Tuple[int, int]]): A list of tuples representing moves between source and destination tubes.
        solution_found (bool): True if a solution is found, False otherwise.

    Methods:
        solve(self, current_state):
            Find a solution to the Water Sort game from the current state.
            After finding solution, please set (self.solution_found) to True and fill (self.moves) list.

        optimal_solve(self, current_state):
            Find an optimal solution to the Water Sort game from the current state.
            After finding solution, please set (self.solution_found) to True and fill (self.moves) list.
    """

    def __init__(self, game):
        """
        Initialize a GameSolution instance.
        Args:
            game (Game): An instance of the Water Sort game.
        """
        self.ws_game = game  # An instance of the Water Sort game.
        self.moves = (
            []
        )  # A list of tuples representing moves between source and destination tubes.
        self.tube_numbers = (
            game.NEmptyTubes + game.NColor
        )  # Number of tubes in the game.
        self.solution_found = False  # True if a solution is found, False otherwise.
        self.visited_tubes = set()  # A set of visited tubes.

    def solve(self, current_state):
        """
        Find a solution to the Water Sort game from the current state.

        Args:
            current_state (List[List[int]]): A list of lists representing the colors in each tube.

        This method attempts to find a solution to the Water Sort game by iteratively exploring
        different moves and configurations starting from the current state.
        """
        
        if self.ws_game.check_victory(current_state):
            self.solution_found = True
            return
        NColorInTube = self.ws_game.NColorInTube
        # choose two tube
        for sourceTubeIndex in range(len(current_state)):
            for destinationTubeIndex in range(len(current_state)):
                # if source and destination tube are same
                if sourceTubeIndex == destinationTubeIndex:
                    continue

                # if source tube is empty
                if len(current_state[sourceTubeIndex]) == 0:
                    continue

                # if destination tube is full
                if len(current_state[destinationTubeIndex]) == NColorInTube:
                    continue

                # number of colors in each tube
                sourceTube_color_count = len(current_state[sourceTubeIndex])
                destinationTube_color_count = len(current_state[destinationTubeIndex])

                if destinationTube_color_count != 0:
                    # check if top colors are same
                    if (
                        current_state[sourceTubeIndex][sourceTube_color_count - 1]
                        != current_state[destinationTubeIndex][
                            destinationTube_color_count - 1
                        ]
                    ):
                        continue

                # avoid moving a tube with all same color to an empty tube
                if (
                    self.allAreSame(current_state[sourceTubeIndex])
                    and len(current_state[destinationTubeIndex]) == 0
                ):
                    continue

                # take copy of source and destination tube
                sourceTubeCopy = copy.deepcopy(current_state[sourceTubeIndex])
                destinationTubecopy = copy.deepcopy(current_state[destinationTubeIndex])

                # move color to another tube
                while True:
                    color = current_state[sourceTubeIndex].pop(
                        sourceTube_color_count - 1
                    )
                    current_state[destinationTubeIndex].append(color)
                    sourceTube_color_count -= 1
                    destinationTube_color_count += 1
                    if len(current_state[sourceTubeIndex]) == 0:
                        break
                    if len(current_state[destinationTubeIndex]) == NColorInTube:
                        break
                    if (
                        current_state[sourceTubeIndex][sourceTube_color_count - 1]
                        != current_state[destinationTubeIndex][
                            destinationTube_color_count - 1
                        ]
                    ):
                        break

                
                if not self.CheckIfItExists(self.visited_tubes, current_state):
                    self.visited_tubes.add(str(current_state))
                    newMove = (sourceTubeIndex, destinationTubeIndex)
                    self.moves.append(newMove)
                    self.solve(current_state)
                    if self.solution_found:
                        return
                    self.moves.pop(len(self.moves) - 1)

                current_state[sourceTubeIndex] = sourceTubeCopy
                current_state[destinationTubeIndex] = destinationTubecopy

    def allAreSame(self, list_a):
        for i in range(len(list_a) - 1):
            if list_a[i] != list_a[i + 1]:
                return False
        return True

    def CheckIfItExists(self, list_parent, list_child):
        for i in list_parent:
            if(type(i)==str):
                if self.CompareTwoListEquality(eval(i), list_child):
                    return True
            else:
                if self.CompareTwoListEquality(i, list_child):
                    return True
        return False

    def CompareTwoListEquality(self, list_a, list_b):
        for i in list_a:
            if i not in list_b:
                return False
        for i in list_b:
            if i not in list_a:
                return False
        return True

    g_n_dict = {}
    h_n_dict = {}

    def optimal_solve(self, current_state):
        """
        Find an optimal solution to the Water Sort game from the current state.

        Args:
            current_state (List[List[int]]): A list of lists representing the colors in each tube.

        This method attempts to find an optimal solution to the Water Sort game by minimizing
        the number of moves required to complete the game, starting from the current state.
        """
        flag=True
        # stores visited state
        exploredStates = []
        # stores stores tuple of string of the state and the f of the state
        waitingToBeExplored = []
        # stores string of the state as the key and tuple of the string of the
        # parent and the string of the move(tuple stored as string) (None means there are none)
        states_dict = {}
        #to avoid repetition
        foundStates=list()
        # add first state to explored states
        states_dict[str(current_state)] = (None, (None, None))
        self.g_n_dict[str(current_state)] = 0
        self.h_n_dict[str(current_state)] = self.h(current_state)
        # stores all approved states
        foundStates.append(copy.deepcopy(current_state))
        if(flag):
            waitingToBeExplored.append(
            (
                self.g_n_dict[str(current_state)]+self.h_n_dict[str(current_state)],
                str(current_state),
            )
        )
        else:
            waitingToBeExplored.append(
            (
                self.h_n_dict[str(current_state)],
                str(current_state),
            )
        )
        while waitingToBeExplored:
            leastCostState = heapq.heappop(waitingToBeExplored)
            exploredStates.append(leastCostState[0])
            leastCostState = leastCostState[1]
            current_state = eval(leastCostState)
            parentStateString = str(current_state)

            if self.ws_game.check_victory(eval(leastCostState)):
                moves = []
                while True:
                    parentString = states_dict[leastCostState]
                    if parentString[0] == None:
                        break
                    moves.insert(0, parentString[1])
                    leastCostState = parentString[0]
                self.moves = moves
                self.solution_found = True
                self.visited_tubes.union(exploredStates)
                break

            for sourceTubeIndex in range(len(current_state)):
                for destinationTubeIndex in reversed(range(len(current_state))):
                    if self.SourceTubeColorCanTransferToDestinationTube(
                        eval(leastCostState),current_state, sourceTubeIndex, destinationTubeIndex
                    ):
                        # number of colors in each tube
                        sourceTube_color_count = len(current_state[sourceTubeIndex])
                        destinationTube_color_count = len(
                            current_state[destinationTubeIndex]
                        )

                        sourceTubeCopy = str(current_state[sourceTubeIndex])
                        destinationTubecopy = str(current_state[destinationTubeIndex])

                        # This while moves color between two tubes
                        while True:
                            color = current_state[sourceTubeIndex].pop(
                                sourceTube_color_count - 1
                            )
                            current_state[destinationTubeIndex].append(color)
                            sourceTube_color_count -= 1
                            destinationTube_color_count += 1
                            if len(current_state[sourceTubeIndex]) == 0:
                                break
                            if (
                                len(current_state[destinationTubeIndex])
                                == self.ws_game.NColorInTube
                            ):
                                break
                            if (
                                current_state[sourceTubeIndex][
                                    sourceTube_color_count - 1
                                ]
                                != current_state[destinationTubeIndex][
                                    destinationTube_color_count - 1
                                ]
                            ):
                                break

                        if(not self.CheckIfItExists(foundStates,current_state)):
                            foundStates.append(copy.deepcopy(current_state))
                            states_dict[str(current_state)] = (
                                parentStateString,
                                (sourceTubeIndex, destinationTubeIndex),
                            )
                            self.g_n_dict[str(current_state)] = (
                                self.g_n_dict[parentStateString] + 1
                            )
                            self.h_n_dict[str(current_state)] = self.h(current_state)
                            
                            if(flag):
                               heapq.heappush(
                                        waitingToBeExplored,
                                        (
                                            self.g_n_dict[str(current_state)]+self.h_n_dict[str(current_state)]
                                           ,
                                            str(current_state),
                                        )            
                                    )
                            else:
                                heapq.heappush(
                                        waitingToBeExplored,
                                        (
                                            self.h_n_dict[str(current_state)]
                                           ,
                                            str(current_state),
                                        )            
                                    )
                        # returns the current_state to its previous form for the next loop
                        current_state[sourceTubeIndex] = eval(sourceTubeCopy)
                        current_state[destinationTubeIndex] = eval(destinationTubecopy)
    
    def SourceTubeColorCanTransferToDestinationTube(
        self,parentState, current_state, sourceTubeIndex, destinationTubeIndex
    ):
        # if source and destination tube are same
        if sourceTubeIndex == destinationTubeIndex:
            return False

        # number of colors in each tube
        sourceTube_color_count = len(current_state[sourceTubeIndex])
        destinationTube_color_count = len(current_state[destinationTubeIndex])

        # if source tube is empty
        if not current_state[sourceTubeIndex]:
            return False
        # if destination tube is full
        if destinationTube_color_count == self.ws_game.NColorInTube:
            return False

        if current_state[destinationTubeIndex]:
            # check if top colors are same
            if (
                current_state[sourceTubeIndex][sourceTube_color_count - 1]
                != current_state[destinationTubeIndex][destinationTube_color_count - 1]
            ):
                return False
        return True
    
    def h(self,current_state):
        """
        Find the h of the A* algorithm.

        Args:
            current_state (List[List[int]]): A list of lists representing the colors in each tube.

        This method attempts to calculate the h function of the A* algorithm.

        """
        colors_count = [0] * self.ws_game.NColor
        seperateColorCount=0
        tubeCount=0
        for tube in current_state:
            tubeLength = len(tube)
            if(tubeLength):
                tubeCount+=1
            else:
                continue
            for index in reversed(range(len(tube))):
                if(index+1!=tubeLength):
                    if(tube[index]==tube[index+1]):
                        continue
                seperateColorCount+=1
            colors_count[tube[0]]+=(seperateColorCount*seperateColorCount)
        return floor(sqrt(sum(colors_count)/tubeCount))-2

    def heapify(self, unsortedList, itemIndex):
        if itemIndex == 0:
            return
        itemParentIndex = floor((itemIndex - 1) / 2)

        itemString = unsortedList[itemIndex][0]
        itemParentString = unsortedList[itemParentIndex][0]

        f_item = self.g_n_dict[itemString] + self.h_n_dict[itemString]
        f_itemParent = self.g_n_dict[itemParentString] + self.h_n_dict[itemParentString]

        if unsortedList[itemParentIndex][1] >= unsortedList[itemIndex][1]:
            temp = unsortedList[itemIndex]
            unsortedList[itemIndex] = unsortedList[itemParentIndex]
            unsortedList[itemParentIndex] = temp
            self.heapify(unsortedList, itemParentIndex)
        return

    def popHeapQueue(self, sortedList, itemIndex=0):
        """
        Args :
            sortedList ( tuple( str, int) )
            itemIndex ( int)
        """
        listLength = len(sortedList)
        # find children indexes of item
        child1Index = 2 * itemIndex + 1
        child2Index = 2 * itemIndex + 2

        if child1Index + 1 > listLength and child2Index + 1 > listLength:
            answer = sortedList[itemIndex]
            self.swap(sortedList, itemIndex, listLength - 1)
            del sortedList[listLength - 1]
            if itemIndex != listLength - 1:
                self.heapify(sortedList, itemIndex)
            return answer
        elif child1Index + 1 <= listLength and child2Index + 1 > listLength:
            self.swap(sortedList, itemIndex, child1Index)
            return self.popHeapQueue(sortedList, child1Index)
        elif child1Index + 1 > listLength and child2Index + 1 <= listLength:
            self.swap(sortedList, itemIndex, child2Index)
            return self.popHeapQueue(sortedList, child2Index)
        else:
            if sortedList[child1Index][1] > sortedList[child2Index][1]:
                self.swap(sortedList, itemIndex, child1Index)
                return self.popHeapQueue(sortedList, child1Index)
            else:
                self.swap(sortedList, itemIndex, child2Index)
                return self.popHeapQueue(sortedList, child2Index)

    def swap(self, myList, index1, index2):
        temp = myList[index1]
        myList[index1] = myList[index2]
        myList[index2] = temp
