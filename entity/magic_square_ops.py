"""Pure domain operations for the 4x4 magic square puzzle."""

from __future__ import annotations

from constants import MATRIX_SIZE


def find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Return 0-indexed (row, col) of cells with value 0, in row-major order."""
    out: list[tuple[int, int]] = []
    for r in range(MATRIX_SIZE):
        for c in range(MATRIX_SIZE):
            if grid[r][c] == 0:
                out.append((r, c))
    return out
