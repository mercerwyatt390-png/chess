from pieces import Piece
from constants import WHITE, BLACK  # if you have constants

class Pawn(Piece):

    def get_legal_moves(self, board):
        moves = []
        direction = -1 if self.color == WHITE else 1
        start_row = 6 if self.color == WHITE else 1

        next_row = self.row + direction

        # Move forward
        if board.is_empty(next_row, self.col):
            moves.append((next_row, self.col))

            # Two-square move
            if self.row == start_row and board.is_empty(next_row + direction, self.col):
                moves.append((next_row + direction, self.col))

        # Captures
        for dc in (-1, 1):
            r = self.row + direction
            c = self.col + dc
            if board.in_bounds(r, c):
                target = board.get_piece(r, c)
                if target and target.color != self.color:
                    moves.append((r, c))

        return moves
