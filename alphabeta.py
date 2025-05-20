import numpy as np
import yavalath as yav
import math
import time

class TTNode:
    def __init__(self, depth, value, node_type, best_move, sudden_end):
        self.depth = depth
        self.value = value
        self.node_type = node_type
        self.best_move = best_move
        self.sudden_end = sudden_end

class Alpha_Beta:
    def __init__(self, board: yav.Board, search_depth = 5):
        self.board = board
        self.search_depth = search_depth
        self.best_move = None

        self.run_iter_deepening = False
        self.start_time = -1
        self.max_time = -1
        self.tp_table: dict[int, TTNode] = {}

        # Pseudozufallszahlen für Zobrist Hashing
        self.table = np.random.randint(2**64-1,size=(81,2),dtype=np.uint64)
        #self.move_second_player = np.random.randint(2**64-1,dtype=np.uint64)

        # Züge die zum sicheren Verlieren führen (für das Endgame von MCTS mit Alpha-Beta verwendet)
        self.death_moves = []

    def _hash(self, board: yav.Board) -> int:
        """
        Zobrist hashing für das gebene Board.
        """
        hashcode = 0
        player = board.move_count % 2
        """if player:
            hashcode ^= self.move_second_player"""
        
        for pos in range(81):
            #bit = yav.position_to_bit(pos) ### position_to_bit kostet zu viel Zeit
            bit = pos
            if board.full & (1 << bit) != 0:
                if board.current & (1 << bit) != 0:
                    belongs_to = player
                else:
                    belongs_to = (player+1) % 2
                hashcode ^= self.table[pos][belongs_to]
        return hashcode

    def iterative_deepening(self, max_time = 15):
        start_time = time.time()
        self.run_iter_deepening = True
        best_move = None
        current_depth = 1
        self.max_time = max_time
        self.start_time = time.time()
        while time.time() - self.start_time < self.max_time:
            try:
                self.search_depth = current_depth
                best_move, sudden_end = self.alpha_beta(current_depth)
                current_depth += 1
            except TimeoutError:
                break
        print("Zeit all Iterations: " + str(time.time()-start_time))
        print(self.best_move)
        return best_move, sudden_end
    
    def alpha_beta(self, depth = -1):
        if depth == -1:
            # Falls alpha_beta nicht mit iterativer Tiefensuche aufgerufen wird
            depth = self.search_depth
        inf = math.inf
        start_time = time.time()
        print("")
        last_value, sudden_end = self._nega_max(self.board, depth, -inf, inf)
        print("Zeit: " + str(time.time()-start_time))
        if self.best_move != None:
            return self.best_move, sudden_end
        else:
            print("this shouldnt happen, unless the game is over")
            random_moves = self.board.get_possible_actions()
            if random_moves == []:
                return (0,0), 0
            return random_moves[np.random.randint(len(random_moves))], 0


    def _nega_max(self, board: yav.Board, depth, alpha, beta):
        if self.run_iter_deepening:
            if time.time() - self.start_time > self.max_time:
                raise TimeoutError("max time reached")

        hash = self._hash(board)
        entry = None
        if hash in self.tp_table:
            entry = self.tp_table[hash]
            if entry.depth >= depth:
                if entry.node_type == "EXACT":
                    return entry.value, entry.sudden_end
                elif entry.node_type == "LOWER" and entry.value >= beta:
                    alpha = max(alpha, entry.value)
                elif entry.node_type == "UPPER" and entry.value < alpha:
                    beta = min(beta, entry.value)
            if alpha >= beta:
                return entry.value, entry.sudden_end

        if depth == 0 or board.is_over:
            return -evaluate(board), board.is_end_opponent() * (-1 if self.search_depth % 2 == 1 else 1)
        
        max_value = -math.inf
        best_move = None
        sudden_end = 1 if depth % 2 == 1 else -1 ### TODO is this correct?

        moves = board.get_possible_actions()
        if self.run_iter_deepening and entry is not None:
            moves.remove(entry.best_move)
            moves.insert(0, entry.best_move)
        
        for move in moves:
            new_board, result = board.simulate_move(move)
            value, end = self._nega_max(new_board, depth-1, -beta, -alpha)
            value = -value

            if (depth % 2 == 0 and end > sudden_end) or (depth % 2 == 1 and end < sudden_end):
                sudden_end = end
            if depth == self.search_depth:
                if end == -1:
                    self.death_moves.append(move)

            if value > max_value:
                max_value = value
                best_move = move

                if value > alpha:
                    alpha = value
            if value >= beta:
                break

        if depth == self.search_depth:
            self.best_move = best_move
        
        if max_value >= beta:
            node_type = "LOWER"
        elif max_value <= alpha:
            node_type = "UPPER"
        else:
            node_type = "EXACT"

        assert best_move is not None, f"best_move is None at depth {depth}"
        self.tp_table[hash] = TTNode(depth, max_value, node_type, best_move, sudden_end)
        return max_value, sudden_end


# bitboards where the coordinates where the border blocks a row beeing completed are set to 1 and the rest to 0
bb_ver_left_two_row = 226895168490722393064963
bb_ver_left_one_gap = 75631722830240797688321
bb_ver_right_two_row = 908468717675168296611852
bb_ver_right_one_gap = 302822905891722765537284

bb_bt_left_two_row = 9033613328809503
bb_bt_left_one_gap = 17609382707231
bb_bt_right_two_row = 4583872209753932562432
bb_bt_right_one_gap = 8935423410826379264

bb_tb_left_two_row = 70575306079775
bb_tb_left_one_gap = 68853957151
bb_tb_right_two_row = 2291942662183741030400
bb_tb_right_one_gap = 2236041621642674176

