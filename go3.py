from go3_board import RED, WHITE, BLUE, gameboard_points
from go3_display import Go3Display


def on_move(point: tuple[int, int]) -> None:
    print(point)


def main() -> None:
    # Temporary testing code:
    pts = list(gameboard_points())
    assert len(pts) == 91
    assert (1, 1) in pts
    assert (6, 11) in pts
    assert (1, 11) not in pts    # row 11 starts at col 6

    display = Go3Display(on_click=on_move)

    # Temporary stone placement for visual testing:
    display.draw_stone((4, 4), RED)
    display.draw_stone((9, 9), WHITE)
    display.draw_stone((4, 6), BLUE)
    display.draw_stone((2, 3), RED)
    display.draw_stone((5, 9), WHITE)
    display.draw_stone((3, 4), BLUE)

    display.run()


if __name__ == "__main__":
    main()
