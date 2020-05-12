import argparse
import time

import numpy as np


r"""Generator of unit-tests. It's reproducible in case seed is known."""


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, required=True,
                        help="Size of puzzle.")
    parser.add_argument("--n_tests", type=int, required=True,
                        help="Number of tests that will be generated.")
    parser.add_argument("--seed", type=int, default=42, help="Radom seed.")
    args = parser.parse_args()

    N = args.size
    n_tests = args.n_tests

    seed = args.seed
    np.random.seed(seed)

    f_name = "tests_" + time.strftime("%Y%m%d-%H%M%S") + ".txt"
    with open(f_name, "w") as f:
        print(seed, file=f)
        state = np.arange(N * N)

        for test_id in range(n_tests):
            np.random.shuffle(state)
            print(state.reshape((N, N)).tolist(), file=f)
