from game import Game
import pygame
import sys
from constants import BOARD_SIZE, SQUARE_SIZE, WINDOW_SIZE, WHITE_COLOR, BLACK_COLOR, NAVY_BLUE, LIGHT_GREY, DARK_GREY, HIGHLIGHT_COLOR, WHITE, BLACK
from pawn import Pawn
from rook import Rook
from bishop import Bishop
from knight import Knight
from queen import Queen
from king import King


def draw_board(screen, x, y, square_size):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE_COLOR if (row + col) % 2 == 0 else BLACK_COLOR
            pygame.draw.rect(
                screen,
                color,
                (x + col * square_size, y + row * square_size, square_size, square_size)
            )

def draw_highlight(screen, game, x, y, square_size):
    # Highlight selected piece's square with a semi-transparent yellow tint
    if game.selected_piece:
        row, col = game.selected_piece.row, game.selected_piece.col
        highlight_surf = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
        highlight_surf.fill((*HIGHLIGHT_COLOR, 100))
        screen.blit(highlight_surf, (x + col * square_size, y + row * square_size))

def draw_move_dots(screen, game, x, y, square_size):
    # Draw dark grey dots on squares that the selected piece can legally move to
    for move in game.legal_moves:
        r, c = move
        center = (x + c * square_size + square_size // 2, y + r * square_size + square_size // 2)
        radius = max(4, square_size // 12)
        pygame.draw.circle(screen, DARK_GREY, center, radius)

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

def draw_win_screen(screen, winner):
    font = pygame.font.SysFont(None, 64)
    small_font = pygame.font.SysFont(None, 36)

    text = font.render(f"{winner.capitalize()} Wins!", True, (255, 255, 255))
    restart = small_font.render("Click to Play Again", True, (200, 200, 200))

    screen.blit(text, (WINDOW_SIZE//2 - text.get_width()//2, 300))
    screen.blit(restart, (WINDOW_SIZE//2 - restart.get_width()//2, 380))

def draw_pieces(screen, board, images, x, y, square_size):
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

                # Scale image to current square size
                scaled_image = pygame.transform.smoothscale(image, (square_size, square_size))

                screen.blit(
                    scaled_image,
                    (x + col * square_size, y + row * square_size)
                )

def draw_move_list(screen, move_history, x, y, width, height):
    font = pygame.font.SysFont(None, 24)
    move_height = 30
    for i, move in enumerate(move_history):
        bg_color = LIGHT_GREY if i % 2 == 0 else DARK_GREY  # Alternate colors
        pygame.draw.rect(screen, bg_color, (x, y + i * move_height, width, move_height))
        text = font.render(move, True, (0, 0, 0))
        screen.blit(text, (x + 10, y + i * move_height + 5))

def draw_game_over(screen, winner):
    font = pygame.font.SysFont(None, 48)
    if winner:
        text = f"{winner.capitalize()} Wins!"
    else:
        text = "Stalemate!"
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (WINDOW_SIZE // 2 - text_surface.get_width() // 2, WINDOW_SIZE // 2 - text_surface.get_height() // 2))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE), pygame.RESIZABLE)
    pygame.display.set_caption("Python Chess")

    clock = pygame.time.Clock()
    game = Game()

    images = load_piece_images()

    current_width, current_height = WINDOW_SIZE, WINDOW_SIZE

    running = True
    while running:
        clock.tick(60)

        # Fill background with Navy Blue
        screen.fill(NAVY_BLUE)

        # Calculate board size
        if current_width > WINDOW_SIZE + 200:  # If wide enough, leave space for moves
            board_size = min(current_width - 200, current_height)
            board_x = (current_width - board_size - 200) // 2
            board_y = (current_height - board_size) // 2
            square_size = board_size // BOARD_SIZE
            show_moves = True
        else:
            board_size = min(current_width, current_height)
            board_x = (current_width - board_size) // 2
            board_y = (current_height - board_size) // 2
            square_size = board_size // BOARD_SIZE
            show_moves = False

        # Draw board
        draw_board(screen, board_x, board_y, square_size)

        # Highlight selected piece's square (under pieces)
        draw_highlight(screen, game, board_x, board_y, square_size)

        # Draw pieces
        draw_pieces(screen, game.board, images, board_x, board_y, square_size)

        # Draw legal move dots (on top of pieces for visibility)
        draw_move_dots(screen, game, board_x, board_y, square_size)

        # Draw move list if space
        if show_moves:
            draw_move_list(screen, game.move_history, current_width - 200, 0, 200, current_height)

        # Draw game over screen if needed
        if game.game_over:
            overlay = pygame.Surface((current_width, current_height))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            draw_game_over(screen, game.winner)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                current_width, current_height = event.w, event.h
                screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN and game.game_over:
                # Reset game on click when game over
                game.reset()
            elif event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                x, y = pygame.mouse.get_pos()
                # Adjust for board position
                if board_x <= x < board_x + board_size and board_y <= y < board_y + board_size:
                    row = (y - board_y) // square_size
                    col = (x - board_x) // square_size
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
        
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
