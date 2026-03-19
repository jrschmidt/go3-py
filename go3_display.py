# # # #    #   #   #   #   #     # # # #
# # #         go3_display.py         # # #
# # # #    #   #   #   #   #     # # # #

# This module manages the Go3 GUI in a Tkinter display.
# It draws the Go3 gameboard, and draws and erases Go stones.
# Mouse click events are handled by the callback passed
# from go3.py when the display is instantiated.


import tkinter as tk
import tkinter.ttk as ttk
from collections.abc import Callable

from go3_board import Point, StoneColor, Stones, RED, WHITE, BLUE, is_valid_gameboard_point


# # # # #     Color constants     # # # # #

_STONE_COLOR: dict[StoneColor, str] = {
    RED:   "#cc3333",
    WHITE: "#f0f0f0",
    BLUE:  "#5050cc",
}

# Gameboard widget colors
_APP_COLOR = "#cccc99"
_BOARD_COLOR = "#cc9933"
_LINE_COLOR = "#000000"
_BOARD_MARGIN_COLOR = "#000000"
_STONE_EDGE_COLOR = "#000000"
_GHOST = "#aaaaaa"

# Dashboard widget colors
_CANVAS_TEXT_COLOR = "#3333cc"
_DIALOG_COLOR = "#6699aa"
_DIALOG_TEXT_COLOR = "#ffffff"
_MSG_COLOR = "#000000"
_MSG_TEXT_COLOR = "#ffffff"


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


# # # # #     Dashboard classes     # # # # #

# Two dashboard classes to be inserted into a tabbed tk.Notebook/tk.Frame container
# adjacent to the gameboard widget.

# The primary display area for user interaction during the course of gameplay.
# ("It's your turn", etc.)
class GameDashboard:
    def __init__(self, frame: tk.Frame) -> None:
        self._widget = frame
        self._widget.config(bg=_DIALOG_COLOR)
        # tk.Label(self._widget, text="GAME DASHBOARD",
        #          font=("TkDefaultFont", 14, "bold"),
        #          bg=_DIALOG_COLOR, fg=_DIALOG_TEXT_COLOR).pack(pady=(8, 2))
        tk.Label(self._widget,
                 text="Game dashboard widget, controlled by go3.py.",
                 bg=_DIALOG_COLOR, fg=_DIALOG_TEXT_COLOR).pack()

# A text area for diagnostic messages, displaying variable values for development and
# debugging, etc.
class AnalysisDashboard:
    def __init__(self, frame: tk.Frame) -> None:
        self._widget = frame
        tk.Label(self._widget, text="ANALYSIS DASHBOARD",
                 font=("TkDefaultFont", 14, "bold")).pack(pady=(8, 2))
        self._text = tk.Text(self._widget, wrap="word", relief="flat",
                             bg=_MSG_COLOR, fg=_MSG_TEXT_COLOR)
        self._text.insert("1.0", "Analysis dashboard widget, controlled by go3_analyzer.py.")
        self._text.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def printline(self, s: str) -> None:
        self._text.insert("end", "\n" + s)


# # # # #     Go3Display class     # # # # #

