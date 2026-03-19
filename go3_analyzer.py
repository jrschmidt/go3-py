# # # #    #   #   #   #   #     # # # #
# # #        go3_analyzer.py        # # #
# # # #    #   #   #   #   #     # # # #

# Analyzer module for Go3: finds allowable moves and
# determines move results.


from typing import TypedDict
from go3_board import Point, StoneColor
from go3_display import AnalysisDashboard


# # # # #     Type aliases     # # # # #

GroupId = int


# # # # #     Classes     # # # # #
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

    # Utility to generate a  new ID for a stone group.
    def get_new_group_id(self) -> GroupId:
        group_id = self._next_group_id
        self._next_group_id += 1
        return group_id


def init_analyzer(dashboard: AnalysisDashboard) -> Analyzer:
    return Analyzer(dashboard)
