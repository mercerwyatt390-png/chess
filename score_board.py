import pygame
from constants import WHITE, BLACK, WINDOW_SIZE


def draw_captured_pieces(screen, game, images, board_x, board_size, current_width, current_height, square_size):
    """Draw captured pieces on bottom left with black on bottom and white above, stacked by type."""
    
    # If board is taking up most of the space, don't show captures
    if current_width <= WINDOW_SIZE + 100:
        return
    
    # Get the leading color and score difference
    leading_color, score_diff = game.get_material_score()
    
    piece_order = ["", "N", "B", "R", "Q"]
    piece_names = {
        "": "pawn",
        "N": "knight",
        "B": "bishop",
        "R": "rook",
        "Q": "queen"
    }
    
    stack_offset = 8  # Offset between stacked pieces of the same type
    piece_size = 40
    
    # Draw black captured pieces at bottom (pieces captured by white = black pieces)
    x_start = 10
    y_black = current_height - 60  # Bottom left
    x_position = x_start
    
    # Count and group black pieces by type
    black_count = {notation: 0 for notation in piece_order}
    for piece in game.white_captured:
        black_count[piece] += 1
    
    # Draw black pieces grouped by type
    for notation in piece_order:
        count = black_count[notation]
        if count > 0:
            piece_name = piece_names.get(notation, "pawn")
            image_key = piece_name + "_black"
            
            if image_key in images:
                img = images[image_key]
                scaled_img = pygame.transform.smoothscale(img, (piece_size, piece_size))
                
                # Draw stacked pieces with offset
                for i in range(count):
                    screen.blit(scaled_img, (x_position + i * stack_offset, y_black))
                
                # Move to next piece type position
                x_position += piece_size + 15
    
    # Draw score for white (if leading)
    if leading_color == WHITE:
        font = pygame.font.SysFont(None, 48)
        score_text = f"+{score_diff}"
        score_surface = font.render(score_text, True, (200, 200, 200))
        screen.blit(score_surface, (x_position + 10, y_black + 5))
    
    # Draw white captured pieces above black (pieces captured by black = white pieces)
    x_position_white = x_start
    y_white = current_height - 120  # Above black
    
    # Count and group white pieces by type
    white_count = {notation: 0 for notation in piece_order}
    for piece in game.black_captured:
        white_count[piece] += 1
    
    # Draw white pieces grouped by type
    for notation in piece_order:
        count = white_count[notation]
        if count > 0:
            piece_name = piece_names.get(notation, "pawn")
            image_key = piece_name + "_white"
            
            if image_key in images:
                img = images[image_key]
                scaled_img = pygame.transform.smoothscale(img, (piece_size, piece_size))
                
                # Draw stacked pieces with offset
                for i in range(count):
                    screen.blit(scaled_img, (x_position_white + i * stack_offset, y_white))
                
                # Move to next piece type position
                x_position_white += piece_size + 15
    
    # Draw score for black (if leading)
    if leading_color == BLACK:
        font = pygame.font.SysFont(None, 48)
        score_text = f"+{score_diff}"
        score_surface = font.render(score_text, True, (200, 200, 200))
        screen.blit(score_surface, (x_position_white + 10, y_white + 5))

