from src import helper
from src.helper import Helper


class Board(object):

    def __init__(self):
        self.rows = 'ABCDEFGHI'
        self.columns = '123456789'
        self.placeholder = '.'
        self.boxes = Helper.cross(self.rows, self.columns)
        self.row_units = [Helper.cross(row, self.columns) for row in self.rows]
        self.column_units = [Helper.cross(self.rows, column) for column in self.columns]
        self.square_units = [Helper.cross(row_square, column_square)
                             for row_square in ('ABC', 'DEF', 'GHI')
                             for column_square in ('123', '456', '789')]


    def grid_values(self, grid=None):
        self.grid_dict = {}
        assert grid is not None, "grid should be defined"
        assert len(grid) is 81, "grid should have 81 digits"
        item_index = 0
        for item in grid:
            self._validate(item)
            box = self.boxes[item_index]
            self.grid_dict[box] = item
            item_index = item_index + 1
        return self.grid_dict

    def show(self):
        """
        Display the values as a 2-D grid.
        Input: The sudoku in dictionary form
        Output: None
        """
        width = 1 + max(len(self.grid_dict[s]) for s in self.boxes)
        line = '+'.join(['-' * (width * 3)] * 3)
        for r in self.rows:
            print(''.join(self.grid_dict[r + c].center(width) + ('|' if c in '36' else '')
                          for c in self.columns))
            if r in 'CF': print(line)
        return

    def _validate(self, item):
        if item not in (str(value) for value in range(1, 10)) and item != self.placeholder:
            raise ValueError("grid contains a not valid value: " + item)

    def get_boxes(self):
        return self.boxes

    def get_row_units(self):
        return self.row_units

    def get_column_units(self):
        return self.column_units

    def get_square_units(self):
        return self.square_units
