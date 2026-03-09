from collections.abc import Iterator
from enum import Enum


Point = tuple[int, int]


class StoneColor(Enum):
    RED = "red"
    WHITE = "white"
    BLUE = "blue"

RED   = StoneColor.RED
WHITE = StoneColor.WHITE
BLUE  = StoneColor.BLUE


ROW_BEGIN_END: list[tuple[int, int]] = [
    (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11),
    (2, 11), (3, 11), (4, 11), (5, 11), (6, 11),
]


def is_valid_gameboard_point(point: Point) -> bool:
    a, b = point
    if not 1 <= b <= 11:
        return False
    start, end = ROW_BEGIN_END[b - 1]
    return start <= a <= end


def gameboard_points() -> Iterator[Point]:
    for b, (start, end) in enumerate(ROW_BEGIN_END, start=1):
        for a in range(start, end + 1):
            yield (a, b)
