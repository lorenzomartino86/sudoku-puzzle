import unittest
from unittest import TestCase

from src.board import Board


class TestBoard(TestCase):


    def test_not_grid(self):
        with self.assertRaises(AssertionError):
            board = Board()

    def test_too_long_grid(self):
        grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......' \
                      '8..67.82....26.95..8..2.3..9..5.1.3..' \
                      '........'
        with self.assertRaises(AssertionError):
            Board(grid)

    def test_wrong_placeholder_grid(self):
        grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......' \
                      '8..67.82....26.95..8..2.3..9..5.1.3.*'
        with self.assertRaises(ValueError):
            Board(grid)

    def test_correct_grid(self):
        grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......' \
                      '8..67.82....26.95..8..2.3..9..5.1.3..'
        board = Board(grid)

    def test_correspondences_grid(self):
        grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......' \
                      '8..67.82....26.95..8..2.3..9..5.1.3..'
        board = Board(grid)
        correspondences = board.grid_values()
        self.assertEqual(correspondences['A1'], '123456789')
        self.assertEqual(correspondences['A3'], '3')

    def test_eliminate(self):
        grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......' \
               '8..67.82....26.95..8..2.3..9..5.1.3..'
        board = Board(grid)
        values = board.grid_values()
        values = board.eliminate(values)
        self.assertEqual(values['A1'], '45')

    def test_only_choice(self):
        grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......' \
               '8..67.82....26.95..8..2.3..9..5.1.3..'
        board = Board(grid)
        values = board.grid_values()
        values = board.eliminate(values)
        values = board.only_choice(values)

    def test_reduce_puzzle(self):
        grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......' \
               '8..67.82....26.95..8..2.3..9..5.1.3..'
        board = Board(grid)
        values = board.grid_values()
        values = board.reduce_puzzle(values)
        self.assertEqual(values['A1'], '4')
        self.assertEqual(values['B1'], '9')
        self.assertEqual(values['C1'], '2')
        self.assertEqual(values['D1'], '5')
        self.assertEqual(values['E1'], '7')
        self.assertEqual(values['F1'], '1')
        self.assertEqual(values['G1'], '3')
        self.assertEqual(values['H1'], '8')
        self.assertEqual(values['I1'], '6')

    def test_harder_sudoku(self):
        """
         test to assert that with a harder sudoku grid the algorithm is not enouth to solve this 
         kind of problem
        """
        grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
        board = Board(grid2)
        values = board.grid_values()
        values = board.reduce_puzzle(values)
        board.show(values)
        self.assertEqual(values['A1'], '4')
        self.assertEqual(values['B1'], '9')
        self.assertEqual(values['C1'], '2')
        self.assertEqual(values['D1'], '5')
        self.assertEqual(values['E1'], '7')
        self.assertEqual(values['F1'], '1')
        self.assertEqual(values['G1'], '3')
        self.assertEqual(values['H1'], '8')
        self.assertEqual(values['I1'], '6')






if __name__ == '__main__':
    unittest.main()