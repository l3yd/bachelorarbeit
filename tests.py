import yavalath as yav
import sys
import numpy as np
import minimax as mm
import alphabeta as ab
import mcts

def game(board:yav.Board, players = ["human", "human"], start = np.random.randint(1,3), printing = True, C = [np.sqrt(2), np.sqrt(2)]):
    board.reset_board()
    if printing:
        if players[0] == "human" or players[1] == "human":
            print("Provide moves in the format: x y")
            print("")
        board.print_board()
        print("")
        print("---")
        print("")
    turn = start
    while True:
        coords = find_move(players, turn, board, printing, C[turn-1])
        result = board.do_move((int(coords[0]),int(coords[1])))
        if printing:
            print("")
            board.print_board()
            print("")
            print("---")
            print("")
        if result == 1:
            if printing:
                announce_winner(players, turn, C)
            return turn
        turn = (turn % 2) +1
        if result == -1:
            if printing:
                announce_winner(players, turn, C)
            return turn
        #print(board.move_count)

def find_move(players, turn, board, printing, c):
    player = players[turn-1]
    if player == "human":
        move = input("Player " + str(turn) + ", please provide a move: ")
        coords = move.split()
    else:
        if printing:
            if player == "mcts":
                print(str(player) + "(" + str(turn) + " | c=" + str(c) + ")'s turn:")
            else:
                print(str(player) + "(" + str(turn) + ")'s turn:")
        if player == "minimax":
            coords = mm.MiniMax(board).main()
        elif player == "alphabeta":
            coords = ab.Alpha_Beta(board).alpha_beta()
        elif player == "mcts":
            coords = mcts.MCTS(board, c)
        elif player == "abiter":
            coords = ab.Alpha_Beta(board).iterative_deepening()
        else: # (randomplayer):
            actions = board.get_possible_actions()
            np.random.shuffle(actions)
            coords =  actions[0]
    return coords

def announce_winner(players, turn, C):
    player = players[turn-1]
    if player == "human":
        print("Player " + str(turn) + " wins!")
    else:
        if player == "mcts":
            print(str(player) + "(" + str(turn) + " | c=" + str(C[turn-1]) + ")'s turn")
        else:
            print(str(player) + "(" + str(turn) + ") wins!")

def compare_mcts_params(n_iterations, C, printing):
    wins = [0,0]
    for i in range(n_iterations):
        winner = game(Board, ["mcts","mcts"], printing=printing,C=C)
        wins[winner-1] += 1
        print("Game " + str(i+1) + " (of " + str(n_iterations) + ") is over.")
    print("c=" + str(C[0]) + " won " + str(wins[0]) + " | " + "c=" + str(C[1]) + " won " + str(wins[1]))
    winrate = (max(wins)/n_iterations) * 100
    print(str(winrate) + "%")

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

def test_full_board_ab(b):
    b.full = int("101100000111111000111111100111111110111111111011111111001111111000111111000011111", 2)
    b.move_count = 61
    instance = ab.Alpha_Beta(b)
    coords = instance.alpha_beta()
    print(coords)

def _create_testboard(b,coords_current,coords_full):
    for i in range(len(coords_current)):
        b.current |= (1<<yav.coords_to_bit(coords_current[i]))
    for i in range(len(coords_full)):
        b.full |= (1<<yav.coords_to_bit(coords_full[i]))
    b.full |= b.current
    b.move_count = len(coords_current) +  len(coords_full)
    b.print_board()
    return b

def testboard_0(b):
    coords_current = [(0,0), (0,3), (2,0),(3,0),(3,1)]
    coords_full = [(0,1), (1,0),(1,1),(3,2),(4,3)]
    return _create_testboard(b,coords_current,coords_full)

def testboard_1(b):
    coords_current = [(0,0), (1,0), (3,0),(4,0),(3,2),(4,3),(4,4),(4,6),(5,6),(6,5)]
    coords_full = [(2,0),(2,1),(3,3),(3,5),(2,5),(5,5),(5,4),(5,7),(6,3),(6,6)]
    return _create_testboard(b,coords_current,coords_full)

def testboard_2(b):
    coords_current = [(0,0),(3,3)]
    coords_full = [(2,2),(2,3)]
    return _create_testboard(b,coords_current,coords_full)

def testboard_3(b):
    coords_current = [(0,0),(1,1),(1,2),(3,3)]
    coords_full = [(0,2),(2,2),(3,2),(3,5)]
    return _create_testboard(b,coords_current,coords_full)

def testboard_4(b):
    coords_current = [(0,0),(0,1),(1,1),(3,1),(3,3),(3,4),(3,6),(5,5),(6,6)]
    coords_full = [(2,2),(2,3),(3,2),(3,5),(5,3),(5,4),(5,6),(7,5),(7,6),(8,6)]
    return _create_testboard(b,coords_current,coords_full)

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
    elif arg == "test_full_board":
        test_full_board_ab(Board)
    elif arg == "test_ab_borders":
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
    elif arg == "generation": # generation der bitbords für die borderüberprüfung
        coords = [(0,3),(1,4),(2,5),(3,6),(4,7),(6,7),(7,7),(8,7),(5,7)]
        for x in coords:
            bit = yav.coords_to_bit(x)
            Board.full |= (1 << bit)
        Board.print_board()
        print(Board.full)
    elif arg == "zusammen": # addieren der oben generierten bitboards
        n1 = 302822905891722765537284
        n2 = 605645811783445531074568
        Board.full = n1 + n2
        Board.print_board()
        print(Board.full)
    elif arg == "test_ab":
        Board = testboard_4(Board)

        correct_board = Board.simulate_move((2,1))[0]
        correct_board.print_board()

        coords = ab.Alpha_Beta(Board).alpha_beta()
        new_board = Board.simulate_move(coords)[0]
        new_board.print_board()
        coords = ab.Alpha_Beta(Board).iterative_deepening()
        Board.do_move(coords)
        Board.print_board()

        ab.evaluate(correct_board,debug=True)
        ab.evaluate(new_board,debug=True)
        ab.evaluate(Board,debug=True)
    elif arg == "compare_mcts_params":
        n_iterations = int(sys.argv[2])
        c1 = np.float64(sys.argv[3])
        c2 = np.float64(sys.argv[4])
        printing = sys.argv[5] == "True"

        compare_mcts_params(n_iterations, [c1,c2], printing)
    else:
        print("Name of test not found")