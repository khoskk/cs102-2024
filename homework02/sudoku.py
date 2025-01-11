import pathlib
import random
import typing as tp
from pprint import pprint

T = tp.TypeVar("T")


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Group values into a list of lists with n elements each.

    >>> group([1, 2, 3, 4], 2)
    [[1, 2], [3, 4]]
    >>> group([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i : i + n] for i in range(0, len(values), n)]


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    return group(digits, 9)


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Read Sudoku from a file."""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def display(grid: tp.List[tp.List[str]]) -> None:
    """Display Sudoku grid in a readable format."""
    for i, row in enumerate(grid):
        print(" ".join(row[:3]), "|", " ".join(row[3:6]), "|", " ".join(row[6:]))
        if i in [2, 5]:
            print("------+-------+------")


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return [grid[i][pos[1]] for i in range(len(grid))]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    block_row, block_col = pos[0] // 3 * 3, pos[1] // 3 * 3
    return [grid[i][j] for i in range(block_row, block_row + 3) for j in range(block_col, block_col + 3)]


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == ".":
                return (i, j)
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    used_values = set(get_row(grid, pos) + get_col(grid, pos) + get_block(grid, pos))
    return set("123456789") - used_values


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    for i in range(9):
        row = get_row(solution, (i, 0))
        col = get_col(solution, (0, i))
        block = get_block(solution, (i // 3 * 3, (i % 3) * 3))
        if set(row) != set("123456789") or set(col) != set("123456789") or set(block) != set("123456789"):
            return False
    return True


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    pos = find_empty_positions(grid)
    if not pos:
        return grid

    row, col = pos
    for value in find_possible_values(grid, pos):
        grid[row][col] = value
        solution = solve(grid)
        if solution:
            return solution
        grid[row][col] = "."

    return None


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    grid = [["." for _ in range(9)] for _ in range(9)]
    for _ in range(17):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while grid[row][col] != ".":
            row, col = random.randint(0, 8), random.randint(0, 8)
        value = random.choice(list(find_possible_values(grid, (row, col))))
        grid[row][col] = value

    solution = solve([row[:] for row in grid])
    if not solution:
        return generate_sudoku(N)

    for _ in range(81 - N):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while grid[row][col] == ".":
            row, col = random.randint(0, 8), random.randint(0, 8)
        grid[row][col] = "."

    return grid


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # Example usage
    puzzle = read_sudoku("puzzle1.txt")
    display(puzzle)
    print("\nSolving Sudoku...")
    solution = solve(puzzle)
    if solution:
        display(solution)
        print("Solution is correct:", check_solution(solution))
    else:
        print("No solution found.")

    print("\nGenerated Sudoku:")
    generated = generate_sudoku(40)
    display(generated)
