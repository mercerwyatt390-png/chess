class Piece:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.has_moved = False

    def get_legal_moves(self, board):
        """
        Override in subclasses (Pawn, Rook, etc.)
        Returns list of (row, col)
        """
        return []

    def move(self, row, col):
        self.row = row
        self.col = col
        self.has_moved = True
