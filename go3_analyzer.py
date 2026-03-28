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


class SingletonEye(TypedDict):
    point: Point
    groups: list[StoneGroup]


class Analyzer:
    def __init__(self, dashboard: AnalysisDashboard) -> None:
        self._dashboard = dashboard
        self.next_player: StoneColor = RED
        self.stones: Stones = []


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


    def determine_stone_groups(self, stones: Stones) -> list[StoneGroup]:
        groups: list[StoneGroup] = []
        all_occupied = {pt for pt, _ in stones}

        for color in StoneColor:
            color_points = {pt for pt, c in stones if c == color}
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
                groups.append(group)
                unvisited -= visited

        return groups


    def find_singleton_eyes(self, stones: Stones, groups: list[StoneGroup]) -> list[SingletonEye]:
        all_occupied = {pt for pt, _ in stones}
        eye_to_groups: dict[Point, list[StoneGroup]] = {}

        for group in groups:
            for pt in group['clear_points']:
                neighbors = adjacent_points(pt)
                if all(nb in all_occupied for nb in neighbors):
                    if pt not in eye_to_groups:
                        eye_to_groups[pt] = []
                    eye_to_groups[pt].append(group)

        singleton_eyes: list[SingletonEye] = [
            {'point': pt, 'groups': grps}
            for pt, grps in eye_to_groups.items()
        ]
        return singleton_eyes


    def compute_legal_moves(self, stones: Stones, singleton_eyes: list[SingletonEye], next_player: StoneColor) -> set[Point]:
        all_occupied = {pt for pt, _ in stones}
        eye_points = {eye['point'] for eye in singleton_eyes}

        legal_moves = all_gameboard_points() - all_occupied - eye_points

        for eye in singleton_eyes:
            pt = eye['point']
            for group in eye['groups']:
                # Opposing group whose only liberty is this point (capturing move).
                if group['player'] != next_player and len(group['clear_points']) == 1:
                    legal_moves.add(pt)
                    break
                # Own group adjacent to the point that still has another liberty.
                if group['player'] == next_player and len(group['clear_points']) >= 2:
                    legal_moves.add(pt)
                    break

        return legal_moves


    def analyze_move(self, move: Stone) -> GameState:
        stones: Stones = self.stones
        next_player: StoneColor = self.get_next_player()

        stones.append(move)
        groups = self.determine_stone_groups(stones)

        # Capture any opposing groups with no liberties.
        played_color = move[1]
        captured: list[Point] = []
        for group in groups:
            if group['player'] != played_color and len(group['clear_points']) == 0:
                captured.extend(group['stones'])

        if captured:
            stones = [(p, c) for p, c in stones if p not in captured]
            groups = self.determine_stone_groups(stones)

        singleton_eyes = self.find_singleton_eyes(stones, groups)
        legal_moves = self.compute_legal_moves(stones, singleton_eyes, next_player)

        self.next_player = next_player
        self.stones = stones

        self._dashboard.printline(" ")
        self._dashboard.printline(f"You clicked {move[0]} {move[1].name}")
        self._dashboard.printline(f"number of stones on board: {len(stones)}")
        self._dashboard.printline(f"number of legal moves: {len(legal_moves)}")
        for group in groups:
            self._dashboard.printline(
                f"  {group['player'].name}: "
                f"{list(group['stones'][0])} "
                f"{len(group['stones'])} stones, "
                f"{len(group['clear_points'])} liberties"
            )
        self._dashboard.printline(f"singleton eyes: {len(singleton_eyes)}")
        for eye in singleton_eyes:
            group_descs = [f"{g['player'].name}@{list(g['stones'][0])}" for g in eye['groups']]
            self._dashboard.printline(f"  eye {list(eye['point'])}: {', '.join(group_descs)}")

        state: GameState = {"next_player": next_player, "stones": stones, "legal_moves": legal_moves}
        return state



