import numpy as np
import yavalath as yav

illegalMoves = [5,6,7,8,
                15,16,17,
                25,26,
                35,
                45,
                54,55,
                63,64,65,
                72,73,74,75]

def getPossibleActions(board: yav.Board):
    moves = []
    for i in range(81):
        if i in illegalMoves:
            continue
        if (board.full >> i) & 1 == 0:
            moves.append(yav.bit_to_coords(i))
    return moves

class MCTS:
    def __init__(self):
        pass

    def selection():
        return 0
    
    def expansion():
        return 0

    def simulation():
        return 0
    
    def backpropagation():
        return 0
        
class MCTNode:
    def __init__(self, board):
        self.state = board
        self.score = 0
        self.num_visits = 0


if __name__ == '__main__':
    b = yav.Board()