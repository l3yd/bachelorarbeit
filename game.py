import sys
import numpy as np
import yavalath as yav
import mcts
import alphabeta as ab
import minimax as mm

"""
Mit diesem Skript können Spiele manuel gestartet werden. Zum testen gedacht.
"""

def game(board:yav.Board, players, start = np.random.randint(1,3), printing = True, C = [np.sqrt(2), np.sqrt(2)], wait_to_continue=False):
    if printing:
        if players[0] == "human" or players[1] == "human":
            print("Provide moves in the format: x y")
            print("")
        board.print_board()
        print("")
        print("---")
        print("")
    turn = start
    continue_with_ab = [False, False]
    while True:
        if wait_to_continue:
            input("Press Enter to continue...")
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
        if result == 0.5:
            if printing:
                print("Draw!")
            return -1

def find_move(players, turn, board, printing, c, continue_with_ab):
    player = players[turn-1]
    if continue_with_ab[turn-1]:
        player = "ab_iter"

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
            coords = mcts.MCTS(board, c, use_gdk=True)[0]
        elif player == "ab_iter":
            coords, sudden_end = ab.Alpha_Beta(board).iterative_deepening(max_time=15)
        elif player == "mcts_ab":
            returned_values = mcts.MCTS_alphabeta(board, c, use_gdk=True, max_time=15)
            coords = returned_values[0]
            sudden_win_found = returned_values[3]
            if sudden_win_found:
                continue_with_ab[turn-1] = True
        elif player == "mcts_pns":
            coords = mcts.MCTS_PNS(board, c, use_gdk=True)[0]
        else: # (randomplayer):
            actions = board.get_possible_actions()
            np.random.shuffle(actions)
            coords = actions[0]
    return coords, continue_with_ab

def announce_winner(players, turn, C):
    player = players[turn-1]
    if player == "human":
        print("Player " + str(turn) + " wins!")
    else:
        if player == "mcts" or player == "mcts_ab" or player == "mcts_pns":
            print(str(player) + "(" + str(turn) + " | c=" + str(C[turn-1]) + ")'s wins!")
        else:
            print(str(player) + "(" + str(turn) + ") wins!")




def n_games(Board: yav.Board, n_iterations, players, start = None, printing=False, C = [np.sqrt(2), np.sqrt(2)]):
    wins = [0,0]
    draws = 0
    for i in range(n_iterations):
        if start == None:
            winner = game(Board.copy(), players, printing=printing, C=C)
        else:
            winner = game(Board.copy(), players,start=start, printing=False, C=C)
        if winner == -1:
            draws += 1
        wins[winner-1] += 1
        print("Game " + str(i+1) + " (of " + str(n_iterations) + ") is over. " + str(players[0]) + " won " + str(wins[0]) + " | " + str(players[1]) + " won " + str(wins[1]) + " | draws: " + str(draws))
    print(str(players[0]) + " won " + str(wins[0]) + " | " + str(players[1]) + " won " + str(wins[1]) + " | draws: " + str(draws))
    winrate = (max(wins)/n_iterations) * 100
    print(str(winrate) + "%")

def print_help():
    print("")
    print("Invalid arguments!")
    print("")
    print("To play a game, execute the script with the following arguments:")
    print("python3 game.py <player1> <player2> [<starting_player>]")
    print("")
    print("To let the computer play a number of games against itself, execute the script with the following arguments:")
    print("python3 game.py <n_iterations> <player1> <player2> [<starting_player>]")
    print("")
    print("Available players:")
    print(legal_players)
    print("")

legal_players = ["human", "minimax", "mm", "alphabeta", "ab", "ab_iter", "mcts","mcts_ab", "mcts_pns", "random"]

if __name__ == '__main__':
    Board = yav.Board()
    arg = sys.argv[1]

    C = [np.sqrt(2),np.sqrt(2)]
    if arg in legal_players:
        # 'n_iterations' 'player' 'player' [staring_player]
        player1 = arg
        try:
            player2 = sys.argv[2]
        except:
            print_help()
            raise ValueError("Not enough players provided!")
        assert player1 in legal_players and player2 in legal_players
        players = [player1, player2]
        for i in range(len(players)):
            if players[i] == "mm":
                players[i] = "minimax"
            if players[i] == "ab":
                players[i] = "alphabeta"
        try:
            start = int(sys.argv[3])
        except:
            start = None
        
        if start == None:
            game(Board, players, C=C)
        else:
            game(Board, players, start=start, C=C)
    
    elif arg.isdigit():
        # 'n_iterations' 'player' 'player' [staring_player]
        try:
            player1 = sys.argv[2]
            player2 = sys.argv[3]
        except:
            print_help()
            raise ValueError("Not enough players provided!")
        assert player1 in legal_players and player2 in legal_players
        assert player1 != "human" and player2 != "human"
        players = [player1, player2]
        n_iterations = int(sys.argv[1])

        try:
            start = int(sys.argv[3])
        except:
            start = None

        n_games(Board, n_iterations, players, start=start, printing=False)
    elif arg == "control":
        # 'n_iterations' 'player' 'player' [staring_player]
        try:
            player1 = sys.argv[2]
            player2 = sys.argv[3]
        except:
            print_help()
            raise ValueError("Not enough players provided!")
        assert player1 in legal_players and player2 in legal_players
        players = [player1, player2]
        for i in range(len(players)):
            if players[i] == "mm":
                players[i] = "minimax"
            if players[i] == "ab":
                players[i] = "alphabeta"
        try:
            start = int(sys.argv[4])
        except:
            start = None
        
        if start == None:
            game(Board, players, C=C, wait_to_continue=True)
        else:
            game(Board, players, start=start, C=C, wait_to_continue=True)
    else:
        print_help()
        