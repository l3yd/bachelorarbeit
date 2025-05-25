import numpy as np
import yavalath as yav
import alphabeta as ab
import time
import math


class MCTNode:
    def __init__(self, board: yav.Board, possible_actions: list[tuple[int,int]]):
        self.state = board
        self.q = 0
        self.n = 0
        self.parent = None
        self.a = None
        self.actions = board.get_possible_actions()
        self.child_nodes = []

        # keeping track of moves leading to sudden death (used in root note for MCTS with alphabeta)
        self.death_moves = []

        # variables used by PNS
        self.PN = 1
        self.DPN = 1
        self.PNS_type = None
        self.is_internal = False
    
    def print_node(self):
        self.state.print_board()
        print("q: " + str(self.q))
        print("n: " + str(self.n))
        print("parent: " + str(self.parent))
        print("a: " + str(self.a))
        print("actions: " + str(self.actions))
        print("child_nodes: " + str(self.child_nodes))
        print("death_moves: " + str(self.death_moves))
        print("PN: " + str(self.PN))
        print("DPN: " + str(self.DPN))
        print("PNS_type: " + str(self.PNS_type))
        print("is_internal: " + str(self.is_internal))

def bewertung(e):
    return e.q/e.n

def sort_by_action(e):
    return e.a

def MCTS_alphabeta(board: yav.Board, c = np.sqrt(2), k = 4, use_gdk=True, max_time = 15):
    root = MCTNode(board, board.get_possible_actions())
    start_time = time.time()
    n_iter = 0
    nodes_expanded = 0
    while time.time() - start_time < max_time:
        steps_from_root, expanded = _MCTS_one_iteration(root, c, use_gdk)
        if expanded:
            nodes_expanded += 1
        n_iter += 1
        if steps_from_root < k and root.death_moves == []:
            ab_object = ab.Alpha_Beta(board,k)
            move, sudden_end = ab_object.iterative_deepening(detect_sudden_end_k=k)
            if sudden_end == 1:
                print(f"Number of iterations: {n_iter} and sudden win was found!")
                return move, n_iter, nodes_expanded, True
            elif sudden_end == -1:
                root.death_moves = ab_object.death_moves
    #print("Number of iterations: " + str(n_iter))
    return _UCT(root, 0).a, n_iter, nodes_expanded, False

def MCTS_PNS(board: yav.Board, c = np.sqrt(2), C_pn = 1, use_gdk=True, max_time = 15):
    root = MCTNode(board, board.get_possible_actions())
    root.PNS_type = "OR"
    start_time = time.time()
    n_iter = 0
    nodes_expanded = 0
    while time.time() - start_time < max_time:
        v, expanded = _selection(root, c, C_pn)
        leaf_result = v.state.is_end_opponent()
        reward, _ = _simulation_gdk(v.state) if use_gdk else _simulation(v.state)
        _backpropagation_PNS(v, reward, leaf_result)
        if expanded:
            nodes_expanded += 1
        n_iter += 1
    #print("Number of iterations: " + str(n_iter))
    return _UCT(root, 0).a, n_iter, nodes_expanded

def MCTS(board: yav.Board, c = np.sqrt(2), use_gdk=True, max_time = 15, plot=False):
    root = MCTNode(board, board.get_possible_actions())
    start_time = time.time()
    n_iter = 0

    values_to_plot = []
    nodes_expanded = 0
    while time.time() - start_time < max_time:
        if plot and root.child_nodes != []:
            steps, expanded, uct_values = _MCTS_one_iteration(root, c,use_gdk, plot=plot)
            values_to_plot.append({'time': time.time()-start_time,
                               'uct': uct_values[0],
                               'exploitation': uct_values[1],
                               'exploration': uct_values[2]})
        else:
            steps, expanded = _MCTS_one_iteration(root, c,use_gdk)
        if expanded:
            nodes_expanded += 1
        n_iter += 1
    #print("Number of iterations: " + str(n_iter))
    if plot:
        return _UCT(root, 0).a, n_iter, nodes_expanded, values_to_plot
    return _UCT(root, 0).a, n_iter, nodes_expanded

def _MCTS_one_iteration(root: MCTNode, c, use_gdk, C_pn=0, plot=False):
    if plot and root.child_nodes != []:
        uct_values_at_root = _UCT(root, c, plot)
    v, expanded = _selection(root, c, C_pn)
    reward, steps = _simulation_gdk(v.state) if use_gdk else _simulation(v.state)
    if plot and root.child_nodes != []:
        return _backpropagation_negamax(v,reward) + steps, expanded, uct_values_at_root
    return _backpropagation_negamax(v, reward) + steps, expanded

def _selection(node: MCTNode, c, C_pn=0) -> tuple[MCTNode, bool]:
    while node.state.is_over == False:
        if len(node.actions) == 0:
            node = _UCT(node, c) if C_pn == 0 else _UCT_PNS(node, c, C_pn)
        else:
            return _expansion(node), True
    return node, False

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

