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

class MCTNode:
    def __init__(self, board: yav.Board, parent=None):
        self.state = board
        self.q = 0
        self.n = 0
        self.child_nodes = []
        self.actions = get_possible_actions(board)
        self.a = None
        self.parent = parent

### Alpha-Beta
def evaluate(board: yav.Board):
    result = board.is_end()
    if result != 0:
        if result == 0.5:
            return 0
        return math.inf * result
    
    return 0

def alpha_beta(board: yav.Board, turn: int):
    search_depth = 4
    inf = math.inf
    if turn % 2 != 0:
        return _maximize(search_depth, -inf, inf)
    return _minimize(search_depth, -inf, inf)

def _maximize(depth, alpha, beta):
    return 0

def _minimize(depth, alpha, beta):
    return 0
    

### MCTS

def MCTS(board: yav.Board):
    root = MCTNode(board)
    for i in range(10000):
        v = _selection(root)
        reward = _simulation(v.state)
        _backpropagation_negamax(v, reward)
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
    child_state = node.state.simulate_move(a)
    child = MCTNode(child_state, node)
    child.a = a
    node.child_nodes.append(child)
    return child

def _UCT(node: MCTNode, c = 1.5) -> MCTNode:
    num_children = len(node.child_nodes)
    values = np.zeros(num_children)
    for i in range(num_children):
        values[i] = (node.child_nodes[i].q/node.child_nodes[i].n) + c * np.sqrt(2*np.log(node.n)/node.child_nodes[i].n)
    return node.child_nodes[np.argmax(values)]

def _simulation(state: yav.Board) -> int:
    while state.is_end() == 0:
        actions = get_possible_actions(state)
        state = state.simulate_move(actions[np.random.randint(0, len(actions))])
    return state.is_end()

def _backpropagation_negamax(node: MCTNode, reward):
    while node is not None:
        node.n += 1
        node.q += reward
        reward = -reward
        node = node.parent

if __name__ == '__main__':
    b = yav.Board()
    print(MCTS(b))