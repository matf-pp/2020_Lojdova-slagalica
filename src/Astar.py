import heapq

import numpy as np

from src.BaseSolver import BaseSolver
from utils.utils import is_solvable, h


class Astar(BaseSolver):
    def __init__(self, start_state):
        super().__init__(start_state)

    def solve(self):
        r"""Solving given puzzle. This implementation assumes that given
        heurstics is consistent meaning that it's sufficient to relax distance
        the moment it becomes possible and such action will never be possible
        in the future. Manhattan distance is used.

        Returns:
            flag, n_iters: Flag (True/False) if it's possible to solve the
                puzzle and number of iterations in solving process."""    

        n_iters = 0

        # trivial check if the given puzzle can be solved or not
        if not is_solvable(self._start_state):
            return False, n_iters

        # initializing dictionaries for distances and parents
        dist, parent = {}, {}
        dist[self._start_state], parent[self._start_state] = 0, None

        min_heap = []  # this list is used as Min-Heap
        heapq.heappush(min_heap, (h(self._start_state), self._start_state))

        while len(min_heap) > 0:
            _, state = heapq.heappop(min_heap)

            if state == self._end_state:
                return True, n_iters
            else:
                n_iters += 1

                for next_state, w in self._get_neighbors(state):
                    cur_dist = dist[state] + w

                    if cur_dist < dist.get(next_state, float("inf")):  # relaxing
                        dist[next_state] = cur_dist
                        parent[next_state] = state
                        cost_guess = cur_dist + h(next_state)

                        heapq.heappush(min_heap, (cost_guess, next_state))

        return False, n_iters


if __name__ == "__main__":
    starting_states = [
        [[1, 2, 3], [0, 4, 5], [6, 8, 7]],  # not solvable
        [[6, 8, 7], [0, 1, 2], [3, 4, 5]],  # medium solution
        [[2, 3, 5], [1, 4, 0], [7, 8, 6]],  # easy solution
        [[1, 2, 0], [3, 4, 5], [6, 7, 8]]  # trivial solution
    ]

    for state in starting_states:
        solver = Astar(state)
        print(solver.solve())
