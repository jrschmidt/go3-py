import tkinter as tk

# Board geometry constants

Point = tuple[int, int]

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

def get_x(ab: Point) -> int: return 150 + 50 * ab[0] - 25 * ab[1]
def get_y(ab: Point) -> int: return 6 + 44 * ab[1]

# Drawing functions

def draw_base_hex(canvas: tk.Canvas) -> None:
    canvas.create_polygon(157, 26, 443, 26, 576, 270, 443, 514, 157, 514, 25, 270,
        fill="#cc9933", outline="#000000", width=5)

def draw_base_margin(canvas: tk.Canvas) -> None:
    canvas.create_polygon(163, 34, 437, 34, 567, 270, 437, 506, 163, 506, 33, 270,
        fill="", outline="#000000", width=3)

def draw_line(canvas: tk.Canvas, beg: Point, end: Point) -> None:
    canvas.create_line(get_x(beg), get_y(beg), get_x(end), get_y(end),
        fill="#000000", width=3)

def draw_lines(canvas: tk.Canvas) -> None:
    for beg, end in W_E:   draw_line(canvas, beg, end)
    for beg, end in SW_NE: draw_line(canvas, beg, end)
    for beg, end in NW_SE: draw_line(canvas, beg, end)

def draw(canvas: tk.Canvas) -> None:
    draw_base_hex(canvas)
    draw_base_margin(canvas)
    draw_lines(canvas)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Go3 Board")
    canvas = tk.Canvas(root, width=600, height=540, bg="#cccc99",
                       highlightthickness=2, highlightbackground="red")
    canvas.pack()
    draw(canvas)
    root.mainloop()
