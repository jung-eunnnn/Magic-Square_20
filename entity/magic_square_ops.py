"""Pure domain operations for the 4x4 magic square puzzle."""

from __future__ import annotations

from constants import MATRIX_SIZE

_CELL_COUNT: int = MATRIX_SIZE * MATRIX_SIZE
_MAGIC_SUM: int = MATRIX_SIZE * (_CELL_COUNT + 1) // 2


def find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Return 0-indexed (row, col) of cells with value 0, in row-major order."""
    out: list[tuple[int, int]] = []
    for r in range(MATRIX_SIZE):
        for c in range(MATRIX_SIZE):
            if grid[r][c] == 0:
                out.append((r, c))
    return out


def find_not_exist_nums(grid: list[list[int]]) -> list[int]:
    """Return the two missing values from 1..n², sorted ascending."""
    present = {
        grid[r][c]
        for r in range(MATRIX_SIZE)
        for c in range(MATRIX_SIZE)
        if grid[r][c] != 0
    }
    full = set(range(1, _CELL_COUNT + 1))
    return sorted(full - present)


def is_magic_square(grid: list[list[int]]) -> bool:
    """True iff the grid is complete (no zeros) and all 10 lines sum to the magic constant."""
    if len(grid) != MATRIX_SIZE or any(len(row) != MATRIX_SIZE for row in grid):
        return False
    if any(grid[r][c] == 0 for r in range(MATRIX_SIZE) for c in range(MATRIX_SIZE)):
        return False
    for r in range(MATRIX_SIZE):
        if sum(grid[r][c] for c in range(MATRIX_SIZE)) != _MAGIC_SUM:
            return False
    for c in range(MATRIX_SIZE):
        if sum(grid[r][c] for r in range(MATRIX_SIZE)) != _MAGIC_SUM:
            return False
    if sum(grid[i][i] for i in range(MATRIX_SIZE)) != _MAGIC_SUM:
        return False
    if sum(grid[i][MATRIX_SIZE - 1 - i] for i in range(MATRIX_SIZE)) != _MAGIC_SUM:
        return False
    return True


def solution(grid: list[list[int]]) -> list[int]:
    """Return ``[r1,c1,n1,r2,c2,n2]`` with 1-based row/col; try smaller missing first, then reverse."""
    g = [row[:] for row in grid]
    blanks = find_blank_coords(g)
    (r1, c1), (r2, c2) = blanks[0], blanks[1]
    missing = find_not_exist_nums(g)
    if len(missing) != 2:
        raise ValueError
    a, b = missing[0], missing[1]

    def try_place(first_val: int, second_val: int) -> list[int] | None:
        trial = [row[:] for row in g]
        trial[r1][c1] = first_val
        trial[r2][c2] = second_val
        if is_magic_square(trial):
            return [r1 + 1, c1 + 1, first_val, r2 + 1, c2 + 1, second_val]
        return None

    out = try_place(a, b)
    if out is not None:
        return out
    out = try_place(b, a)
    if out is not None:
        return out
    raise ValueError
