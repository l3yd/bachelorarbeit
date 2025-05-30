import yavalath as yav
import sys
import numpy as np
import minimax as mm
import alphabeta as ab
import mcts
import matplotlib.pyplot as plt
import csv
import time

"""
Dieses Skript wurde für das Testsen während der Implementierung der Algorithmen genutzt.
Die Tests sind nicht vollständig und werden nicht mehr genutzt.
"""

def game(board:yav.Board, players = ["human", "human"], start = np.random.randint(1,3), printing = True, C = [np.sqrt(2), 0.7]):
    board.reset_board()
    if printing:
        if players[0] == "human" or players[1] == "human":
            print("Provide moves in the format: x y")
            print("")
            print(C)
        board.print_board()
        print("")
        print("---")
        print("")
    turn = start
    continue_with_ab = [False, False]
    while True:
        coords, continue_with_ab = find_move(players, turn, board, printing, C[turn-1], continue_with_ab)
        try:
            result = board.do_move((int(coords[0]),int(coords[1])))
        except:
            raise ValueError("Illegal move!")
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

def find_move(players, turn, board, printing, c, continue_with_ab):
    player = players[turn-1]
    if continue_with_ab[turn-1]:
        player = "abiter"

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
            coords, sudden_end = ab.Alpha_Beta(board).alpha_beta()
        elif player == "mcts":
            coords = mcts.MCTS(board, c, use_gdk=True)
        elif player == "abiter":
            coords, sudden_end = ab.Alpha_Beta(board).iterative_deepening()
        elif player == "mcts_ab":
            coords, sudden_win_found = mcts.MCTS_alphabeta(board, c, use_gdk=True)
            if sudden_win_found:
                continue_with_ab[turn-1] = True
                print("sudden win found!!!!!")
        elif player == "mcts_pns":
            coords = mcts.MCTS_PNS(board, c, use_gdk=True)
        else: # (randomplayer):
            actions = board.get_possible_actions()
            np.random.shuffle(actions)
            coords =  actions[0]
    return coords, continue_with_ab

def announce_winner(players, turn, C):
    player = players[turn-1]
    if player == "human":
        print("Player " + str(turn) + " wins!")
    else:
        if player == "mcts":
            print(str(player) + "(" + str(turn) + " | c=" + str(C[turn-1]) + ")'s wins!")
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

def testboard_5(b) -> yav.Board:
    coords_current = [(0,1),(0,4)]
    coords_full = [(0,3),(2,3),(5,3)]
    return _create_testboard(b,coords_current,coords_full)

def testboard_6(b) -> yav.Board:
    coords_current = [(1,3),(2,1),(2,3),(2,4),(2,6),(4,3),(4,6),(5,4),(7,6)]
    coords_full = [(2,2),(2,5),(3,2),(3,3),(5,3),(5,5),(5,6),(6,5),(8,6)]
    return _create_testboard(b,coords_current,coords_full)

def testboard_7(b) -> yav.Board:
    coords_current = [(2,3),(2,4),(2,6),(4,5),(5,6),(7,8)]
    coords_full = [(0,4),(2,5),(3,4),(3,7),(5,3),(6,7)]
    return _create_testboard(b,coords_current,coords_full)

def testboard_8(b) -> yav.Board:
    coords_current = [(2,1),(2,3),(2,4),(2,6),(3,6),(4,2),(4,5),(5,2),(5,6),(5,7),(6,5),(6,6),(7,8)]
    coords_full = [(0,4),(2,2),(2,5),(3,4),(3,7),(4,3),(4,6),(5,1),(5,3),(5,4),(6,7),(7,3),(7,6)]
    return _create_testboard(b,coords_current,coords_full)

