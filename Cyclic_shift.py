from collections import deque
from itertools import chain


def loopover(mixed_up_board, solved_board):
    return Cyclic_shift(mixed_up_board, solved_board).solve()


class Node:
    current = dict()
    target = dict()  # target coordinates value: (row, col)

    def __init__(self, position, value):
        self.position = position
        self.value = value

    def __repr__(self):
        return str(self.value)


class Row(list):
    def __init__(self, iterable):
        """:param iterable: an ordered collection of Node instances"""
        super(Row, self).__init__(iterable)
        self.queue = deque(maxlen=len(iterable))

    def rowshift(self, direction):
        """:param direction: integer, either 0 (left) or 1 (right)"""
        self.queue.extend([node.value for node in self])

        if direction == 0:
            self.queue.append(self.queue[0])
        else:
            self.queue.appendleft(self.queue[-1])

        for node, v in zip(self, self.queue):
            node.value = v
            Node.current[v] = node.position  # still efficient as merely pointer
            # to immutable tuple is shared (no new tuple is created)

        self.queue.clear()  # necessary! to ensure the state is always correct!


class Cyclic_shift:
    direct = {'L': 0, 'R': 1, 'D': 1, 'U': 0}
    perspective = {'L': 'rows', 'R': 'rows', 'D': 'cols', 'U': 'cols'}

    def __init__(self, mixed_up_board, solved_board):
        """
        kata: https://www.codewars.com/kata/5c1d796370fee68b1e000611/train/python
        :param mixedUpBoard: two-dim arrays (or lists of lists) of symbols
        representing the initial (unsolved) grid
        :param solvedBoard:  same as mixedUpBoard but final (solved) grid.

        Different grid sizes are tested: from 2x2 to 9x9 grids
        (including rectangular grids like 4x5)
        """

        # Consider: translating latters to numbers (as modulo devision allows immediate
        # calculation of the target position. also this allows to ).
        # Make the Node aware of (/allow to inquire) where the target of the currently occupying value is.
        Node.current = {val: (r, c) for r, row in enumerate(mixed_up_board) for c, val in enumerate(row)}
        Node.target = {val: (r, c) for r, row in enumerate(solved_board) for c, val in enumerate(row)}

        # Create a playable board
        self.rows = [Row([Node((i, j), val) for j, val in enumerate(row)]) for i, row in enumerate(mixed_up_board)]
        self.cols = [Row(col) for col in zip(*self.rows)]
        self.board = {'rows': self.rows, 'cols': self.cols}

        print(self)

        # DEPREC: FOR DEBUG ONLY: CHECK METHOD
        self.nodes = {node.position: node for node in chain(*self.rows)}
        self.solved_board = solved_board

    def __repr__(self):
        return '\n'.join([' '.join([str(val) for val in row]) for row in self.rows])

    def shift(self, direction):
        """Primary method to play the game (change the state of board)
        :param direction: string such as L0, R1, D1, U2
        where L & R refer to rowshifts and D & U to column shifts"""
        direct, pos = tuple(direction)
        board = self.board[self.perspective[direct]]
        board[int(pos)].rowshift(direction=self.direct[direct])

        print(self)

    def solve(self):
        """Your task: return a List of moves that will transform the unsolved
        grid into the solved one. All values of the scrambled and unscrambled
        grids will be unique! Moves will be 2 character long Strings"""
        unsolvable = False
        if unsolvable:
            return None
        pass

    # DEPREC: DEBUG METHODS: REMOVE WHEN SUBMITTING ----------------------------
    def debug_col_repr(self):  # DEPREC to print the columns (primarily debug method)
        print('\n'.join([' '.join([str(val) for val in row]) for row in self.cols]))

    def debug_check(self, moves):  # Deprec: Debug only
        for move in moves:
            self.shift(move)

        board = [[self.nodes[(r, c)].value for c in range(len(self.rows[0]))]
                 for r in range(len(self.rows))]

        return board == self.solved_board

    def debug_shuffle(self, number):  # Deprec: Debug only
        """method to create random tests"""
        from random import randint
        pass


if __name__ == '__main__':
    def board(str):
        return [list(row) for row in str.split('\n')]


    def run_test(start, end, unsolvable):

        # print_info(board(start), board(end))
        moves = loopover(board(start), board(end))
        if unsolvable:
            assert moves is None  # 'Unsolvable configuration

        else:
            assert Cyclic_shift(start, end).debug_check(moves) == True
            # TODO write check function!


    c = Cyclic_shift(board('ACDBE\nFGHIJ\nKLMNO\nPQRST'),
                     board('ABCDE\nFGHIJ\nKLMNO\nPQRST'))

    c.shift('L0')
    c.shift('U0')
    print()

    # @test.it('Test 2x2 (1)')
    run_test('12\n34', '12\n34', False)

    # @test.it('Test 2x2 (2)')
    run_test('42\n31', '12\n34', False)

    # @test.it('Test 4x5')
    run_test('ACDBE\nFGHIJ\nKLMNO\nPQRST',
             'ABCDE\nFGHIJ\nKLMNO\nPQRST', False)

    # @test.it('Test 5x5 (1)')
    run_test('ACDBE\nFGHIJ\nKLMNO\nPQRST\nUVWXY',
             'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY', False)

    # @test.it('Test 5x5 (2)')

    run_test('ABCDE\nKGHIJ\nPLMNO\nFQRST\nUVWXY',
             'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY', False)

    # @test.it('Test 5x5 (3)')
    run_test('CWMFJ\nORDBA\nNKGLY\nPHSVE\nXTQUI',
             'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY', False)

    # @test.it('Test 5x5 (unsolvable)')
    run_test('WCMDJ\nORFBA\nKNGLY\nPHVSE\nTXQUI',
             'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY', True)

    # @test.it('Test 6x6')
    run_test('WCMDJ0\nORFBA1\nKNGLY2\nPHVSE3\nTXQUI4\nZ56789',
             'ABCDEF\nGHIJKL\nMNOPQR\nSTUVWX\nYZ0123\n456789', False)
