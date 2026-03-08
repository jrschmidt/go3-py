import tkinter as tk


# Color constants

RED = "#cc3333"
WHITE = "#f0f0f0"
BLUE = "#5050cc"
APP_COLOR = "#CCCC99"
BOARD_COLOR = "#CC9933"
LINE_COLOR = "#000000"
BOARD_MARGIN_COLOR = "#000000"
STONE_EDGE_COLOR = "#000000"
GHOST = "#aaaaaa"


# Board geometry constants

Point = tuple[int, int]

STAR_POINTS: list[Point] = [ [3,3], [6,3], [3,6], [6,6], [9,6], [6,9], [9,9] ]

ROW_START = [1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6]
ROW_END   = [6, 7, 8, 9, 10, 11, 11, 11, 11, 11, 11]

W_E: list[tuple[Point, Point]] = [
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

SW_NE: list[tuple[Point, Point]] = [
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

NW_SE: list[tuple[Point, Point]] = [
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


# Coordinate transform functions

_HEX_VERTS = [(157,26),(443,26),(576,270),(443,514),(157,514),(25,270)]

def is_in_board_hex(x: int, y: int) -> bool:
    verts = _HEX_VERTS
    n = len(verts)
    for i in range(n):
        x1, y1 = verts[i]
        x2, y2 = verts[(i + 1) % n]
        if (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1) > 0:
            return False
    return True

def get_x(ab: Point) -> int: return 150 + 50 * ab[0] - 25 * ab[1]
def get_y(ab: Point) -> int: return 6 + 44 * ab[1]

def is_valid_gameboard_point(point: Point) -> bool:
    a, b = point
    return 1 <= b <= 11 and ROW_START[b - 1] <= a <= ROW_END[b - 1]

def get_point(x: int, y: int) -> Point | None:
    b = (y - 28) // 44 + 1
    a = (x - 125 + 25 * b) // 50
    if not is_valid_gameboard_point((a, b)):
        return None
    return (a, b)


# Drawing functions

def draw_base_hex(canvas: tk.Canvas) -> None:
    canvas.create_polygon(157, 26, 443, 26, 576, 270, 443, 514, 157, 514, 25, 270,
        fill=BOARD_COLOR, outline=BOARD_MARGIN_COLOR, width=5)

def draw_base_margin(canvas: tk.Canvas) -> None:
    canvas.create_polygon(163, 34, 437, 34, 567, 270, 437, 506, 163, 506, 33, 270,
        fill="", outline=BOARD_MARGIN_COLOR, width=3)

def draw_line(canvas: tk.Canvas, beg: Point, end: Point) -> None:
    canvas.create_line(get_x(beg), get_y(beg), get_x(end), get_y(end),
        fill=LINE_COLOR, width=3)

def draw_lines(canvas: tk.Canvas) -> None:
    for beg, end in W_E:   draw_line(canvas, beg, end)
    for beg, end in SW_NE: draw_line(canvas, beg, end)
    for beg, end in NW_SE: draw_line(canvas, beg, end)

def draw_star_points(canvas: tk.Canvas) -> None:
    for ab in STAR_POINTS:
        cx, cy = get_x(ab), get_y(ab)
        canvas.create_oval(cx - 7, cy - 7, cx + 7, cy + 7,
            fill=LINE_COLOR, outline=LINE_COLOR)

def draw_empty_board(canvas: tk.Canvas) -> None:
    draw_base_hex(canvas)
    draw_base_margin(canvas)
    draw_lines(canvas)
    draw_star_points(canvas)

def draw_stone(canvas: tk.Canvas, ab: Point, color: str) -> None:
    if not is_valid_gameboard_point(ab):
        raise ValueError(f"Point {ab} is not a valid gameboard position")
    cx, cy = get_x(ab), get_y(ab)
    canvas.create_oval(cx - 17, cy - 17, cx + 17, cy + 17,
        fill=color, outline=STONE_EDGE_COLOR, width=2)
    canvas.create_oval(cx - 19, cy - 19, cx + 19, cy + 19,
        fill="", outline=BOARD_COLOR, width=2)


# Starting code:

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Go3 Board")
    canvas = tk.Canvas(root, width=600, height=540, bg=APP_COLOR,
                       highlightthickness=2, highlightbackground="red")
    canvas.pack()

    draw_empty_board(canvas)

    hover_circle = None

    def clear_hover(event=None):
        global hover_circle
        if hover_circle is not None:
            canvas.delete(hover_circle)
            hover_circle = None
        canvas.config(cursor="")

    def on_mouse_move(event):
        global hover_circle
        clear_hover()
        pt = get_point(event.x, event.y)
        if pt is not None:
            cx = get_x(pt)
            cy = get_y(pt)
            r = 21
            hover_circle = canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                outline=GHOST, fill="", width=2
            )
        if is_in_board_hex(event.x, event.y):
            canvas.config(cursor="none")
        else:
            canvas.config(cursor="")

    canvas.bind("<Button-1>", lambda e: print(get_point(e.x, e.y)))
    canvas.bind("<Motion>", on_mouse_move)
    canvas.bind("<Leave>", clear_hover)


    # Temporary testing code:

    draw_stone(canvas, (4, 4), RED)
    draw_stone(canvas, (9, 9), WHITE)
    draw_stone(canvas, (4, 6), BLUE)
    draw_stone(canvas, (2, 3), RED)
    draw_stone(canvas, (5, 9), WHITE)
    draw_stone(canvas, (3, 4), BLUE)


    root.mainloop()
