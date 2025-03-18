import numpy as np
import yavalath as yav
import math

illegalMoves = [5,6,7,8,
                15,16,17,
                25,26,
                35,
                45,
                54,55,
                63,64,65,
                72,73,74,75]

def get_possible_actions(board: yav.Board) -> list:
    moves = []
    for i in range(81):
        if i in illegalMoves:
            continue
        if (board.full >> i) & 1 == 0:
            moves.append(yav.bit_to_coords(i))
    return moves


### Alpha-Beta
class Alpha_Beta:
    def __init__(self, board: yav.Board, search_depth = 3):
        self.board = board
        self.search_depth = search_depth
        self.best_move = None
        self.checks = 0

    def alpha_beta(self):
        inf = math.inf
        self._nega_max(self.board, self.search_depth, -inf, inf)

        if self.best_move != None:
            new_board = self.board.simulate_move(self.best_move)[0]
            print("Best move: " + str(self.evaluate(new_board)))
            return self.best_move
        else:
            # TODO: dieser Fall trifft zu früh / oft ein!
            print("ERROR: Game should allready be over!")
            return (0,0)


    def _nega_max(self, board: yav.Board, depth, alpha, beta):
        if depth == 0 or board.move_count == 61:
            return self.evaluate(board)
        
        max_value = alpha
        for move in get_possible_actions(board):
            new_board, result = board.simulate_move(move)
            value = -(self._nega_max(new_board, depth-1, -beta, -max_value))
            if value != 0:
                print(str(value) + " " + str(depth))
            #print(str(value) + " " + str(max_value) + " " + str(self.best_move))
            if value > max_value:
                max_value = value
                if depth == self.search_depth:
                    self.best_move = move
                if max_value >= beta:
                    break
        
        return max_value


    """
    TODO: evaluate beachtet bisher nicht die steine des gegners
    """
    def evaluate(self, board: yav.Board, p_two_row = 2, p_one_gap = -10, p_two_gap = 10, p_four_thread = 20):
        result = board.is_end()
        if result != 0:
            if result == 0.5:
                return 0
            return math.inf * result

        bitboard = board.full ^ board.current # steine des spielers der als letztes einen platziert hat ??
        #bitboard = board.current

        # two_in_a_row = int("11",2)
        ver_two_row = bitboard & (bitboard >> 1)
        diag_bt_two_row = bitboard & (bitboard >> 9)
        diag_tb_two_row = bitboard & (bitboard >> 10)
        n_two_row = ver_two_row.bit_count() + diag_bt_two_row.bit_count() + diag_tb_two_row.bit_count()

        # one_gap = int("101",2)
        ver_one_gap = bitboard & (bitboard >> 2)
        diag_bt_one_gap = bitboard & (bitboard >> 18)
        diag_tb_one_gap = bitboard & (bitboard >> 20)
        n_one_gap = ver_one_gap.bit_count() + diag_bt_one_gap.bit_count() + diag_tb_one_gap.bit_count()

        # two_gap = int("1001",2)
        ver_two_gap = bitboard & (bitboard >> 3)
        diag_bt_two_gap = bitboard & (bitboard >> 27)
        diag_tb_two_gap = bitboard & (bitboard >> 30)
        n_two_gap = ver_two_gap.bit_count() + diag_bt_two_gap.bit_count() + diag_tb_two_gap.bit_count()

        # four_thread_1 = int("1101",2)
        ver = ver_two_row & ver_two_gap
        diag_bottom_top = diag_bt_two_row & diag_bt_two_gap
        diag_top_bottom = diag_tb_two_row & diag_tb_two_gap
        n_four_thread = ver.bit_count() + diag_bottom_top.bit_count() + diag_top_bottom.bit_count()

        # four_thread_2 = int("1011",2)
        ver = ver_one_gap & ver_two_gap
        diag_bottom_top = diag_bt_one_gap & diag_bt_two_gap
        diag_top_bottom = diag_tb_one_gap & diag_tb_two_gap
        n_four_thread += ver.bit_count() + diag_bottom_top.bit_count() + diag_top_bottom.bit_count()

        return (n_two_row * p_two_row) + (n_one_gap * p_one_gap) + (n_two_gap * p_two_gap) + (n_four_thread * p_four_thread)


