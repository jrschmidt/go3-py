# # # #    #   #   #   #   #     # # # #
# # #        run_tests.py          # # #
# # # #    #   #   #   #   #     # # # #

# This module is scaffolded with a stripped down version of the
# main app module go3.py. Additional code can be added or removed
# to execute testing as desired.

# These two lines are added to enable us to execute this file from project
# root with `python3 test/run_tests.py`.
import sys, os, time, tkinter as tk, tkinter as tk
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from go3_board import RED, WHITE, BLUE, gameboard_points, Stones
from go3_display import display_init, run, place_stone, remove_stone
from go3_analyze import init_analyzer

from test_points import test_set_3 as test_points


# This function is the callback supplied to go3_display.py as
# the `on_click()` value when display_init is called .
def on_move(point: tuple[int, int]) -> None:
    print(point)


def main() -> None:
    anz = init_analyzer()
    board: Stones = []

    display_init(on_click=on_move)

    for move in test_points:
        place_stone(move[0], move[1])

    for i, move in enumerate(test_points):
        tk._default_root.after((i + 1) * 1000, lambda m=move: remove_stone(m[0]))

    run()


if __name__ == "__main__":
    main()
