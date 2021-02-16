import unittest

from ..Board.Game import Game
from ..Board.Solution import Solution
from ..Util import board


class TestSolvables(unittest.TestCase):
    def tearDown(self):
        solution = Solution(board(self.result))
        m = Game(board=solution.covered_board, n=solution.n, context=solution)

        m.solve()

        self.assertEqual(m.board, board(self.result))

    def test_board1(self):
        self.result = """
        0 0 0 1 x 1 1 x 1 0 0 0 0 0 1 1 1 0 0 1 x 3 x 3 1 2 1
        1 1 0 1 1 1 1 1 1 0 0 0 0 0 1 x 1 1 1 2 1 3 x 3 x 2 x
        x 2 1 1 0 0 0 0 0 0 1 1 1 0 1 1 1 1 x 1 0 2 2 3 1 3 2
        1 2 x 1 0 0 0 0 0 0 1 x 1 0 0 0 0 1 1 1 0 1 x 2 1 2 x
        0 1 1 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 1 2 3 x 2 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 x 2 1 0
        """

    def test_board2(self):
        self.result = """
        1 x 1 0 1 1 1 0 1 x 2 x 1 0 0 0 1 x 1 0 0 0 0 0 0 1 1 1 0 0
        1 1 1 0 1 x 2 2 3 2 2 1 1 0 0 0 1 1 2 1 1 0 0 0 0 1 x 1 0 0
        0 0 0 1 2 2 2 x x 2 1 1 0 0 0 0 0 0 1 x 1 0 0 0 0 1 2 2 1 0
        1 1 1 1 x 1 1 2 2 2 x 1 1 1 1 0 0 0 1 1 1 0 0 0 0 0 2 x 2 0
        2 x 1 1 1 1 1 1 1 1 1 1 1 x 2 1 0 0 0 1 1 1 0 0 0 0 2 x 2 0
        x 2 1 0 0 0 1 x 1 0 0 0 2 3 x 1 0 0 0 1 x 1 0 0 0 0 1 1 1 0
        1 1 0 0 0 0 2 2 2 0 0 0 1 x 2 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0
        0 0 0 0 0 0 1 x 1 0 0 0 2 2 2 0 1 1 1 0 0 0 1 1 1 1 x 1 0 0
        0 0 0 0 1 1 2 1 1 0 0 0 1 x 1 0 1 x 1 1 1 2 2 x 1 1 1 1 0 0
        0 0 0 0 1 x 1 0 0 0 0 0 1 1 1 0 2 2 2 2 x 3 x 2 1 0 0 0 1 1
        0 0 0 0 1 1 1 0 0 0 0 1 1 1 0 0 1 x 1 2 x 4 2 2 0 1 1 1 1 x
        0 1 1 1 0 0 0 0 0 0 0 1 x 1 0 0 1 2 2 2 1 2 x 1 0 1 x 1 1 1
        0 1 x 2 1 2 1 1 0 0 0 1 1 1 0 0 0 1 x 1 0 1 2 2 1 1 1 1 0 0
        0 1 1 2 x 2 x 3 2 1 0 1 2 2 1 0 0 1 2 2 1 0 1 x 1 0 0 0 0 0
        1 1 0 1 1 2 2 x x 1 0 1 x x 1 0 0 0 1 x 1 0 1 2 2 1 0 0 0 0
        x 1 0 0 0 0 2 3 3 1 0 1 2 2 1 0 0 0 1 1 1 0 0 2 x 2 0 0 0 0
        1 1 0 0 0 0 1 x 1 0 0 0 0 1 1 1 0 0 0 0 0 0 0 2 x 3 1 0 0 0
        0 0 0 0 0 0 1 1 1 0 0 0 0 1 x 1 0 0 0 1 1 1 0 1 2 x 1 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 2 x 2 0 1 2 2 1 0 0 0
        1 2 2 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 x 2 0 1 x 1 0 1 1 1
        1 x x 1 1 1 1 0 1 1 1 0 0 1 1 2 1 1 0 1 1 1 1 2 2 1 0 1 x 1
        1 2 3 2 2 x 1 0 1 x 2 1 0 1 x 3 x 2 0 0 0 0 1 x 1 0 0 1 1 1
        0 0 1 x 3 2 2 0 1 2 x 1 1 2 2 3 x 3 1 0 0 0 1 1 1 0 0 0 0 0
        0 0 1 1 2 x 1 0 0 1 1 2 2 x 2 2 2 x 2 1 1 0 0 0 0 0 0 0 0 0
        0 0 0 0 1 1 1 0 0 0 0 1 x 4 x 1 1 1 2 x 1 1 1 1 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 1 1 2 2 x 2 1 0 0 1 1 1 1 x 2 1 1 0 0 0 0
        0 0 0 0 0 1 1 2 1 2 x 1 1 1 1 0 0 1 2 2 1 1 1 2 x 2 1 1 1 1
        0 0 0 0 0 1 x 4 x 4 2 1 0 0 0 0 0 2 x x 2 2 2 2 3 x 2 1 x 1
        0 0 0 0 0 1 2 x x x 1 0 0 0 0 0 0 2 x 3 2 x x 1 2 x 2 1 1 1
        """

    def test_board3(self):
        self.result = """
        0 0 0 0 0 0 0 1 1 1
        1 1 1 1 1 1 0 2 x 2
        1 x 2 2 x 1 0 2 x 2
        1 1 2 x 2 1 0 1 1 1
        0 0 2 2 2 1 1 1 0 0
        0 0 1 x 1 1 x 2 1 1
        0 0 1 1 2 2 2 3 x 2
        0 0 0 0 1 x 1 2 x 2
        0 0 0 0 1 1 1 1 1 1
        0 0 0 1 2 2 1 0 0 0
        0 0 0 1 x x 1 0 0 0
        0 0 0 1 2 2 1 0 0 0
        0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0
        1 1 0 1 1 1 0 0 0 0
        x 1 0 1 x 1 0 0 0 0
        2 3 1 3 2 2 1 1 1 0
        x 2 x 2 x 1 1 x 2 1
        1 2 1 2 1 1 1 2 x 1
        0 0 1 1 1 0 0 1 1 1
        0 0 1 x 1 1 1 2 2 2
        0 0 1 1 1 1 x 2 x x
        0 0 0 0 0 1 1 2 2 2
        """

    def test_board4(self):
        self.result = """
        1 1 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0
        x 1 0 0 1 1 1 0 0 0 1 1 1 0 1 x 1 0
        1 1 0 0 1 x 1 0 0 0 2 x 2 0 1 1 1 0
        0 1 1 1 1 1 1 0 0 0 2 x 2 0 0 0 0 0
        0 1 x 1 0 0 0 0 0 1 2 2 1 0 0 0 0 0
        0 1 1 1 0 0 0 0 0 1 x 1 1 1 1 1 2 2
        0 0 0 1 1 1 0 0 0 1 1 1 1 x 1 1 x x
        0 1 1 2 x 2 1 0 1 1 1 0 1 1 2 2 4 x
        0 1 x 2 2 x 1 0 1 x 2 1 1 0 1 x 2 1
        0 2 2 2 1 2 2 1 1 1 3 x 2 0 1 1 1 0
        0 1 x 1 0 1 x 1 0 0 2 x 2 0 0 0 0 0
        0 1 1 1 0 1 1 1 0 0 2 2 2 0 0 0 0 0
        0 1 1 1 1 1 1 0 0 0 1 x 1 0 0 0 0 0
        1 2 x 2 2 x 1 0 0 0 1 2 3 2 1 0 0 0
        x 2 1 2 x 2 1 0 1 1 1 2 x x 1 0 0 0
        1 2 1 2 1 1 0 0 1 x 1 2 x 3 1 0 1 1
        0 1 x 1 0 0 0 0 1 1 1 1 1 1 0 0 1 x
        0 1 1 1 0 0 0 0 0 1 1 1 0 0 0 0 1 1
        1 1 1 1 1 0 0 0 0 1 x 1 0 0 0 0 0 0
        x 3 2 x 2 1 1 0 0 1 1 1 0 0 0 0 0 0
        x 3 x 3 3 x 1 0 0 0 1 1 1 0 1 1 1 0
        1 2 1 2 x 2 1 0 0 0 1 x 1 0 1 x 1 0
        """

    def test_board5(self):
        self.result = """
        0 1 1 2 1 1 0 0 0 1 1 2 2 2 2 x 1 0 0 0
        0 1 x 2 x 1 0 0 0 1 x 3 x x 3 2 1 0 0 0
        0 1 1 2 1 1 0 0 0 1 2 x 3 3 x 1 0 0 1 1
        0 0 0 1 1 1 0 0 0 0 1 1 1 1 1 1 0 0 1 x
        0 0 0 1 x 1 0 0 0 0 0 0 0 0 0 0 0 1 2 2
        0 1 1 2 1 1 0 0 0 0 0 0 0 0 0 0 0 1 x 1
        0 1 x 1 0 1 1 1 0 0 0 0 0 1 1 1 0 1 1 1
        0 1 1 1 0 1 x 2 2 2 1 0 0 1 x 2 1 1 0 0
        0 1 1 1 0 1 1 2 x x 1 0 0 1 1 2 x 1 0 0
        0 1 x 1 0 0 0 1 2 2 1 0 0 0 0 2 2 2 0 0
        0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 1 x 2 1 0
        0 1 1 1 0 0 0 0 0 1 1 1 0 0 0 1 2 x 1 0
        0 1 x 1 0 0 0 0 0 1 x 2 1 1 0 1 3 3 2 0
        1 2 1 1 0 0 0 0 0 1 1 2 x 1 0 2 x x 1 0
        x 1 0 0 0 0 0 0 0 0 0 1 1 1 0 2 x 4 3 2
        1 2 1 1 0 0 0 0 0 0 0 0 0 0 0 1 1 2 x x
        1 2 x 1 0 0 1 2 3 2 1 0 1 1 1 0 0 1 2 2
        1 x 3 3 1 1 1 x x x 1 0 2 x 2 0 0 0 0 0
        1 2 x 2 x 1 2 3 4 2 1 0 2 x 3 1 0 0 0 0
        0 1 1 2 2 2 2 x 1 0 0 0 1 2 x 1 0 0 0 0
        0 0 0 0 1 x 2 1 1 0 0 0 1 2 2 1 0 0 0 0
        0 0 0 0 1 1 1 0 0 0 0 0 1 x 2 1 0 0 0 0
        0 0 0 0 0 0 0 1 2 2 1 0 1 2 x 1 0 0 0 0
        1 1 1 1 1 0 0 1 x x 2 1 1 1 2 2 2 1 1 0
        x 2 3 x 2 0 0 1 2 2 2 x 1 0 1 x 2 x 2 1
        2 x 3 x 2 0 0 0 0 0 1 2 2 1 1 1 2 1 2 x
        2 3 3 3 2 1 0 0 0 0 0 1 x 1 0 0 0 1 2 2
        x 2 x 2 x 1 0 0 0 0 0 1 1 1 0 0 0 1 x 1
        1 2 1 2 1 1 0 0 0 0 0 0 0 0 0 0 0 1 1 1
        """

    def test_board6(self):
        self.result = """
        0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 1 x 2 1 1 0 0 1 1 1
        0 0 1 2 2 1 1 1 1 0 0 0 1 x 1 0 1 2 3 x 1 0 0 1 x 1
        0 0 1 x x 1 1 x 1 0 0 0 1 2 2 1 0 1 x 3 2 1 0 1 1 1
        0 0 1 2 2 1 1 1 1 0 0 0 0 1 x 1 0 1 1 2 x 1 0 0 0 0
        """

    def test_board7(self):
        self.result = 'x'

    def test_board8(self):
        self.result = """
        0 0 0 0
        0 0 0 0
        1 1 0 0
        x 2 1 1
        x 3 1 x
        x 2 1 1
        1 1 0 0
        0 0 0 0
        0 0 0 0
        0 0 0 0
        """


if __name__ == '__main__':
    unittest.main()
