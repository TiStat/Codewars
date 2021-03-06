import sys
from itertools import product, combinations

sys.setrecursionlimit(10 ** 6)
DEBUG = True


class Position:
    game = None
    dim = 1, 1

    def __init__(self, position, clue='?'):
        self.position = position
        self._clue = clue
        self._state = 0

        neighbours = self._find_neighbours(position)
        self.neighbours = neighbours
        self.neighb_inst = set()
        self.questionmarks = set()

    def __repr__(self):  # for debugging only
        # return str(self._clue)
        return str((self.position, 'clue:', self._clue, 'state:', self.state))

    def __str__(self):
        return str(self._clue)

    def __hash__(self):  # to support in
        return hash(self.position)

    def __eq__(self, other):  # to support in
        return self.position == other.position

    def isneighb(self, other):
        return other in self.neighb_inst

    @property
    def clue(self):
        return self._clue

    @clue.setter
    def clue(self, value):
        # called at open of this position.
        self._clue = value
        self.state = value + self.state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        # open all questionmarks by state hitting 0
        if value == 0:
            self._state = 0
            toopen = self.questionmarks.copy()
            for q in toopen:
                Position.game.open(*q.position)

            for n in self.neighb_inst:
                if n.state == len(n.questionmarks):
                    n.found_bomb()

        # default case, setting the received value
        else:
            self._state = value
            if self.state == len(self.questionmarks):
                self.found_bomb()

    def found_bomb(self):
        toopen = self.questionmarks.copy()  # TODO: fix mistake where self.questionmark produces neighb with clue 'x'
        if bool(toopen):
            self.bombastic(bombs=toopen)

    @staticmethod
    def bombastic(bombs):
        for b in bombs:
            if b._clue == '?':  # needed until deep copy problem in found_bomb is not solved
                b._clue = 'x'
                b.game.remain_bomb -= 1

                for n in b.neighb_inst:
                    n._state -= 1
                    if b in n.questionmarks:
                        n.questionmarks.discard(b)

                for n in b.neighb_inst:
                    n.state = n._state

    @staticmethod
    def _find_neighbours(position):
        """returns the set of all neighbours (excluding self's position).
        all of them are bound checked"""
        r, c = position
        cond = lambda r, c: 0 <= r < Position.dim[0] and 0 <= c < Position.dim[1]
        kernel = (-1, 0, 1)
        neighb = set((r + i, c + j) for i in kernel for j in kernel
                     if cond(r + i, c + j) and cond(r + i, c + j))
        neighb.discard((r, c))
        return neighb


def relentless(func):
    def wrapper(self, *args):
        before = True
        after = False
        while before != after:
            before = str(self)
            func(self, *args)
            after = str(self)

    return wrapper


