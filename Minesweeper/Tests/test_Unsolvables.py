import unittest

from ..Board.Game import Game
from ..Board.Solution import Solution
from ..Util import board


class TestUnsolvables(unittest.TestCase):

    def tearDown(self) -> None:
        solution = Solution(board(self.result))
        m = Game(board=solution.covered_board, n=solution.n, context=solution)

        self.assertEqual(m.solve(), '?')

    def test_unsolvable1(self):
        # Ambivalent state
        self.result = """
        0 1 x
        0 1 1
        """

    def test_unsolvable2(self):
        """Huge ambivalent state"""

        self.result = """
        1 1 0 1 1 1 0 0 1 1 1 0 0 0 0 1 1 1 0
        x 1 0 1 x 1 0 0 2 x 2 0 0 0 0 1 x 2 1
        1 1 0 2 3 3 1 1 3 x 2 0 0 0 0 1 2 x 1
        0 1 1 2 x x 1 2 x 3 1 0 0 0 0 0 1 1 1
        0 1 x 2 2 2 1 3 x 3 0 0 0 0 0 0 0 0 0
        0 1 1 1 0 0 0 2 x 2 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 1 1 1 1 2 2 1 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 1 x x 1 0 0 0 0 0
        0 0 1 1 1 0 1 1 1 0 1 2 2 1 0 0 0 0 0
        0 0 1 x 2 1 3 x 2 0 0 0 0 0 0 1 1 1 0
        0 0 1 1 2 x 3 x 3 1 1 0 0 0 0 1 x 1 0
        0 0 0 0 1 2 3 2 2 x 1 0 0 0 0 1 1 1 0
        0 0 0 0 0 1 x 1 1 1 1 0 0 0 0 0 1 1 1
        0 0 1 1 2 2 2 1 0 0 0 0 0 0 0 0 1 x 1
        0 0 1 x 2 x 2 1 1 0 0 0 0 0 0 0 1 1 1
        0 0 1 1 2 1 3 x 3 1 0 0 0 0 0 0 0 1 1
        0 0 0 0 0 0 2 x x 1 0 0 0 1 1 1 0 1 x
        0 0 0 1 1 1 1 2 2 1 0 0 0 1 x 1 1 2 2
        0 0 0 1 x 3 2 1 0 0 0 1 1 2 1 1 1 x 2
        0 0 0 1 2 x x 1 0 0 0 1 x 1 0 1 2 3 x
        0 0 0 0 1 2 2 1 1 1 1 1 1 1 0 1 x 3 2
        0 0 0 0 1 1 1 1 2 x 1 1 1 1 0 2 3 x 2
        0 0 0 0 1 x 1 1 x 2 1 1 x 1 0 1 x 3 x
        """

    def test_unsolvable3(self):
        # differently shaped ambivalent state

        self.result = """
        0 0 0 0 0 0 0 0 1 x x 2 1 0 1 x 1 0 1 2 x
        0 0 0 0 0 0 0 0 1 2 3 x 1 0 2 2 2 1 2 x 2
        0 0 0 0 0 0 0 0 0 0 2 2 2 0 1 x 1 1 x 2 1
        0 0 0 0 0 1 1 1 0 0 1 x 1 0 1 2 2 2 1 1 0
        1 1 0 0 0 1 x 1 0 1 2 2 1 0 0 1 x 1 1 1 1
        x 1 0 0 0 1 1 1 0 1 x 1 0 0 0 1 1 1 1 x 1
        2 2 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 1 1 1
        1 x 1 0 0 0 0 0 0 0 1 2 2 1 0 0 1 1 1 0 0
        1 1 1 0 0 0 0 0 0 0 1 x x 1 0 0 1 x 1 0 0
        """

    def test_unsolvable4(self):
        self.result = """
        x x x
        x 8 x
        x x x
        """


if __name__ == '__main__':
    unittest.main(exit=False)
