from puzzle import Puzzle
from copy import deepcopy


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    # implement __eq__, __str__ methods
    # __repr__ is up to you

    def __eq__(self, other):
        """
        Return whether GridPegSolitairePuzzle self is equivalent to other.

        @type self: GridPegSolitairePuzzle
        @type other: GridPegSolitairePuzzle | Any
        @rtype: bool

        >>> grid = [["*", "*", "*", "*", "*"], \
        ["*", "*", "*", "*", "*"], \
        ["*", "*", "*", "*", "*"], \
        ["*", "*", ".", "*", "*"], \
        ["*", "*", "*", "*", "*"]]
        >>> s1 = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> grid1 = [["*", "*", "*", "*", "*"], \
        ["*", "*", "*", "*", "*"], \
        ["*", "*", "*", "*", "*"], \
        ["*", "*", ".", "*", "*"], \
        ["*", "*", "*", "*", "*"]]
        >>> s2 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> s1.__eq__(s2)
        True
        >>> grid2 = [[".", ".", ".", ".", "."], \
        [".", ".", ".", ".", "."], \
        [".", ".", ".", ".", "."], \
        [".", ".", ".", ".", "."], \
        [".", ".", "*", ".", "."]]
        >>> s3 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> s1.__eq__(s3)
        False
        """
        return ((type(other) == type(self)) and
                (self._marker == other._marker) and
                (self._marker_set == other._marker_set))

    def __str__(self):
        """
        Return a human-readable string representation of \
        GridPegSolitairePuzzle self.

        @type self: GridPegSolitairePuzzle
        @rtype: str

        >>> grid2 = [[".", ".", "*", ".", "."], \
        [".", ".", ".", ".", "."], \
        [".", ".", ".", ".", "."], \
        [".", ".", "*", ".", "."], \
        [".", ".", "*", ".", "."]]
        >>> s3 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> print(s3)
        .|.|*|.|.
        .|.|.|.|.
        .|.|.|.|.
        .|.|*|.|.
        .|.|*|.|.
        """
        total = []
        result = ""
        # make a string representation of each row
        for i in self._marker:
            for j in i:
                result += j + "|"

            total += [result[:-1]]
            result = ""
        # between each row leave blank space
        tot_result = ""
        for i in total:
            tot_result += i + '\n'
        return tot_result[:-1]

    # override extensions
    # legal extensions consist of all configurations that can be reached by
    # making a single jump from this configuration

    def extensions(self):
        """
        Return a list of extensions that are one step away from the \
        current configuration.

        @type self: GridPegSolitairePuzzle
        @rtype: list[GridPegSolitairePuzzle]

        >>> grid = [["*", "*", "*", "*", "*"], \
        ["*", "*", "*", "*", "*"], \
        ["*", "*", "*", "*", "*"], \
        ["*", "*", ".", "*", "*"], \
        ["*", "*", "*", "*", "*"]]
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> gpsp.extensions()
        [GridPegSolitairePuzzle(\
        [["*", "*", "*", "*", "*"], \
        ["*", "*", ".", "*", "*"], \
        ["*", "*", ".", "*", "*"], \
        ["*", "*", "*", "*", "*"], \
        ["*", "*", "*", "*", "*"]], {"*", ".", "#"}), \
        GridPegSolitairePuzzle(\
        [["*", "*", "*", "*", "*"], \
        ["*", "*", "*", "*", "*"], \
        ["*", "*", "*", "*", "*"], \
        [".", ".", "*", "*", "*"], \
        ["*", "*", "*", "*", "*"]], {"*", ".", "#"}), \
        GridPegSolitairePuzzle(\
        [["*", "*", "*", "*", "*"], \
        ["*", "*", "*", "*", "*"], \
        ["*", "*", "*", "*", "*"], \
        ["*", "*", "*", ".", "."], \
        ["*", "*", "*", "*", "*"]], {"*", ".", "#"})
        """
        result = []
        # choose an item with column j and row i
        for i in range(len(self._marker)):
            for j in range(len(self._marker[i])):
                # make sure that this item is peg
                if self._marker[i][j] == "*":
                    # look at all choices where it can be moved and add all
                    # possible extensions to the list
                    if i >= 2 and self._marker[i - 1][j] == "*" \
                            and self._marker[i - 2][j] == ".":
                        new_marker = deepcopy(self._marker)
                        new_marker[i][j] = "."
                        new_marker[i - 1][j] = "."
                        new_marker[i - 2][j] = "*"
                        new = GridPegSolitairePuzzle(new_marker,
                                                     self._marker_set)
                        result += [new]

                    if (i + 2 < len(self._marker)) and \
                            (self._marker[i + 1][j] == "*") and \
                            (self._marker[i + 2][j] == "."):
                        new_marker = deepcopy(self._marker)
                        new_marker[i][j] = "."
                        new_marker[i + 1][j] = "."
                        new_marker[i + 2][j] = "*"
                        new = GridPegSolitairePuzzle(new_marker,
                                                     self._marker_set)
                        result += [new]
                    if (j + 2 < len(self._marker[i])) and \
                            (self._marker[i][j + 1] == "*") \
                            and (self._marker[i][j + 2] == "."):
                        new_marker = deepcopy(self._marker)
                        new_marker[i][j] = "."
                        new_marker[i][j + 1] = "."
                        new_marker[i][j + 2] = "*"
                        new1 = GridPegSolitairePuzzle(new_marker,
                                                      self._marker_set)
                        result += [new1]

                    if j - 2 >= 0 and self._marker[i][j - 1] == "*" \
                            and self._marker[i][j - 2] == ".":
                        new_marker = deepcopy(self._marker)
                        new_marker[i][j] = "."
                        new_marker[i][j - 1] = "."
                        new_marker[i][j - 2] = "*"
                        new = GridPegSolitairePuzzle(new_marker,
                                                     self._marker_set)
                        result += [new]

        return result

    # override is_solved
    # A configuration is solved when there is exactly one "*" left
    def is_solved(self):
        """
        Return True if exactly one peg is left and False otherwise.

        @type self: GridPegSolitairePuzzle
        @rtype: bool

        >>> grid = [["*", "*", "*", "*", "*"], \
        ["*", "*", "*", "*", "*"], \
        ["*", "*", "*", "*", "*"], \
        ["*", "*", ".", "*", "*"], \
        ["*", "*", "*", "*", "*"]]
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> gpsp.is_solved()
        False
        >>> grid2 = [[".", ".", ".", ".", "."], \
        [".", ".", ".", ".", "."], \
        [".", ".", ".", ".", "."], \
        [".", ".", ".", ".", "."], \
        [".", ".", "*", ".", "."]]
        >>> gpsp1 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> gpsp1.is_solved()
        True
        """
        result = ""
        for i in self._marker:
            for j in i:
                if j == "*":
                    result += j
        return result == "*"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
