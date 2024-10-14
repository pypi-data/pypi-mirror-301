"""
A fast script+module for finding points in a row on a 2D plane.
"""

import sys


def find_rows(coords: tuple[tuple[int, int]] | list[tuple[int, int]], row_size: int, steps: int = 1) -> tuple[tuple[int, int]]:
    """
    Find all rows of `row_size` points by checking from each point in 4 directions.
    right, top, top-right, and bottom+right.
    """
    if not isinstance(coords, tuple | list) or not all(isinstance(coord, tuple) for coord in coords):
        raise ValueError("coords should be a tuple/list of tuples [(x1, y1), (x2, y2), ...]")

    if not isinstance(row_size, int) or row_size < 2:
        raise ValueError("row_size should be an integer greater than 1")

    if not isinstance(steps, int) or steps < 1:
        raise ValueError("steps should be an integer greater than 0")

    coords_set = frozenset(coords)
    coords = list(coords_set)
    rows = set()
    walk = ((1, 0), (0, 1), (1, 1), (1, -1))
    for x, y in coords:
        for dx, dy in walk:
            if (x + (row_size - 1) * dx * steps, y + (row_size - 1) * dy * steps) not in coords_set:
                continue

            row = [(x + i * dx * steps, y + i * dy * steps) for i in range(row_size)]
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


def get_coordinates() -> tuple[tuple[int, int]]:
    """
    Get the coordinates from the command line arguments.
    """
    coords = []
    for value in sys.argv[3:]:
        try:
            x, y = map(int, value.split(","))
            coords.append((x, y))

        except ValueError:
            print(f"error: invalid coordinate: {value} (should be in the format: x,y)")
            sys.exit(1)

    return tuple(coords)


def main() -> None:
    """
    Entry point when run as a script.
    """
    if len(sys.argv) < 4:
        print("usage: rowfind.py <row_size> <steps> x1,y1 x2,y2 x3,y3 ...")
        sys.exit(1)

    try:
        row_size = int(sys.argv[1])
        steps = int(sys.argv[2])
        if row_size < 2 or steps < 1:
            raise ValueError

    except ValueError:
        print(f"error: invalid row_size/steps: row_size should be an integer greater than 1, steps should be an integer greater than 0")
        sys.exit(1)

    coords = get_coordinates()
    rows = find_rows(coords, row_size, steps)
    if not rows:
        print("No rows were found")
        sys.exit(0)

    print("\n".join(str(row) for row in rows))
    print(draw_graph(coords, rows))


if __name__ == "__main__":
    main()
