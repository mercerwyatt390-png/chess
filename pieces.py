class Piece:
    notation = "" # To be defined in subclasses

    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.has_moved = False


    def get_legal_moves(self, board):
        return []

    def move(self, row, col):
        self.row = row
        self.col = col
        self.has_moved = True
