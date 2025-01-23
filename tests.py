import yavalath as yav
import algorithms as alg
import sys
import numpy as np

def basic_test(b: yav.Board):
    b.reset_board()
    x = b.do_move((0,0))
    x = b.do_move((1,1))
    x = b.do_move((0,1))
    x = b.do_move((3,3))
    x = b.do_move((0,4))
    x = b.do_move((5,5))
    x = b.do_move((0,2))
    b.print_board()
    print(alg.evaluate(b))
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

def gameMCTS(b: yav.Board):
    b.reset_board()
    print()
    print("Provide moves in the format: x y")
    player = np.random.randint(1,3)
    player = 2
    print("Player " + str(player) + " starts!")
    print()
    b.print_board()
    while True:
        if player == 1:
            move = input("Player " + str(player) + ", please provide a move: ")
            coords = move.split()
        else:
            coords = alg.MCTS(b)
        print("")
        print("")
        result = b.do_move((int(coords[0]),int(coords[1])))
        b.print_board()
        if result == 1:
            print("Player " + str(player) + " wins!")
            break
        player = (player % 2) +1
        if result == -1:
            print("Player " + str(player) + " wins!")
            break

def mcts_states(b: yav.Board):
    b.full += int("1101000001011",2)
    b.current += int("1011",2)
    b.print_board()
    alg.MCTS(b)
    b.print_board()

def mcts_2(b: yav.Board):
    b.reset_board()
    print()
    print("Provide moves in the format: x y")
    player = np.random.randint(1,3)
    player = 2
    print("Player " + str(player) + " starts!")
    print()
    b.print_board()
    while True:
        coords = alg.MCTS(b)
        print("")
        print("")
        result = b.do_move((int(coords[0]),int(coords[1])))
        b.print_board()
        if result == 1:
            print("Player " + str(player) + " wins!")
            break
        player = (player % 2) +1
        if result == -1:
            print("Player " + str(player) + " wins!")
            break

def eval_ab(board: yav.Board):
    board.print_board()
    alg.evaluate(board)

def mcts_vs_ab(b: yav.Board):
    #b.reset_board()
    print()
    print("Provide moves in the format: x y")
    player = np.random.randint(1,3)
    player = 2
    if player == 1:
        print("MCTS starts!")
    else:
        print("Alpha-Beta starts!")
    print()
    b.print_board()
    while True:
        if player == 1:
            coords = alg.MCTS(b)
        else:
            coords = alg.Alpha_Beta(b).alpha_beta()
        print("")
        print("")
        result = b.do_move((int(coords[0]),int(coords[1])))
        b.print_board()
        if result == 1:
            if player == 1:
                print("MCTS wins!")
            else:
                print("Alpha-Beta wins!")
            break
        player = (player % 2) +1
        if result == -1:
            if player == 1:
                print("MCTS wins!")
            else:
                print("Alpha-Beta wins!")
            break

if __name__ == '__main__':
    Board = yav.Board()
    arg = sys.argv[1]
    if arg == "basic":
        basic_test(Board)
    elif arg == "g2p":
        game2p(Board)
    elif arg == "gMCTS":
        gameMCTS(Board)
    elif arg == "mcts_states":
        mcts_states(Board)
    elif arg == "mcts_2":
        mcts_2(Board)
    elif arg == "eval_ab":
        Board.full = int("11000000111",2)
        Board.current = int("100",2)
        eval_ab(Board)
    elif arg == "mcts_vs_ab":
        Board.full = int("10000000000001000001111000001111",2)
        Board.current = int("00000000000001000000011000001100",2)
        Board.move_count = 10
        evaluation = alg.Alpha_Beta(Board).evaluate(Board)
        print(evaluation)
        Board.print_board()
        Board.full = int("10000000001001000001111000001111",2)
        Board.current = int("00000000001001000000011000001100",2)
        Board.move_count = 10
        evaluation = alg.Alpha_Beta(Board).evaluate(Board)
        print(evaluation)
        Board.print_board()
        #mcts_vs_ab(Board)
    else:
        print("Provide a test from this list: basic, g2p, gMCTS, mcts_states, mcts_2, eval_ab")