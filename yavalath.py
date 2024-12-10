import math

class Board:
    def __init__(self, current=0, full=0, move_count=0):
        self.current = current
        self.full = full
        self.move_count = move_count

    def reset_board(self):
        self.current = 0
        self.full = 0
        self.move_count = 0

    def is_end(self):
        """
        function returns:
            1 if player wins
            -1 if player loses
            0.5 if the game is a draw
            0 if game continues
        """

        """ DRAW """
        if self.full == int("111110000111111000111111100111111110111111111011111111001111111000111111000011111", 2):
            return 0.5
        
        board = self.full ^ self.current

        """ WINS """
        # vertical (1-er Schritte)
        ver = board & (board >> 1) & (board >> 2)
        if ver & (board >> 3) != 0:
            return 1
        # diagonal bottom -> top (9-er Schritte)
        diag_bottom_top = board & (board >> 9) & (board >> 18)
        if diag_bottom_top & (board >> 27) != 0:
            return 1
        # diagonal top -> bottom (10-er Schritte)
        diag_top_bottom = board & (board >> 10) & (board >> 20)
        if diag_top_bottom & (board >> 30) != 0:
            return 1
        
        """ LOSES """
        if ver != 0 or diag_bottom_top != 0 or diag_top_bottom != 0:
            return -1
        
        return 0

    def do_move(self, coords) -> int:
        """
        returns result of is_end after given move
        """

        bit = coords_to_bit(coords)
        self.current ^= self.full
        self.full |= (1<<bit)
        self.move_count += 1
        return self.is_end()
    
    def simulate_move(self, coords) -> object:
        new_board = Board(self.current, self.full, self.move_count)
        result = new_board.do_move(coords)
        return new_board

    """
    def undo_move(coords):
        bit = coords_to_bit(coords)
        return board & ~(1 << bit)
    """

    def print_board(self):
        print("      0 1 2 3 4")
        for row in range(9):
            print(str(row) + " ", end="")
            for _ in range(abs(4-row)):
                print(" ", end="")

            first_col = row - 4
            if first_col < 0:
                first_col = 0
            last_col = row + 4
            if last_col > 8:
                last_col = 8

            for col in range(first_col, last_col+1):
                bit = coords_to_bit((row, col))
                next_turn = "⧆ "
                current_turn = "⧇ "
                if self.move_count % 2 == 0:
                    next_turn = "⧇ "
                    current_turn = "⧆ "
                if (self.full >> bit) & 1 == 1:
                    if (self.current >> bit) & 1 == 1:
                        print(next_turn, end="")
                    else:
                        print(current_turn, end="")
                else:
                    print("◻ ", end="")
            if 5 + row < 9:
                print(str(5+row), end="")
            print("")


def coords_to_bit(coords):
    row, col = coords
    return row*9 + col

def bit_to_coords(bit):
    return (math.floor(bit / 9), bit % 9)