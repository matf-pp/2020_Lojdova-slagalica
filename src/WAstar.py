import heapq
import copy

import numpy as np

from src.BaseSolver import BaseSolver
from utils.utils import hash_state, is_solvable, h


class WAstar(BaseSolver):
    r"""Weighted A* algorithm. It's possible to use either static or dynamic
    weighting. Both should reduce time needed to solve the puzzle."""

    def __init__(self, N, static_weight=None, dynamic_weight=None):
        r"""If `static_weight` is provided then `dynamic_weight` should not and
        vice versa.

        Arguments:
            N (int): Size of puzzle.
            static_weight (number): Multiplier of heurstics.
            dynamic_weight (callable): Multiplier of heuristics."""

        super().__init__(N)
        self._static_weight = static_weight
        self._dynamic_weight = dynamic_weight

    def solve(self, start_state):
        r"""Solving given puzzle. This implementation assumes that given
        heurstics is consistent meaning that it's sufficient to relax distance
        the moment it becomes possible and such action will never be possible
        in the future. Manhattan distance is used.

        Arguments:
            start_state (list or np.ndarray): Starting state.

        Returns:
            flag, n_iters: Flag (True/False) if it's possible to solve the
                puzzle and number of iterations in solving process."""

        self._start_state = hash_state(start_state)
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

                    if cur_dist < dist.get(next_state, float("inf")):  # relax
                        dist[next_state] = cur_dist
                        parent[next_state] = state

                        h_val = h(next_state)
                        # weighting heuristics
                        if self._static_weight is not None:
                            cost_guess = cur_dist + \
                                self._static_weight * h_val
                        elif self._dynamic_weight is not None:
                            h_val = h(next_state)
                            cost_guess = cur_dist + \
                                self._dynamic_weight(h_val) * h_val
                        else:
                            cost_guess = cur_dist + h_val

                        heapq.heappush(min_heap, (cost_guess, next_state))

        return False, n_iters


if __name__ == "__main__":
    starting_states = [
        [[7, 1, 2], [0, 8, 3], [6, 4, 5]],
        [[8, 5, 9, 11], [7, 12, 10, 4], [0, 15, 13, 14], [1, 2, 6, 3]],
    ]

    static_weight = 1 + 4
    for state in starting_states:
        solver = WAstar(len(state), static_weight=static_weight)
        print(solver.solve(state))