class Go3Display:

    # Instantiate a Tkinter Canvas widget.
    def __init__(self, on_click: Callable[[Point], None]) -> None:
        self._on_click = on_click
        self._root = tk.Tk()
        self._root.title("Go3 Board")
        _main_frame = tk.Frame(self._root)
        _main_frame.pack(fill="both", expand=True)
        self._canvas = tk.Canvas(_main_frame, width=600, height=540, bg=_APP_COLOR,
                                 highlightthickness=2, highlightbackground="red")
        self._canvas.pack(side="left")
        _dash_frame = tk.Frame(_main_frame, width=480)
        _dash_frame.pack(side="left", fill="y")
        _dash_frame.pack_propagate(False)
        self._dashboard          = ttk.Notebook(_dash_frame)
        self._game               = tk.Frame(self._dashboard)
        self._analysis           = tk.Frame(self._dashboard)
        self._dashboard.add(self._game,     text="GAME")
        self._dashboard.add(self._analysis, text="ANALYSIS")
        self._dashboard.pack(fill="both", expand=True)
        self._dashboard.bind("<<NotebookTabChanged>>",
                             lambda e: self._root.update_idletasks())
        self._game_dashboard     = GameDashboard(self._game)
        self._analysis_dashboard = AnalysisDashboard(self._analysis)
        self._hover_circle: int | None = None
        self._hover_label: int | None = None
        self._canvas.bind("<Button-1>", self._handle_click)
        self._canvas.bind("<Motion>", self._handle_mouse_move)
        self._canvas.bind("<Leave>", self._clear_hover)
        self._draw_empty_board()


    # # # # #     Public methods     # # # # #

    @property
    def game_dashboard(self) -> GameDashboard:
        return self._game_dashboard

    @property
    def analysis_dashboard(self) -> AnalysisDashboard:
        return self._analysis_dashboard

    def start_loop(self) -> None:
        self._root.mainloop()

    # Clears the board and redraws all stones in the given stones list.
    def draw_stones(self, stones: Stones) -> None:
        self._draw_empty_board()
        for stone in stones:
            self._place_stone(stone[0], stone[1])


    # # # # #     Private methods — stone placement     # # # # #

    # Draw a stone at point (a,b) of the designated color.
    def _place_stone(self, ab: Point, color: StoneColor) -> None:
        self._draw_stone(ab, color)


    # # # # #     Private methods — coordinate transforms     # # # # #

    # Determine if a tuple (a,b) represents a legitimate point on the Go3 gameboard.
    def _is_in_board_hex(self, x: int, y: int) -> bool:
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
    def _get_x(self, ab: Point) -> int: return 150 + 50 * ab[0] - 25 * ab[1]
    def _get_y(self, ab: Point) -> int: return 6 + 44 * ab[1]

    # Determine which gameboard point (a,b), if any, is closest to pixel (x,y)
    # on the Tkinter Canvas widget.
    def _get_point(self, x: int, y: int) -> Point | None:
        b = (y - 28) // 44 + 1
        a = (x - 125 + 25 * b) // 50
        if not is_valid_gameboard_point((a, b)):
            return None
        return (a, b)


    # # # # #     Private methods — drawing     # # # # #

    # Draw a hexagon on the Canvas widget as a base layer for the Go3 board visual representation.
    def _draw_base_hex(self) -> None:
        self._canvas.create_polygon(157, 26, 443, 26, 576, 270, 443, 514, 157, 514, 25, 270,
            fill=_BOARD_COLOR, outline=_BOARD_MARGIN_COLOR, width=5)

    # Draw a thinner hexagonal margin directly inside the hexagon's outer margin, in keeping
    # with the visual design of traditional Go boards.
    def _draw_base_margin(self) -> None:
        self._canvas.create_polygon(163, 34, 437, 34, 567, 270, 437, 506, 163, 506, 33, 270,
            fill="", outline=_BOARD_MARGIN_COLOR, width=3)

    # Draw a line on the Go3 board from one gameboard point to another.
    def _draw_line(self, beg: Point, end: Point) -> None:
        self._canvas.create_line(self._get_x(beg), self._get_y(beg),
                                 self._get_x(end), self._get_y(end),
                                 fill=_LINE_COLOR, width=3)

    # Draw all the lines in all directions necessary to draw the Go3 gameboard.
    def _draw_lines(self) -> None:
        for beg, end in _W_E:   self._draw_line(beg, end)
        for beg, end in _SW_NE: self._draw_line(beg, end)
        for beg, end in _NW_SE: self._draw_line(beg, end)

    # Draw the star points (thick black dots) at the designated locations as an analog
    # to the star points on traditional rectangular gameboards.
    def _draw_star_points(self) -> None:
        for ab in _STAR_POINTS:
            cx, cy = self._get_x(ab), self._get_y(ab)
            self._canvas.create_oval(cx - 7, cy - 7, cx + 7, cy + 7,
                fill=_LINE_COLOR, outline=_LINE_COLOR)

    # Draw the entire Go3 board (with no stones placed yet).
    def _draw_empty_board(self) -> None:
        self._draw_base_hex()
        self._draw_base_margin()
        self._draw_lines()
        self._draw_star_points()

    # Draw a stone of the designated color at point (a,b).
    def _draw_stone(self, ab: Point, color: StoneColor) -> None:
        if not is_valid_gameboard_point(ab):
            raise ValueError(f"Point {ab} is not a valid gameboard position")
        cx, cy = self._get_x(ab), self._get_y(ab)
        fill = _STONE_COLOR[color]
        self._canvas.create_oval(cx - 17, cy - 17, cx + 17, cy + 17,
            fill=fill, outline=_STONE_EDGE_COLOR, width=2)
        self._canvas.create_oval(cx - 19, cy - 19, cx + 19, cy + 19,
            fill="", outline=_BOARD_COLOR, width=2)


    # # # # #     Private methods — event handlers     # # # # #

    # Passes the click event at (x,y) to the callback function provided
    # by go3.py or a test program.
    def _handle_click(self, event) -> None:
        pt = self._get_point(event.x, event.y)
        if pt is not None:
            self._on_click(pt)

    # Prints a string in the upper right corner of the Canvas widget.
    def _update_coord_label(self, text: str) -> None:
        if self._hover_label is None:
            self._hover_label = self._canvas.create_text(
                590, 10, anchor="ne", text=text,
                font=("TkDefaultFont", 20), fill=_CANVAS_TEXT_COLOR
            )
        else:
            self._canvas.itemconfig(self._hover_label, text=text)

    # Clears the mouse hover circle if the mouse moves out of the gameboard hexagon.
    def _clear_hover(self, event=None) -> None:
        if self._hover_circle is not None:
            self._canvas.delete(self._hover_circle)
            self._hover_circle = None
        self._canvas.config(cursor="")
        self._update_coord_label("")

    # Draws a light circle around the closest Go3 gameboard point as the mouse moves around the gameboard
    # and displays the (a,b) coordinates of the point on the Canvas widget outside of the gameboard hexagon.
    def _handle_mouse_move(self, event) -> None:
        self._clear_hover()
        pt = self._get_point(event.x, event.y)
        if pt is not None:
            cx = self._get_x(pt)
            cy = self._get_y(pt)
            r = 21
            self._hover_circle = self._canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                outline=_GHOST, fill="", width=2
            )
        if self._is_in_board_hex(event.x, event.y):
            self._canvas.config(cursor="none")
        else:
            self._canvas.config(cursor="")
        coord_text = f"{pt[0]}, {pt[1]}" if pt is not None else "-  -"
        self._update_coord_label(coord_text)