def _UCT(node: MCTNode, c, plot=False) -> MCTNode:
    num_children = len(node.child_nodes)
    values = np.zeros(num_children)
    children = node.child_nodes
    if node.death_moves != []:
        children = list(set(children) - set(node.death_moves))
    for i in range(num_children):
        values[i] = (children[i].q/children[i].n) + c * np.sqrt(np.log(node.n)/children[i].n)

    if plot:
        i = np.argmax(values)
        return [values[i], (children[i].q/children[i].n), c * np.sqrt(2*np.log(node.n)/children[i].n)]
    return children[np.argmax(values)]


# modified UCT for PN-MCTS

def _UCT_PNS(node: MCTNode, c, C_pn, plot=False) -> MCTNode:
    num_children = len(node.child_nodes)
    children = node.child_nodes

    children.sort(key=_rank)
    current_rank = 1
    max_rank = 1
    pn_rank = {}
    for i in range(num_children):
        pn_rank[children[i]] = current_rank
        max_rank = current_rank
        if i < num_children-1:
            number = (children[i].PN if node.PNS_type == "OR" else children[i].DPN)
            next_number = (children[i+1].PN if node.PNS_type == "OR" else children[i+1].DPN)
            if number < next_number:
                current_rank += 1

    values = np.zeros(num_children)
    for i in range(num_children):
        values[i] = (children[i].q/children[i].n) + c * np.sqrt(2*np.log(node.n)/children[i].n + C_pn * (1 - pn_rank[children[i]] / max_rank))
    if plot:
        return [values[i], (children[i].q/children[i].n), c * np.sqrt(2*np.log(node.n)/children[i].n), (1 - pn_rank[children[i]] / max_rank)]
    return children[np.argmax(values)]

def _rank(e: MCTNode):
        return (e.PN if e.PNS_type == "AND" else e.DPN)

def _simulation(state: yav.Board) -> int:
    player = state.move_count % 2
    result = state.is_end()
    steps = 0
    while result == 0:
        actions = state.get_possible_actions()
        state, result = state.simulate_move(actions[np.random.randint(0, len(actions))])
        steps += 1
    if state.move_count % 2 != player:
        result = -result
    return result, steps

def _backpropagation_negamax(node: MCTNode, reward) -> int:
    steps = 0
    while node is not None:
        node.n += 1
        node.q += reward
        if reward != 0.5:
            reward = -reward
        node = node.parent

        steps += 1
    return steps


# Backpropagation for PN-MCTS

def _backpropagation_PNS(node: MCTNode, reward, result) -> None:
    node.PN = (0 if result == 1 else math.inf)
    node.DPN = (math.inf if result == -1 or result == 0.5 else 0)
    # Falls result == 0 oder müssen beide Zahlen 1 sein, dies wird schon bei der Initatilisierung der Node sichergestellt
    update_parents = True
    while node is not None:
        node.n += 1
        node.q += reward
        if reward != 0.5:
            reward = -reward

        parent = node.parent
        if parent is not None:
            if not parent.is_internal:
                parent.is_internal = True
            if update_parents:
                pn, dpn = calculate_PN_DPN(parent)
                if pn == parent.PN and dpn == parent.DPN:
                    update_parents = False
                parent.PN = pn
                parent.DPN = dpn

        node = parent

def calculate_PN_DPN(node: MCTNode) -> tuple[int, int]:
    pn_list = [child.PN for child in node.child_nodes]
    dpn_list = [child.DPN for child in node.child_nodes]

    pn = (min(pn_list) if node.PNS_type == "OR" else sum(pn_list))
    dpn = (sum(dpn_list) if node.PNS_type == "OR" else min(dpn_list))

    return pn, dpn

# Simulation using General Domain Knowledge

def _simulation_gdk(state:yav.Board) -> int:
    player = state.move_count % 2
    result = state.is_end()
    steps = 0
    while result == 0:
        move = None
        move = find_winning_move(state)
        if move == None:
            move = find_blocking_win(state)
            if move == None:
                move = find_not_losing(state)
                if move == None:
                    moves = state.get_possible_actions()
                    move = moves[np.random.randint(len(moves))]
        state, result = state.simulate_move(move)
        steps += 1
    if state.move_count % 2 != player:
        result = -result
    return result, steps

def find_winning_move(state: yav.Board):
    bitboard = state.current
    opponent = state.full ^ state.current

    # two_gap = int("1001",2)
    ver_two_gap = bitboard & (bitboard >> 3)
    diag_bt_two_gap = bitboard & (bitboard >> 27)
    diag_tb_two_gap = bitboard & (bitboard >> 30)

    # four_threat_1 = int("1101",2)
    ver = bitboard & (bitboard >> 2) & ver_two_gap & ~(opponent >> 1)
    diag_bottom_top = bitboard & (bitboard >> 18) & diag_bt_two_gap & ~(opponent >> 9)
    diag_top_bottom = bitboard & (bitboard >> 20) & diag_tb_two_gap & ~(opponent >> 10)
    if ver != 0:
        return yav.bit_to_coords(random_index(ver) + 1)
    if diag_bottom_top != 0:
        return yav.bit_to_coords(random_index(diag_bottom_top) + 9)
    if diag_top_bottom != 0:
        return yav.bit_to_coords(random_index(diag_top_bottom) + 10)

    # four_threat_2 = int("1011",2)
    ver = bitboard & (bitboard >> 1) & ver_two_gap & ~(opponent >> 2)
    diag_bottom_top = bitboard & (bitboard >> 9) & diag_bt_two_gap & ~(opponent >> 18)
    diag_top_bottom = bitboard & (bitboard >> 10) & diag_tb_two_gap & ~(opponent >> 20)
    if ver != 0:
        return yav.bit_to_coords(random_index(ver) + 2)
    if diag_bottom_top != 0:
        return yav.bit_to_coords(random_index(diag_bottom_top) + 18)
    if diag_top_bottom != 0:
        return yav.bit_to_coords(random_index(diag_top_bottom) + 20)
    
    return None


