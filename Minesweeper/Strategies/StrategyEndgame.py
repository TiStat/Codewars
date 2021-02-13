from itertools import combinations

from ..Board.Position import relentless


class StrategyEndgame:
    def executeStrategy(Game):
        pass

    @relentless
    def endgame(self):
        """TODO: update doc"""
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

            # TODO: this information could be reused, to decrease the amount of
            #  computation for the next step.
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