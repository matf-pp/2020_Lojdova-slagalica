import sys
import unittest


class TestSolver3x3(unittest.TestCase):
    r"""Unit-testing class for 3x3 puzzles.

    Unit tests are separated based on difficulty. There are exactly 4 types i)
    not solvable ii) easy iii) medium iv) hard."""

    def setUp(self):
        self._solver_callback = sys.argv[1]

    def test_impossible_3x3_1(self):
        start_state = [[1, 2, 3], [0, 4, 5], [6, 8, 7]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, False)

    def test_easy_3x3_2(self):
        start_state = [[2, 3, 5], [1, 4, 0], [7, 8, 6]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)

    def test_medium_3x3_1(self):
        start_state = [[6, 8, 7], [0, 1, 2], [3, 4, 5]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)

    def test_hard_3x3_1(self):
        start_state = [[8, 6, 7], [2, 5, 4], [3, 0, 1]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)

    def test_hard_3x3_2(self):
        start_state = [[6, 4, 7], [8, 5, 0], [3, 2, 1]]

        solver = self._solver_callback(len(start_state))
        result, _ = solver.solve(start_state)

        self.assertEqual(result, True)
