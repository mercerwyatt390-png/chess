from constants import WHITE
from pieces import Piece


class Pawn(Piece):
    def get_legal_moves(self, board):
        moves = []
        direction = -1 if self.color == WHITE else 1
        start_row = 6 if self.color == WHITE else 1

        # One square forward
        if board.is_empty(self.row + direction, self.col):
            moves.append((self.row + direction, self.col))

            # Two squares from start
            if self.row == start_row and board.is_empty(self.row + 2 * direction, self.col):
                moves.append((self.row + 2 * direction, self.col))

        return moves
