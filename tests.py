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
    board.full = int("1111",2)
    board.current = int("100",2)
    board.print_board()
    ab = alg.Alpha_Beta(board)
    print(ab.evaluate(board))

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

def minimax_vs_mcts(b):
    print()
    player = np.random.randint(1,3)
    print()
    b.print_board()
    while True:
        if player == 1:
            coords = alg.MiniMax(b).main()
        else:
            coords = alg.MCTS(b)
        print("")
        print("")
        result = b.do_move((int(coords[0]),int(coords[1])))
        b.print_board()
        if result == 1:
            if player == 1:
                print("MinMax wins!")
            else:
                print("MCTS wins!")
            break
        if result == -1:
            if player == 1:
                print("MCTS wins!")
            else:
                print("MiniMax wins!")
            break
        player = (player % 2) +1

def minimax_vs_player(b):
    b.reset_board()
    print()
    print("Provide moves in the format: x y")
    player = np.random.randint(1,3)
    player = 2
    if player == 1:
        print("Player starts!")
    else:
        print("Minimax starts!")
    print()
    b.print_board()
    while True:
        if player == 1:
            move = input("Player " + str(player) + ", please provide a move: ")
            coords = move.split()
        else:
            coords = alg.MiniMax(b).main()
        print("")
        print("")
        result = b.do_move((int(coords[0]),int(coords[1])))
        b.print_board()
        if result == 1:
            if player == 1:
                print("Player wins!")
            else:
                print("Minmax wins!")
            break
        player = (player % 2) +1
        if result == -1:
            if player == 1:
                print("Player wins!")
            else:
                print("Minimax wins!")
            break

def ab_vs_player(b):
    b.reset_board()
    print()
    print("Provide moves in the format: x y")
    player = np.random.randint(1,3)
    player = 1
    if player == 1:
        print("Player starts!")
    else:
        print("Alpha-Beta starts!")
    print()
    b.print_board()
    while True:
        if player == 1:
            move = input("Player " + str(player) + ", please provide a move: ")
            coords = move.split()
        else:
            coords = alg.Alpha_Beta(b).alpha_beta()
        print("")
        print("")
        result = b.do_move((int(coords[0]),int(coords[1])))
        b.print_board()
        if result == 1:
            if player == 1:
                print("Player wins!")
            else:
                print("Alpha-Beta wins!")
            break
        player = (player % 2) +1
        if result == -1:
            if player == 1:
                print("Player wins!")
            else:
                print("Minimax wins!")
            break

def minimax_2(b):
    b.reset_board()
    print()
    print("Provide moves in the format: x y")
    player = np.random.randint(1,3)
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

def create_test_board(b):
    coords = [(2,6), (3,0), (3,2), (3,3), (6,3)]
    for i in range(len(coords)):
        b.full |= (1<<yav.coords_to_bit(coords[i]))
    coords = [(1,1), (4,0), (4,7), (5,8)]
    for i in range(len(coords)):
        b.current |= (1<<yav.coords_to_bit(coords[i]))
    b.full |= b.current
    b.move_count = 9
    b.print_board()
    return b

def one_position_minimax(b):
    coords = alg.MiniMax(b).main()
    b.do_move(coords)
    b.print_board()

def create_another_test_board(b):
    coords = [(0,1), (1,1), (3,1)]
    for i in range(len(coords)):
        b.full |= (1<<yav.coords_to_bit(coords[i]))
    coords = [(0,0), (0,2), (0,3)]
    for i in range(len(coords)):
        b.current |= (1<<yav.coords_to_bit(coords[i]))
    b.full |= b.current
    b.move_count = 6
    b.print_board()
    return b

def another_position_minimax(b):
    coords = alg.MiniMax(b).main()
    b.do_move(coords)
    b.print_board()

def test_is_end(b):
    b.full |= (1<< yav.coords_to_bit((2,1)))
    b.current |= (1<< yav.coords_to_bit((1,0)))
    test_coord = (4,0)
    b.current |= (1<< yav.coords_to_bit(test_coord))
    b.full |= b.current
    b.move_count += 3
    b.print_board()
    print(b.is_end())
    print(b.is_end_opponent())

def create_test_board_ab(b):
    coords = [(1,4), (4,6), (5,4), (8,4), (8,5), (8,7)]
    for i in range(len(coords)):
        b.full |= (1<<yav.coords_to_bit(coords[i]))
    coords = [(0,0), (0,4), (1,2), (2,1), (2,5), (4,0)]
    for i in range(len(coords)):
        b.current |= (1<<yav.coords_to_bit(coords[i]))
    b.full |= b.current
    b.move_count = 12
    b.print_board()
    return b

def one_position_ab(b):
    ab = alg.Alpha_Beta(b)
    coords = ab.alpha_beta()
    correct_board = b.simulate_move((2,0))[0].simulate_move((0,1))[0].simulate_move((0,2))[0].simulate_move((0,3))[0]
    b.do_move(coords)
    b.print_board()
    
    print(ab.evaluate(b))
    print(ab.evaluate(correct_board))
    

def create_another_test_board_ab(b):
    coords = [(2,1), (3,3), (8,5)]
    for i in range(len(coords)):
        b.full |= (1<<yav.coords_to_bit(coords[i]))
    coords = [(0,0), (1,0), (3,0)]
    for i in range(len(coords)):
        b.current |= (1<<yav.coords_to_bit(coords[i]))
    b.full |= b.current
    b.move_count = 6
    b.print_board()
    return b

def test_full_board(b):
    b.full = int("101100000111111000111111100111111110111111111011111111001111111000111111000011111", 2)
    b.move_count = 61
    ab = alg.Alpha_Beta(b)
    coords = ab.alpha_beta()
    print(coords)

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
        eval_ab(Board)
    elif arg == "mcts_vs_ab_extra":
        """Board.full = int("10000000000001000001111000001111",2)
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
        Board.print_board()"""
        Board.full = int("10000000000000000000000000000000000000000000000000000000000000000001",2)
        Board.current = int("1",2)
        Board.move_count = 2
        Board.print_board()
        coords = alg.Alpha_Beta(Board).alpha_beta()
        print("")
        print("")
        result = Board.do_move((int(coords[0]),int(coords[1])))
        Board.print_board()
        #mcts_vs_ab(Board)
    elif arg == "mcts_vs_ab":
        mcts_vs_ab(Board)
    elif arg == "minimax_vs_mcts":
        minimax_vs_mcts(Board)
    elif arg == "minimax_vs_player":
        minimax_vs_player(Board)
    elif arg == "ab_vs_player":
        ab_vs_player(Board)
    elif arg == "minimax_2":
        minimax_2(Board)
    elif arg == "one_position_minimax":
        Board = create_test_board(Board)
        one_position_minimax(Board)
    elif arg == "another_position_minimax":
        Board = create_another_test_board(Board)
        another_position_minimax(Board)
    elif arg == "is_end":
        Board = create_another_test_board(Board)
        test_is_end(Board)
    elif arg == "one_position_ab":
        Board = create_test_board_ab(Board)
        one_position_ab(Board)
    elif arg == "another_position_ab":
        Board = create_another_test_board_ab(Board)
        one_position_ab(Board)
    elif arg == "test_full_board":
        test_full_board(Board)
    else:
        print("Name of test not found")