import math

board = int('0',2)
full = int('0',2)

def create_empty_board():
    return int('0',2)

def is_end():
    """
    function returns:
        1 if player wins
        -1 if player loses
        0 if game continues
    """

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

def do_move(coords):
    bit = coords_to_bit(coords)
    return board | (1 << bit)

def undo_move(coords):
    bit = coords_to_bit(coords)
    return board & ~(1 << bit)

def coords_to_bit(coords):
    row, col = coords
    return row*9 + col

def bit_to_coords(bit):
    modulo = bit % 9
    return (modulo, math.floor(modulo)*9)


def print_board():
    for row in range(9):
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
            print(str((board >> bit) & 1) + " ", end="")

        print("")




if __name__ == '__main__':
    board = do_move((0,0))
    board = do_move((1,1))
    board = do_move((2,3))
    print_board()
    print(is_end())