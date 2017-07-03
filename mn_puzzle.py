from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    # implement __eq__ and __str__
    # __repr__ is up to you

    def __eq__(self, other):
        """
        Return whether MNPuzzle self is equivalent to other.

        @type self: MNPuzzle
        @type other: MNPuzzle | Any
        @rtype: bool

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> target_grid1 = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid1 = (("1", "2", "3"), ("4", "5", "*"))
        >>> mn1 = MNPuzzle(start_grid1, target_grid1)
        >>> mn.__eq__(mn1)
        False
        """
        return (type(other) == type(self) and
                self.from_grid == other.from_grid and
                self.to_grid == other.to_grid)

    def __str__(self):
        """
        Return a human-readable string representation of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: str

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> print(mn)
        *|2|3
        1|4|5
        ->
        1|2|3
        4|5|*
        """
        # string representation of from_grid
        total = []
        result = ""
        for i in self.from_grid:
            for j in i:
                result += j + "|"
            total += [result[:-1]]
            result = ""
        tot_result = ""
        for i in total:
            tot_result += i + '\n'
        # string representation of to_grid
        total1 = []
        result1 = ""
        for i in self.to_grid:
            for j in i:
                result1 += j + "|"
            total1 += [result1[:-1]]
            result1 = ""
        tot_result1 = ""
        for i in total1:
            tot_result1 += i + '\n'
        return tot_result[:-1] + "\n->\n" + tot_result1[:-1]

    # override extensions
    # legal extensions are configurations that can be reached by swapping one
    # symbol to the left, right, above, or below "*" with "*"
    def extensions(self):
        """
        Return a list of extensions that are one step away from the current \
        configuration of self.

        @type self: MNPuzzle
        @rtype: list[MNPuzzle]
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> mn.extensions()
        [MNPuzzle((("1", "2", "3"), ("*", "4", "5")),\
        (("1", "2", "3"), ("4", "5", "*")), \
        MNPuzzle(((21", "*", "3"), ("1", "4", "5")), \
        (("1", "2", "3"), ("4", "5", "*"))]
        """
        result = []
        # choose an element from row i and column j which is an empty space
        for i in range(len(self.from_grid)):
            for j in range(len(self.from_grid[i])):
                if self.from_grid[i][j] == "*":
                    # find all possibilities of moving and add them to the list
                    if j + 1 < len(self.from_grid[i]):
                        new_from_row = list(self.from_grid[i])
                        new_from_row[j] = new_from_row[j+1]
                        new_from_row[j+1] = "*"
                        new_row = tuple(new_from_row)
                        new_from = tuple(self.from_grid[:i]) + (new_row,) + \
                            tuple(self.from_grid[i+1:])
                        new = MNPuzzle(new_from, self.to_grid)
                        result += [new]
                    if j - 1 >= 0:
                        new_from_row = list(self.from_grid[i])
                        new_from_row[j] = new_from_row[j-1]
                        new_from_row[j-1] = "*"
                        new_row = tuple(new_from_row)
                        new_from = tuple(self.from_grid[:i]) + (new_row,) + \
                            tuple(self.from_grid[i+1:])
                        new = MNPuzzle(new_from, self.to_grid)
                        result += [new]
                    if i + 1 < len(self.from_grid):
                        new_from_rowi = list(self.from_grid[i])
                        new_from_rowi1 = list(self.from_grid[i])
                        new_from_rowi[j] = new_from_rowi1[j]
                        new_from_rowi1[j] = "*"
                        new_rowi = tuple(new_from_rowi)
                        new_rowi1 = tuple(new_from_rowi1)
                        new_from = tuple(self.from_grid[:i]) + (new_rowi,) + \
                            (new_rowi1,) + tuple(self.from_grid[i+2:])
                        new = MNPuzzle(new_from, self.to_grid)
                        result += [new]
                    if i - 1 >= 0:
                        new_from_rowi = list(self.from_grid[i])
                        new_from_rowi1 = list(self.from_grid[i])
                        new_from_rowi[j] = new_from_rowi1[j]
                        new_from_rowi1[j] = "*"
                        new_rowi = tuple(new_from_rowi)
                        new_rowi1 = tuple(new_from_rowi1)
                        new_from = tuple(self.from_grid[:i-1]) + \
                            (new_rowi1, new_rowi) + tuple(self.from_grid[i+1:])
                        new = MNPuzzle(new_from, self.to_grid)
                        result += [new]
        return result

    # override is_solved
    # a configuration is solved when from_grid is the same as to_grid

    def is_solved(self):
        """
        Return True if the MNPuzzle is in solved configuration \
        i.e. when from_grid equals to to_grid and False otherwise.

        @type self: MNPuzzle
        @rtype: bool

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> mn.is_solved()
        False
        >>> target_grid1 = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid1 = (("1", "2", "3"), ("4", "5", "*"))
        >>> mn1 = MNPuzzle(start_grid1, target_grid1)
        >>> mn1.is_solved()
        True
        """
        return self.from_grid == self.to_grid

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
