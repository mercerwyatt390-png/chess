from board import Board
from constants import WHITE, BLACK



class Game:
    def __init__(self):
        self.board = Board()
        self.turn = WHITE
        self.selected_piece = None
        self.legal_moves = []

    def select_piece(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece and piece.color == self.turn:
            self.selected_piece = piece
            self.legal_moves = piece.get_legal_moves(self.board)

    def move_selected(self, row, col):
        if self.selected_piece and (row, col) in self.legal_moves:
            self.board.move_piece(self.selected_piece, row, col)
            self.end_turn()

    def end_turn(self):
        self.selected_piece = None
        self.legal_moves = []
        self.turn = BLACK if self.turn == WHITE else WHITE
