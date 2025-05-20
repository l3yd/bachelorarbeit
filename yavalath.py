import math

class Board:
    def __init__(self, current=0, full=0, move_count=0):
        self.current = current
        self.full = full
        self.move_count = move_count
        self.is_over = False
        self.illegalMoves = [5,6,7,8,
                            15,16,17,
                            25,26,
                            35,
                            45,
                            54,55,
                            63,64,65,
                            72,73,74,75]

    def reset_board(self):
        self.current = 0
        self.full = 0
        self.move_count = 0

    def copy(self) -> 'Board':
        """
        Gibt eine Kopie des Boards zurück.
        """
        return Board(self.current, self.full, self.move_count)

    def is_end(self, check_opponent=False) -> int:
        """
        Funktion gibt zurück, ob das Spiel zu Ende ist:
            1 falls der letzte Zug gewonnen hat
            -1 falls er verloren hat
            0.5 falls das Spiel in einem Unentschieden endet
            0 falls das Spiel noch nicht zu Ende ist
        """
        
        board = self.current if check_opponent else self.full ^ self.current

        # vertical (1-er Schritte)
        ver = board & (board >> 1) & (board >> 2)
        # diagonal bottom -> top (9-er Schritte)
        diag_bottom_top = board & (board >> 9) & (board >> 18)
        # diagonal top -> bottom (10-er Schritte)
        diag_top_bottom = board & (board >> 10) & (board >> 20)
        
        """ WINS """
        if ver & (board >> 3) != 0 or diag_bottom_top & (board >> 27) != 0 or diag_top_bottom & (board >> 30) != 0:
            return 1

        """ LOSES """
        if ver != 0 or diag_bottom_top != 0 or diag_top_bottom != 0:
            return -1
        
        """ DRAW """
        #if self.full == 0b111110000111111000111111100111111110111111111011111111001111111000111111000011111:
        if self.move_count == 61:
            return 0.5
        
        return 0
    
    def is_end_opponent(self) -> int:
        result = self.is_end()
        if result == 0:
            result = self.is_end(check_opponent=True)
            if result != 0.5:
                result = -result
        return result

    def do_move(self, coords: tuple[int,int]) -> int:
        """
        Führt den Zug aus, und gibt das Ergebnis zurück.
        """

        bit = coords_to_bit(coords)
        self.current ^= self.full
        self.full |= (1<<bit)
        self.move_count += 1
        result = self.is_end()
        if result != 0:
            self.is_over = True
        return result
    
    def simulate_move(self, coords: tuple[int,int]) -> tuple['Board', int]:
        """
        Gibt eine Kopie des Boards, auf dem der gegebene Zug ausgeführt wurde und das Ergebnis des Spiels, zurück.
        """
        new_board = self.copy()
        result = new_board.do_move(coords)
        return new_board, result

    """
    def undo_move(coords):
        bit = coords_to_bit(coords)
        return board & ~(1 << bit)
    """

    def get_possible_actions(self) -> list[tuple[int,int]]:
        """
        Gibt eine Liste aller mögliche Züge zurück.
        """

        """moves = []
        for i in range(81):
            if i in self.illegalMoves:
                continue
            if (self.full >> i) & 1 == 0:
                moves.append(bit_to_coords(i))"""
        moves = [bit_to_coords(i) for i in range(81) if (self.full >> i) & 1 == 0 and i not in self.illegalMoves]
        return moves

    def print_board(self):
        """
        Gibt das Board in der Konsole aus.
        """

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
                next_turn = "⧆ "
                current_turn = "⧇ "
                if self.move_count % 2 == 0:
                    next_turn = "⧇ "
                    current_turn = "⧆ "
                if (self.full >> bit) & 1 == 1:
                    if (self.current >> bit) & 1 == 1:
                        print(next_turn, end="")
                    else:
                        print(current_turn, end="")
                else:
                    print("◻ ", end="")
            if 5 + row < 9:
                print(str(5+row), end="")
            print("")


def coords_to_bit(coords: tuple[int, int]) -> int:
    """
    Berechnet die Bit-Position der gegebenen Koordinaten.
    """
    row, col = coords
    return row*9 + col

def bit_to_coords(bit: int) -> tuple[int, int]:
    """
    Berechnet die Koordinaten der gegebenen Bit-Position.
    """
    return (math.floor(bit / 9), bit % 9)



difference = [0,4,7,9,10,11,13,16,20]

def position_to_bit(pos: int) -> int:
    thresholds = [(0,4),(5,10),(11,17),(18,25),(26,34),(35,42),(43,49),(50,55),(56,60)]
    for i in range(len(thresholds)):
        if pos >= thresholds[i][0] and pos <= thresholds[i][1]:
            return pos + difference[i]

def bit_to_position(bit: int) -> int:
    thresholds = [(0,5),(9,15),(18,25),(27,35),(36,45),(46,54),(56,63),(66,72),(76,81)]
    for i in range(len(thresholds)):
        if bit < thresholds[i][1] and bit >= thresholds[i][0]:
            return bit - difference[i]