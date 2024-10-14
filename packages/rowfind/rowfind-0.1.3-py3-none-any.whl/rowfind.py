"""
A fast script+module for finding points in a row on a 2D plane.
"""

import sys


def find_rows(coords: tuple[tuple[int, int]] | list[tuple[int, int]], row_size: int, steps: int | tuple[int] | list[int] | None = 1) -> tuple[tuple[int, int]]:
    """
    Find all rows of `row_size` points by checking from each point in 4 directions.
    right, top, top-right, and bottom-right.
    """
    if not isinstance(coords, tuple | list) or not all(isinstance(coord, tuple) for coord in coords):
        raise ValueError("coords should be a tuple/list of tuples [(x1, y1), (x2, y2), ...]")

    if not isinstance(row_size, int) or row_size < 2:
        raise ValueError("row_size should be an integer greater than 1")

    if (steps is not None and not isinstance(steps, int) and not
       (isinstance(steps, tuple | list) or all(isinstance(step, int) for step in steps))):
        raise ValueError("steps should be an integer, a tuple/list of integers, or None")

    coords_set = frozenset(coords)
    coords = list(coords_set)
    rows = set()
    if not steps:
        steps = range(1, len(coords))

    elif isinstance(steps, int):
        steps = (steps,)

    walk = ((1, 0), (0, 1), (1, 1), (1, -1))
    for x, y in coords:
        for dx, dy in walk:
            for step in steps:
                if (x + (row_size - 1) * dx * step, y + (row_size - 1) * dy * step) not in coords_set:
                    continue

                row = [(x + i * dx * step, y + i * dy * step) for i in range(row_size)]
                if all(point in coords_set for point in row):
                    rows.add(tuple(row))

    return tuple(rows)


def draw_graph(coords: tuple[tuple[int, int]] | list[tuple[int, int]], rows: tuple[tuple[int, int]]) -> str:
    """
    Draw an ASCII graph with the given coordinates.
    Coordinates that form a row are marked with 'X' while the rest are marked with 'O'.
    """
    if not isinstance(coords, tuple | list) or not all(isinstance(coord, tuple) for coord in coords):
        raise ValueError("coords should be a tuple/list of tuples [(x1, y1), (x2, y2), ...]")

    if not isinstance(rows, tuple) or not all(isinstance(row, tuple) for row in rows):
        raise ValueError("rows should be a tuple of tuples (((x1, y1), (x2, y2)), ...)")

    coords_set = frozenset(coords)
    coords = list(coords_set)
    rows_set = frozenset(coord for row in rows for coord in row)
    min_x, max_x = min(x for x, y in coords), max(x for x, y in coords)
    min_y, max_y = min(y for x, y in coords), max(y for x, y in coords)
    return "\n".join(
        "".join(
            " X" if (x, y) in rows_set else
            " O" if (x, y) in coords_set else
            " ."
            for x in range(min_x, max_x + 1)
        )
        for y in range(max_y, min_y - 1, -1)
    )
