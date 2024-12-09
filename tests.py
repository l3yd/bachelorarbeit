import yavalath as yav
import sys

def basic_test(b: yav.Board):
    b.reset_board()
    x = b.do_move((0,0))
    x = b.do_move((1,1))
    x = b.do_move((2,2))
    x = b.do_move((3,3))
    x = b.do_move((4,4))
    b.print_board()
    print()
    print("is_end: " + str(x))


def game2p(b: yav.Board):
    b.reset_board()
    b.print_board()
    print("Provide moves in the format: x y")
    player = 1
    while True:
        move = input("Player " + str(player) + ", please provide a move: ")
        print("")
        print("")
        coords = move.split()
        result = b.do_move((int(coords[0]),int(coords[1])))
        b.print_board()
        if result == 1:
            print("Player " + str(player) + " wins!")
            break
        player = (player % 2) +1
        if result == -1:
            print("Player " + str(player) + " wins!")
            break

if __name__ == '__main__':
    Board = yav.Board()
    arg = sys.argv[1]
    if arg == "basic":
        basic_test(Board)
    elif arg == "game":
        game2p(Board)
    else:
        print("Provide a test from this list: basic, game")