### Mini-Max

class MiniMax:
    def __init__(self, board: yav.Board):
        self.move = None
        self.search_depth = 3
        self.board = board
        """self.parent_move = None
        self.move_at_two = None"""

    def main(self):
        print()
        self.mini_max(self.board, self.search_depth)
        if self.move == None:
            print("No more moves possible!")
        else:
            return self.move
        
    def mini_max(self, board: yav.Board, depth):
        if depth == 0 or board.move_count == 61:
            return self.evaluate(board)
        max_value = -math.inf
        possible_moves = get_possible_actions(board)
        np.random.shuffle(possible_moves)
        for move in possible_moves:

            #testblock
            """if depth == 2 and move != (2,1):
                continue
            if depth == self.search_depth:
                self.parent_move = move
            if depth == 2:
                self.move_at_two = move"""

            new_board = board.simulate_move(move)[0]
            
            #printblock
            """if depth == self.search_depth and (self.parent_move == (1,0) or self.parent_move == (1,0)):
                print()
                print(str(move) + " :")"""

            if depth == self.search_depth and new_board.is_end() == 1:
                self.move = move
                break
            value = -self.mini_max(new_board, depth-1)
            #printblock
            """if self.parent_move == (1,0) and self.move_at_two == (2,1) and depth == 1:
                print(str(move) + " | " + str(value))"""
            if value > max_value:

                #printblock
                """if max_value == -math.inf:
                    max_value = '€'
                if self.parent_move == (1,0):
                    print(str(max_value) + " -> " + str(value) + " | " + str(move) + " @ " + str(depth))
                if max_value == '€':
                    max_value = -math.inf"""

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

### MCTS

class MCTNode:
    def __init__(self, board: yav.Board, parent=None):
        self.state = board
        self.q = 0
        self.n = 0
        self.child_nodes = []
        self.actions = get_possible_actions(board)
        self.a = None
        self.parent = parent

def MCTS(board: yav.Board):
    root = MCTNode(board)
    for i in range(2000):
        v = _selection(root)
        reward = _simulation(v.state)
        _backpropagation_negamax(v, reward)
    """
    for c in root.child_nodes:
        print(str(c.q) + str(c.a)+ str(c.n))
        
    print(_UCT(root, 0).a)
    """
    return _UCT(root, 0).a

def _selection(node: MCTNode) -> MCTNode:
    while node.state.is_end() == 0:
        if len(node.actions) > 0:
            return _expansion(node)
        else:
            node = _UCT(node)
    return node

def _expansion(node: MCTNode) -> MCTNode:
    a = node.actions.pop()
    child_state, result = node.state.simulate_move(a)
    child = MCTNode(child_state, node)
    child.a = a
    node.child_nodes.append(child)
    return child

def _UCT(node: MCTNode, c = 0.8) -> MCTNode:
    num_children = len(node.child_nodes)
    values = np.zeros(num_children)
    for i in range(num_children):
        values[i] = (node.child_nodes[i].q/node.child_nodes[i].n) + c * np.sqrt(2*np.log(node.n)/node.child_nodes[i].n)
    return node.child_nodes[np.argmax(values)]

def _simulation(state: yav.Board) -> int:
    result = state.is_end()
    while result == 0:
        actions = get_possible_actions(state)
        state, result = state.simulate_move(actions[np.random.randint(0, len(actions))])
    return result * (61 - state.move_count)

def _backpropagation_negamax(node: MCTNode, reward):
    while node is not None:
        node.n += 1
        node.q += reward
        reward = -reward
        node = node.parent