def find_blocking_win(state: yav.Board):
    me = state.current
    bitboard = state.full ^ state.current

    # two_gap = int("1001",2)
    ver_two_gap = bitboard & (bitboard >> 3)
    diag_bt_two_gap = bitboard & (bitboard >> 27)
    diag_tb_two_gap = bitboard & (bitboard >> 30)

    # four_threat_1 = int("1101",2)
    ver = bitboard & (bitboard >> 2) & ver_two_gap & ~(me >> 1)
    diag_bottom_top = bitboard & (bitboard >> 18) & diag_bt_two_gap & ~(me >> 9)
    diag_top_bottom = bitboard & (bitboard >> 20) & diag_tb_two_gap & ~(me >> 10)
    if ver != 0:
        return yav.bit_to_coords(random_index(ver) + 1)
    if diag_bottom_top != 0:
        return yav.bit_to_coords(random_index(diag_bottom_top) + 9)
    if diag_top_bottom != 0:
        return yav.bit_to_coords(random_index(diag_top_bottom) + 10)

    # four_threat_2 = int("1011",2)
    ver = bitboard & (bitboard >> 1) & ver_two_gap & ~(me >> 2)
    diag_bottom_top = bitboard & (bitboard >> 9) & diag_bt_two_gap & ~(me >> 18)
    diag_top_bottom = bitboard & (bitboard >> 10) & diag_tb_two_gap & ~(me >> 20)
    if ver != 0:
        return yav.bit_to_coords(random_index(ver) + 2)
    if diag_bottom_top != 0:
        return yav.bit_to_coords(random_index(diag_bottom_top) + 18)
    if diag_top_bottom != 0:
        return yav.bit_to_coords(random_index(diag_top_bottom) + 10)
    
    return None

def find_not_losing(state: yav.Board):
    seperating_bits = 0b11111111111111111111000001111000000111000000011000000001000000000100000000110000000111000000111100000
    to_avoid = []

    bitboard = state.current
    ver_two_row = bitboard & (bitboard >> 1)
    diag_bt_two_row = bitboard & (bitboard >> 9)
    diag_tb_two_row = bitboard & (bitboard >> 10)
    #left
    if ver_two_row != 0:
        indices = all_indices(ver_two_row & ~0b1)
        to_avoid += [x-1 for x in indices]
    if diag_bt_two_row != 0:
        indices = all_indices(diag_bt_two_row & ~0b11111)
        to_avoid += [x-9 for x in indices]
    if diag_tb_two_row != 0:
        indices = all_indices(diag_tb_two_row & ~0b1000011111)
        to_avoid += [x-10 for x in indices]
    #right
    if ver_two_row != 0:
        indices = all_indices(ver_two_row)
        to_avoid += [x+2 for x in indices]
    if diag_bt_two_row != 0:
        indices = all_indices(diag_bt_two_row)
        to_avoid += [x+18 for x in indices]
    if diag_tb_two_row & ab.bb_tb_right_two_row != 0:
        indices = all_indices(diag_tb_two_row)
        to_avoid += [x+20 for x in indices]

    ver_one_gap = bitboard & (bitboard >> 2) & ~(bitboard >> 1)
    diag_bt_one_gap = bitboard & (bitboard >> 18) & ~(bitboard >> 9)
    diag_tb_one_gap = bitboard & (bitboard >> 20) & ~(bitboard >> 10)
    if ver_one_gap != 0:
        indices = all_indices(ver_one_gap)
        to_avoid += [x+1 for x in indices]
    if diag_bt_one_gap != 0:
        indices = all_indices(diag_bt_one_gap)
        to_avoid += [x+9 for x in indices]
    if diag_tb_one_gap != 0:
        indices = all_indices(diag_tb_one_gap)
        to_avoid += [x+10 for x in indices]

    if to_avoid == []:
        return None
    to_avoid = list(set(to_avoid))
    try:
        losing_positions = sum(1 << i for i in to_avoid)
    except:
        print(to_avoid)
    return yav.bit_to_coords(random_index(~(state.full | losing_positions | seperating_bits)))


def random_index(bitboard: int) -> int:
    indices = [i for i in range(bitboard.bit_length()) if (bitboard >> i) & 1]
    return indices[np.random.randint(len(indices))]

def all_indices(bitboard: int) -> list[int]:
    indices = [i for i in range(bitboard.bit_length()) if (bitboard >> i) & 1]
    return indices