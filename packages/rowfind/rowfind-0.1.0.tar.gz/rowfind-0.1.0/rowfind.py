"""
A simple script+module to find points in a row on a 2D plane.
"""

import sys
import itertools


def check(coords: tuple[tuple[int, int], ...]) -> bool:
    """
    Check if the given coordinates form a row.
    """
    Xs, Ys = zip(*coords)

    if len(set(Xs)) == 1 and sorted(Ys) == list(range(min(Ys), max(Ys) + 1)):
        return True

    if len(set(Ys)) == 1 and sorted(Xs) == list(range(min(Xs), max(Xs) + 1)):
        return True

    if len(set(x - y for x, y in coords)) == 1 and sorted(Xs) == list(range(min(Xs), max(Xs) + 1)):
        return True

    if len(set(x + y for x, y in coords)) == 1 and sorted(Xs) == list(range(min(Xs), max(Xs) + 1)):
        return True

    return False


def find_rows(coords: list[tuple[int, int]], row_size: int) -> tuple[tuple[int, int]]:
    """
    Find all possible combinations of `row_size` points and check each
    combination with check()
    """
    rows = []
    for combination in itertools.combinations(coords, row_size):
        if check(combination):
            rows.append(combination)

    return tuple(rows)


def get_coordinates() -> list[tuple[int, int]]:
    """
    Get the coordinates from the command line arguments.
    """
    coords = []
    for value in sys.argv[2:]:
        try:
            x, y = map(int, value.split(","))
            coords.append((x, y))

        except ValueError:
            print(f"error: invalid coordinate: {value} (should be in the format: x,y)")
            sys.exit(1)

    coords = list(set(coords))
    return coords


def draw_graph(coords: list[tuple[int, int]], rows: tuple[tuple[int, int]]):
    """
    Draw an ASCII graph with the given coordinates. Coordinates that form
    a row are marked with 'X' while the rest are marked with 'O'.
    """
    min_x, max_x = min(x for x, y in coords), max(x for x, y in coords)
    min_y, max_y = min(y for x, y in coords), max(y for x, y in coords)

    grid = [[" ." for _ in range(min_x, max_x + 1)] for _ in range(min_y, max_y + 1)]

    for x, y in coords:
        grid[y - min_y][x - min_x] = " O"

    for row in rows:
        for x, y in row:
            grid[y - min_y][x - min_x] = " X"

    graph = []
    for row in reversed(grid):
        graph.append("".join(row))

    return "\n".join(graph)


def main():
    if len(sys.argv) < 4:
        print("usage: rowfind.py <row_size> x1,y1 x2,y2 x3,y3 ...")
        sys.exit(1)

    try:
        row_size = int(sys.argv[1])

    except ValueError:
        print(f"error: invalid row size: {sys.argv[1]} (should be an integer)")
        sys.exit(1)

    coords = get_coordinates()
    rows = find_rows(coords, row_size)
    print("\n".join(str(row) for row in rows))
    print(draw_graph(coords, rows))


if __name__ == "__main__":
    main()
