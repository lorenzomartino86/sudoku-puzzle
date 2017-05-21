from src import helper
from src.helper import Helper


class Board(object):
    def __init__(self, grid=None):
        self.rows = 'ABCDEFGHI'
        self.columns = '123456789'
        self.placeholder = '.'
        self.boxes = Helper.cross(self.rows, self.columns)
        self.row_units = [Helper.cross(row, self.columns) for row in self.rows]
        self.column_units = [Helper.cross(self.rows, column) for column in self.columns]
        self.square_units = [Helper.cross(row_square, column_square)
                             for row_square in ('ABC', 'DEF', 'GHI')
                             for column_square in ('123', '456', '789')]
        unitlist = self.row_units + self.column_units + self.square_units
        units = dict((s, [u for u in unitlist if s in u]) for s in self.boxes)
        self.peers = dict((s, set(sum(units[s],[]))-set([s])) for s in self.boxes)
        self.__build_grid(grid)

    def grid_values(self):
        """
        Returns:
            Sudoku grid with corresponding boxes in dictionary form:
            - keys: Box labels, e.g. 'A1'
            - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
        """
        for key in self.grid:
            value = self.grid[key]
            if value == self.placeholder:
                self.grid[key] = self.columns
            else:
                self.grid[key] = value
        return self.grid

    def eliminate(self):
        """Eliminate values from peers of each box with a single value.

        Go through all the boxes, and whenever there is a box with a single value,
        eliminate this value from the set of values of all its peers.

        Args:
            values: Sudoku in dictionary form.
        Returns:
            Resulting Sudoku in dictionary form after eliminating values.
        """
        for box in self.grid:
            for peer in self.peers[box]:
                peer_digit = self.initial_grid[peer]
                if self.__is_not_same_box(box, peer) \
                        and self.__is_not_all_digits(peer_digit) \
                        and self.__has_an_assigned_value(peer_digit):
                    self.grid[box] = self.grid[box].replace(peer_digit, "")


    def show(self):
        """
        Display the values as a 2-D grid.
        Input: The sudoku in dictionary form
        Output: None
        """
        width = 1 + max(len(self.grid[s]) for s in self.boxes)
        line = '+'.join(['-' * (width * 3)] * 3)
        for r in self.rows:
            print(''.join(self.grid[r + c].center(width) + ('|' if c in '36' else '')
                          for c in self.columns))
            if r in 'CF': print(line)
        return

    def get_boxes(self):
        return self.boxes

    def get_row_units(self):
        return self.row_units

    def get_column_units(self):
        return self.column_units

    def get_square_units(self):
        return self.square_units

    def __build_grid(self, grid):
        """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

               Args:
                   grid: Sudoku grid in string form, 81 characters long
               Returns:
                   Sudoku grid in dictionary form:
                   - keys: Box labels, e.g. 'A1'
                   - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
               """
        self.grid = {}
        assert grid is not None, "grid should be defined"
        assert len(grid) is 81, "grid should have 81 digits"
        item_index = 0
        for item in grid:
            self.__validate(item)
            box = self.boxes[item_index]
            self.grid[box] = item
            item_index = item_index + 1
        self.initial_grid = self.grid.copy()

    def __validate(self, item):
        if item not in (str(value) for value in range(1, 10)) and item != self.placeholder:
            raise ValueError("grid contains a not valid value: " + item)

    def __is_contained(self, box_value, peer_value):
        return peer_value in box_value

    def __is_not_all_digits(self, value):
        return value != self.columns

    def __has_an_assigned_value(self, value):
        return len(value) == 1

    def __is_not_same_box(self, first_box, second_box):
        return first_box != second_box
