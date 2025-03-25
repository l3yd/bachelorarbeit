import yavalath as yav
import algorithms as alg
import sys
import numpy as np
import minimax as mm
import alphabeta as ab
import mcts

def game(board:yav.Board, players = ["human", "human"], start = np.random.randint(1,3)):
    board.reset_board()
    board.print_board()
    print("Provide moves in the format: x y")
    turn = start
    while True:
        coords = find_move(players, turn, board)
        print("")
        print("")
        result = board.do_move((int(coords[0]),int(coords[1])))
        board.print_board()
        if result == 1:
            announce_winner(players, turn)
            break
        turn = (turn % 2) +1
        if result == -1:
            announce_winner(players, turn)
            break

def find_move(players, turn, board):
    player = players[turn-1]
    if player == "human":
        move = input("Player " + str(turn) + ", please provide a move: ")
        coords = move.split()
    else:
        print(str(player) + "(" + str(turn) + ")'s turn")
        if player == "minimax":
            coords = mm.MiniMax(board).main()
        elif player == "alphabeta":
            coords = ab.Alpha_Beta(board).alpha_beta()
        else: # player == "mcts":
            coords = mcts.MCTS(board)
    return coords

def announce_winner(players, turn):
    player = players[turn-1]
    if player == "human":
        print("Player " + str(turn) + " wins!")
    else:
        print(str(player) + "(" + str(turn) + ") wins!")

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
    print("is_end: " + str(x))

def mcts_states(b: yav.Board):
    b.full += int("1101000001011",2)
    b.current += int("1011",2)
    b.print_board()
    mcts.MCTS(b)
    b.print_board()

def eval_ab(board: yav.Board):
    board.full = int("1111",2)
    board.current = int("100",2)
    board.print_board()
    instance = ab.Alpha_Beta(board)
    print(instance.evaluate(board))

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
    coords = mm.MiniMax(b).main()
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
    ab = ab.Alpha_Beta(b)
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

def test_full_board_ab(b):
    b.full = int("101100000111111000111111100111111110111111111011111111001111111000111111000011111", 2)
    b.move_count = 61
    instance = ab.Alpha_Beta(b)
    coords = instance.alpha_beta()
    print(coords)

legal_players = ["human", "minimax", "mm", "alphabeta", "ab", "mcts"]

if __name__ == '__main__':
    Board = yav.Board()
    arg = sys.argv[1]
    if arg == "game":
        player1 = sys.argv[2]
        player2 = sys.argv[3]
        assert player1 in legal_players and player2 in legal_players
        players = [player1, player2]
        for i in range(len(players)):
            if players[i] == "mm":
                players[i] = "minimax"
            if players[i] == "ab":
                players[i] = "alphabeta"
        try:
            game(Board, players, sys.argv[4])
        except:
            game(Board, players)
    elif arg == "basic":
        basic_test(Board)
    elif arg == "mcts_states":
        mcts_states(Board)
    elif arg == "eval_ab":
        eval_ab(Board)
    elif arg == "one_position_minimax":
        Board = create_test_board(Board)
        one_position_minimax(Board)
    elif arg == "another_position_minimax":
        Board = create_another_test_board(Board)
        one_position_minimax(Board)
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
        test_full_board_ab(Board)
    else:
        print("Name of test not found")