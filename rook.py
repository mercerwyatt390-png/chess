from pieces import Piece
from constants import WHITE, BLACK  # if you have constants

class Rook(Piece):
    notation = "R"

    def get_legal_moves(self, board):
        moves = []

        # Directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            r, c = self.row, self.col
            while True:
                r += dr
                c += dc
                if not board.in_bounds(r, c):
                    break
                target = board.get_piece(r, c)
                if target is None:
                    moves.append((r, c))
                else:
                    if target.color != self.color:
                        moves.append((r, c))
                    break

        return moves