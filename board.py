from pawn import Pawn
from rook import Rook
from bishop import Bishop
from knight import Knight
from queen import Queen
from king import King
from constants import WHITE, BLACK

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_pieces()

    def setup_pieces(self):
        for col in range(8):
            self.grid[6][col] = Pawn(WHITE, 6, col)
            self.grid[1][col] = Pawn(BLACK, 1, col)
        self.grid[7][0] = Rook(WHITE, 7, 0)
        self.grid[7][7] = Rook(WHITE, 7, 7)
        self.grid[0][0] = Rook(BLACK, 0, 0)
        self.grid[0][7] = Rook(BLACK, 0, 7)
        self.grid[7][2] = Bishop(WHITE, 7, 2)
        self.grid[7][5] = Bishop(WHITE, 7, 5)
        self.grid[0][2] = Bishop(BLACK, 0, 2)
        self.grid[0][5] = Bishop(BLACK, 0, 5)
        self.grid[7][1] = Knight(WHITE, 7, 1)
        self.grid[7][6] = Knight(WHITE, 7, 6)
        self.grid[0][1] = Knight(BLACK, 0, 1)
        self.grid[0][6] = Knight(BLACK, 0, 6)
        self.grid[7][3] = Queen(WHITE, 7, 3)
        self.grid[0][3] = Queen(BLACK, 0, 3)
        self.grid[7][4] = King(WHITE, 7, 4)
        self.grid[0][4] = King(BLACK, 0, 4)


    def get_piece(self, row, col):
        if self.in_bounds(row, col):
            return self.grid[row][col]
        return None

    def is_empty(self, row, col):
        return self.get_piece(row, col) is None

    def in_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def move_piece(self, piece, row, col):
        self.grid[piece.row][piece.col] = None
        self.grid[row][col] = piece
        piece.move(row, col)
