import time

import numpy as np

from permutation import Permutation


def generate_state(N):
    r"""Generate random state and determine if it's solvable."""
    state = np.arange(N * N)

    timestamp = int(time.time())
    np.random.seed(timestamp)
    np.random.shuffle(state)
    state = state.reshape((N, N)).tolist()

    return state, is_solvable(state)


def reconstruct_path(parent, state):
    r"""
    Reconstructs the shortest path in the search tree.

    It's assumed that starting node have `None` as a parent.

    Arguments:
        parent (dict): Dictionary of parents for each node.
        state (str): Hash of the terminating state.
    """

    path = [state]

    while parent[state] is not None:
        state = parent[state]
        path.append(state)

    return path[::-1]


def deserialize(hash_val):
    r"""
    Deserialization of the given string.

    Arguments:
        hash_val (str): Serialized state.
    Returns:
        state (np.ndarray): Deserialized state.
    """

    state = hash_val.split(':')
    state = [int(x) for x in state]
    N = int(np.round(np.sqrt(len(state))))

    return np.array(state).reshape((N, N))


def h(state):
    r"""
    Calculates Manhattan distance between given state and final state.

    Used as a heuristics for A* variants.

    Arguments:
        state (str, np.ndarray or list): Given state.
    Returns:
        cost (int): Manhattan distance between goal and given state.
    """

    # state has to be either list of np.ndarray for further calculations
    if isinstance(state, str):
        state = deserialize(state)

    # calculating state's dimension
    if isinstance(state, np.ndarray):
        N = state.shape[0]
    elif isinstance(state, list):
        N = len(N)

    # summing distances for all tiles
    cost = 0
    for i, row in enumerate(state):
        for j, x in enumerate(row):
            cost += abs(x % N - j) + abs(x // N - i)

    return cost


def serialize(state):
    r"""
    Serializing given state.

    It's basically 2D array flattening.

    Arguments:
        state (list or np.ndarray): Given state.
    Returns:
        hash value (str): Serialized state.
    """

    # flattening either 2D list or 2D np.ndarray
    if isinstance(state, list):
        hash_val = sum(state, [])
    elif isinstance(state, np.ndarray):
        hash_val = state.flatten()

    hash_val = [str(x) for x in hash_val]

    return ':'.join(hash_val)


def is_solvable(state):
    r"""
    Determines if its given puzzle solvable.

    It's done by calculating sign of sum of the state's permutation and
    Manhattan distance of empty cell. If aforementioned sum is odd there is no
    solution.

    Arguments:
        state (str, list or np.ndarray): Given state.
    Returns:
        flag (bool): True if it's possible to solve the puzzle and false
            otherwise.
    """

    # np.ndarray is necessary for futher calculations
    if isinstance(state, str):
        state = deserialize(state)
    elif isinstance(state, list):
        state = np.array(state)

    p = (state + 1).flatten()  # elements have to be positive
    p = Permutation(*p)
    sign = 0 if p.is_even else 1

    r, c = np.squeeze(np.argwhere(state == 0))

    return (sign + r + c) % 2 == 0
