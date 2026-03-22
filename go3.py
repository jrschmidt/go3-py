# # # #    #   #   #   #   #     # # # #
# # #         go3.py         # # #
# # # #    #   #   #   #   #     # # # #

# This is a Claude Code assisted python/Tkinter port
# of Go3. This is the main module.


from go3_board import RED, WHITE, BLUE, gameboard_points, Point, Stone, Stones, GameState
from go3_display import Go3Display
from go3_analyzer import Analyzer

display = Go3Display(on_click=None)   # (on_click defined below)
analyzer = Analyzer(display.analysis_dashboard)


# After recieving a response to a move from the analysis module, this
# function forwards the results to the display to reflect the changes
# in the gui and prompt the user for the next move.
def forward_state_changes(state: GameState) -> None:
    display.respond_to_state_change(state)


# This function is the callback supplied to go3_display.py as
# the `on_click()` value when the display is instantiated.
# 
# After sending the move data to the analyzer (go3_analyzer.py),
# the resulting changes are forwarded to the display (go3_display.py).
def on_move(point: Point) -> None:
    move: Stone = (point, BLUE)
    state: GameState = analyzer.analyze_move(move)
    forward_state_changes(state)


init_state = analyzer.get_initial_game_state()
forward_state_changes(init_state)

display._on_click = on_move   # (hook up the callback after on_move is defined)

display.start_loop()
