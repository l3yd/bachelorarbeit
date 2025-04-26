import numpy as np
import yavalath as yav
import math


class MCTNode:
    def __init__(self, board: yav.Board, parent=None):
        self.state = board
        self.q = 0
        self.n = 0
        self.child_nodes = []
        self.actions = board.get_possible_actions()
        self.a = None
        self.parent = parent

def MCTS(board: yav.Board, c = np.sqrt(2)):
    root = MCTNode(board)
    for i in range(10000):
        v = _selection(root, c)
        reward = _simulation(v.state)
        _backpropagation_negamax(v, reward)
    A = np.zeros(len(root.child_nodes))
    for i in range(len(root.child_nodes)):
        child = root.child_nodes[i]
        print(str(child.a) + ": " + str(child.q) + "| " + str(child.n))
        A[i] = child.q
    #return root.child_nodes[np.argmax(A)].a
    return _UCT(root, 0).a

def _selection(node: MCTNode, c) -> MCTNode:
    while node.state.is_end() == 0:
        if len(node.actions) > 0:
            return _expansion(node)
        else:
            node = _UCT(node, c)
    return node

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
    for i in range(num_children):
        values[i] = (node.child_nodes[i].q/node.child_nodes[i].n) + c * np.sqrt(2*np.log(node.n)/node.child_nodes[i].n)
    return node.child_nodes[np.argmax(values)]

def _simulation(state: yav.Board) -> int:
    result = state.is_end()
    while result == 0:
        actions = state.get_possible_actions()
        state, result = state.simulate_move(actions[np.random.randint(0, len(actions))])
    return result #* (61 - state.move_count)

def _backpropagation_negamax(node: MCTNode, reward):
    while node is not None:
        node.n += 1
        node.q += reward
        reward = -reward
        node = node.parent