class Game:
    def __init__(self, board, n, result=None):
        self.board = self.parse_board(board)
        self.dim = len(self.board), len(self.board[0])  # no. of rows, columns of map
        Position.dim = self.dim  # preset for all positions
        self.remain_bomb = n

        zeroind = [i for i, val in enumerate(board.replace(' ', '').replace('\n', '')) if val == '0']
        self.zerotup = [(ind // self.dim[1], ind % self.dim[1]) for ind in zeroind]

        if result is not None:
            self.result = self.parse_board(result)
            self.count = result.count('x')  # no. of bombs

        tuples = [(i, j) for i in range(self.dim[0]) for j in range(self.dim[1])]
        self.clues = {k: Position(k) for k in tuples}  # {position_tuple: Position_instance}

        # setting up the neighbourhood structure
        for inst in self.clues.values():
            inst.neighb_inst = set(self.clues[k] for k in inst.neighbours)
            inst.questionmarks = inst.neighb_inst.copy()

    def __repr__(self):
        return '\n'.join([' '.join([str(self.clues[(r, c)])
                                    for c in range(self.dim[1])]) for r in range(self.dim[0])])

    @staticmethod
    def parse_board(map):
        return [row.split() for row in map.split('\n')]

    def open(self, row, column):
        if self.clues[(row, column)].clue == '?':
            if DEBUG:
                value = int(self.result[row][column])
                if value == 'x':
                    raise ValueError('What a bummer.')
            else:
                value = open(row, column)

            inst = self.clues[(row, column)]
            for n in inst.neighb_inst:
                n.questionmarks.discard(inst)

            inst.clue = value

    @relentless
    def superset_solver(self):
        # first find the neighbours to remaining questionmarks
        inquestion = set(n for q in self.clues.values()
                         for n in q.neighb_inst
                         if q.clue == '?' and n.clue not in ['?', 'x'])  # TODO discard this simplification

        # most informative intersections start with:
        single = set(n for n in inquestion if n._state == 1)
        candidates = ([inst1, inst2] for inst1, inst2 in product(single, inquestion)
                      if (inst1.isneighb(inst2)) and inst2._state != 0)

        for inst1, inst2 in candidates:
            a = inst1.questionmarks
            b = inst2.questionmarks

            if b.issuperset(a) and bool(a):  # SUPERSET and a was not filled
                # in the meantime whilest iterating over candidates
                remain = (b - a)

                # remaining can be opened
                if inst2._state - inst1._state == 0:  # since inst1 is subset
                    toopen = remain.copy()
                    for n in toopen:
                        self.open(*n.position)

                # remaining are bombs
                elif len(remain) == inst2._state - inst1._state:
                    Position.bombastic(bombs=remain)

            elif inst2._state - inst1._state == len(a.union(b) - a):
                remain = a.union(b) - a
                Position.bombastic(bombs=remain)

        # search for all direct neighbor triplet who share the same questionmarks to make inferrence about bomb location
        inquestion = set(n for q in self.clues.values()
                         for n in q.neighb_inst
                         if q.clue == '?' and n.clue not in ['?', 'x'])

        single = set(n for n in inquestion if n._state == 1)
        candidates2 = ([inst1, inst2, inst3] for inst1, inst2, inst3 in product(single, inquestion, single)
                       if (inst1.isneighb(inst2) and inst3.isneighb(inst2)) and inst2._state != 0 and inst1 != inst3)

        for inst1, inst2, inst3 in candidates2:
            a = inst1.questionmarks
            b = inst2.questionmarks
            c = inst3.questionmarks
            union = a.union(c)

            if b.issuperset(union) and bool(a) and bool(b):
                remain = (b - union)

                if inst2._state - inst1._state - inst3._state == 0 \
                        and len(union) == len(a) + len(c):  # otherwise the code opens fields which it cannot
                    toopen = remain.copy()
                    for n in toopen:
                        self.open(*n.position)

                    # remaining are bombs
                elif len(remain) == inst2._state - inst1._state - inst3._state:
                    Position.bombastic(bombs=remain)

    @relentless
    def endgame(self):
        remain_q = set(q for q in self.clues.values() if q._clue == '?')
        anreiner = set(n for q in self.clues.values()
                       for n in q.neighb_inst
                       if q.clue == '?' and n.clue not in ['?', 'x'])

        potential_bomb = set()
        for bombcombi in combinations(remain_q, self.remain_bomb):
            # update the states for this trial
            for bomb in bombcombi:
                for n in bomb.neighb_inst:
                    n._state -= 1

            # check if this is a valid combinations (all anreiner are happy)
            if set(a._state for a in anreiner) == {0}:
                potential_bomb.update(set(bombcombi))

            # undo this trial
            for bomb in bombcombi:
                for n in bomb.neighb_inst:
                    n._state += 1

        untouched = remain_q - potential_bomb
        for Pos in untouched:
            self.open(*Pos.position)

    def solve(self):
        # (0) causal (state) communication logic from initial zeros
        for zero in self.zerotup:
            self.open(*zero)

        # (1) exacly one bomb in questionmarks logic
        self.superset_solver()

        remain_q = [_ for _ in self.clues.values() if _._clue == '?']
        if self.remain_bomb == len(remain_q):
            Position.bombastic(remain_q)
        elif self.remain_bomb == 0 and len(remain_q) != 0:
            for _ in remain_q:
                self.open(*_.position)

        # (2) Endgame logic based on number of bombs.
        if bool(self.remain_bomb) and self.remain_bomb <= 3:
            self.endgame()

        # ambiguity?
        if bool([inst._clue for inst in self.clues.values() if inst._clue == '?']):
            return '?'
        else:
            return Position.game


def solve_mine(gamemap, n, resultmap=None):
    """surrogate solver to match this katas desired interface
    https://www.codewars.com/kata/57ff9d3b8f7dda23130015fa"""
    if n == 0: return '0'
    Position.game = Game(gamemap, n, resultmap)
    return str(Position.game.solve())


# !!!!!!!!! ENDGAME ENDGAME ENDGAME !!!!!!
gamemap = """
0 0 0 0 0 0 0 0 0 0 0
0 0 0 ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? 0 0 0
0 0 0 0 0 0 0 0 0 0 0
""".strip()
result = """
0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 2 3 3 2 1 0 0
0 0 1 3 x x x x 1 0 0
0 0 2 x x 6 x 5 2 0 0
0 0 3 x 4 4 x x 2 0 0
0 0 3 x 5 5 x x 2 0 0
0 0 2 x x x x 3 1 0 0
0 0 1 2 3 3 2 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
""".strip()
game1 = Game(gamemap, 17,  result)
assert solve_mine(gamemap, 17, result) == result
# #
# gamemap = """
# ? ? ? 0 0 ? ? ? ? ? ? 0 0 ? ? ? ?
# ? ? ? 0 0 ? ? ? ? ? ? 0 0 ? ? ? ?
# 0 0 0 0 0 ? ? ? ? 0 0 0 0 0 ? ? ?
# 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 ? ? ?
# 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ? ? ?
# ? ? ? 0 0 0 0 0 0 0 0 0 0 ? ? ? ?
# ? ? ? 0 0 0 0 0 0 0 0 0 0 ? ? ? ?
# """.strip()
# result = """
# 1 x 1 0 0 2 x 2 1 x 1 0 0 1 x x 1
# 1 1 1 0 0 2 x 3 2 1 1 0 0 1 3 4 3
# 0 0 0 0 0 1 2 x 1 0 0 0 0 0 1 x x
# 0 0 0 0 0 0 1 1 1 0 0 0 0 0 1 2 2
# 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1
# 1 1 1 0 0 0 0 0 0 0 0 0 0 1 2 x 1
# 1 x 1 0 0 0 0 0 0 0 0 0 0 1 x 2 1
# """.strip()
# game1 = Game(gamemap, 12, result)
# assert solve_mine(gamemap, game1.count, result) == result

gamemap = """
0 0 0 0 0 0 0 0 0 0 0
0 0 0 ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? 0 0 0
0 0 0 0 0 0 0 0 0 0 0
""".strip()
result = """
0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 2 3 3 2 1 0 0
0 0 1 3 x x x x 1 0 0
0 0 2 x x x x 5 2 0 0
0 0 3 x x x x x 2 0 0
0 0 3 x x x x x 2 0 0
0 0 2 x x x x 3 1 0 0
0 0 1 2 3 3 2 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
""".strip()
game1 = Game(gamemap, 22, result)
assert solve_mine(gamemap, 22, result) == result
# #

gamemap = """
0 0 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ? ? ? ? ? ? ?
? ? 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ?
? ? ? ? 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? ? 0 ? ? ? ? ? ?
? ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0 ? ? ? ? ? ?
0 ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 ? ? ? ? ? ?
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? ? 0
""".strip()

result = """
0 0 0 1 x 1 1 x 1 0 0 0 0 0 1 1 1 0 0 1 x 3 x 3 1 2 1
1 1 0 1 1 1 1 1 1 0 0 0 0 0 1 x 1 1 1 2 1 3 x 3 x 2 x
x 2 1 1 0 0 0 0 0 0 1 1 1 0 1 1 1 1 x 1 0 2 2 3 1 3 2
1 2 x 1 0 0 0 0 0 0 1 x 1 0 0 0 0 1 1 1 0 1 x 2 1 2 x
0 1 1 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 1 2 3 x 2 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 x 2 1 0
""".strip()
assert solve_mine(gamemap, result.count('x'), result) == result

# Ambivalent state
gamemap = """
0 ? ?
0 ? ?
""".strip()
result = """
0 1 x
0 1 1
""".strip()
assert solve_mine(gamemap, result.count('x'), result) == "?"

# Deterministic board
gamemap = """
? ? ? ? 0 0 0
? ? ? ? 0 ? ?
? ? ? 0 0 ? ?
? ? ? 0 0 ? ?
0 ? ? ? 0 0 0
0 ? ? ? 0 0 0
0 ? ? ? 0 ? ?
0 0 0 0 0 ? ?
0 0 0 0 0 ? ?
""".strip()
result = """
1 x x 1 0 0 0
2 3 3 1 0 1 1
1 x 1 0 0 1 x
1 1 1 0 0 1 1
0 1 1 1 0 0 0
0 1 x 1 0 0 0
0 1 1 1 0 1 1
0 0 0 0 0 1 x
0 0 0 0 0 1 1
""".strip()
assert solve_mine(gamemap, result.count('x'), result) == result

# Huge ambivalent state
gamemap = """
? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? 0
? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? ?
? ? 0 ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? ?
0 ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 0
0 ? ? ? 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 ? ? ? ? 0 0 0 0 0
0 0 ? ? ? 0 ? ? ? 0 ? ? ? ? 0 0 0 0 0
0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? 0
0 0 ? ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
0 0 0 0 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? 0 0 0 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ?
0 0 0 0 0 0 ? ? ? ? 0 0 0 ? ? ? 0 ? ?
0 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? ?
0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? ?
0 0 0 ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
""".strip()
result = """
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
""".strip()
assert solve_mine(gamemap, result.count('x'), result) == "?"

# differently shaped ambivalent state
gamemap = """
0 0 0 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? 0 ? ? ?
0 0 0 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? ? ? ? ?
0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? ? ?
0 0 0 0 0 ? ? ? 0 0 ? ? ? 0 ? ? ? ? ? ? 0
? ? 0 0 0 ? ? ? 0 ? ? ? ? 0 0 ? ? ? ? ? ?
? ? 0 0 0 ? ? ? 0 ? ? ? 0 0 0 ? ? ? ? ? ?
? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 ? ? ?
? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? 0 0
? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? 0 0
""".strip()
result = """
0 0 0 0 0 0 0 0 1 x x 2 1 0 1 x 1 0 1 2 x
0 0 0 0 0 0 0 0 1 2 3 x 1 0 2 2 2 1 2 x 2
0 0 0 0 0 0 0 0 0 0 2 2 2 0 1 x 1 1 x 2 1
0 0 0 0 0 1 1 1 0 0 1 x 1 0 1 2 2 2 1 1 0
1 1 0 0 0 1 x 1 0 1 2 2 1 0 0 1 x 1 1 1 1
x 1 0 0 0 1 1 1 0 1 x 1 0 0 0 1 1 1 1 x 1
2 2 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 1 1 1
1 x 1 0 0 0 0 0 0 0 1 2 2 1 0 0 1 1 1 0 0
1 1 1 0 0 0 0 0 0 0 1 x x 1 0 0 1 x 1 0 0
""".strip()
assert solve_mine(gamemap, result.count('x'), result) == "?"
