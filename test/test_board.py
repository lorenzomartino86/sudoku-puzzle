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
        board.grid_values()
        board.eliminate()
        grid_dict = board.grid_dict
        self.assertEqual(grid_dict['A1'], '45')
        self.assertEqual(grid_dict['A3'], '3')
        #self.assertEqual(grid_dict['E8'], '13456')
        print(board.show())



if __name__ == '__main__':
    unittest.main()