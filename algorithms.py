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

def getPossibleActions(board: yav.Board) -> list:
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
        self.actions = getPossibleActions(board)
        self.a = None
        self.parent = parent

def MCTS(board: yav.Board):
    root = MCTNode(board)
    for i in range(1000):
        v = selection(root)
        reward = simulation(v.state)
        backpropagation(v, reward)
    return UCT(root, 0).a

def selection(node: MCTNode) -> MCTNode:
    while node.state.is_end() == 0:
        if len(node.actions) > 0:
            return expansion(node)
        else:
            node = UCT(node)
    return node

def expansion(node: MCTNode) -> MCTNode:
    a = node.actions.pop()
    child_state = node.state.simulate_move(a)
    child = MCTNode(child_state, node)
    node.child_nodes.append(child)
    node.a = a
    return child

def UCT(node: MCTNode, c = 1.5):
    num_children = len(node.child_nodes)
    values = np.zeros(num_children)
    for i in range(num_children):
        values[i] = (node.child_nodes[i].q/node.child_nodes[i].n) + c * np.sqrt(2*np.log(node.n)/node.child_nodes[i].n)
    a = np.argmax(values)
    return node.child_nodes[a]

def simulation(state: yav.Board) -> int:
    while state.is_end() == 0:
        actions = getPossibleActions(state)
        state = state.simulate_move(actions[np.random.randint(0, len(actions))])
    return state.is_end()

def backpropagation(node: MCTNode, reward):
    while node is not None:
        node.n += 1
        node.q += reward
        node = node.parent


if __name__ == '__main__':
    b = yav.Board()
    print(MCTS(b))