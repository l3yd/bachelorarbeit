import numpy as np
import yavalath as yav
import math


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
            return self.best_move
        else:
            print("ERROR: Game should already be over?!")
            random_moves = self.board.get_possible_actions()
            if random_moves == []:
                return (0,0)
            np.random.shuffle(random_moves)
            return random_moves[0]


    def _nega_max(self, board: yav.Board, depth, alpha, beta):
        if depth == 0 or board.move_count == 61:
            return -self.evaluate(board)
        
        max_value = alpha
        for move in board.get_possible_actions():
            new_board, result = board.simulate_move(move)
            self.moves[depth-1] = move
            value = -(self._nega_max(new_board, depth-1, -beta, -max_value))
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
            return score
        else:
            return score  - self.evaluate(board, True)
