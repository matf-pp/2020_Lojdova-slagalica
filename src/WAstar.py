import heapq
import sys
import os

import numpy as np

from BaseSolver import BaseSolver

sys.path.extend([os.path.join(os.getcwd(), "utils")])
from utils import reconstruct_path, serialize, is_solvable, h


class WAstar(BaseSolver):
    r"""Weigthing A* algorithm. It's possible to use either static or dynamic
    weighting. Both should reduce time needed to solve the puzzle."""

    def __init__(self, N, weight, mode="none"):
        r"""If `mode` is anything but "static" or "dynamic" ValueError will be
        raised. Static weighting will always multiply heuristics value with the
        same number. Dynamic weighting will reduce impact of heuristics value
        in deeper parts of search tree.

        Arguments:
            N (int): Size of puzzle.
            weight (number): Multiplier of heurstics.
            mode (str): Either "dynamic" or "static"."""

        super().__init__(N)

        mode = mode.lower()
        if mode not in ["dynamic", "static"]:
            raise ValueError("Invalid mode")

        self._weight = weight
        self._mode = mode
        self._max_depth = 80 if N == 4 else 31

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
        n_iters = 0

        # trivial check if the given puzzle can be solved or not
        if not is_solvable(self._start_state):
            return False, (n_iters, None)

        # initializing dictionaries for distances, parents and depth
        dist, parent, depth = {}, {}, {}
        dist[self._start_state] = 0
        parent[self._start_state] = None
        depth[self._start_state] = 0

        min_heap = []  # this list is used as Min-Heap
        heapq.heappush(min_heap, (h(self._start_state), self._start_state))

        while len(min_heap) > 0:
            _, state = heapq.heappop(min_heap)

            if state == self._end_state:
                path = reconstruct_path(parent, state)

                return True, (n_iters, path)
            else:
                n_iters += 1

                for next_state, w in self._get_neighbors(state):
                    cur_dist = dist[state] + w

                    if cur_dist < dist.get(next_state, float("inf")):  # relax
                        dist[next_state] = cur_dist
                        parent[next_state] = state
                        depth[next_state] = depth[state] + 1

                        g_val, h_val = cur_dist, h(next_state)
                        # weighting heuristics
                        if self._mode == "static":
                            h_val *= (1 + self._weight) * h_val
                        else:
                            h_smoothing = depth[next_state] / self._max_depth
                            h_val *= (1 + self._weight - h_smoothing)

                        heapq.heappush(min_heap, (g_val + h_val, next_state))

        return False, (n_iters, None)


if __name__ == "__main__":
    starting_states = [
        [[7, 1, 2], [0, 8, 3], [6, 4, 5]],
        [[8, 5, 9, 11], [7, 12, 10, 4], [0, 15, 13, 14], [1, 2, 6, 3]],
    ]

    for state in starting_states:
        solver = WAstar(len(state), 4, mode="dynamic")
        print(solver.solve(state))
