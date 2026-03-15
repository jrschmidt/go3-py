# # # #      #   #   #   #   #       # # # #
# # #           go3_board.py           # # #
# # #       _ _ _ _ _ _ _ _ _ _        # # #
# # #                                  # # #
# # #   A hexagonal 3-player Go game   # # #
# # # #      #   #   #   #   #       # # # #


# Types, constants and methods pertaining to the
# Go3 gameboard layout and structure.


from collections.abc import Iterator
from typing import Literal


# # # # #     Type definitions     # # # # #

# Coordinates of a point on the gameboard. The first coordinate designates
# a diagonal line running form lower left to upper right ("SW-NE"), numbered
# 1 to 11. The second number designates a horizontal line ("W-E"), also 1 to 11.
Point = tuple[int, int]

# The stone colors of the three players. (Traditional two-player rectangular Go
# uses black and white stones.)
StoneColor = Literal["RED", "WHITE", "BLUE"]

# Represent a stone played on the board.
Stone = tuple[Point, StoneColor]

# A Stones[] list is used to represent all the stones currently on the board.
# Stones[] lists are also used in test and game analysis functions.
Stones = list[Stone]


# # # # #     Constants     # # # # #

# This constant is used to determine if a tuple (a,b) represents a valid point
# within the gameboard, and to iterate through all the points on the board.
# 
# (1,6) indicates that the first horizontal row starts at (1,1) and ends at (6,1).
# (1,7) indicates that the second horizontal row starts at (1,2) and ends at (7,2).
#     ....
# (5,11) indicates that the tenth horizontal row starts at (5,10) and ends at (11,10).
# (6,11) indicates that the eleventh horizontal row starts at (6,11) and ends at (11,11).
ROW_BEGIN_END: list[tuple[int, int]] = [
    (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11),
    (2, 11), (3, 11), (4, 11), (5, 11), (6, 11),
]

# Define RED, WHITE, and BLUE as constants of type StoneColor.
RED:   StoneColor = "RED"
WHITE: StoneColor = "WHITE"
BLUE:  StoneColor = "BLUE"


# # # # #     Functions     # # # # #

# Determines if a tuple (a,b) represents a valid point on the Go3 Gameboard.
def is_valid_gameboard_point(point: Point) -> bool:
    a, b = point
    if not 1 <= b <= 11:
        return False
    start, end = ROW_BEGIN_END[b - 1]
    return start <= a <= end


# Iterates through all the points on the gameboard.
def gameboard_points() -> Iterator[Point]:
    for b, (start, end) in enumerate(ROW_BEGIN_END, start=1):
        for a in range(start, end + 1):
            yield (a, b)
