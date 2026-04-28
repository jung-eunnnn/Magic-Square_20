"""Track A — UI / Boundary RED: ``solution`` 공개 계약만 단언한다.

GREEN 이전에는 ``boundary.magic_square`` 모듈이 없으므로
각 테스트의 첫 ``import`` 또는 ``solution`` 호출에서 실패(RED)한다.

계약 출처: PRD §9.1, §9.5, §10.2; 사용자 입력(6원소·1-index).
"""

from __future__ import annotations

import pytest

# --- 고정 Given (RED 단계에서 테스트 데이터로만 사용) ---
_VALID_PARTIAL_TWO_BLANKS: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]


def _solution(grid: list[list[int]]) -> list[int]:
    """Boundary 진입점. GREEN에서 ``boundary.magic_square`` 가 제공한다."""
    from boundary.magic_square import solution  # type: ignore[import-not-found]

    return solution(grid)


# ---------------------------------------------------------------------------
# BOUND-MS-UI-001 — 4x4가 아닌 입력
# Invariant: FR-1.1 격자 구조; 잘못된 형태는 도메인으로 넘어가지 않음 (INV-01)
# ---------------------------------------------------------------------------
def test_bound_ms_ui_001_non_4x4_raises() -> None:
    """Given: 3x3 행렬 / When: solution 호출 / Then: ValueError."""
    bad = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    with pytest.raises(ValueError):
        _solution(bad)


def test_bound_ms_ui_001_non_rectangular_raises() -> None:
    """Given: 행 길이 불일치 / When: solution / Then: ValueError."""
    bad = [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    with pytest.raises(ValueError):
        _solution(bad)


# ---------------------------------------------------------------------------
# BOUND-MS-UI-002 — 빈칸(0) 개수가 2가 아님
# Invariant: FR-1.2; 빈칸 정확히 2개 (Story 1 AC)
# ---------------------------------------------------------------------------
def test_bound_ms_ui_002_zero_blanks_raises() -> None:
    """Given: 0개 빈칸(완전 채움) / Then: ValueError."""
    full = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, 6, 12],
        [4, 14, 15, 1],
    ]
    with pytest.raises(ValueError):
        _solution(full)


def test_bound_ms_ui_002_one_blank_raises() -> None:
    """Given: 빈칸 1개 / Then: ValueError."""
    one_blank = [row[:] for row in _VALID_PARTIAL_TWO_BLANKS]
    one_blank[3][3] = 1
    with pytest.raises(ValueError):
        _solution(one_blank)


def test_bound_ms_ui_002_three_blanks_raises() -> None:
    """Given: 빈칸 3개 / Then: ValueError."""
    three = [row[:] for row in _VALID_PARTIAL_TWO_BLANKS]
    three[0][0] = 0
    with pytest.raises(ValueError):
        _solution(three)


# ---------------------------------------------------------------------------
# BOUND-MS-UI-003 — 값 범위 위반 (0 제외 1~16)
# Invariant: FR-1.4 INV-01
# ---------------------------------------------------------------------------
def test_bound_ms_ui_003_out_of_range_raises() -> None:
    """Given: 17 포함, 빈칸은 여전히 2곳 / Then: ValueError."""
    g = [row[:] for row in _VALID_PARTIAL_TWO_BLANKS]
    g[0][0] = 17
    with pytest.raises(ValueError):
        _solution(g)


# ---------------------------------------------------------------------------
# BOUND-MS-UI-004 — 중복 (0 제외)
# Invariant: FR-1.3 INV-01
# ---------------------------------------------------------------------------
def test_bound_ms_ui_004_duplicate_raises() -> None:
    """Given: 동일 값 중복 / Then: ValueError."""
    g = [row[:] for row in _VALID_PARTIAL_TWO_BLANKS]
    g[0][0] = 7
    g[1][0] = 7
    with pytest.raises(ValueError):
        _solution(g)


# ---------------------------------------------------------------------------
# BOUND-MS-UI-005 — 반환 길이 6
# Invariant: FR-5.3 출력 형식
# ---------------------------------------------------------------------------
def test_bound_ms_ui_005_result_length_six() -> None:
    """Given: 유효 부분 격자 / When: solution / Then: len(result)==6."""
    result = _solution([row[:] for row in _VALID_PARTIAL_TWO_BLANKS])
    assert len(result) == 6


# ---------------------------------------------------------------------------
# BOUND-MS-UI-006 — 좌표 1-index (1~4), 값은 누락 두 수
# Invariant: FR-5.3; §10.1 좌표 혼동 방지
# ---------------------------------------------------------------------------
def test_bound_ms_ui_006_coordinates_one_indexed() -> None:
    """Given: 유효 부분 격자 / Then: r,c ∈ {1,2,3,4}, n ∈ 1..16."""
    result = _solution([row[:] for row in _VALID_PARTIAL_TWO_BLANKS])
    r1, c1, n1, r2, c2, n2 = result
    for x in (r1, c1, r2, c2):
        assert 1 <= x <= 4
    for n in (n1, n2):
        assert 1 <= n <= 16
    assert n1 != n2


# ---------------------------------------------------------------------------
# BOUND-MS-UI-007 (보강) — 타입 계약: None / 비정수
# Invariant: §10 계약·경계 거부
# ---------------------------------------------------------------------------
def test_bound_ms_ui_007_none_input_raises_type_error() -> None:
    with pytest.raises(TypeError):
        _solution(None)  # type: ignore[arg-type]


def test_bound_ms_ui_007_non_integer_cell_raises_type_error() -> None:
    bad: list[list[object]] = [["16", 2, 3, 13], [5, 11, 10, 8], [9, 7, 0, 12], [4, 14, 15, 0]]
    with pytest.raises(TypeError):
        _solution(bad)  # type: ignore[arg-type]
