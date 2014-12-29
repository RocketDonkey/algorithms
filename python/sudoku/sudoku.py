"""Yet Another Sudoku Solver.

This is a simple script meant to help my mom when she gets stuck on Sudoku
puzzles and just wants a hint.
"""

import itertools
import os
import sys

ALL_VALUES = {str(val) for val in range(1, 10)}


CELL_POSSIBILITIES = {(row, col): ALL_VALUES.copy()
                      for row in range(9) for col in range(9)}


USAGE = """\
Usage: python sudoku.py path/to/file [hint_row hint_column]

'file' should be a 9x9 grid representing the puzzle to solve, where a dot (.)
represents unsolved squares. Whitespace is ignored, so you can add
newlines/padding to make input easier.

hint_row / hint_column are the x and y coordinates of a cell for which to
determine the correct value. Note that both values must be provided.

Example:

..5 ..3 .4.
..7 ..9 12.
.2. ... ...

.5. 816 ..3
4.. 3.7 ..6
1.. 492 .5.

... ... .3.
.34 5.. 8..
.8. 2.. 9..
"""


def MakeGrid(input_string):
  """Covert an 81-character string of text into a sudoku grid.

  Args:
    input_string: An 81-character string of text, where every 9 characters
        represents a row.

  Returns:
    A list of lists, where each inner list contains 9 items representing the
        value at that particular row/column.
  """
  grid = [['.' for _ in range(9)] for _ in range(9)]
  for index, value in enumerate(_ProcessInput(input_string)):
    # Row: index / 9 | column: index % 9
    grid[index / 9][index % 9] = value
  return grid


def _ProcessInput(input_string):
  """Strip all whitespace from the input string.

  Args:
    input_string: An 81-character string of text, where every 9 characters
        represents a row.

  Returns:
    An 81-character string of text with all whitespace removed.
  """
  return ''.join(char.strip() for char in input_string if char.strip())


def IdentifyChoices(grid, row, col):
  """Identify the possible choices for a (row, column) cell.

  The possible choices for a cell is the set of all legal values, where a legal
  value is one that, if chosen, does not result in an immediate 'impossible'
  state. For example, if a row contains the number 1, adding a 1 into any other
  cell in that row would result in an impossible state.

  Args:
    grid: A list of lists, where each inner list contains 9 items representing
        the value at that particular row/column.
    row: The integer row number of the cell for which to calculate choices.
    column: The integer column number of the cell for which to calculate
        choices.

  Returns:
    A set containing all possible legal choices for a particular cell.
  """
  # Rows.
  used = {grid[row][idx] for idx in range(9)}

  # Columns.
  used.update({grid[idx][col] for idx in range(9)})

  # Blocks. Normalize the row and column numbers to be the closest (lowest)
  # multiple of three.
  row = (row // 3) * 3
  col = (col // 3) * 3

  for row_idx in range(row, row+3):
    for col_idx in range(col, col+3):
      used.add(grid[row_idx][col_idx])

  used.discard('.')
  return used


def PrintGrid(grid):
  """Print the grid in 'human-readable' form.

  Args:
    grid: A 9-item iterable, where each item is itself a 9-item iterable.
  """
  for row_index, row in enumerate(grid, 1):
    row_ = []
    for val_idx, value in enumerate(row, 1):
      row_.append(value + ' ' + ('|' if val_idx in (3, 6) else ''))
    print '{}'.format(''.join(row_))
    if not row_index % 3:
      print '+'.join('-' * 6 for _ in range(3))


def SinglePossibility(grid):
  """Run the 'Single Possibility' strategy over a grid.

  The Single Possibility strategy simply looks at each cell, and in the case
  that there is only one legal choice, fills in the cell with that value.

  Args:
    grid: A 9-item iterable, where each item is itself a 9-item iterable.

  Returns:
    The input grid, with all single possibility candidates filled in.
  """
  changes = True
  total_changes = 0
  while changes:
    changes = False
    for row_idx, col_idx in itertools.product(xrange(9), xrange(9)):
      if grid[row_idx][col_idx] == '.':
        choices = ALL_VALUES - IdentifyChoices(grid, row_idx, col_idx)

        if len(choices) == 1:
          IdentifyChoices(grid, row_idx, col_idx)
          # Set the new value
          value = choices.pop()
          grid[row_idx][col_idx] = value
          changes = True
          total_changes += 1

  return grid


def ShowOutput(grid, hint_row, hint_col):
  """Print the requested input to the console.

  Args:
    grid: The grid to print to the console.
    hint_row: The row number of the cell for which to provide a hint.
    hint_col: The column number of the cell for which to provide a hint.
  """
  # Print the input puzzle.
  print '{:*^19}'.format('Input puzzle')
  PrintGrid(grid)

  # Apply the 'Single Possibility' strategy to the current grid.
  grid = SinglePossibility(grid)

  # Determine if a hint is requested. If not, print the entire solution.
  if hint_row:
    print '\nThe value at cell (%s, %s) is %s\n' % (
        hint_row,
        hint_col,
        grid[int(hint_row)-1][int(hint_col)-1]
    )
  else:
    print '\n{:*^19}'.format('Solved puzzle')
    PrintGrid(grid)


def main():
  """Solve a sudoku puzzle."""
  argv_len = len(sys.argv)
  hint_row = hint_col = None
  if argv_len < 2 or argv_len > 4 or argv_len == 3:
    print USAGE
    sys.exit(1)

  if argv_len == 4:
    hint_row, hint_col = sys.argv[-2:]

  # Generate the grid for the input puzzle.
  filename = sys.argv[1]
  with open(filename) as f:
    grid = MakeGrid(f.read())

  ShowOutput(grid, hint_row, hint_col)


if __name__ == '__main__':
  main()
