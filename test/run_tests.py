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


from go3_board import RED, WHITE, BLUE, Stones
from go3_display import Go3Display, GameDashboard
from go3_analyze import init_analyzer

from test_points import test_set_0 as test_points_0
from test_points import test_set_1 as test_points_1
from test_points import test_set_2 as test_points_2
from test_points import test_set_3 as test_points_3


test_sets = [test_points_0, test_points_1, test_points_2, test_points_3]
ts_i = -1


def next_test_set():
    global ts_i

    ts_i = ts_i + 1 if ts_i < len(test_sets) - 1 else 0
    return test_sets[ts_i]


###########################################################
###########################################################

board: Stones = []

display = Go3Display(on_click=None)   # on_click defined below
game_dash = display.game_dashboard
anz = init_analyzer(display.analysis_dashboard)


# This function is the callback supplied to go3_display.py as
# the `on_click()` value when the display is instantiated.
def on_move(point: tuple[int, int]) -> None:
    set = next_test_set()
    display.draw_stones(set)


display._on_click = on_move   # wire callback after on_move is defined

display.start_loop()


###########################################################
###########################################################


# This function is the callback supplied to go3_display.py as
# the `on_click()` value when the display is instantiated.
# def on_move(point: tuple[int, int]) -> None:
#     global display

#     # print(point)
#     set = next_test_set()
#     display.draw_stones(set)
