import heapq
import sys
import os

import numpy as np

from .BaseSolver import BaseSolver
from utils.utils import reconstruct_path, serialize, is_solvable, h


class IDAstar(BaseSolver):
    r"""Iterative deepening A*. States will be explored in case their f score
    isn't greater than the given threshold. Threshold will be properly updated
    in order to reach the final state."""

    def __init__(self, N):
        super().__init__(N)

    def _solve_threshold(self, start_state, threshold):
        n_iters, next_threshold = 0, float("inf")

        # initializing dictionaries for distances and parents
        dist, parent = {}, {}
        dist[self._start_state], parent[self._start_state] = 0, None

        min_heap = []  # this list is used as Min-Heap
        heapq.heappush(min_heap, (h(self._start_state), self._start_state))

        while len(min_heap) > 0:
            _, state = heapq.heappop(min_heap)

            if state == self._end_state:
                path = reconstruct_path(parent, state)

                return True, (n_iters, None, path)
            else:
                n_iters += 1

                for next_state, w in self._get_neighbors(state):
                    cur_dist = dist[state] + w

                    if cur_dist < dist.get(next_state, float("inf")):  # relax
                        dist[next_state] = cur_dist
                        parent[next_state] = state
                        cost_guess = cur_dist + h(next_state)

                        if cost_guess <= threshold:
                            heapq.heappush(min_heap, (cost_guess, next_state))
                        else:
                            next_threshold = min(next_threshold, cost_guess)

        return False, (n_iters, next_threshold, None)

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

        self._start_state = serialize(start_state)
        n_iters, threshold = 0, 0

        # trivial check if the given puzzle can be solved or not
        if not is_solvable(self._start_state):
            return False, (n_iters, None)

        flag, (threshold_iters, next_threshold, path) = \
            self._solve_threshold(start_state, threshold)
        while not flag:
            threshold = next_threshold
            n_iters += threshold_iters

            flag, (threshold_iters, next_threshold, path) = \
                self._solve_threshold(start_state, threshold)

        return True, (n_iters + threshold_iters, path)


if __name__ == "__main__":
    starting_states = [
        [[7, 1, 2], [0, 8, 3], [6, 4, 5]],
        # [[8, 5, 9, 11], [7, 12, 10, 4], [0, 15, 13, 14], [1, 2, 6, 3]],
    ]

    for state in starting_states:
        solver = IDAstar(len(state))
        print(solver.solve(state))
