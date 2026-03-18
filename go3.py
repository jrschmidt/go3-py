# # # #    #   #   #   #   #     # # # #
# # #         go3.py         # # #
# # # #    #   #   #   #   #     # # # #

# This is a Claude Code assisted python/Tkinter port
# of Go3. This is the main module.


from go3_board import RED, WHITE, BLUE, gameboard_points, Stones
from go3_display import Go3Display
from go3_analyze import init_analyzer


# This function is the callback supplied to go3_display.py as
# the `on_click()` value when the display is instantiated.
def on_move(point: tuple[int, int]) -> None:
    print(point)


def main() -> None:
    anz = init_analyzer()
    board: Stones = []

    display = Go3Display(on_click=on_move)

    # # Temporary stone placement for visual testing:
    stones: Stones = [
        ((4, 4), RED),
        ((9, 9), WHITE),
        ((4, 6), BLUE),
        ((2, 3), RED),
        ((5, 9), WHITE),
        ((3, 4), BLUE),
    ]
    display.draw_stones(stones)

    display.start_loop()


if __name__ == "__main__":
    main()
