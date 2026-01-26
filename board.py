from constants import BOARD_SIZE, WHITE, BLACK
from pawn import Pawn

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.setup_pieces()

    def setup_pieces(self):
        # Pawns
        for col in range(BOARD_SIZE):
            self.grid[6][col] = Pawn(WHITE, 6, col)
            self.grid[1][col] = Pawn(BLACK, 1, col)

        # You’ll add rooks, knights, etc. later

    def get_piece(self, row, col):
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return self.grid[row][col]
        return None

    def is_empty(self, row, col):
        return self.get_piece(row, col) is None

    def move_piece(self, piece, row, col):
        self.grid[piece.row][piece.col] = None
        self.grid[row][col] = piece
        piece.move(row, col)
