import unittest
import sys

from src.Astar import Astar
from src.WAstar import WAstar
from src.IDAstar import IDAstar

from tests.TestSolver3x3 import TestSolver3x3
from tests.TestSolver4x4 import TestSolver4x4

valid_tags = ["astar", "idastar", "wastar_static", "wastar_dynamic"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise RuntimeError("Solver tag is not provided")
    elif sys.argv[1] not in valid_tags:
        raise ValueError("Solver tag is inappropriate")

    callbacks = {
        "astar": lambda N: Astar(N),
        "idastar": lambda N: IDAstar(N),
        "wastar_static": lambda N: WAstar(N, 4, mode="static"),
        "wastar_dynamic": lambda N: WAstar(N, 4, mode="dynamic")
    }

    # making callback visible to unittest classes
    sys.argv[1] = callbacks[sys.argv[1]]

    # unittest for 3x3 puzzle
    suite3x3 = unittest.TestLoader().loadTestsFromTestCase(TestSolver3x3)
    unittest.TextTestRunner(verbosity=2).run(suite3x3)

    # unittest for 4x4 puzzle
    suite4x4 = unittest.TestLoader().loadTestsFromTestCase(TestSolver4x4)
    unittest.TextTestRunner(verbosity=2).run(suite4x4)
