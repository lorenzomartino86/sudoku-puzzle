from collections import defaultdict

assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [charA + charB
            for charA in A
            for charB in B]

def diagonal_combinations(A, B):
    """ retrieve box key for diagonal units 
        given two string of same length
    """
    assert len(A) == len(B), "A and B strings with different length"
    first_diagonal = list()
    second_diagonal = list()
    dimension = len(A)
    pos = 0
    while (pos < dimension):
        first_diagonal.append(A[pos]+B[pos])
        second_diagonal.append(A[pos]+B[(dimension-1) - pos])
        pos += 1
    return [first_diagonal, second_diagonal]

rows = 'ABCDEFGHI'
columns = '123456789'
boxes = cross(rows, columns)
row_units = [cross(row, columns) for row in rows]
column_units = [cross(rows, column) for column in columns]
square_units = [cross(row_square, column_square)
                             for row_square in ('ABC', 'DEF', 'GHI')
                             for column_square in ('123', '456', '789')]
diagonals = diagonal_combinations(rows, columns)

unitlist = row_units + column_units + square_units + diagonals
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    for unit in unitlist:
        possible_twins = [(box, values[box]) for box in unit if len(values[box]) == 2]
        if len(possible_twins) >= 2:
            twins_by_digit = defaultdict(list)
            for box, digit in possible_twins: twins_by_digit[digit].append(box)
            for digit, boxes in twins_by_digit.items():
                if len(boxes) == 2:
                    values = remove_digit_from_same_unit(boxes, digit, unit, values)
    return values


def remove_digit_from_same_unit(boxes, digit, unit, values):
    for box in unit:
        if box not in boxes:
            for number in digit:
                if number in values[box] and len(values[box]) > 1:
                    values[box] = values[box].replace(number, '')
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert grid is not None, "grid should be defined"
    assert len(grid) is 81, "grid should have 81 digits"
    values = dict()
    index = 0
    for value in grid:
        box = boxes[index]
        if value == '.':
            values[box] = '123456789'
        else:
            values[box] = value
        index += 1
    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in columns))
        if r in 'CF': print(line)
    return

def eliminate(values):
    for box in values:
        for peer in peers[box]:
            peer_digit = values[peer]
            if box != peer and peer_digit != columns \
                and len(peer_digit) == 1:
                values[box] = values[box].replace(peer_digit, "")
    return values

def only_choice(values):
    """     
       Finalize all values that are the only choice for a unit.
       Go through all the units, and whenever there is a unit with a value
       that only fits in one box, assign the value to this box.

       Input: Sudoku in dictionary form.
       Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        digit_frequencies = get_digit_frequencies(unit, values)
        unique_digit_box = {digit: frequency
                            for digit, frequency in digit_frequencies.items()
                            if len(frequency) == 1}
        for update_digit, update_box in unique_digit_box.items():
            values[update_box[0]] = update_digit
    return values

def get_digit_frequencies(boxes, values):
    digit_frequencies = {}
    for box in boxes:
        for digit in list(values[box]):
            digit_frequencies.setdefault(digit, []).append(box)
    return digit_frequencies

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before_strategies = len([box for box in values.keys() if len(values[box]) == 1])

        # Eliminate Strategy
        values = eliminate(values)

        # Only Choice Strategy
        values = only_choice(values)

        # Naked Twins Strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after_strategies = len([box for box in values.keys() if len(values[box]) == 1])

        # If no new values were added, stop the loop.
        stalled = solved_values_before_strategies == solved_values_after_strategies

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values


def search(values):
    """Using depth-first search and propagation, create a search tree and solve the sudoku."""
    reduced_puzzle = reduce_puzzle(values)
    if reduced_puzzle is False:
        return False

    if are_all_box_assigned(values):
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    unfilled_squares = dict((box, len(digit))
                       for (box, digit) in values.items()
                       if len(digit) > 1)
    best_unfilled_square = min(unfilled_squares.keys(), key=(lambda box: unfilled_squares[box]))

    # Now use recursion to solve each one of the resulting sudokus,
    # and if one returns a value (not False), return that answer!
    for digit in values[best_unfilled_square]:
        recursive_values = values.copy()
        recursive_values[best_unfilled_square] = digit
        answer = search(recursive_values)
        if answer:
            return answer

def are_all_box_assigned(values):
    """ check if all box are assigned """
    for box in values:
        if len(values[box]) > 1:
            return False
    return True

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    # Conversion of String into a Grid in dictionary form
    values = grid_values(grid)

    # solver
    values = search(values)

    # display solved sudoku if solved
    if values:
        display(values)

    return values

def check_solution(values):
    for unit in unitlist:
        checked_value = list()
        for box in unit:
            if values[box] in checked_value:
                return False
            checked_value.append(values[box])
    return True


if __name__ == '__main__':
    complex_diagonal_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    solution = solve(complex_diagonal_grid)
    print("Solution is correct" if check_solution(solution) else "Solution is wrong")

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
