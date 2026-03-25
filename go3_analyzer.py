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


class StoneGroup(TypedDict):
    player: StoneColor
    stones: list[Point]
    clear_points: list[Point]


class Analyzer:
    def __init__(self, dashboard: AnalysisDashboard) -> None:
        self.groups: list[StoneGroup] = []
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

    def get_next_player(self) -> StoneColor:
        players = list(StoneColor)
        idx = players.index(self.next_player)
        next_player = players[(idx + 1) % len(players)]
        self.next_player = next_player
        return next_player


    def rebuild_groups(self) -> list[StoneGroup]:
        self.groups = []
        all_occupied = {pt for pt, _ in self.stones}

        for color in StoneColor:
            color_points = {pt for pt, c in self.stones if c == color}
            unvisited = set(color_points)

            while unvisited:
                start = next(iter(unvisited))
                visited: set[Point] = {start}
                queue: list[Point] = [start]
                while queue:
                    p = queue.pop()
                    for nb in adjacent_points(p):
                        if nb not in visited and nb in color_points:
                            visited.add(nb)
                            queue.append(nb)

                component = list(visited)
                clear_pts = list({
                    nb
                    for pt in component
                    for nb in adjacent_points(pt)
                    if nb not in all_occupied
                })

                group: StoneGroup = {
                    'player': color,
                    'stones': component,
                    'clear_points': clear_pts,
                }
                self.groups.append(group)
                unvisited -= visited

        return self.groups


    def analyze_move(self, move: Stone) -> GameState:
        stones = self.stones
        legal_moves = self.legal_moves

        # Increment next_player, save and return revised game state.
        next = self.get_next_player()

        self.legal_moves.discard(move[0])
        self.stones.append(move)

        self.rebuild_groups()

        # Capture any opposing groups with no liberties.
        played_color = move[1]
        captured: list[Point] = []
        for group in self.groups:
            if group['player'] != played_color and len(group['clear_points']) == 0:
                captured.extend(group['stones'])

        if captured:
            for pt in captured:
                self.stones = [(p, c) for p, c in self.stones if p != pt]
                self.legal_moves.append(pt)
            self.rebuild_groups()

        self._dashboard.printline(" ")
        self._dashboard.printline(f"You clicked {move[0]} {move[1].name}")
        self._dashboard.printline(f"number of stones on board: {len(self.stones)}")
        self._dashboard.printline(f"number of legal moves: {len(self.legal_moves)}")
        for group in self.groups:
            self._dashboard.printline(
                f"  {group['player'].name}: "
                f"{list(group['stones'][0])} "
                f"{len(group['stones'])} stones, "
                f"{len(group['clear_points'])} liberties"
            )

        state: GameState = {"next_player": next, "stones": stones, "legal_moves": legal_moves}
        return state



