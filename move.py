

class Move:
    def __init__(self, end_pos, piece_moved, piece_captured=None):
        self.end_pos = end_pos
        self.piece_moved = piece_moved
        self.piece_captured = piece_captured

