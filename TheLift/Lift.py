class Lift:
    def __init__(self, capacity, height=None):
        """
        https://www.codewars.com/kata/58905bfa1decb981da00009e
        """
        self.capacity = capacity
        self.height = height  # of building
        self.load = []
        self._state = None
        self.visited = [0]

        self.switch_state(StateUP())

    @property
    def heading(self):
        return self._state.heading

    @property
    def current_load(self):
        return len(self.load)

    @property
    def current_floor(self):
        return self.visited[-1]

    @current_floor.setter
    def current_floor(self, v):
        self.visited.append(v)

    @property
    def next_floor(self):
        # part of the state pattern
        # "When called, the Lift will stop at a floor even if it is full":
        # to avoid sorting lift at each floor to determine the next floor to visit
        # min(self.load)/ max(self.load) are used!
        return self._state.next_floor

    def parse_queues(self, queue):
        """TODO make up and down FIFO queue.Priority_queue objects for a
            real life example with dynamic requests"""
        self.height = len(queue)

        up = [[person for person in v if person > floor] for floor, v in enumerate(queue)]
        down = [[person for person in v if person < floor] for floor, v in enumerate(queue)]
        self.requests = {'up': up, 'down': down}

    def switch_state(self, state):
        # set state & make state context aware; i.e. add reference to the lift obj.!
        self._state = state
        self._state.context = self

    def _exit_lift(self):
        # remove all those passengers with the same floor number
        self.load = [v for v in self.load if v != self.current_floor]

    def _enter_lift(self):
        """
        People are in "queues" that represent their order of arrival to wait for the Lift
        Only people going the same direction as the Lift may enter it
        Entry is according to the "queue" order, but those unable to enter do not block those behind them
        """
        if self.current_load < self.capacity:
            queue = self.requests[self.heading][self.current_floor]
            entering = min(len(queue), self.capacity - self.current_load)
            self.load.extend(queue[: entering])
            del queue[0:entering]

    def move(self):
        """
        The Lift never changes direction until there are no more people wanting
        to get on/off in the direction it is already travelling When empty the
        Lift tries to be smart. For example, If it was going up then it may
        continue up to collect the highest floor person wanting to go down If it
        was going down then it may continue down to collect the lowest floor
        person wanting to go up.
        """
        any_more_requests = lambda: any(bool(floor) for direct in ['up', 'down']
                                        for floor in self.requests[direct])

        while self.current_load > 0 or any_more_requests():  # lazy eval!
            self.current_floor = self.next_floor
            self._exit_lift()
            self._enter_lift()  # works with 0 people entering!
            self._state.check_end_ofthe_line()

        else:
            # If the lift is empty, and no people are waiting, then it will return to the ground floor
            self.current_floor = 0
            self.switch_state(state=StateUP())


# State pattern: https://refactoring.guru/design-patterns/state/python/example
class StateUP:
    heading = 'up'
    context = None

    @property
    def next_floor(self):
        lift = self.context
        # next in load or next non empty floor requesting to go in the same direction
        up_requests = (f for f, queue in enumerate(lift.requests[lift.heading][lift.current_floor:]) if f)
        return min([min(lift.load, default=lift.height), next(up_requests)])

    @property
    def check_end_ofthe_line(self):
        lift = self.context
        # no up requests, that are higher than current ("smart" strategy)
        if not any(bool(floor) for floor in lift.requests['up'][lift.current_floor:]):
            lift.switch_state(StateDown())


class StateDown:
    heading = 'down'
    context = None

    @property
    def next_floor(self):
        lift = self.context
        down_requests = (f for f, queue in enumerate(lift.requests[lift.heading][:lift.current_floor]) if f)
        return max([max(lift.load, default=0), next(down_requests)])

    @property
    def check_end_ofthe_line(self):
        lift = self.context
        # no down requests, that are lower than current ("smart" strategy)
        if not any(bool(floor) for floor in lift.requests['down'][:lift.current_floor]):
            lift.switch_state(StateUP())


if __name__ == '__main__':
    queue = ((6, 3, 5), (3, 3, 4), (5, 1, 5), (6,), (1,), (), (0,))

    lift = Lift(capacity=5)
    lift.parse_queues(queue)

    # Test enter_lift ---------
    # at floor 0:
    lift._enter_lift()
    assert lift.load == [6, 3, 5]
    assert lift.current_load == 3

    lift.current_floor = 3
    lift._exit_lift()
    assert lift.load == [6, 5]