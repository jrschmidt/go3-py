# # # #    #   #   #   #   #     # # # #
# # #         go3_display.py         # # #
# # # #    #   #   #   #   #     # # # #

# This module manages the Go3 GUI in a Tkinter display.
# It draws the Go3 gameboard, and draws and erases Go stones.
# Mouse click events are handled by the callback passed
# from go3.py when the display is instantiated.


import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from collections.abc import Callable

import math

from go3_board import Point, StoneColor, Stones, GameState, RED, WHITE, BLUE, is_valid_gameboard_point
import go3_board


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
    # Analysis dashboard
_MSG_COLOR = "#000000"
_MSG_TEXT_COLOR = "#ffffff"
    # Game dashboard
_GAME_DASH_COLOR = "#999999"
_GAME_TEXT_COLOR = "#333333"
_CANVAS_TEXT_COLOR = "#3333cc"
_DIALOG_COLOR = "#6699aa"
_DIALOG_TEXT_COLOR = "#ffffff"


# # # # #     Board geometry constants     # # # # #

# Actual pixel coordinates of the corners of the gameboard display. This is
# the board's fixed physical boundary — independent of board size, since a
# denser/sparser point grid is scaled to fit within this same hexagon.
_HEX_VERTICES = [(157,26),(443,26),(576,270),(443,514),(157,514),(25,270)]

# The side length and pixel-spacing constants that the board's original
# hand-typed geometry (and its _get_x/_get_y formulas) were built around.
# Used as a baseline to scale point spacing for other side lengths so the
# grid still fits within the same on-screen hexagon (_HEX_VERTICES above).
_REFERENCE_SIDE_LENGTH = 6
_REFERENCE_STEP = 50       # pixels per 'a' step, at _REFERENCE_SIDE_LENGTH
_REFERENCE_ROW_STEP = 44   # pixels per 'b' step, at _REFERENCE_SIDE_LENGTH
_CENTER_PX = (300, 270)    # pixel location of the board's center point

# How much to shrink/grow point spacing, relative to _REFERENCE_SIDE_LENGTH,
# so a board with more (or fewer) points per side still spans roughly the
# same physical hexagon.
def _spacing_scale(side_length: int) -> float:
    reference_rows = 2 * _REFERENCE_SIDE_LENGTH - 1
    rows = 2 * side_length - 1
    return (reference_rows - 1) / (rows - 1)


# # # # #     Dashboard classes     # # # # #

# Two dashboard classes to be inserted into a tabbed tk.Notebook/tk.Frame container
# adjacent to the gameboard widget.

# The primary display area for user interaction during the course of gameplay.
# ("It's your turn", etc.)
class GameDashboard:
    def __init__(self, frame: tk.Frame) -> None:
        self._widget = frame
        self._widget.config(bg=_DIALOG_COLOR)
        tk.Label(self._widget,
                 text="Game dashboard widget, controlled by go3.py.",
                 bg=_DIALOG_COLOR, fg=_DIALOG_TEXT_COLOR).pack()

        # Turn indicator (140px tall, between header label and text area)
        _turn_border = tk.Frame(self._widget, bg=_GAME_TEXT_COLOR)
        _turn_border.pack(fill="x", padx=8, pady=4)
        _turn_frame = tk.Frame(_turn_border, height=140, bg=_GAME_DASH_COLOR)
        _turn_frame.pack(fill="x", padx=2, pady=2)
        _turn_frame.pack_propagate(False)

        # Left: turn icon — gameboard intersection with hexagon, radiating lines, and stone
        self._turn_canvas = tk.Canvas(_turn_frame, width=140, height=140,
                                      bg=_GAME_DASH_COLOR, highlightthickness=0)
        self._turn_canvas.pack(side="left")
        self._turn_canvas.create_polygon(
            106, 70, 88, 39, 52, 39, 34, 70, 52, 101, 88, 101,
            fill=_BOARD_COLOR, outline="")
        self._turn_canvas.create_line(88, 70, 103, 70, fill=_LINE_COLOR, width=3)
        self._turn_canvas.create_line(79, 54, 87, 41, fill=_LINE_COLOR, width=3)
        self._turn_canvas.create_line(61, 54, 54, 41, fill=_LINE_COLOR, width=3)
        self._turn_canvas.create_line(52, 70, 37, 70, fill=_LINE_COLOR, width=3)
        self._turn_canvas.create_line(61, 86, 54, 99, fill=_LINE_COLOR, width=3)
        self._turn_canvas.create_line(79, 86, 87, 99, fill=_LINE_COLOR, width=3)
        self._turn_circle = self._turn_canvas.create_oval(
            53, 53, 87, 87, fill=_STONE_COLOR[RED], outline=_STONE_EDGE_COLOR, width=2)

        # Right: two centered text labels
        _label_frame = tk.Frame(_turn_frame, bg=_GAME_DASH_COLOR)
        _label_frame.pack(side="left", fill="both", expand=True)
        _inner = tk.Frame(_label_frame, bg=_GAME_DASH_COLOR)
        _inner.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(_inner, text="YOUR TURN:", font=("TkDefaultFont", 18),
                 bg=_GAME_DASH_COLOR, fg=_GAME_TEXT_COLOR).pack()
        self._next_player_label = tk.Label(_inner, text=RED.value,
                                           font=("TkDefaultFont", 30, "bold"),
                                           bg=_GAME_DASH_COLOR, fg=_GAME_TEXT_COLOR)
        self._next_player_label.pack()

        self._text = ScrolledText(self._widget, wrap="word", relief="flat",
                                  bg=_DIALOG_COLOR, fg=_DIALOG_TEXT_COLOR)
        self._text.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def update_next_player_icon(self, color: StoneColor) -> None:
        self._turn_canvas.itemconfig(self._turn_circle, fill=_STONE_COLOR[color])
        self._next_player_label.config(text=color.value)

