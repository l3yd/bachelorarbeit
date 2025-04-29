import numpy as np
import yavalath as yav
import alphabeta as ab
import time


class MCTNode:
    def __init__(self, board: yav.Board, parent=None):
        self.state = board
        self.q = 0
        self.n = 0
        self.child_nodes = []
        self.actions = board.get_possible_actions()
        self.a = None
        self.parent = parent
        # keeping track of moves leading to sudden death (in root node)
        self.death_moves = []

def MCTS_alphabeta(board: yav.Board, c = np.sqrt(2), k = 4, max_time = 1):
    root = MCTNode(board)
    start_time = time.time()
    while time.time() - start_time < max_time:
        steps_from_root = _MCTS_one_iteration(root, c)
        if steps_from_root > k and root.death_moves == []:
            AB = ab.Alpha_Beta(board,k)
            move, sudden_end = AB.iterative_deepening()
            if sudden_end == 1:
                return move
            elif sudden_end == -1:
                root.death_moves = AB.death_moves
    return _UCT(root, 0).a

def MCTS(board: yav.Board, c = np.sqrt(2), max_time = 1):
    root = MCTNode(board)
    start_time = time.time()
    while time.time() - start_time < max_time:
        _MCTS_one_iteration(root, c)
    return _UCT(root, 0).a

def _MCTS_one_iteration(root: MCTNode, c) -> int:
    v = _selection(root, c)
    reward = _simulation(v.state)
    return _backpropagation_negamax(v, reward)

def _selection(node: MCTNode, c) -> MCTNode:
    while len(node.actions) == 0:
        node = _UCT(node, c)
    return _expansion(node)

def _expansion(node: MCTNode) -> MCTNode:
    np.random.shuffle(node.actions)
    a = node.actions.pop()
    child_state, result = node.state.simulate_move(a)
    child = MCTNode(child_state, node)
    child.a = a
    node.child_nodes.append(child)
    return child

def _UCT(node: MCTNode, c) -> MCTNode:
    num_children = len(node.child_nodes)
    values = np.zeros(num_children)
    children = node.child_nodes
    if node.death_moves != []:
        children = list(set(children) - set(node.death_moves))
    for i in range(num_children):
        values[i] = (children[i].q/children[i].n) + c * np.sqrt(2*np.log(node.n)/children[i].n)
    return children[np.argmax(values)]

def _simulation(state: yav.Board) -> int:
    player = state.move_count % 2
    result = state.is_end()
    while result == 0:
        actions = state.get_possible_actions()
        state, result = state.simulate_move(actions[np.random.randint(0, len(actions))])
    if state.move_count % 2 != player:
        result = -result
    return result

def _backpropagation_negamax(node: MCTNode, reward) -> int:
    steps = 0
    while node is not None:
        node.n += 1
        node.q += reward
        reward = -reward
        node = node.parent

        steps += 1
    return steps