"""UI boundary: validate input then produce ``[r1,c1,n1,r2,c2,n2]`` (1-index)."""

from __future__ import annotations

_MAGIC_SUM = 34


def _is_magic_square(grid: list[list[int]]) -> bool:
    if len(grid) != 4 or any(len(row) != 4 for row in grid):
        return False
    if any(grid[r][c] == 0 for r in range(4) for c in range(4)):
        return False
    for r in range(4):
        if sum(grid[r][c] for c in range(4)) != _MAGIC_SUM:
            return False
    for c in range(4):
        if sum(grid[r][c] for r in range(4)) != _MAGIC_SUM:
            return False
    if sum(grid[i][i] for i in range(4)) != _MAGIC_SUM:
        return False
    if sum(grid[i][3 - i] for i in range(4)) != _MAGIC_SUM:
        return False
    return True


def _find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for r in range(4):
        for c in range(4):
            if grid[r][c] == 0:
                out.append((r, c))
    return out


def _find_not_exist_nums(grid: list[list[int]]) -> list[int]:
    present = {grid[r][c] for r in range(4) for c in range(4) if grid[r][c] != 0}
    return sorted(set(range(1, 17)) - present)


def _validate_grid(grid: object) -> list[list[int]]:
    if grid is None:
        raise TypeError
    if not isinstance(grid, list):
        raise TypeError
    if len(grid) != 4:
        raise ValueError
    for row in grid:
        if not isinstance(row, list) or len(row) != 4:
            raise ValueError
        for cell in row:
            if type(cell) is not int:
                raise TypeError
    g: list[list[int]] = grid  # type: ignore[assignment]
    for r in range(4):
        for c in range(4):
            v = g[r][c]
            if v != 0 and not (1 <= v <= 16):
                raise ValueError
    non_zero = [g[r][c] for r in range(4) for c in range(4) if g[r][c] != 0]
    if len(non_zero) != len(set(non_zero)):
        raise ValueError
    blanks = _find_blank_coords(g)
    if len(blanks) != 2:
        raise ValueError
    return g


def solution(grid: list[list[int]]) -> list[int]:
    """Return ``[r1,c1,n1,r2,c2,n2]`` with 1-based row/col; two missing numbers placed."""
    g = [row[:] for row in _validate_grid(grid)]
    blanks = _find_blank_coords(g)
    (r1, c1), (r2, c2) = blanks[0], blanks[1]
    missing = _find_not_exist_nums(g)
    if len(missing) != 2:
        raise ValueError
    a, b = missing[0], missing[1]

    def try_place(first_val: int, second_val: int) -> list[int] | None:
        trial = [row[:] for row in g]
        trial[r1][c1] = first_val
        trial[r2][c2] = second_val
        if _is_magic_square(trial):
            return [r1 + 1, c1 + 1, first_val, r2 + 1, c2 + 1, second_val]
        return None

    out = try_place(a, b)
    if out is not None:
        return out
    out = try_place(b, a)
    if out is not None:
        return out
    raise ValueError
