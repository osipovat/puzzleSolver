from puzzle import Puzzle


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

        # implement __eq__ and __str__
        # __repr__ is up to you

    def __eq__(self, other):
        """
        Return whether WordLadderPuzzle self is equivalent to other.

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle | Any
        @rtype: bool

        >>> w1 = WordLadderPuzzle("same", "cost", {"some", "came", "lame"})
        >>> w2 = WordLadderPuzzle("same", "cost", {"some", "came", "lame"})
        >>> w1.__eq__(w2)
        True
        """
        return ((type(other) == type(self)) and
                (self._from_word == other._from_word) and
                (self._to_word == other._to_word) and
                (self._word_set == other._word_set))

    def __str__(self):
        """
        Return a human-readable string representation of \
        WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype: str

        >>> w = WordLadderPuzzle("same", "cost", {"some", "came", "lame"})
        >>> w.__str__()
        "from same to cost given dictionary:some, came, lame"
        """
        a = ""
        for i in self._word_set:
            a += i + ", "
        return "from {} to {}".format(self._from_word, self._to_word) + \
               " given dictionary:" + a[:-2]

        # override extensions
        # legal extensions are WordLadderPuzzles that have a from_word that can
        # be reached from this one by changing a single letter to one of those
        # in self._chars
    def extensions(self):
        """
        Return a list of extensions that are a single move away from \
        a current configuration.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]

        >>> w = WordLadderPuzzle("same", "cost", {"some", "came", "lame"})
        >>> w.extensions()
        [WordLadderPuzzle("some", "cost", {"some", "came", "lame"}), \
        WordLadderPuzzle("came", "cost", {"some", "came", "lame"}), \
        WordLadderPuzzle("lame", "cost", {"some", "came", "lame"})]
        """
        result = []
        for i in range(len(self._from_word)):
            for letter in self._chars:
                # find a letter in alphabet that is not a given _to_word
                if letter != self._from_word[i]:
                    # construct a word using new letter
                    next_word = self._from_word[:i] + letter + \
                        self._from_word[i+1:]
                    # if this word is in set of words put it into the list
                    if next_word in self._word_set:
                        next1 = WordLadderPuzzle(next_word, self._to_word,
                                                 self._word_set)
                        result += [next1]
        return result

        # override is_solved
        # this WordLadderPuzzle is solved when _from_word is the same as
        # _to_word

    def is_solved(self):
        """
        Return True if the WordLadderPuzzle is in solved configuration \
        i.e. when _from_word equals to _to_word and False otherwise.

        @type self: WordLadderPuzzle
        @rtype: bool

        >>> w = WordLadderPuzzle("cost", "cost", {"some", "came", "lame"})
        >>> w.is_solved()
        True
        """
        return self._from_word == self._to_word


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words", "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
