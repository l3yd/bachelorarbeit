import sys
import numpy as np
import yavalath as yav
import mcts
import alphabeta as ab
import minimax as mm

def game(board:yav.Board, players, start = np.random.randint(1,3), printing = True, C = [np.sqrt(2), np.sqrt(2)]):
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
            coords = mcts.MCTS(board, c, use_gdk=True)
        elif player == "ab_iter":
            coords, sudden_end = ab.Alpha_Beta(board).iterative_deepening()
        elif player == "mcts_ab":
            coords, sudden_win_found = mcts.MCTS_alphabeta(board, c, use_gdk=True)
            if sudden_win_found:
                continue_with_ab[turn-1] = True
        elif player == "mcts_pns":
            coords = mcts.MCTS_PNS(board, c, use_gdk=True)
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
        if player == "mcts":
            print(str(player) + "(" + str(turn) + " | c=" + str(C[turn-1]) + ")'s wins!")
        else:
            print(str(player) + "(" + str(turn) + ") wins!")




def _n_games(Board: yav.Board, n_iterations, players, start = None, printing=False):
    wins = [0,0]
    for i in range(n_iterations):
        if start == None:
            winner = game(Board.copy(), players, printing=printing, C=C)
        else:
            winner = game(Board.copy(), players,start=start, printing=False, C=C)
        wins[winner-1] += 1
        print("Game " + str(i+1) + " (of " + str(n_iterations) + ") is over. " + str(players[0]) + " won " + str(wins[0]) + " | " + str(players[1]) + " won " + str(wins[1]))
    print(str(players[0]) + " won " + str(wins[0]) + " | " + str(players[1]) + " won " + str(wins[1]))
    winrate = (max(wins)/n_iterations) * 100
    print(str(winrate) + "%")


legal_players = ["human", "minimax", "mm", "alphabeta", "ab", "ab_iter", "mcts","mcts_ab", "mcts_pns", "random"]

if __name__ == '__main__':
    Board = yav.Board()
    arg = sys.argv[1]

    C = [1/np.sqrt(2),np.sqrt(2)]

    if arg in legal_players:
        # 'n_iterations' 'player' 'player' [staring_player]
        player1 = arg
        player2 = sys.argv[2]
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
        player1 = sys.argv[2]
        player2 = sys.argv[3]
        assert player1 in legal_players and player2 in legal_players
        assert player1 != "human" and player2 != "human"
        players = [player1, player2]
        n_iterations = int(sys.argv[1])

        try:
            start = int(sys.argv[3])
        except:
            start = None

        _n_games(Board, n_iterations, players, start=start, printing=False)
    else:
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