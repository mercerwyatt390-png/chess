from game import Game
import pygame
import sys
from constants import BOARD_SIZE, SQUARE_SIZE, WINDOW_SIZE, WHITE_COLOR, BLACK_COLOR, WHITE, BLACK
from pawn import Pawn
from rook import Rook
from bishop import Bishop
from knight import Knight
from queen import Queen
from king import King


def draw_board(screen):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE_COLOR if (row + col) % 2 == 0 else BLACK_COLOR
            pygame.draw.rect(
                screen,
                color,
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )

def load_piece_images():
    images = {}

    images["pawn_white"] = pygame.image.load(
        "assets/pieces/Pawn_White_PNG.png"
    ).convert_alpha()

    images["pawn_black"] = pygame.image.load(
        "assets/pieces/Pawn_Black_PNG.png"
    ).convert_alpha()

    images["rook_white"] = pygame.image.load(
        "assets/pieces/Rook_White_PNG.png"
    ).convert_alpha()

    images["rook_black"] = pygame.image.load(
        "assets/pieces/Rook_Black_PNG.png"
    ).convert_alpha()

    images["bishop_white"] = pygame.image.load(
        "assets/pieces/Bishop_White_PNG.png"
    ).convert_alpha()

    images["bishop_black"] = pygame.image.load(
        "assets/pieces/Bishop_Black_PNG.png"
    ).convert_alpha()

    images["knight_white"] = pygame.image.load(
        "assets/pieces/Knight_White_PNG.png"
    ).convert_alpha()

    images["knight_black"] = pygame.image.load(
        "assets/pieces/Knight_Black_PNG.png"
    ).convert_alpha()

    images["queen_white"] = pygame.image.load(
        "assets/pieces/Queen_White_PNG.png"
    ).convert_alpha()

    images["queen_black"] = pygame.image.load(
        "assets/pieces/Queen_Black_PNG.png"
    ).convert_alpha()

    images["king_white"] = pygame.image.load(
        "assets/pieces/King_White_PNG.png"
    ).convert_alpha()

    images["king_black"] = pygame.image.load(
        "assets/pieces/King_Black_PNG.png"
    ).convert_alpha()

    # Scale to square size
    for key in images:
        images[key] = pygame.transform.smoothscale(
            images[key], (SQUARE_SIZE, SQUARE_SIZE)
        )

    return images

def draw_pieces(screen, board, images):
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece:
                if isinstance(piece, Pawn):
                    piece_type = "pawn"
                elif isinstance(piece, Rook):
                    piece_type = "rook"
                elif isinstance(piece, Bishop):
                    piece_type = "bishop"
                elif isinstance(piece, Knight):
                    piece_type = "knight"
                elif isinstance(piece, Queen):
                    piece_type = "queen"
                elif isinstance(piece, King):
                    piece_type = "king"
                else:
                    piece_type = "pawn"  # default

                color_suffix = "_white" if piece.color == WHITE else "_black"
                image_key = piece_type + color_suffix
                image = images.get(image_key, images["pawn_white"])  # fallback

                screen.blit(
                    image,
                    (col * SQUARE_SIZE, row * SQUARE_SIZE)
                )

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Python Chess")

    clock = pygame.time.Clock()
    game = Game()

    images = load_piece_images()

    running = True
    while running:
        clock.tick(60)
        draw_board(screen)
        draw_pieces(screen, game.board, images)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE
                piece = game.board.get_piece(row, col)

                if game.selected_piece:
                    if game.selected_piece.row == row and game.selected_piece.col == col:
                        # Deselect the piece
                        game.selected_piece = None
                        game.legal_moves = []
                    elif piece and piece.color == game.turn:
                        # Select another piece of the same color
                        game.select_piece(row, col)
                    else:
                        # Try to move to the clicked square
                        game.move_selected(row, col)
                else:
                    game.select_piece(row, col)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
