A simple script+module to find points in a row on a 2D plane.

Usecases are almost none, but I was bored.
Can be used for tic-tac-toe ig.

Script usage:
    $ rowfind <row_size> x1,y1 x2,y2 x3,y3 ...

Module usage:
    import rowfind
    coords = [(0, 0), (1, 1), (2, 2), (2, 3), (2, 4), (5, 5), (4, 4)]
    row_size = 3
    rows = rowfind.find_rows(coords, row_size)

    # Where `coords` is a list of (x, y) coordinates and `row_size` is
    # the number of points in a row to find.
    # The return value is a tuple of tuples, where each tuple is a group
    # of points that form a row.

    # To visualize the results:
    print("\n".join(str(row) for row in rows))
    graph = rowfind.draw_graph(coords, rows)
    print(graph)

Output:
    ((0, 0), (1, 1), (2, 2))
    ((2, 2), (2, 3), (2, 4))
    . . . . . O
    . . X . O .
    . . X . . .
    . . X . . .
    . X . . . .
    X . . . . .

Build as wheel:
    $ poetry build -f wheel -o dist
