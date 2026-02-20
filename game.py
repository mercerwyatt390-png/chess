from board import Board
from constants import WHITE, BLACK, PIECE_VALUES
from pawn import Pawn
from queen import Queen
from rook import Rook
from bishop import Bishop
from knight import Knight



class Game:
    def __init__(self):
        self.board = Board()
        self.turn = WHITE
        self.selected_piece = None
        self.legal_moves = []
        self.move_history = []
        self.game_over = False
        self.winner = None
        self.promotion_pending = None
        self.pending_promotion_notation = None
        self.white_captured = []  # List of captured pieces by white
        self.black_captured = []  # List of captured pieces by black
        self.promotion_bonuses = {WHITE: 0, BLACK: 0}  # Track total promotion bonuses for scoring


    def select_piece(self, row, col):
        if self.game_over:
            return
        piece = self.board.get_piece(row, col)
        if piece and piece.color == self.turn:
            self.selected_piece = piece
            all_moves = piece.get_legal_moves(self.board)
            
            # Filter castling moves
            if piece.notation == "K":
                enemy_color = BLACK if piece.color == WHITE else WHITE
                filtered_moves = []
                for move in all_moves:
                    if abs(move[1] - piece.col) == 2:  # Castling move
                        valid_castling = False
                        if not self.is_in_check(piece.color):
                            if move[1] == 6:  # Kingside
                                if not (self.is_square_attacked(piece.row, 5, enemy_color) or 
                                        self.is_square_attacked(piece.row, 6, enemy_color)):
                                    valid_castling = True
                            elif move[1] == 2:  # Queenside
                                if not (self.is_square_attacked(piece.row, 1, enemy_color) or 
                                        self.is_square_attacked(piece.row, 2, enemy_color) or 
                                        self.is_square_attacked(piece.row, 3, enemy_color)):
                                    valid_castling = True
                        if valid_castling:
                            filtered_moves.append(move)
                    else:
                        filtered_moves.append(move)
                all_moves = filtered_moves
            
            self.legal_moves = [move for move in all_moves if self.simulate_move(piece, move)]

    def move_selected(self, row, col):
        if not self.selected_piece or self.game_over:
            return

        if (row, col) not in self.legal_moves:
            return

        piece = self.selected_piece
        target = self.board.get_piece(row, col)

        # Handle castling
        is_castling = False
        if piece.notation == "K" and abs(col - piece.col) == 2:
            is_castling = True
            if col == 6:  # Kingside
                rook = self.board.get_piece(row, 7)
                self.board.move_piece(rook, row, 5)
            elif col == 2:  # Queenside
                rook = self.board.get_piece(row, 0)
                self.board.move_piece(rook, row, 3)

        notation = self.create_move_notation(piece, row, col, target, is_castling)
        if not self.board.move_piece(piece, row, col):
            return  # Invalid move (e.g., capturing king)

        # Track captured pieces
        if target:
            if piece.color == WHITE:
                self.white_captured.append(target.notation)
            else:
                self.black_captured.append(target.notation)

        # Handle pawn promotion: if pawn reaches last rank, pause for selection
        if isinstance(piece, Pawn) and ((piece.color == WHITE and piece.row == 0) or (piece.color == BLACK and piece.row == 7)):
            # Store pending promotion state; wait for UI selection
            self.promotion_pending = piece
            self.pending_promotion_notation = notation
            return

        # Normal move (not promotion)
        self.move_history.append(notation)

        enemy = BLACK if piece.color == WHITE else WHITE

        if self.is_checkmate(enemy):
            self.winner = piece.color
            self.game_over = True
        elif self.is_stalemate(enemy):
            self.game_over = True
            self.winner = None  # Draw

        self.end_turn()

    def promote_pawn(self, choice):
        """Promote the pending pawn to one of: 'queen','rook','bishop','knight'."""
        if not self.promotion_pending:
            return
        pawn = self.promotion_pending
        r, c = pawn.row, pawn.col

        class_map = {
            'queen': Queen,
            'rook': Rook,
            'bishop': Bishop,
            'knight': Knight
        }
        letter_map = {
            'queen': 'Q',
            'rook': 'R',
            'bishop': 'B',
            'knight': 'N'
        }

        cls = class_map.get(choice)
        if not cls:
            return

        # Replace pawn with new piece instance of same color at same square
        new_piece = cls(pawn.color, r, c)
        self.board.grid[r][c] = new_piece
        
        # Add promotion bonus to score (difference between promoted piece and pawn)
        promo_letter = letter_map.get(choice, 'Q')
        promotion_bonus = PIECE_VALUES.get(promo_letter, 0) - 1  # -1 because pawn was worth 1
        self.promotion_bonuses[new_piece.color] += promotion_bonus

        # Append promotion notation (e.g., e8=Q)
        self.move_history.append(f"{self.pending_promotion_notation}={promo_letter}")

        # Clear pending promotion state
        self.promotion_pending = None
        self.pending_promotion_notation = None

        # After promotion, check for game end and end turn
        enemy = BLACK if new_piece.color == WHITE else WHITE
        if self.is_checkmate(enemy):
            self.winner = new_piece.color
            self.game_over = True
        elif self.is_stalemate(enemy):
            self.game_over = True
            self.winner = None

        self.end_turn()
        
    def square_to_notation(self, row, col):
        file = chr(ord('a') + col)
        rank = str(8 - row)
        return file + rank

    def create_move_notation(self, piece, row, col, target, is_castling=False):
        if is_castling:
            if col == 6:
                return "O-O"
            elif col == 2:
                return "O-O-O"

        destination = self.square_to_notation(row, col)
        capture = target is not None

        # Pawn
        if piece.notation == "":
            if capture:
                start_file = chr(ord('a') + piece.col)
                notation = f"{start_file}x{destination}"
            else:
                notation = destination
        else:
            # Other pieces
            if capture:
                notation = f"{piece.notation}x{destination}"
            else:
                notation = f"{piece.notation}{destination}"

        # Check for check or checkmate
        enemy_color = BLACK if piece.color == WHITE else WHITE
        if self.is_checkmate(enemy_color):
            notation += "#"
        elif self.is_in_check(enemy_color):
            notation += "+"

        return notation


    def end_turn(self):
        self.selected_piece = None
        self.legal_moves = []
        self.turn = BLACK if self.turn == WHITE else WHITE

    def is_square_attacked(self, row, col, by_color):
        for r in range(8):
            for c in range(8):
                piece = self.board.get_piece(r, c)
                if piece and piece.color == by_color:
                    if (row, col) in piece.get_legal_moves(self.board):
                        return True
        return False
    
    def is_in_check(self, color):
        king = self.board.find_king(color)
        if not king:
            return False

        enemy_color = BLACK if color == WHITE else WHITE
        return self.is_square_attacked(king.row, king.col, enemy_color)
    
    def has_legal_move(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == color:
                    for move in piece.get_legal_moves(self.board):
                        if self.simulate_move(piece, move):
                            return True
        return False
    
    def simulate_move(self, piece, move):
        original_row, original_col = piece.row, piece.col
        target_piece = self.board.get_piece(*move)

        self.board.grid[original_row][original_col] = None
        self.board.grid[move[0]][move[1]] = piece
        piece.row, piece.col = move

        in_check = self.is_in_check(piece.color)

        # Undo move
        self.board.grid[original_row][original_col] = piece
        self.board.grid[move[0]][move[1]] = target_piece
        piece.row, piece.col = original_row, original_col

        return not in_check
    
    def is_checkmate(self, color):
        return self.is_in_check(color) and not self.has_legal_move(color)
    
    def is_stalemate(self, color):
        return not self.is_in_check(color) and not self.has_legal_move(color)
    
    def reset(self):
        self.board = Board()
        self.turn = WHITE
        self.selected_piece = None
        self.legal_moves = []
        self.move_history = []
        self.game_over = False
        self.winner = None
        self.white_captured = []
        self.black_captured = []
        self.promotion_bonuses = {WHITE: 0, BLACK: 0}
    
    def get_material_score(self):
        """Calculate net material advantage. Returns (leading_color, score_difference)."""
        white_score = sum(PIECE_VALUES.get(piece, 0) for piece in self.white_captured)
        black_score = sum(PIECE_VALUES.get(piece, 0) for piece in self.black_captured)
        
        # Add promotion bonuses
        white_score += self.promotion_bonuses[WHITE]
        black_score += self.promotion_bonuses[BLACK]
        
        if white_score > black_score:
            return (WHITE, white_score - black_score)
        elif black_score > white_score:
            return (BLACK, black_score - white_score)
        else:
            return (None, 0)  # Equal material

