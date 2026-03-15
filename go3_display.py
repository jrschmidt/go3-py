# # # #    #   #   #   #   #     # # # #
# # #         go3_display.py         # # #
# # # #    #   #   #   #   #     # # # #

# This module manages the Go3 GUI in a Tkinter display.
# It draws the Go3 gameboard, and draws and erases Go stones.
# Mouse click events are handled by the callback passed
# from go3.py when the display is instantiated.


import tkinter as tk
from collections.abc import Callable

from go3_board import Point, StoneColor, RED, WHITE, BLUE, is_valid_gameboard_point


# # # # #     Module-level state     # # # # #

_on_click: Callable[[Point], None] | None = None
_root: tk.Tk | None = None
_canvas: tk.Canvas | None = None
_hover_circle: int | None = None
_hover_label: int | None = None


# # # # #     Color constants     # # # # #

_STONE_COLOR: dict[StoneColor, str] = {
    RED:   "#cc3333",
    WHITE: "#f0f0f0",
    BLUE:  "#5050cc",
}

_APP_COLOR = "#cccc99"
_BOARD_COLOR = "#cc9933"
_LINE_COLOR = "#000000"
_BOARD_MARGIN_COLOR = "#000000"
_STONE_EDGE_COLOR = "#000000"
_GHOST = "#aaaaaa"
_TEXT_COLOR = "#3333cc"


# # # # #     Board geometry constants     # # # # #

# Actual pixel coordinates of the corners of the gameboard display.
_HEX_VERTICES = [(157,26),(443,26),(576,270),(443,514),(157,514),(25,270)]

# Star points in traditional Go are thick black dots placed as visual markers.
# These points are placed on the hexagonal Go3 board as corresponding equivalents.
_STAR_POINTS: list[Point] = [ [3,3], [6,3], [3,6], [6,6], [9,6], [6,9], [9,9] ]

# The end points of the 11 horizontal ("W-E") lines on the Go3 gameboard.
_W_E: list[tuple[Point, Point]] = [
    ((1, 1),  (6, 1)),
    ((1, 2),  (7, 2)),
    ((1, 3),  (8, 3)),
    ((1, 4),  (9, 4)),
    ((1, 5),  (10, 5)),
    ((1, 6),  (11, 6)),
    ((2, 7),  (11, 7)),
    ((3, 8),  (11, 8)),
    ((4, 9),  (11, 9)),
    ((5, 10), (11, 10)),
    ((6, 11), (11, 11)),
]

# The end points of the 11 diagonal "SW-NE" lines that run from the lower left
# to the upper right of the Go3 gameboard at an angle 60 degrees counterclockwise
# to horizontal.
_SW_NE: list[tuple[Point, Point]] = [
    ((1, 6),  (1, 1)),
    ((2, 7),  (2, 1)),
    ((3, 8),  (3, 1)),
    ((4, 9),  (4, 1)),
    ((5, 10), (5, 1)),
    ((6, 11), (6, 1)),
    ((7, 11), (7, 2)),
    ((8, 11), (8, 3)),
    ((9, 11), (9, 4)),
    ((10, 11),(10, 5)),
    ((11, 11),(11, 6)),
]

# The end points of the 11 diagonal "NW-SE" lines that run from the upper left
# to the lower right of the Go3 gameboard at an angle 60 degrees clockwise to
# horizontal.
_NW_SE: list[tuple[Point, Point]] = [
    ((1, 6),  (6, 11)),
    ((1, 5),  (7, 11)),
    ((1, 4),  (8, 11)),
    ((1, 3),  (9, 11)),
    ((1, 2),  (10, 11)),
    ((1, 1),  (11, 11)),
    ((2, 1),  (11, 10)),
    ((3, 1),  (11, 9)),
    ((4, 1),  (11, 8)),
    ((5, 1),  (11, 7)),
    ((6, 1),  (11, 6)),
]


# # # # #     Public API     # # # # #

# Instantiate a Tkinter Canvas widget.
def display_init(on_click: Callable[[Point], None]) -> None:
    global _on_click, _root, _canvas, _hover_circle, _hover_label
    _on_click = on_click
    _root = tk.Tk()
    _root.title("Go3 Board")
    _canvas = tk.Canvas(_root, width=600, height=540, bg=_APP_COLOR,
                        highlightthickness=2, highlightbackground="red")
    _canvas.pack()
    draw_empty_board(_canvas)
    _hover_circle = None
    _canvas.bind("<Button-1>", _handle_click)
    _canvas.bind("<Motion>", _handle_mouse_move)
    _canvas.bind("<Leave>", _clear_hover)


def run() -> None:
    _root.mainloop()

# Draw a stone at point (a,b) of the designated color.
def place_stone(ab: Point, color: StoneColor) -> None:
    draw_stone(_canvas, ab, color)


# # # # #     Coordinate transform functions     # # # # #

# Determine if a tuple (a,b) represents a legitimate point on the Go3 gameboard.
def is_in_board_hex(x: int, y: int) -> bool:
    verts = _HEX_VERTICES
    n = len(verts)
    for i in range(n):
        x1, y1 = verts[i]
        x2, y2 = verts[(i + 1) % n]
        if (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1) > 0:
            return False
    return True

