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
        self.unitlist = self.row_units + self.column_units + self.square_units
        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.boxes)
        self.peers = dict((s, set(sum(self.units[s], [])) - set([s])) for s in self.boxes)
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

    def eliminate(self, values):
        """ First technique of reduce a Sudoku
        Eliminate values from peers of each box with a single value.

        Go through all the boxes, and whenever there is a box with a single value,
        eliminate this value from the set of values of all its peers.

        Args:
            values: Sudoku in dictionary form.
        Returns:
            Resulting Sudoku in dictionary form after eliminating values.
        """
        for box in values:
            for peer in self.peers[box]:
                peer_digit = values[peer]
                if self.__is_not_same_box(box, peer) \
                        and self.__is_not_all_digits(peer_digit) \
                        and self.__has_an_assigned_value(peer_digit):
                    values[box] = values[box].replace(peer_digit, "")
        return values

    def only_choice(self, values):
        """ Second technique of reduce a Sudoku
        Finalize all values that are the only choice for a unit.

        Go through all the units, and whenever there is a unit with a value
        that only fits in one box, assign the value to this box.

        Input: Sudoku in dictionary form.
        Output: Resulting Sudoku in dictionary form after filling in only choices.
        """
        for unit in self.unitlist:
            digit_frequencies = self.__get_digit_frequencies(unit, values)
            unique_digit_box = {digit: frequency
                                    for digit, frequency in digit_frequencies.items()
                                                    if len(frequency) == 1}
            for update_digit, update_box in unique_digit_box.items():
                values[update_box[0]] = update_digit
        return values

    def reduce_puzzle(self, values):
        """
        
        :param values: Sudoku grid as dict type
        :return: resolved Sudoku in dictionary form
        """
        stalled = False
        while not stalled:
            # Check how many boxes have a determined value
            solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

            # Your code here: Use the Eliminate Strategy
            values = self.eliminate(values)

            # Your code here: Use the Only Choice Strategy
            values = self.only_choice(values)

            # Check how many boxes have a determined value, to compare
            solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
            # If no new values were added, stop the loop.
            stalled = solved_values_before == solved_values_after
            # Sanity check, return False if there is a box with zero available values:
            if len([box for box in values.keys() if len(values[box]) == 0]):
                return False
        return values

    def search(self, values):
        "Using depth-first search and propagation, create a search tree and solve the sudoku."
        # First, reduce the puzzle using the previous function
        reduced_puzzle = self.reduce_puzzle(values)
        if reduced_puzzle is False:
            return False

        if self.__all_box_assigned(values):
            return values

        # Choose one of the unfilled squares with the fewest possibilities
        number_of_possibilities = lambda digit: len(digit)

        frequencies = dict((box, number_of_possibilities(digit))
               for (box, digit) in values.items()
                       if len(digit) > 1)
        best_unfilled_box = min(frequencies.keys(), key=(lambda box: frequencies[box]))

        # Now use recursion to solve each one of the resulting sudokus,
        # and if one returns a value (not False), return that answer!
        for digit in values[best_unfilled_box]:
            recursive_values = values.copy()
            recursive_values[best_unfilled_box] = digit
            answer = self.search(recursive_values)
            if answer:
                return answer

    def naked_twins(self, values):
        """Eliminate values using the naked twins strategy.
        Args:
            values(dict): a dictionary of the form {'box_name': '123456789', ...}

        Returns:
            the values dictionary with the naked twins eliminated from peers.
        """
        self.show(values)

        if self.__all_box_assigned(values):
            return values

        values = self.eliminate(values)

        # Find all instances of naked twins
        twins_list = self.__all_naked_twins(values)
        print ("\n\ntwins --> ", twins_list, "\n\n")

        # Eliminate the naked twins as possibilities for their peers
        for twins in twins_list:
            digits = values[twins[0]]
            values = self.__eliminate_values_from_peers(twins, digits, values)

        return self.naked_twins(values)





    def show(self, values):
        """
        Display the values as a 2-D grid.
        Input: The sudoku in dictionary form
        Output: None
        """
        width = 1 + max(len(values[s]) for s in self.boxes)
        line = '+'.join(['-' * (width * 3)] * 3)
        for r in self.rows:
            print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
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

    def get_undefined_boxes(self, square):
        return [box for box in square if not self.__has_an_assigned_value(self.grid[box])]

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

    def __get_digit_frequencies(self, boxes, values):
        digit_frequencies = {}
        for box in boxes:
            for digit in list(values[box]):
                digit_frequencies.setdefault(digit, []).append(box)
        return digit_frequencies

    def __all_box_assigned(self, values):
        for box in values:
            if len(values[box]) > 1:
                return False
        return True

    def __all_naked_twins(self, values):
        twins = {}
        two_digits_boxes = [(box, values[box]) for box in values if len(values[box]) == 2]
        for box, value in two_digits_boxes:
            for unit in self.units[box]:
                box_unit_list = [box_unit for box_unit in unit
                                 if box_unit != box and values[box_unit] == value]

                for twin in box_unit_list:
                    twins.setdefault(value, list())
                    twins[value].append(twin)
                    #print("added ", twin, values[twin], box, value)

        twins = list(boxes for boxes in twins.values()
                     if len(boxes) == 2)
        return twins

    def __eliminate_values_from_peers(self, twins, digits_to_be_removed, values):
        digits_to_be_removed = list(digits_to_be_removed)
        boxA = twins[0]
        boxB = twins[1]
        for peer in self.peers[boxA]:
            if peer != boxB and len(values[peer]) > 1:
                for digit in values[peer]:
                    if digit in digits_to_be_removed:
                        print ("removing ", digit, " from ", peer)
                        values[peer].replace(digit, '')

        for peer in self.peers[boxB]:
            if peer != boxA and len(values[peer]) > 1:
                for digit in values[peer]:
                    if digit in digits_to_be_removed:
                        print("removing ", digit, " from ", peer)
                        values[peer].replace(digit, '')
        return values






