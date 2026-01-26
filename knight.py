from pieces import Piece
from constants import WHITE, BLACK  # if you have constants

class Knight(Piece):
    notation = "N"
    
    def get_legal_moves(self, board):
        moves = []
        knight_moves = [
            (-2, -1), (-2, 1), (2, -1), (2, 1),
            (-1, -2), (-1, 2), (1, -2), (1, 2)
        ]

        for dr, dc in knight_moves:
            r, c = self.row + dr, self.col + dc
            if board.in_bounds(r, c):
                target = board.get_piece(r, c)
                if target is None or target.color != self.color:
                    moves.append((r, c))

        return moves