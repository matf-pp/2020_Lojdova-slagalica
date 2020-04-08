from utils import serialize, deserialize
import random
import sys
import os

import numpy as np

sys.path.extend([os.path.join(os.getcwd(), "utils")])


class BaseSolver:
    r"""Base class for Loyd puzzle solver. It doesn't implement any algorithm
    and it's expected that any of such extends this class. It provides general
    and useful functions for easier implementation of algorithms."""

    def __init__(self, N):
        r"""Initializing puzzle. It's assumed that final position has blank
        tile in upper-left corner.

        Arguments:
            start_state (list): Starting state."""

        self._N = N
        self._N2 = N * N

        end_state = np.arange(self._N2).reshape((self._N, self._N))
        self._end_state = serialize(end_state)

    def _get_neighbors(self, state):
        r"""Returns all states that can be directly obtained from the given
        state. These states are randomly shuffled before returned along with
        proper (unit) weights.

        Arguments:
            state (str, list or np.ndarray): Given state.

        Returns:
            iterable (zip): Tuples of states and weights."""

        def _is_valid(r, c):
            r"""Helper function for veryfing valid moves.

            Arguments:
                r, c: Row and column of blank tile.
            """
            return r >= 0 and c >= 0 and r < self._N and c < self._N

        # state should be np.ndarray because of further calculations
        if isinstance(state, str):
            state = deserialize(state)
        elif isinstance(state, list):
            state = np.array(state)

        br, bc = np.squeeze(np.argwhere(state == 0))  # there is only one blank tile

        # shuffling all possible moves
        moves = [(br + 1, bc), (br - 1, bc), (br, bc + 1), (br, bc - 1)]
        random.shuffle(moves)

        neighbors = []

        for xt_r, xt_c in moves:
            if _is_valid(xt_r, xt_c):  # veryifing correctness
                new_state = np.copy(state)
                new_state[br, bc], new_state[xt_r, xt_c] = \
                    new_state[xt_r, xt_c], new_state[br, bc]  # swapping
                neighbors.append(serialize(new_state))

        return zip(neighbors, [1] * len(neighbors))

    def solve(self, start_state):
        raise NotImplementedError  # each subclass needs to implement this
