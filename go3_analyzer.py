# # # #    #   #   #   #   #     # # # #
# # #        go3_analyzer.py        # # #
# # # #    #   #   #   #   #     # # # #

# Analyzer module for Go3: finds allowable moves and
# determines move results.


from typing import TypedDict

from go3_board import Point, StoneColor, Stone, Stones, RED, WHITE, BLUE
from go3_board import GameState, all_gameboard_points
from go3_display import AnalysisDashboard


# # # # #     Types     # # # # #

GroupId = int


class StoneGroup(TypedDict):
    id: GroupId
    player: StoneColor
    stones: list[Point]
    clear_points: list[Point]
    neighbors: list[GroupId]


class Analyzer:
    def __init__(self, dashboard: AnalysisDashboard) -> None:
        self.groups: list[StoneGroup] = []
        self._next_group_id: int = 1
        self._dashboard = dashboard
        self.next_player: StoneColor = RED
        self.stones: Stones = []
        self.legal_moves: list[Point] = all_gameboard_points()


# # # # #     Methods     # # # # #

    def get_initial_game_state(self) -> GameState:
        state: GameState = {
            "next_player": RED,
            "stones": [],
            "legal_moves": all_gameboard_points()
        }
        return state

    # Utility to generate a  new ID for a stone group.
    def get_new_group_id(self) -> GroupId:
        group_id = self._next_group_id
        self._next_group_id += 1
        return group_id

    def get_next_player(self) -> StoneColor:
        players = list(StoneColor)
        idx = players.index(self.next_player)
        return players[(idx + 1) % len(players)]


    def analyze_move(self, move: Stone) -> GameState:
        self._dashboard.printline(f"You clicked {move[0]} {move[1].name}")
        next = self.get_next_player()

        # TEMP #
        # stones[] and legal_moves[] will be changed as required when this method is fully implemented.
        stones = self.stones
        legal_moves = self.legal_moves
        # TEMP #

        state: GameState = {"next_player": next, "stones": stones, "legal_moves": legal_moves}
        self._dashboard.printline(f"next_player (from state) = {state["next_player"].name}")
        return state



