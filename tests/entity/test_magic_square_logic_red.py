"""Track B — Logic RED: Entity 순수 함수 계약.

GREEN 이전에는 ``entity.magic_square_ops`` 가 없으므로 import 단계에서 RED.

검증 대상: find_blank_coords, find_not_exist_nums, is_magic_square, solution
출력 계약: solution → int[6], 좌표 1-index [r1,c1,n1,r2,c2,n2]
"""

from __future__ import annotations

import pytest

_VALID_MAGIC_FULL: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 1],
]

_PARTIAL_GHERKIN: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

_INVALID_ROW_SUM: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 9],
    [9, 7, 6, 12],
    [4, 14, 15, 1],
]


def _import_ops() -> object:
    import entity.magic_square_ops as ops  # type: ignore[import-not-found]

    return ops


# ---------------------------------------------------------------------------
# LOGIC-MS-L-001 find_blank_coords — row-major, 정확히 2좌표 (0-index)
# Invariant: FR-2.1, FR-2.2, FR-2.3
# ---------------------------------------------------------------------------
def test_logic_ms_l_001_find_blank_coords_row_major_two_cells() -> None:
    ops = _import_ops()
    find_blank_coords = ops.find_blank_coords
    coords = find_blank_coords([row[:] for row in _PARTIAL_GHERKIN])
    assert coords == [(2, 2), (3, 3)]


# ---------------------------------------------------------------------------
# LOGIC-MS-L-002 find_not_exist_nums — 누락 2개, 오름차순
# Invariant: FR-3.1, FR-3.2, FR-3.3
# ---------------------------------------------------------------------------
def test_logic_ms_l_002_find_not_exist_nums_sorted_pair() -> None:
    ops = _import_ops()
    find_not_exist_nums = ops.find_not_exist_nums
    missing = find_not_exist_nums([row[:] for row in _PARTIAL_GHERKIN])
    assert missing == [1, 6]


# ---------------------------------------------------------------------------
# LOGIC-MS-L-003 is_magic_square — 10선 합 34, 완전 격자
# Invariant: FR-4, INV-02, INV-03; 매직 합 _MAGIC_SUM
# ---------------------------------------------------------------------------
def test_logic_ms_l_003_is_magic_true_on_known_square() -> None:
    ops = _import_ops()
    assert ops.is_magic_square([row[:] for row in _VALID_MAGIC_FULL]) is True


def test_logic_ms_l_003_is_magic_false_when_row_wrong() -> None:
    ops = _import_ops()
    assert ops.is_magic_square([row[:] for row in _INVALID_ROW_SUM]) is False


# ---------------------------------------------------------------------------
# LOGIC-MS-L-004 solution — FR-5 시도 순서 (small→first, 실패 시 reverse)
# Invariant: FR-5.1~FR-5.3; Level 4 Gherkin 동일 Given
# ---------------------------------------------------------------------------
def test_logic_ms_l_004_solution_length_six_one_indexed() -> None:
    ops = _import_ops()
    out = ops.solution([row[:] for row in _PARTIAL_GHERKIN])
    assert len(out) == 6
    r1, c1, n1, r2, c2, n2 = out
    assert all(1 <= x <= 4 for x in (r1, c1, r2, c2))


def test_logic_ms_l_004_solution_gherkin_grid_expected_placement() -> None:
    """역순 시도로 성립하는 Given: (3,3)=6, (4,4)=1 (1-index)."""
    ops = _import_ops()
    out = ops.solution([row[:] for row in _PARTIAL_GHERKIN])
    assert out == [3, 3, 6, 4, 4, 1]


def test_logic_ms_l_004_solution_filled_grid_is_magic() -> None:
    """배치 후 완전 격자가 is_magic_square 를 만족."""
    ops = _import_ops()
    r1, c1, n1, r2, c2, n2 = ops.solution([row[:] for row in _PARTIAL_GHERKIN])
    g = [row[:] for row in _PARTIAL_GHERKIN]
    g[r1 - 1][c1 - 1] = n1
    g[r2 - 1][c2 - 1] = n2
    assert ops.is_magic_square(g) is True


# ---------------------------------------------------------------------------
# LOGIC-MS-L-005 (보강) — is_magic_square 거부 케이스
# Invariant: 완전 격자에서 합·대각 불일치 시 False
# ---------------------------------------------------------------------------
def test_logic_ms_l_005_is_magic_false_bad_main_diagonal() -> None:
    ops = _import_ops()
    m = [row[:] for row in _VALID_MAGIC_FULL]
    m[0][0], m[3][3] = m[3][3], m[0][0]
    assert ops.is_magic_square(m) is False
