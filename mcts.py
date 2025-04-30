import numpy as np
import yavalath as yav
import alphabeta as ab
import time
import math


class MCTNode:
    def __init__(self, board: yav.Board, possible_actions: list):
        self.state = board
        self.q = 0
        self.n = 0
        self.parent = None
        self.a = None
        self.actions = board.get_possible_actions()
        self.child_nodes = []

        # keeping track of moves leading to sudden death (used in root note for MCTS with alphabeta)
        self.death_moves = []

        # numbers used by PNS
        self.PN = 1
        self.DPN = 1
        self.PNS_type = None
        self.is_internal = False

def MCTS_alphabeta(board: yav.Board, c = np.sqrt(2), k = 4, max_time = 4):
    root = MCTNode(board, board.get_possible_actions())
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

def MCTS_PN(board: yav.Board, c = np.sqrt(2), C_pn = 1, max_time = 7):
    root = MCTNode(board, board.get_possible_actions())
    root.PNS_type = "OR"
    start_time = time.time()
    #while time.time() - start_time < max_time:
    for _ in range(10000):
        v = _selection_PN(root, c, C_pn)
        leaf_result = v.state.is_end_opponent()
        reward = _simulation(v.state)
        _backpropagation_PNS(v, reward, leaf_result)
    return _UCT_PN(root, 0, C_pn).a

def MCTS(board: yav.Board, c = np.sqrt(2), max_time = 4):
    root = MCTNode(board, board.get_possible_actions)
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

def _selection_PN(node: MCTNode, c, C_pn) -> MCTNode:
    while len(node.actions) == 0:
        node = _UCT_PN(node, c, C_pn)
    return _expansion(node)

def _expansion(node: MCTNode) -> MCTNode:
    np.random.shuffle(node.actions)
    a = node.actions.pop()
    child_state, result = node.state.simulate_move(a)
    possible_actions = list(set(node.actions) - set([a]))
    child = MCTNode(child_state, possible_actions)
    child.parent = node
    child.a = a
    if node.PNS_type != None:
        child.PNS_type = {"OR": "AND", "AND": "OR"}[node.PNS_type]
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

def _UCT_PN(node: MCTNode, c, C_pn) -> MCTNode:
    num_children = len(node.child_nodes)
    values = np.zeros(num_children)
    children = node.child_nodes
    children.sort(key=_rank)

    current_rank = 1
    max_rank = 1
    pn_rank = {}
    for i in range(num_children):
        child = children[i]
        pn_rank[child] = current_rank
        max_rank = current_rank
        number = (child.PN if node.PNS_type == "OR" else child.DPN)
        if i < num_children-1:
            next_number = (children[0].PN if node.PNS_type == "OR" else children[0].DPN)
            if number < next_number:
                current_rank += 1

    for i in range(num_children):
        values[i] = (children[i].q/children[i].n) + c * np.sqrt(2*np.log(node.n)/children[i].n + C_pn * (1 - pn_rank[children[i]] / max_rank))
    return children[np.argmax(values)]

def _rank(e: MCTNode):
        return (e.PN if e.PNS_type == "AND" else e.DPN)

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

def _backpropagation_PNS(node: MCTNode, reward, result) -> None:
    node.PN = (0 if result == 1 else math.inf)
    node.DPN = (math.inf if result == -1 else 0)
    # Falls result == 0 oder == 0.5 müssen beie Zahlen 1 sein, dies wird schon bei der Initatilisierung der Node sichergestellt
    
    while node is not None:
        node.n += 1
        node.q += reward
        reward = -reward
        parent = node.parent
        if parent is not None:
            if not parent.is_internal:
                parent.is_internal = True
                parent.PN = {"OR": math.inf, "AND": 0}[parent.PNS_type]
                parent.DPN = {"OR": 0, "AND": math.inf}[parent.PNS_type]
            if parent.PNS_type == "OR":
                parent.PN = min(parent.PN, node.PN)
                parent.DPN += node.DPN
            else:
                parent.PN += node.PN
                parent.DPN = min(parent.DPN, node.DPN)
        node = parent