legal_players = ["human", "minimax", "mm", "alphabeta", "ab", "mcts", "random","abiter","mcts_ab", "mcts_pns", "mcts_gdk"]

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
        C = [1/np.sqrt(2),np.sqrt(2)]
        if arg == "game":
            try:
                game(Board, players, int(sys.argv[4]), C=C)
            except:
                game(Board, players, C=C)
        else: # arg == "n_game"
            n_iterations = int(sys.argv[4])
            wins = [0,0]
            for i in range(n_iterations):
                winner = game(Board, players, printing=True)
                wins[winner-1] += 1
                print("Game " + str(i+1) + " (of " + str(n_iterations) + ") is over." + str(players[0]) + " won " + str(wins[0]) + " | " + str(players[1]) + " won " + str(wins[1]))
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
    elif arg == "oneposition":
        Board = testboard_5(Board)
        coords = mcts.MCTS_alphabeta(Board)
        result = Board.do_move(coords)
        print("")
        Board.print_board()
        
        result = 0
        player = 0
        while result == 0:
            if player == 0:
                coords = mcts.MCTS_PNS(Board)
            else:
                coords = input("Please provide a move: ")
            result = Board.do_move(coords)
            print("")
            Board.print_board()
            player = (player+1)%2
    elif arg == "firstmoveMCTS":
        nochmal = "yes"
        while nochmal == "yes":
            print("MCTS")
            mcts.MCTS(Board)
            input("MCTS_ab? ")
            Board.reset_board()
            mcts.MCTS_alphabeta(Board)
            input("MCTS_pns? ")
            Board.reset_board()
            mcts.MCTS_PNS(Board)
            nochmal = input("Nochmal? ")
        print("")
    elif arg == "oneposition_ab":
        Board = testboard_6(Board)
        coords, sudden_end = ab.Alpha_Beta(Board).alpha_beta()
        Board.do_move(coords)
        Board.print_board()
    elif arg == "start":
        #ab.Alpha_Beta(Board).iterative_deepening()
        mcts.MCTS_alphabeta(Board)
    elif arg == "mcts_cs":
        try:
            usegdk = sys.argv[2]
        except:
            raise ValueError("No filename provided")
        coords = mcts.MCTS_alphabeta(Board, c=np.sqrt(2), use_gdk=False)
    elif arg == "plot_mcts":
        try:
            filename = sys.argv[2]
            print(filename)
        except:
            raise ValueError("No filename provided")
        
        with open(filename, 'r', newline='', encoding='utf-16') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            line_count = 0
            
            at_border = [0, 1, 2, 3, 4, 5, 10, 11, 17, 18, 25, 26, 34, 35, 42, 43, 49, 50, 55, 56, 57, 58, 59, 60, 61]
            one_step = [6, 7, 8, 9, 12, 16, 19, 24, 27, 33, 36, 41, 44, 48, 51, 52, 53, 54]
            two_steps = [13, 14, 15, 20, 23, 28, 32, 37, 40, 45, 46, 47]
            middle = [21, 22, 29, 31, 38, 39, 30]

            x = []
            y_uct = []
            y_exploration = []
            y_exploitation = []

            fig1, ax1 = plt.subplots()
            line11, = ax1.plot([], [], label='at_border', color='blue')
            line12, = ax1.plot([], [], label='one_step', color='red')
            line13, = ax1.plot([], [], label='two_steps', color='green')
            line14, = ax1.plot([], [], label='middle', color='purple')
            ax1.legend()
            fig2, ax2 = plt.subplots()
            line21, = ax2.plot([], [], label='at_border', color='blue')
            line22, = ax2.plot([], [], label='one_step', color='red')
            line23, = ax2.plot([], [], label='two_steps', color='green')
            line24, = ax2.plot([], [], label='middle', color='purple')
            ax2.legend()
            fig3, ax3 = plt.subplots()
            line31, = ax3.plot([], [], label='at_border', color='blue')
            line32, = ax3.plot([], [], label='one_step', color='red')
            line33, = ax3.plot([], [], label='two_steps', color='green')
            line34, = ax3.plot([], [], label='middle', color='purple')
            ax3.legend()
            plt.ion()
            plt.show()

            uct = [0,0,0,0]
            exploration = [0,0,0,0]
            exploitation = [0,0,0,0]

            for row in reader:
                curr = line_count % 61
                if curr in at_border:
                    index = 0
                elif curr in one_step:
                    index = 1
                elif curr in two_steps:
                    index = 2
                elif curr in middle:
                    index = 3
                else: # curr in middle / should happen da auskomentiert
                    print(f"whoops {curr}")
                    index = 4
                
                uct[index] += float(row[1])
                exploitation[index] += float(row[2])
                exploration[index] += float(row[3])

                line_count += 1
                if line_count % 61 == 0:
                    x.append(float(row[0]))

                    uct[0] /= len(at_border)
                    uct[1] /= len(one_step)
                    uct[2] /= len(two_steps)
                    uct[3] /= len(middle)

                    y_uct.append(uct)

                    exploitation[0] /= len(at_border)
                    exploitation[1] /= len(one_step)
                    exploitation[2] /= len(two_steps)
                    exploitation[3] /= len(middle)

                    y_exploitation.append(exploitation)

                    exploration[0] /= len(at_border)
                    exploration[1] /= len(one_step)
                    exploration[2] /= len(two_steps)
                    exploration[3] /= len(middle)
                    for i in range(4):
                        if exploration[i] < 0:
                            print(exploration[i])

                    y_exploration.append(exploration)

                    line11.set_data(x, [value[0] for value in y_uct])
                    line12.set_data(x, [value[1] for value in y_uct])
                    line13.set_data(x, [value[2] for value in y_uct])
                    line14.set_data(x, [value[3] for value in y_uct])

                    line21.set_data(x, [value[0] for value in y_exploitation])
                    line22.set_data(x, [value[1] for value in y_exploitation])
                    line23.set_data(x, [value[2] for value in y_exploitation])
                    line24.set_data(x, [value[3] for value in y_exploitation])

                    line31.set_data(x, [value[0] for value in y_exploration])
                    line32.set_data(x, [value[1] for value in y_exploration])
                    line33.set_data(x, [value[2] for value in y_exploration])
                    line34.set_data(x, [value[3] for value in y_exploration])

                    """ax1.relim()
                    ax1.autoscale_view()
                    ax2.relim()
                    ax2.autoscale_view()
                    ax3.relim()
                    ax3.autoscale_view()
                    plt.draw()"""

                    uct = [0,0,0,0,0]
                    exploration = [0,0,0,0,0]
                    exploitation = [0,0,0,0,0]
            ax1.relim()
            ax1.autoscale_view()
            ax2.relim()
            ax2.autoscale_view()
            ax3.relim()
            ax3.autoscale_view()
            plt.draw()
            plt.show(block=True) 
    elif arg == "test_tt":
        for i in range(3,7):
            Board.reset_board()
            start_time = time.time()
            coords, _ = ab.Alpha_Beta(Board, search_depth=i, use_tt=False).alpha_beta()
            time_used = time.time() - start_time
            print(f'Alpha Beta took {time_used} seconds for search depth {i}.')
            Board.do_move(coords)
            Board.print_board()
        for i in range(3,7):
            Board.reset_board()
            start_time = time.time()
            # detect_sudden_end=True beendet den Algorithmus, wenn search_depth berechnet wurde
            coords, _ = ab.Alpha_Beta(Board, search_depth=i, use_tt=False).iterative_deepening(max_time=60, detect_sudden_end_k=i)
            time_used = time.time() - start_time
            print(f'Iterative Deepening took {time_used} seconds for search depth {i}.')
            Board.do_move(coords)
            Board.print_board()
    elif arg == "detect_sudden_end":
        #first_player = [(2,3),(5,3),(2,0),(5,6),(3,3),(2,2),(4,2),(0,0)]
        #second_player = [(3,4),(4,5),(6,7),(5,5),(4,3),(2,1),(3,1),(2,5)]
        first_player = [(2,3),(5,3),(2,0),(5,6),(3,3),(2,2),(0,3),(4,2)]#,(0,0)]
        second_player = [(3,4),(4,5),(6,7),(5,5),(4,3),(2,1),(1,3),(3,1)]
        Board.setup(first_player, second_player)
        Board.print_board()
        ab_object = ab.Alpha_Beta(Board, 4, use_tt=True)
        move, sudden_end = ab_object.iterative_deepening(max_time=1,detect_sudden_end_k=4)
        
        print(f'{move} | {sudden_end}')
        print(ab_object.death_moves)
        #move , _, _, sudden_end = mcts.MCTS_alphabeta(Board,0.7,4,max_time=10)
        print(f'{move} | {sudden_end}')
        
    else:
        print("Name of test not found")