# Calculate the (x,y) pixel coordinates in the Tkinter Canvas widget of
# point (a,b) on the gameboard.
def get_x(ab: Point) -> int: return 150 + 50 * ab[0] - 25 * ab[1]
def get_y(ab: Point) -> int: return 6 + 44 * ab[1]

# Determine which gameboard point (a,b), if any, is closest to pixel (x,y)
# on the Tkinter Canvas widget.
def get_point(x: int, y: int) -> Point | None:
    b = (y - 28) // 44 + 1
    a = (x - 125 + 25 * b) // 50
    if not is_valid_gameboard_point((a, b)):
        return None
    return (a, b)


# # # # #     Drawing functions     # # # # #

# Draw a hexagon on the Canvas widget as a base layer for the Go3 board visual representation.
def draw_base_hex(canvas: tk.Canvas) -> None:
    canvas.create_polygon(157, 26, 443, 26, 576, 270, 443, 514, 157, 514, 25, 270,
        fill=_BOARD_COLOR, outline=_BOARD_MARGIN_COLOR, width=5)

# Draw a thinner hexagonal margin directly inside the hexagon's outer margin, in keeping
# with the visual design of traditional Go boards.
def draw_base_margin(canvas: tk.Canvas) -> None:
    canvas.create_polygon(163, 34, 437, 34, 567, 270, 437, 506, 163, 506, 33, 270,
        fill="", outline=_BOARD_MARGIN_COLOR, width=3)

# Draw a line on the Go3 board from one gameboard point to another.
def draw_line(canvas: tk.Canvas, beg: Point, end: Point) -> None:
    canvas.create_line(get_x(beg), get_y(beg), get_x(end), get_y(end),
        fill=_LINE_COLOR, width=3)

# Draw all the lines in all directions necessary to draw the Go3 gameboard.
def draw_lines(canvas: tk.Canvas) -> None:
    for beg, end in _W_E:   draw_line(canvas, beg, end)
    for beg, end in _SW_NE: draw_line(canvas, beg, end)
    for beg, end in _NW_SE: draw_line(canvas, beg, end)


# Draw the star points (thick black dots) at the designated locations as an analog
# to the star points on traditional rectangular gameboards.
def draw_star_points(canvas: tk.Canvas) -> None:
    for ab in _STAR_POINTS:
        cx, cy = get_x(ab), get_y(ab)
        canvas.create_oval(cx - 7, cy - 7, cx + 7, cy + 7,
            fill=_LINE_COLOR, outline=_LINE_COLOR)

# Draw the entire Go3 board (with no stones placed yet).
def draw_empty_board(canvas: tk.Canvas) -> None:
    draw_base_hex(canvas)
    draw_base_margin(canvas)
    draw_lines(canvas)
    draw_star_points(canvas)

# Draw a stone of the designated color at point (a,b).
def draw_stone(canvas: tk.Canvas, ab: Point, color: StoneColor) -> None:
    if not is_valid_gameboard_point(ab):
        raise ValueError(f"Point {ab} is not a valid gameboard position")
    cx, cy = get_x(ab), get_y(ab)
    color = _STONE_COLOR[color]
    canvas.create_oval(cx - 17, cy - 17, cx + 17, cy + 17,
        fill=color, outline=_STONE_EDGE_COLOR, width=2)
    canvas.create_oval(cx - 19, cy - 19, cx + 19, cy + 19,
        fill="", outline=_BOARD_COLOR, width=2)


# # # # #     Event handlers     # # # # #

# Passes the click event at (x,y) to the callback function provided
# by go3.py or a test program.
def _handle_click(event) -> None:
    pt = get_point(event.x, event.y)
    if pt is not None:
        _on_click(pt)


# Prints a string in the upper right corner of the Canvas widget.
def _update_coord_label(text: str) -> None:
    global _hover_label
    if _hover_label is None:
        _hover_label = _canvas.create_text(
            590, 10, anchor="ne", text=text,
            font=("TkDefaultFont", 20), fill=_TEXT_COLOR
        )
    else:
        _canvas.itemconfig(_hover_label, text=text)

# Clears the mouse hover circle if the mouse moves out of the gameboard hexagon.
def _clear_hover(event=None) -> None:
    global _hover_circle
    if _hover_circle is not None:
        _canvas.delete(_hover_circle)
        _hover_circle = None
    _canvas.config(cursor="")
    _update_coord_label("")


# Draws a light circle around the closest Go3 gameboard point as the mouse moves around the gameboard
# and displays the (a,b) coordinates of the point on the Canvas widget outside of the gameboard hexagon.
def _handle_mouse_move(event) -> None:
    _clear_hover()
    pt = get_point(event.x, event.y)
    if pt is not None:
        cx = get_x(pt)
        cy = get_y(pt)
        r = 21
        global _hover_circle
        _hover_circle = _canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            outline=_GHOST, fill="", width=2
        )
    if is_in_board_hex(event.x, event.y):
        _canvas.config(cursor="none")
    else:
        _canvas.config(cursor="")
    coord_text = f"{pt[0]}, {pt[1]}" if pt is not None else "-  -"
    _update_coord_label(coord_text)
