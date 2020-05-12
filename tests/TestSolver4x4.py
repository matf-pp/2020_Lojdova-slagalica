import sys
import unittest


class TestSolver4x4(unittest.TestCase):
    """
    Unit-testing class for 4x4 puzzles.

    Unit tests are separated based on difficulty. There are exactly 4 types i)
    not solvable ii) easy iii) medium iv) hard.
    """

    def setUp(self):
        self._solver_callback = sys.argv[1]

    def test_medium_4x4_1(self):
        start_state = [[5, 9, 0, 10], [15, 1, 8, 14],
                       [12, 4, 2, 7], [11, 6, 13, 3]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)

    def test_medium_4x4_2(self):
        start_state = [[8, 6, 11, 12], [14, 7, 4, 9],
                       [1, 13, 5, 0], [2, 10, 3, 15]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)

    def test_medium_4x4_3(self):
        start_state = [[5, 1, 0, 13], [11, 14, 15, 2],
                       [7, 4, 6, 3], [10, 9, 8, 12]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)

    def test_medium_4x4_4(self):
        start_state = [[6, 13, 14, 2], [5, 3, 4, 15],
                       [11, 10, 9, 12], [7, 8, 1, 0]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)

    def test_medium_4x4_5(self):
        start_state = [[8, 2, 13, 14], [4, 15, 6, 5],
                       [9, 10, 3, 12], [11, 0, 7, 1]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)

    def test_medium_4x4_6(self):
        start_state = [[10, 14, 7, 9], [8, 13, 4, 0],
                       [15, 11, 1, 6], [2, 5, 3, 12]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)

    def test_medium_4x4_7(self):
        start_state = [[6, 0, 10, 7], [3, 2, 5, 9],
                       [1, 14, 8, 11], [4, 13, 12, 15]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)

    def test_medium_4x4_8(self):
        start_state = [[8, 11, 3, 2], [15, 6, 9, 7],
                       [1, 4, 12, 10], [14, 13, 5, 0]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)

    def test_medium_4x4_9(self):
        start_state = [[3, 9, 1, 13], [12, 5, 8, 11],
                       [10, 4, 14, 0], [15, 2, 6, 7]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)

    def test_medium_4x4_10(self):
        start_state = [[8, 5, 9, 11], [7, 12, 10, 4],
                       [0, 15, 13, 14], [1, 2, 6, 3]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)

    def test_medium_4x4_11(self):
        start_state = [[1, 12, 3, 6], [9, 2, 0, 11],
                       [4, 8, 13, 7], [5, 10, 15, 14]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)

    def test_medium_4x4_12(self):
        start_state = [[0, 13, 2, 6], [11, 8, 7, 4],
                       [3, 1, 15, 14], [5, 10, 12, 9]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)

    def test_medium_4x4_13(self):
        start_state = [[1, 4, 11, 3], [6, 12, 2, 13],
                       [15, 10, 8, 9], [0, 14, 7, 5]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)

    def test_medium_4x4_14(self):
        start_state = [[5, 11, 14, 3], [8, 2, 12, 13],
                       [4, 0, 7, 10], [1, 6, 9, 15]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)

    def test_medium_4x4_15(self):
        start_state = [[1, 12, 14, 0], [5, 8, 3, 6],
                       [13, 15, 9, 11], [10, 2, 4, 7]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)

    def test_hard_4x4_1(self):
        start_state = [[15, 14, 8, 12], [10, 11, 9, 13],
                       [2, 6, 5, 1], [3, 7, 4, 0]]

        solver = self._solver_callback(len(start_state))
        result, stats = solver.solve(start_state)
        print(stats[0], len(stats[1]))

        self.assertEqual(result, True)
