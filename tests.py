import yavalath as yav
import sys
import numpy as np
import minimax as mm
import alphabeta as ab
import mcts

def game(board:yav.Board, players = ["human", "human"], start = np.random.randint(1,3), printing = True):
    board.reset_board()
    if printing:
        if players[0] or players[1]:
            print("Provide moves in the format: x y")
        board.print_board()
    turn = start
    while True:
        coords = find_move(players, turn, board, printing)
        result = board.do_move((int(coords[0]),int(coords[1])))
        if printing:
            print("")
            print("")
            board.print_board()
        if result == 1:
            if printing:
                announce_winner(players, turn)
            return turn
        turn = (turn % 2) +1
        if result == -1:
            if printing:
                announce_winner(players, turn)
            return turn
        #print(board.move_count)

def find_move(players, turn, board, printing):
    player = players[turn-1]
    if player == "human":
        move = input("Player " + str(turn) + ", please provide a move: ")
        coords = move.split()
    else:
        if printing:
            print(str(player) + "(" + str(turn) + ")'s turn")
        if player == "minimax":
            coords = mm.MiniMax(board).main()
        elif player == "alphabeta":
            coords = ab.Alpha_Beta(board).alpha_beta()
        elif player == "mcts":
            coords = mcts.MCTS(board)
        elif player == "abiter":
            coords = ab.Alpha_Beta(board).iterative_deepening()
        else: # (randomplayer):
            actions = board.get_possible_actions()
            np.random.shuffle(actions)
            coords =  actions[0]
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

legal_players = ["human", "minimax", "mm", "alphabeta", "ab", "mcts", "random","abiter"]

if __name__ == '__main__':
    Board = yav.Board()
    arg = sys.argv[1]
    if arg == "game" or arg == "n_game":
        """
            game 'player' 'player' [staring_player]
            n_game 'player' 'player' 'n_iterrations'
        """
        player1 = sys.argv[2]
        player2 = sys.argv[3]
        assert player1 in legal_players and player2 in legal_players
        players = [player1, player2]
        for i in range(len(players)):
            if players[i] == "mm":
                players[i] = "minimax"
            if players[i] == "ab":
                players[i] = "alphabeta"
        if arg == "game":
            try:
                game(Board, players, int(sys.argv[4]))
            except:
                game(Board, players)
        else: # arg == "n_game"
            n_iterations = int(sys.argv[4])
            wins = [0,0]
            for i in range(n_iterations):
                winner = game(Board, players, printing=False)
                wins[winner-1] += 1
                print("Game " + str(i+1) + " (of " + str(n_iterations) + ") is over.")
            print(str(players[0]) + " won " + str(wins[0]) + " | " + str(players[1]) + " won " + str(wins[1]))
            winrate = (max(wins)/n_iterations) * 100
            print(str(winrate) + "%")
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
    elif arg == "ab_borders":
        coords = [(2,6),(4,8)]
        coords_current = [(1,5)]

        for x in coords:
            bit = yav.coords_to_bit(x)
            Board.full |= (1 << bit)
        for y in coords_current:
            bit = yav.coords_to_bit(y)
            Board.current |= (1 << bit)
        
        Board.full |= Board.current
        Board.print_board()
        albe = ab.Alpha_Beta(Board)
        print(albe.evaluate(Board))
    elif arg == "generation":
        coords = [(0,3),(1,4),(2,5),(3,6),(4,7),(6,7),(7,7),(8,7),(5,7)]
        for x in coords:
            bit = yav.coords_to_bit(x)
            Board.full |= (1 << bit)
        Board.print_board()
        print(Board.full)
    elif arg == "zusammen":
        n1 = 302822905891722765537284
        n2 = 605645811783445531074568
        Board.full = n1 + n2
        Board.print_board()
        print(Board.full)
    else:
        print("Name of test not found")