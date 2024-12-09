import math

current: int
full: int
move_count: int


def setup_board():
    global current
    global full
    global move_count

    current = 0
    full = 0
    move_count = 0

def is_end():
    """
    function returns:
        1 if player wins
        -1 if player loses
        0 if game continues
    """

    board = full ^ current

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
    """
    returns result of is_end after given move
    """
    global current
    global full
    global move_count

    bit = coords_to_bit(coords)
    current ^= full
    full |= (1<<bit)
    move_count += 1
    return is_end()

def undo_move(coords):
    """
    broken
    """
    bit = coords_to_bit(coords)
    return board & ~(1 << bit)

def coords_to_bit(coords):
    row, col = coords
    return row*9 + col

def bit_to_coords(bit):
    return (math.floor(bit / 9), bit % 9)


def print_board():
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
            next_turn = "0 "
            current_turn = "X "
            if move_count % 2 == 0:
                next_turn = "X "
                current_turn = "O "
            if (full >> bit) & 1 == 1:
                if (current >> bit) & 1 == 1:
                    print(next_turn, end="")
                else:
                    print(current_turn, end="")
            else:
                print("* ", end="")
        if 5 + row < 9:
            print(str(5+row), end="")
        print("")


### TESTING

def game2p():
    setup_board()
    print("Provide moves in the format: x y")
    player = 1
    while True:
        move = input("Player " + str(player) + ", please provide a move: ")
        print("")
        print("")
        coords = move.split()
        result = do_move((int(coords[0]),int(coords[1])))
        print_board()
        if result == 1:
            print("Player " + str(player) + " wins!")
            break
        player = (player % 2) +1
        if result == -1:
            print("Player " + str(player) + " wins!")
            break

def basic_test():
    setup_board()
    x = do_move((0,0))
    x = do_move((1,1))
    x = do_move((2,2))
    x = do_move((3,3))
    x = do_move((4,4))
    print_board()

if __name__ == '__main__':
    basic_test()
    #game2p()