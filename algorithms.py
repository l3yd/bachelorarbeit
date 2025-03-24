import numpy as np
import yavalath as yav
import math


### Alpha-Beta
class Alpha_Beta:
    def __init__(self, board: yav.Board, search_depth = 4):
        self.board = board
        self.search_depth = search_depth
        self.best_move = None
        self.checks = 0
        self.moves = [None,None,None, None]

    def alpha_beta(self):
        inf = math.inf
        self._nega_max(self.board, self.search_depth, -inf, inf)

        if self.best_move != None:
            new_board = self.board.simulate_move(self.best_move)[0]
            #print("Best move: " + str(self.evaluate(new_board)))
            return self.best_move
        else:
            # TODO: dieser Fall trifft zu früh / oft ein!
            print("ERROR: Game should allready be over?!")
            random_moves = self.board.get_possible_actions()
            if random_moves == []:
                return (0,0)
            np.random.shuffle(random_moves)
            return random_moves[0]


    def _nega_max(self, board: yav.Board, depth, alpha, beta):
        if depth == 0 or board.move_count == 61:
            #print(self.moves)
            return -self.evaluate(board)
        
        max_value = alpha
        for move in board.get_possible_actions():
            new_board, result = board.simulate_move(move)
            self.moves[depth-1] = move
            value = -(self._nega_max(new_board, depth-1, -beta, -max_value))

            """if self.moves[3] == (4,4) and self.moves[2] == (8,6):
                print(str(self.moves) + " | " + str(value))"""
            #if value != 0:
                #print(str(value) + " " + str(depth))
            #print(str(value) + " " + str(max_value) + " " + str(self.best_move))
            """if self.moves[3] == (2,0):
                print(str(self.moves) + " | " + str(value) + " @ " + str(depth))"""
            if value > max_value:
                if new_board.is_end() == -1:
                    continue
                max_value = value
                if depth == self.search_depth:
                    self.best_move = move
                if max_value >= beta:
                    break
        self.moves[depth-1] = None
        return max_value


    """
    TODO: z.B. |xxox-| gibt wert für x für two in a row, kann aber nicht mehr zum gewinnen genutzt werden 
    """
    def evaluate(self, board: yav.Board, defence = False, p_two_row = 2, p_one_gap = 5, p_two_gap = 11, p_four_thread = 23):
        result = board.is_end_opponent()
        if result != 0:
            if result == 0.5:
                return 0
            return math.inf * result

        if not defence:
            bitboard = board.full ^ board.current # steine des spielers der als letztes einen platziert hat
            opponent = board.current
        else:
            bitboard = board.current
            opponent = board.full ^ board.current

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
            #accounting for enemy
        ver_blocked = ver_one_gap & (opponent >> 1)
        diag_bt_blocked = diag_bt_one_gap & (opponent >> 9)
        diag_tb_blocked = diag_tb_one_gap & (opponent >> 10)
        n_one_gap_blocked = ver_blocked.bit_count() + diag_bt_blocked.bit_count() + diag_tb_blocked.bit_count()
        n_one_gap -= n_one_gap_blocked

        # two_gap = int("1001",2)
        ver_two_gap = bitboard & (bitboard >> 3)
        diag_bt_two_gap = bitboard & (bitboard >> 27)
        diag_tb_two_gap = bitboard & (bitboard >> 30)
        n_two_gap = ver_two_gap.bit_count() + diag_bt_two_gap.bit_count() + diag_tb_two_gap.bit_count()
            #accounting for enemy
        ver_blocked = (ver_two_gap & (opponent >> 1)) | (ver_two_gap & (opponent >> 2))
        diag_bt_blocked = (diag_bt_two_gap & (opponent >> 9)) | (diag_bt_two_gap & (opponent >> 18))
        diag_tb_blocked = (diag_tb_two_gap & (opponent >> 10)) | (diag_bt_two_gap & (opponent >> 20))
        n_two_gap_blocked = ver_blocked.bit_count() + diag_bt_blocked.bit_count() + diag_tb_blocked.bit_count()
        n_two_gap -= n_two_gap_blocked

        # four_thread_1 = int("1101",2)
        ver = ver_one_gap & ver_two_gap
        diag_bottom_top = diag_bt_two_row & diag_bt_two_gap
        diag_top_bottom = diag_tb_two_row & diag_tb_two_gap
        n_four_thread = ver.bit_count() + diag_bottom_top.bit_count() + diag_top_bottom.bit_count()
            #accounting for enemy
        ver_blocked = ver & (opponent >> 1)
        diag_bt_blocked = diag_bottom_top & (opponent >> 9)
        diag_tb_blocked = diag_top_bottom & (opponent >> 10)
        n_four_thred_blocked = ver_blocked.bit_count() + diag_bt_blocked.bit_count() + diag_tb_blocked.bit_count()
        

        # four_thread_2 = int("1011",2)
        ver = ver_two_row & ver_two_gap
        diag_bottom_top = diag_bt_one_gap & diag_bt_two_gap
        diag_top_bottom = diag_tb_one_gap & diag_tb_two_gap
        n_four_thread += ver.bit_count() + diag_bottom_top.bit_count() + diag_top_bottom.bit_count()
            #accounting for enemy
        ver_blocked = ver & (opponent >> 2)
        diag_bt_blocked = diag_bottom_top & (opponent >> 18)
        diag_tb_blocked = diag_top_bottom & (opponent >> 20)
        n_four_thred_blocked += ver_blocked.bit_count() + diag_bt_blocked.bit_count() + diag_tb_blocked.bit_count()

        n_four_thread -= n_four_thred_blocked
        
        score = (n_two_row * p_two_row) + (n_one_gap * p_one_gap) + (n_two_gap * p_two_gap) + (n_four_thread * p_four_thread)
        if defence:
            """if self.moves[1] == (8,6) and self.moves[0] == (0,1):
                print("defence: " + str(score))"""
            return score
        else:
            """if self.moves[1] == (8,6) and self.moves[0] == (0,1):
                print("offence: " + str(score))"""
            return score  - self.evaluate(board, True)


### Mini-Max

class MiniMax:
    def __init__(self, board: yav.Board):
        self.move = None
        self.search_depth = 3
        self.board = board
        """self.parent_move = None
        self.move_at_two = None"""

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
        self.actions = board.get_possible_actions()
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
        actions = state.get_possible_actions()
        state, result = state.simulate_move(actions[np.random.randint(0, len(actions))])
    return result * (61 - state.move_count)

def _backpropagation_negamax(node: MCTNode, reward):
    while node is not None:
        node.n += 1
        node.q += reward
        reward = -reward
        node = node.parent
