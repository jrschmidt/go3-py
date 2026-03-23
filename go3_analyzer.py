# # # #    #   #   #   #   #     # # # #
# # #        go3_analyzer.py        # # #
# # # #    #   #   #   #   #     # # # #

# Analyzer module for Go3: finds allowable moves and
# determines move results.


from typing import TypedDict

from go3_board import Point, StoneColor, Stone, Stones, RED, WHITE, BLUE
from go3_board import GameState, all_gameboard_points, adjacent_points, are_adjacent
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
        next_player = players[(idx + 1) % len(players)]
        self.next_player = next_player
        return next_player


    # # Clauded insisted on including this method when we ported adjancency methods
    # # from go3.rb. Leave it alone until we need it or want to change it.
    # def find_group(self, start: Point, color: StoneColor) -> list[Point]:
    #     stone_points = {pt for pt, c in self.stones if c == color}
    #     visited, queue = {start}, [start]
    #     while queue:
    #         p = queue.pop()
    #         for nb in adjacent_points(p):
    #             if nb not in visited and nb in stone_points:
    #                 visited.add(nb)
    #                 queue.append(nb)
    #     return list(visited)


    def analyze_move(self, move: Stone) -> GameState:
        self._dashboard.printline(f"You clicked {move[0]} {move[1].name}")

        stones = self.stones
        legal_moves = self.legal_moves

        # Increment next_player, save and return revised game state.
        next = self.get_next_player()

        self.legal_moves.discard(move[0])
        self.stones.append(move)

        state: GameState = {"next_player": next, "stones": stones, "legal_moves": legal_moves}
        return state



