# # # #    #   #   #   #   #     # # # #
# # #         hexgo_draw.py         # # #
# # # #    #   #   #   #   #     # # # #

# Draws the Go3 gameboard onto a Tkinter Canvas widget, and nothing else:
# no stones, no dashboards, no click/hover handling.
#
# Board geometry (row widths, the three line-direction lists, and star
# points) is generated from SIDE_LENGTH below rather than hardcoded, so
# the board size can be changed by editing one constant.


import tkinter as tk

from go3_board import Point, HEX_DELTAS
from go3_display import _BOARD_COLOR, _LINE_COLOR, _BOARD_MARGIN_COLOR, _APP_COLOR


# # # # #     Board size     # # # # #

# Number of points along each of the hexagon's 6 sides. All board geometry
# below is generated from this one number. (6 -> 91 points, 8 -> 169 points)
SIDE_LENGTH = 8

# The side length and pixel-spacing constants that go3_display.py's
# hand-typed board data (and its _get_x/_get_y formulas) were built around.
# Used as a baseline to scale point spacing for other side lengths so the
# grid still fits within roughly the same on-screen hexagon.
_REFERENCE_SIDE_LENGTH = 6
_REFERENCE_STEP = 50       # pixels per 'a' step, at _REFERENCE_SIDE_LENGTH
_REFERENCE_ROW_STEP = 44   # pixels per 'b' step, at _REFERENCE_SIDE_LENGTH
_CENTER_PX = (300, 270)    # pixel location of the board's center point


# # # # #     Board geometry, generated from SIDE_LENGTH     # # # # #

# Generalizes go3_board.ROW_BEGIN_END: the (start, end) 'a' bounds of each
# row 'b', for a board with the given number of points per side.
def _row_bounds(side_length: int) -> list[tuple[int, int]]:
    top = 2 * side_length - 1
    bounds = []
    for b in range(1, top + 1):
        if b <= side_length:
            bounds.append((1, b + side_length - 1))
        else:
            bounds.append((b - side_length + 1, top))
    return bounds

# All valid points (a,b) on a board with the given number of points per side.
def _all_points(side_length: int) -> list[Point]:
    return [(a, b) for b, (start, end) in enumerate(_row_bounds(side_length), start=1)
            for a in range(start, end + 1)]

# Groups points by `invariant` and returns the two extreme points (by
# `varying`) of each group as a line segment. Used to build the W-E, SW-NE,
# and NW-SE line lists (go3_display._W_E/_SW_NE/_NW_SE) for any side length:
# each of those three line directions holds one of (b), (a), or (a-b) constant.
def _lines_by_invariant(points, invariant, varying) -> list[tuple[Point, Point]]:
    groups: dict[int, list[Point]] = {}
    for p in points:
        groups.setdefault(invariant(p), []).append(p)
    return [(min(g, key=varying), max(g, key=varying)) for g in groups.values()]

def _board_lines(side_length: int) -> list[tuple[Point, Point]]:
    points = _all_points(side_length)
    w_e   = _lines_by_invariant(points, lambda p: p[1],        lambda p: p[0])
    sw_ne = _lines_by_invariant(points, lambda p: p[0],        lambda p: p[1])
    nw_se = _lines_by_invariant(points, lambda p: p[0] - p[1], lambda p: p[0])
    return w_e + sw_ne + nw_se

# Star points: the board's center point, plus one point offset halfway
# toward each of the 6 hex directions (matches the existing side-6 layout,
# whose star points sit 3 steps from center in each direction).
def _star_points(side_length: int) -> list[Point]:
    cx, cy = side_length, side_length
    offset = side_length // 2
    return [(cx, cy)] + [(cx + offset * da, cy + offset * db) for da, db in HEX_DELTAS]


# # # # #     Coordinate transforms     # # # # #

# How much to shrink/grow point spacing, relative to _REFERENCE_SIDE_LENGTH,
# so a board with more (or fewer) points per side still spans roughly the
# same physical hexagon.
def _spacing_scale(side_length: int) -> float:
    reference_rows = 2 * _REFERENCE_SIDE_LENGTH - 1
    rows = 2 * side_length - 1
    return (reference_rows - 1) / (rows - 1)

# Calculate the (x,y) pixel coordinates on the Canvas widget of point (a,b)
# on a board with the given side length. At _REFERENCE_SIDE_LENGTH this is
# algebraically identical to Go3Display._get_x/_get_y (go3_display.py).
def _get_x(ab: Point, side_length: int) -> int:
    step = _REFERENCE_STEP * _spacing_scale(side_length)
    a, b = ab
    return round(_CENTER_PX[0] + step * (a - side_length) - (step / 2) * (b - side_length))

def _get_y(ab: Point, side_length: int) -> int:
    row_step = _REFERENCE_ROW_STEP * _spacing_scale(side_length)
    _, b = ab
    return round(_CENTER_PX[1] + row_step * (b - side_length))


# # # # #     Drawing     # # # # #

# Draw a hexagon on the Canvas widget as a base layer for the Go3 board visual representation.
def _draw_base_hex(canvas: tk.Canvas) -> None:
    canvas.create_polygon(157, 26, 443, 26, 576, 270, 443, 514, 157, 514, 25, 270,
        fill=_BOARD_COLOR, outline=_BOARD_MARGIN_COLOR, width=5)

# Draw a thinner hexagonal margin directly inside the hexagon's outer margin, in keeping
# with the visual design of traditional Go boards.
def _draw_base_margin(canvas: tk.Canvas) -> None:
    canvas.create_polygon(163, 34, 437, 34, 567, 270, 437, 506, 163, 506, 33, 270,
        fill="", outline=_BOARD_MARGIN_COLOR, width=3)

# Draw a line on the Go3 board from one gameboard point to another.
def _draw_line(canvas: tk.Canvas, beg: Point, end: Point, side_length: int) -> None:
    canvas.create_line(_get_x(beg, side_length), _get_y(beg, side_length),
        _get_x(end, side_length), _get_y(end, side_length), fill=_LINE_COLOR, width=3)

# Draw all the lines needed to draw the Go3 gameboard at the given side length.
def _draw_lines(canvas: tk.Canvas, side_length: int) -> None:
    for beg, end in _board_lines(side_length):
        _draw_line(canvas, beg, end, side_length)

# Draw the star points (thick black dots) at the designated locations as an analog
# to the star points on traditional rectangular gameboards.
def _draw_star_points(canvas: tk.Canvas, side_length: int) -> None:
    r = round(7 * _spacing_scale(side_length))
    for ab in _star_points(side_length):
        cx, cy = _get_x(ab, side_length), _get_y(ab, side_length)
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=_LINE_COLOR, outline=_LINE_COLOR)

# Draw the entire Go3 gameboard (with no stones placed) at the given side length.
def draw_empty_board(canvas: tk.Canvas, side_length: int = SIDE_LENGTH) -> None:
    _draw_base_hex(canvas)
    _draw_base_margin(canvas)
    _draw_lines(canvas, side_length)
    _draw_star_points(canvas, side_length)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Go3 Board")
    canvas = tk.Canvas(root, width=600, height=540, bg=_APP_COLOR, highlightthickness=0)
    canvas.pack()
    draw_empty_board(canvas)
    root.mainloop()
