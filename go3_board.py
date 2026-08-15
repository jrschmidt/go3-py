# # # #      #   #   #   #   #       # # # #
# # #           go3_board.py           # # #
# # #       _ _ _ _ _ _ _ _ _ _        # # #
# # #                                  # # #
# # #   A hexagonal 3-player Go game   # # #
# # # #      #   #   #   #   #       # # # #


# Types, constants and methods pertaining to the
# Go3 gameboard layout and structure.


from collections.abc import Iterator
from enum import Enum
from typing import TypedDict


# # # # #     Type definitions     # # # # #

# Coordinates of a point on the gameboard. The first coordinate designates
# a diagonal line running form lower left to upper right ("SW-NE"), numbered
# 1 to 11. The second number designates a horizontal line ("W-E"), also 1 to 11.
Point = tuple[int, int]

# The stone colors of the three players. (Traditional two-player rectangular Go
# uses black and white stones.)
class StoneColor(str, Enum):
    RED   = "RED"
    WHITE = "WHITE"
    BLUE  = "BLUE"

# Represent a stone played on the board.
Stone = tuple[Point, StoneColor]

# A Stones[] list is used to represent all the stones currently on the board.
# Stones[] lists are also used in test and game analysis functions.
Stones = list[Stone]

# The information that needs to be passed between the display and analyzer modules,
# via the go3.py controller module during gameplay:
    # `next_player` : Which player moves next.
    # `stones` : All the stones currently on the board.
    # `legal_moves` : All the currently available legal moves for the curent player.
class GameState(TypedDict):
    next_player: StoneColor
    stones: Stones
    legal_moves: set[Point]


# # # # #     Constants     # # # # #

# Number of points along each of the hexagon's 6 sides. All board-shape data
# below is generated from this one number. (6 -> 91 points, 8 -> 169 points)
# This is the module's own default, used if the board is imported standalone
# (tests, a REPL) without go3.py calling set_side_length() first.
SIDE_LENGTH: int = 8

# Generalizes the (start, end) 'a' bounds of each row 'b', for a board with
# the given number of points per side.
#
# (1,6) indicates that the first horizontal row starts at (1,1) and ends at (6,1).
# (1,7) indicates that the second horizontal row starts at (1,2) and ends at (7,2).
#     ....
# (5,11) indicates that the tenth horizontal row starts at (5,10) and ends at (11,10).
# (6,11) indicates that the eleventh horizontal row starts at (6,11) and ends at (11,11).
def row_bounds(side_length: int) -> list[tuple[int, int]]:
    top = 2 * side_length - 1
    bounds = []
    for b in range(1, top + 1):
        if b <= side_length:
            bounds.append((1, b + side_length - 1))
        else:
            bounds.append((b - side_length + 1, top))
    return bounds

# This constant is used to determine if a tuple (a,b) represents a valid point
# within the gameboard, and to iterate through all the points on the board.
ROW_BEGIN_END: list[tuple[int, int]] = row_bounds(SIDE_LENGTH)

# Define RED, WHITE, and BLUE as constants of type StoneColor.
RED:   StoneColor = StoneColor.RED
WHITE: StoneColor = StoneColor.WHITE
BLUE:  StoneColor = StoneColor.BLUE


# # # # #     Functions     # # # # #

# Switches the active board size, regenerating ROW_BEGIN_END. Call this
# before any game-state or legal-move computation happens.
def set_side_length(side_length: int) -> None:
    global SIDE_LENGTH, ROW_BEGIN_END
    SIDE_LENGTH = side_length
    ROW_BEGIN_END = row_bounds(side_length)

# Determines if a tuple (a,b) represents a valid point on the Go3 Gameboard.
def is_valid_gameboard_point(point: Point) -> bool:
    a, b = point
    if not 1 <= b <= len(ROW_BEGIN_END):
        return False
    start, end = ROW_BEGIN_END[b - 1]
    return start <= a <= end


# Iterates through all the points on the gameboard.
def gameboard_points() -> Iterator[Point]:
    for b, (start, end) in enumerate(ROW_BEGIN_END, start=1):
        for a in range(start, end + 1):
            yield (a, b)

# Returns a set of all points on the gameboard.
def all_gameboard_points() -> set[Point]:
    return set(gameboard_points())

# All valid points (a,b) on a board with the given number of points per side.
def all_points(side_length: int) -> list[Point]:
    return [(a, b) for b, (start, end) in enumerate(row_bounds(side_length), start=1)
            for a in range(start, end + 1)]

# Groups points by `invariant` and returns the two extreme points (by
# `varying`) of each group as a line segment. Used to build the W-E, SW-NE,
# and NW-SE line lists for any side length: each of those three line
# directions holds one of (b), (a), or (a-b) constant.
def _lines_by_invariant(points, invariant, varying) -> list[tuple[Point, Point]]:
    groups: dict[int, list[Point]] = {}
    for p in points:
        groups.setdefault(invariant(p), []).append(p)
    return [(min(g, key=varying), max(g, key=varying)) for g in groups.values()]

# The line segments (in board coordinates) needed to draw the gameboard grid
# at the given side length: W-E, then SW-NE, then NW-SE lines.
def board_lines(side_length: int) -> list[tuple[Point, Point]]:
    points = all_points(side_length)
    w_e   = _lines_by_invariant(points, lambda p: p[1],        lambda p: p[0])
    sw_ne = _lines_by_invariant(points, lambda p: p[0],        lambda p: p[1])
    nw_se = _lines_by_invariant(points, lambda p: p[0] - p[1], lambda p: p[0])
    return w_e + sw_ne + nw_se

# Star points: the board's center point, plus one point offset halfway
# toward each of the 6 hex directions (matches the original side-6 layout,
# whose star points sit 3 steps from center in each direction).
def star_points(side_length: int) -> list[Point]:
    cx, cy = side_length, side_length
    offset = side_length // 2
    return [(cx, cy)] + [(cx + offset * da, cy + offset * db) for da, db in HEX_DELTAS]


# The 6 adjacent directions on the hexagonal board, in clockwise order:
# NE, E, SE, SW, W, NW
HEX_DELTAS: list[tuple[int, int]] = [(0,-1),(1,0),(1,1),(0,1),(-1,0),(-1,-1)]

# Returns all valid points adjacent to point p.
def adjacent_points(p: Point) -> list[Point]:
    a, b = p
    return [(a+da, b+db) for da, db in HEX_DELTAS
            if is_valid_gameboard_point((a+da, b+db))]

# Returns True if pt1 and pt2 are adjacent on the gameboard.
def are_adjacent(pt1: Point, pt2: Point) -> bool:
    return pt2 in adjacent_points(pt1)