"""
TODO: z.B. |x-x-x| kann nicht zum gewinnen benutzt werden wird aber trozdem positiv bewertet
"""
def evaluate(board: yav.Board, defence = False, p_two_row = 5, p_one_gap = 5, p_two_gap = 20, p_four_threat = 41, debug=False):
    result = board.is_end_opponent()
    if result != 0:
        if result == 0.5:
            return 0
        score = 1e9 * result
        if debug:
            print()
            print(score)
        return score

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
        #checking if there is space to finish the game with this row
    ver_right = ver_two_row & (bb_ver_right_two_row | (board.full >> 2) | (board.full >> 3))
    ver_left = ver_two_row & (bb_ver_left_two_row | (board.full << 1) | (board.full << 2))        
    ver_blocked = ver_left & ver_right
    diag_bt_right = diag_bt_two_row & (bb_bt_right_two_row | (board.full >> 18) | (board.full >> 27))
    diag_bt_left = diag_bt_two_row & (bb_bt_left_two_row | (board.full << 9) | (board.full << 18))
    diag_bt_blocked = diag_bt_right & diag_bt_left
    diag_tb_right = diag_tb_two_row & (bb_tb_right_two_row | (board.full >> 20) | (board.full >> 30))
    diag_tb_left = diag_tb_two_row & (bb_tb_left_two_row | (board.full << 10) | (board.full << 20))
    diag_tb_blocked = diag_tb_right & diag_tb_left
    n_two_row_blocked = ver_blocked.bit_count() + diag_bt_blocked.bit_count() + diag_tb_blocked.bit_count()
    n_two_row -= n_two_row_blocked

    

    # one_gap = int("101",2)
    ver_one_gap = bitboard & (bitboard >> 2)
    diag_bt_one_gap = bitboard & (bitboard >> 18)
    diag_tb_one_gap = bitboard & (bitboard >> 20)
    n_one_gap = ver_one_gap.bit_count() + diag_bt_one_gap.bit_count() + diag_tb_one_gap.bit_count()
        #accounting for enemy
    ver_blocked = ver_one_gap & (opponent >> 1)
    diag_bt_blocked = diag_bt_one_gap & (opponent >> 9)
    diag_tb_blocked = diag_tb_one_gap & (opponent >> 10)
        #checking if there is space to finish the game with this row
    ver_right = ver_one_gap & (bb_ver_right_one_gap | (board.full >> 3))
    ver_left = ver_one_gap & (bb_ver_left_one_gap | (board.full << 1))
    ver_blocked |= (ver_left & ver_right)
    diag_bt_right = diag_bt_one_gap & (bb_bt_right_one_gap | (board.full >> 27))
    diag_bt_left = diag_bt_one_gap & (bb_bt_left_one_gap | (board.full << 9))
    diag_bt_blocked |= (diag_bt_right & diag_bt_left)
    diag_tb_right = diag_tb_one_gap & (bb_tb_right_one_gap | (board.full >> 30))
    diag_tb_left = diag_tb_one_gap & (bb_tb_left_one_gap | (board.full << 10))
    diag_tb_blocked |= (diag_tb_right & diag_tb_left)
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
    diag_tb_blocked = (diag_tb_two_gap & (opponent >> 10)) | (diag_tb_two_gap & (opponent >> 20))
    n_two_gap_blocked = ver_blocked.bit_count() + diag_bt_blocked.bit_count() + diag_tb_blocked.bit_count()
    n_two_gap -= n_two_gap_blocked

    # four_threat_1 = int("1101",2)
    ver = ver_one_gap & ver_two_gap
    diag_bottom_top = diag_bt_one_gap & diag_bt_two_gap
    diag_top_bottom = diag_tb_one_gap & diag_tb_two_gap
    n_four_threat = ver.bit_count() + diag_bottom_top.bit_count() + diag_top_bottom.bit_count()
        #accounting for enemy
    ver_blocked = ver & (opponent >> 1)
    diag_bt_blocked = diag_bottom_top & (opponent >> 18)
    diag_tb_blocked = diag_top_bottom & (opponent >> 20)
    n_four_threat_blocked = ver_blocked.bit_count() + diag_bt_blocked.bit_count() + diag_tb_blocked.bit_count()

    # four_threat_2 = int("1011",2)
    ver = ver_two_row & ver_two_gap
    diag_bottom_top = diag_bt_two_row & diag_bt_two_gap
    diag_top_bottom = diag_tb_two_row & diag_tb_two_gap
    n_four_threat += ver.bit_count() + diag_bottom_top.bit_count() + diag_top_bottom.bit_count()
        #accounting for enemy
    ver_blocked = ver & (opponent >> 2)
    diag_bt_blocked = diag_bottom_top & (opponent >> 9)
    diag_tb_blocked = diag_top_bottom & (opponent >> 10)
    n_four_threat_blocked += ver_blocked.bit_count() + diag_bt_blocked.bit_count() + diag_tb_blocked.bit_count()

    n_four_threat -= n_four_threat_blocked
    
    score = (n_two_row * p_two_row) + (n_one_gap * p_one_gap) + (n_two_gap * p_two_gap) + (n_four_threat * p_four_threat)
    if debug:
        print()
        print("individual scores:")
        print((n_two_row * p_two_row))
        print(n_one_gap * p_one_gap)
        print(n_two_gap * p_two_gap)
        print((n_four_threat * p_four_threat))
        print("---")
        print(score)

    if defence:
        return score
    else:
        return score - evaluate(board, defence=True, debug=False)