# A text area for diagnostic messages, displaying variable values for development and
# debugging, etc.
class AnalysisDashboard:
    def __init__(self, frame: tk.Frame) -> None:
        self._widget = frame
        tk.Label(self._widget, text="ANALYSIS DASHBOARD",
                 font=("TkDefaultFont", 14, "bold")).pack(pady=(8, 2))
        self._text = ScrolledText(self._widget, wrap="word", relief="flat",
                                  bg=_MSG_COLOR, fg=_MSG_TEXT_COLOR)
        self._text.insert("1.0", "ANALYSIS DASHBOARD WIDGET\n")
        self._text.insert("2.0", "Controlled by go3_analyzer.py.\n")
        self._text.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def printline(self, s: str) -> None:
        self._text.insert("end", "\n" + s)
        self._text.see(tk.END)


# # # # #     Go3Display class     # # # # #

class Go3Display:

    # Instantiate a Tkinter Canvas widget.
    def __init__(self, on_click: Callable[[Stone], None], side_length: int = 8) -> None:
        self._on_click = on_click
        self._side_length = side_length
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

    def respond_to_state_change(self, state: GameState) -> None:
        self._next_player = state["next_player"]
        self._legal_moves = state["legal_moves"]
        self.draw_stones(state["stones"])
        self._game_dashboard.update_next_player_icon(state["next_player"])
        self._game_dashboard._text.insert(tk.END, f"'Next player' is {state["next_player"].name}\n\n")
        self._game_dashboard._text.see(tk.END)


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
    # point (a,b) on the gameboard. At _REFERENCE_SIDE_LENGTH this is
    # algebraically identical to the original hand-typed formulas.
    def _get_x(self, ab: Point) -> int:
        side_length = self._side_length
        step = _REFERENCE_STEP * _spacing_scale(side_length)
        a, b = ab
        return round(_CENTER_PX[0] + step * (a - side_length) - (step / 2) * (b - side_length))

    def _get_y(self, ab: Point) -> int:
        side_length = self._side_length
        row_step = _REFERENCE_ROW_STEP * _spacing_scale(side_length)
        _, b = ab
        return round(_CENTER_PX[1] + row_step * (b - side_length))

    # Determine which gameboard point (a,b), if any, is closest to pixel (x,y)
    # on the Tkinter Canvas widget. The algebraic inverse of _get_x/_get_y,
    # snapping to the nearest point (round-half-up), matching the original
    # hand-typed formula exactly at _REFERENCE_SIDE_LENGTH.
    def _get_point(self, x: int, y: int) -> Point | None:
        side_length = self._side_length
        scale = _spacing_scale(side_length)
        step = _REFERENCE_STEP * scale
        row_step = _REFERENCE_ROW_STEP * scale
        cx_px, cy_px = _CENTER_PX
        b_exact = side_length + (y - cy_px) / row_step
        b = math.floor(b_exact + 0.5)
        a_exact = side_length + (x - cx_px) / step + (b - side_length) / 2
        a = math.floor(a_exact + 0.5)
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
        for beg, end in go3_board.board_lines(self._side_length):
            self._draw_line(beg, end)

    # Draw the star points (thick black dots) at the designated locations as an analog
    # to the star points on traditional rectangular gameboards.
    def _draw_star_points(self) -> None:
        r = round(7 * _spacing_scale(self._side_length))
        for ab in go3_board.star_points(self._side_length):
            cx, cy = self._get_x(ab), self._get_y(ab)
            self._canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
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
        scale = _spacing_scale(self._side_length)
        inner_r, outer_r = round(17 * scale), round(19 * scale)
        self._canvas.create_oval(cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r,
            fill=fill, outline=_STONE_EDGE_COLOR, width=2)
        self._canvas.create_oval(cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r,
            fill="", outline=_BOARD_COLOR, width=2)


    # # # # #     Private methods — event handlers     # # # # #

    # Passes the click event at (x,y) to the callback function provided
    # by go3.py or a test program.
    def _handle_click(self, event) -> None:
        pt = self._get_point(event.x, event.y)
        color = self._next_player
        if pt is not None and color is not None and pt in self._legal_moves:
            move: Stone = (pt, color)
            self._on_click(move)

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
        if pt is not None and pt in self._legal_moves:
            cx = self._get_x(pt)
            cy = self._get_y(pt)
            r = round(21 * _spacing_scale(self._side_length))
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
