# # # #    #   #   #   #   #     # # # #
# # #        go3_analyze.py        # # #
# # # #    #   #   #   #   #     # # # #

# Analyzer module for Go3: finds allowable moves and
# determines move results.


from typing import TypedDict
from go3_board import Point, StoneColor


# Type aliases

GroupId = int


class StoneGroup(TypedDict):
    id: GroupId
    player: StoneColor
    stones: list[Point]
    clear_points: list[Point]
    neighbors: list[GroupId]


class Analyzer:
    def __init__(self) -> None:
        self.groups: list[StoneGroup] = []
        self._next_group_id: int = 1

    def get_new_group_id(self) -> GroupId:
        group_id = self._next_group_id
        self._next_group_id += 1
        return group_id


def init_analyzer() -> Analyzer:
    return Analyzer()
