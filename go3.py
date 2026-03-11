# # # #    #   #   #   #   #     # # # #
# # #         go3.py         # # #
# # # #    #   #   #   #   #     # # # #

# This is a Claude Code assisted python/Tkinter port
# of Go3. This is the main module.


from go3_board import RED, WHITE, BLUE, gameboard_points, Stones
from go3_display import display_init, run, place_stone
from go3_analyze import init_analyzer


# This function is the callback supplied to go3_display.py as
# the `on_click()` value when display_init is called .

def on_move(point: tuple[int, int]) -> None:
    print(point)


def main() -> None:
    anz = init_analyzer()
    stones: Stones = []

    # Temporary testing code:
    pts = list(gameboard_points())
    assert len(pts) == 91
    assert (1, 1) in pts
    assert (6, 11) in pts
    assert (1, 11) not in pts    # row 11 starts at col 6

    display_init(on_click=on_move)

    # Temporary stone placement for visual testing:
    place_stone((4, 4), RED)
    place_stone((9, 9), WHITE)
    place_stone((4, 6), BLUE)
    place_stone((2, 3), RED)
    place_stone((5, 9), WHITE)
    place_stone((3, 4), BLUE)

    run()


if __name__ == "__main__":
    main()
