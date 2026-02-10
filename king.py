from pieces import Piece
from constants import WHITE, BLACK  # if you have constants

class King(Piece):
    notation = "K"

    def get_legal_moves(self, board):
        moves = []

        # All possible king moves (one square in any direction)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            if board.in_bounds(r, c):
                target = board.get_piece(r, c)
                if target is None or target.color != self.color:
                    moves.append((r, c))

        # Castling
        if not self.has_moved:
            # Kingside castling
            rook = board.get_piece(self.row, 7)
            if (rook and rook.notation == "R" and not rook.has_moved and
                board.is_empty(self.row, 5) and board.is_empty(self.row, 6)):
                moves.append((self.row, 6))  # King to g-file

            # Queenside castling
            rook = board.get_piece(self.row, 0)
            if (rook and rook.notation == "R" and not rook.has_moved and
                board.is_empty(self.row, 1) and board.is_empty(self.row, 2) and board.is_empty(self.row, 3)):
                moves.append((self.row, 2))  # King to c-file

        return moves