import numpy as np
import yavalath as yav
import math

class MiniMax:
    def __init__(self, board: yav.Board):
        self.move = None
        self.search_depth = 3
        self.board = board

    def main(self):
        self.mini_max(self.board, self.search_depth)
        if self.move == None:
            print("No more moves possible!")
        else:
            return self.move
        
    def mini_max(self, board: yav.Board, depth):
        if depth == 0 or board.move_count == 61:
            return self.evaluate(board)
        max_value = -math.inf
        possible_moves = board.get_possible_actions()
        np.random.shuffle(possible_moves)
        for move in possible_moves:
            new_board = board.simulate_move(move)[0]
            if depth == self.search_depth and new_board.is_end() == 1:
                self.move = move
                break
            value = -self.mini_max(new_board, depth-1)
            if value > max_value:
                if new_board.is_end() == -1:
                    continue
                max_value = value
                if depth == self.search_depth:
                    self.move = move
        return max_value
        
    def evaluate(self, board: yav.Board) -> int:
        result = board.is_end_opponent()
        if result == 0.5:
            return 0
        return -result