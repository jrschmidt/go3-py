# # # #    #   #   #   #   #     # # # #
# # #         go3.py         # # #
# # # #    #   #   #   #   #     # # # #

# This is a Claude Code assisted python/Tkinter port
# of Go3. This is the main module.


from go3_board import RED, WHITE, BLUE, gameboard_points, Stones
from go3_display import Go3Display, GameDashboard
from go3_analyzer import init_analyzer

board: Stones = []

display = Go3Display(on_click=None)   # (on_click defined below)
game_gui = display.game_dashboard
analyzer = init_analyzer(display.analysis_dashboard)


# This function is the callback supplied to go3_display.py as
# the `on_click()` value when the display is instantiated.
def on_move(point: tuple[int, int]) -> None:
    # Temporary stone placement for visual testing:
    stones: Stones = [
        ((4, 4), RED),
        ((9, 9), WHITE),
        ((4, 6), BLUE),
        ((2, 3), RED),
        ((5, 9), WHITE),
        ((3, 4), BLUE),
    ]
    display.draw_stones(stones)


display._on_click = on_move   # (hook up the callback after on_move is defined)

display.start_loop()
