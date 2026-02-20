import pygame
import sys

# Board constants
BOARD_SIZE = 8
SQUARE_SIZE = 80
WINDOW_SIZE = BOARD_SIZE * SQUARE_SIZE

# Colors
WHITE_COLOR = (240, 217, 181)
BLACK_COLOR = (181, 136, 99)
HIGHLIGHT_COLOR = (255, 255, 102)  # Yellow tint for selected square
CHECK_COLOR = (255, 0, 0)  # Red tint for king in check
NAVY_BLUE = (0, 0, 128)
LIGHT_GREY = (200, 200, 200)
DARK_GREY = (100, 100, 100)

WHITE = "white"
BLACK = "black"

# Piece values (material points)
PIECE_VALUES = {
    "": 1,      # Pawn
    "N": 3,     # Knight
    "B": 3,     # Bishop
    "R": 5,     # Rook
    "Q": 9,     # Queen
    "K": 0      # King (shouldn't be captured)
}
