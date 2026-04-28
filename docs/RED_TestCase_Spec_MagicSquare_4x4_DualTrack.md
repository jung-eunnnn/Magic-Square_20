# Magic Square 4×4 — Dual-Track RED 테스트 케이스 명세

| 항목 | 내용 |
|------|------|
| 문서 유형 | RED 단계 전용 테스트 설계 (구현·GREEN·REFACTOR 없음) |
| 방법론 | Track A — UI/Boundary, Track B — Logic |
| 계약 출처 | `docs/PRD_MagicSquare_4x4.md`, 명세 이미지(TC-MS-*) |
| 구현 | 본 문서는 **코드를 작성하지 않음**. 구현 부재 시 모든 해당 자동화 테스트는 **실패(RED)** 상태가 정상이다. |

---

## 입력·출력·상수 (고정)

| 구분 | 내용 |
|------|------|
| 입력 | `int[][]`, 4×4, `0` = 빈칸, 빈칸 **정확히 2개**, 비빈칸 값 1~16, 0 제외 중복 없음 |
| 출력 | `int[6]` = `[r1, c1, n1, r2, c2, n2]`, 좌표 **1-index** (1~4) |
| 마방진 합 | 4×4 → **34** (행·열·주·부 대각선) |

---

## RED 상태에 대한 공통 설명

- **Track A**: 공개 경계 API(예: `boundary.magic_square.solution`) 호출 시 `import` 실패 또는 검증 실패로 **RED**.
- **Track B**: Entity 순수 함수(예: `entity.magic_square_ops`) 미구현 시 `import` 실패로 **RED**; 구현 후에도 스펙 불일치 시 **RED** 유지.
- 본 명세는 **기대 행위만** 정의한다. GREEN에서만 구현을 채운다.

---

# UI RED Tests

경계 계약: 격자 형태, 빈칸 개수, 값 도메인, 중복, **관측 가능한** 출력 형식(길이 6, 1-index 좌표).

| Test ID (문서) | 구현측 추적 ID (선택) | TC-MS 매핑 (참고) |
|----------------|----------------------|-------------------|
| UI-RED-01 | BOUND-MS-UI-001 | TC-MS-D-003, D-006 |
| UI-RED-02 | BOUND-MS-UI-002 | TC-MS-A-003, A-004, A-005 |
| UI-RED-03 | BOUND-MS-UI-003 | TC-MS-D-001 |
| UI-RED-04 | BOUND-MS-UI-004 | TC-MS-D-002 |
| UI-RED-05 | BOUND-MS-UI-005 | TC-MS-C-001 (출력 형식) |
| UI-RED-06 | BOUND-MS-UI-006 | TC-MS-C-001, C-002 |
| UI-RED-07 (보강) | BOUND-MS-UI-007 | TC-MS-D-004, D-005 |

---

### UI-RED-01 — 4×4가 아닌 입력은 예외

- **테스트 이름(예시)**: `test_bound_ms_ui_001_non_4x4_raises` / `test_bound_ms_ui_001_non_rectangular_raises`
- **Given**: (a) 3×3 정수 행렬, 또는 (b) 4행이지만 한 행의 길이가 4가 아닌 비직사각 격자
- **When**: 경계 `solution(grid)` 호출
- **Then**: `ValueError` 발생 (도메인으로 잘못된 형태가 넘어가지 않음)
- **계약 설명**: FR 격자 구조 불변 — **반드시 4×4 직사각**이어야 유스케이스가 성립한다.
- **Scenario**: 잘못된 크기·형태의 입력을 거부한다.
- **Invariant 보호 내용**: **INV-격자 차원** — 입력이 4×4가 아니면 해석·솔브를 시도하지 않는다.

---

### UI-RED-02 — 빈칸(0)이 정확히 2개가 아니면 예외

- **테스트 이름(예시)**: `test_bound_ms_ui_002_zero_blanks_raises`, `test_bound_ms_ui_002_one_blank_raises`, `test_bound_ms_ui_002_three_blanks_raises`
- **Given**: 4×4이나 0의 개수가 0, 1, 3 이상인 격자 (그 외 숫자는 스펙에 맞게 조정 가능)
- **When**: `solution(grid)` 호출
- **Then**: `ValueError` 발생
- **계약 설명**: 스토리 AC — **빈칸은 정확히 두 칸**만 허용; 그 외는 부분 해 문제로 정의되지 않음.
- **Scenario**: 빈칸 개수 위반 시 즉시 거부한다.
- **Invariant 보호 내용**: **INV-빈칸 개수** — “정확히 두 미지수” 가정이 깨지면 솔버 전제가 무너진다.

---

### UI-RED-03 — 값 범위 위반 시 예외

- **테스트 이름(예시)**: `test_bound_ms_ui_003_out_of_range_raises`
- **Given**: 4×4, 빈칸 2개 유지, 비빈칸 셀에 **17** 등 1~16 밖의 정수 포함
- **When**: `solution(grid)` 호출
- **Then**: `ValueError` 발생
- **계약 설명**: 1~16 집합 위배는 완성 마방진 후보 공간 밖이다.
- **Scenario**: 셀 값이 허용 도메인을 벗어나면 거부한다.
- **Invariant 보호 내용**: **INV-값 도메인** — 마방진 조각은 항상 {1,…,16}의 부분집합이어야 한다.

---

### UI-RED-04 — 중복 숫자(0 제외) 시 예외

- **테스트 이름(예시)**: `test_bound_ms_ui_004_duplicate_raises`
- **Given**: 4×4, 빈칸 2개, 비빈칸에 동일한 1~16 값이 두 번 이상 등장
- **When**: `solution(grid)` 호출
- **Then**: `ValueError` 발생
- **계약 설명**: 완성 시 1~16 순열이 되어야 하므로 입력 단계에서 중복은 모순이다.
- **Scenario**: 0을 제외한 중복이 있으면 거부한다.
- **Invariant 보호 내용**: **INV-순열 전제** — 비빈칸은 서로 다른 기호만 허용한다.

---

### UI-RED-05 — 반환 배열 길이는 6

- **테스트 이름(예시)**: `test_bound_ms_ui_005_result_length_six`
- **Given**: 스펙을 만족하는 유효 부분 격자(빈칸 2, 1~16, 중복 없음)
- **When**: `solution(grid)` 호출
- **Then**: 반환 `list`의 `len == 6`
- **계약 설명**: 공개 출력 계약은 **항상 6원소** (두 빈칸 각각의 행·열·값).
- **Scenario**: 성공 경로에서도 출력 형식이 고정 길이다.
- **Invariant 보호 내용**: **INV-출력 형식** — `[r1,c1,n1,r2,c2,n2]` 스키마 위반을 방지한다.

---

### UI-RED-06 — 반환 좌표는 1-index

- **테스트 이름(예시)**: `test_bound_ms_ui_006_coordinates_one_indexed`
- **Given**: 동일 유효 부분 격자
- **When**: `solution(grid)` 호출
- **Then**: `r1,c1,r2,c2` 각각 ∈ {1,2,3,4}; `n1,n2` ∈ {1,…,16} 이고 서로 다름(누락된 두 수)
- **계약 설명**: UI·외부 API와의 좌표계 혼동 방지 — **0-index 금지**.
- **Scenario**: 좌표가 1부터 시작하는 행·열 번호로만 반환된다.
- **Invariant 보호 내용**: **INV-좌표계** — 경계 관측 가능한 값은 항상 1-index다.

---

### UI-RED-07 (보강) — 타입 무결성

- **테스트 이름(예시)**: `test_bound_ms_ui_007_none_input_raises_type_error`, `test_bound_ms_ui_007_non_integer_cell_raises_type_error`
- **Given**: `None`, 또는 셀에 문자열 등 비정수
- **When**: `solution(...)` 호출
- **Then**: `TypeError` 발생
- **계약 설명**: 정수 격자가 아니면 해석 불가.
- **Scenario**: 잘못된 타입은 조용히 통과시키지 않는다.
- **Invariant 보호 내용**: **INV-타입** — 입력은 `int` 이차원 배열 구조여야 한다.

---

# Logic RED Tests

Entity 순수 함수: `find_blank_coords`, `find_not_exist_nums`, `is_magic_square`, `solution`. Boundary와 **다른 모듈**에서 검증한다.

| Test ID (문서) | 구현측 추적 ID (선택) | TC-MS 매핑 (참고) |
|----------------|----------------------|-------------------|
| LOGIC-RED-01 | LOGIC-MS-L-001 | TC-MS-A-001, A-002 |
| LOGIC-RED-02 | LOGIC-MS-L-002 | (누락 수 식별) |
| LOGIC-RED-03 | LOGIC-MS-L-003, L-005 | TC-MS-B-001 ~ B-005 |
| LOGIC-RED-04 | LOGIC-MS-L-004 | TC-MS-C-001, C-002 |

---

### LOGIC-RED-01 — `find_blank_coords()`

- **테스트 이름(예시)**: `test_logic_ms_l_001_find_blank_coords_row_major_two_cells`
- **Given**: 고정 부분 격자(예: `_PARTIAL_GHERKIN` — (0-index) (2,2), (3,3)에 0)
- **When**: `find_blank_coords(grid)` 호출
- **Then**: **row-major** 순서로 빈칸 좌표 **정확히 2개** 반환; 위 Given이면 `[(2,2),(3,3)]` (**함수 내부 관례가 0-index이면 이 형태**, PRD/팀이 1-index로 통일했다면 명세에 맞춰 단언 수정)
- **실패(RED) 명확화**: 모듈 미존재 시 import 실패; 구현 시 순서·개수·좌표 하나라도 틀리면 RED.
- **Scenario**: 두 빈칸의 위치를 읽기 순서대로 식별한다.
- **Invariant 보호 내용**: **INV-빈칸 위치·순서** — 탐색 순서가 알고리즘(작은 수→첫 빈칸 시도)과 일치하도록 고정된다.

---

### LOGIC-RED-02 — `find_not_exist_nums()`

- **테스트 이름(예시)**: `test_logic_ms_l_002_find_not_exist_nums_sorted_pair`
- **Given**: 위와 동일 부분 격자(1~16 중 격자에 없는 두 수가 정해짐)
- **When**: `find_not_exist_nums(grid)` 호출
- **Then**: 누락된 두 정수를 **오름차순** 리스트로 반환 (예: `[1, 6]`)
- **실패(RED) 명확화**: import 실패 또는 정렬·집합 연산 오류 시 RED.
- **Scenario**: 0을 제외한 나머지 14개로부터 {1,…,16}의 보충 2개를 계산한다.
- **Invariant 보호 내용**: **INV-순열 보충** — 채울 수 있는 후보는 정확히 두 수이며 순서 규약은 오름차순이다.

---

### LOGIC-RED-03 — `is_magic_square()`

- **테스트 이름(예시)**: `test_logic_ms_l_003_is_magic_true_on_known_square`, `test_logic_ms_l_003_is_magic_false_when_row_wrong`, `test_logic_ms_l_005_is_magic_false_bad_main_diagonal`
- **Given**: (1) 알려진 완전 유효 4×4 마방진; (2) 한 행의 합이 34가 아닌 완전 격자; (3) 주대각선 합이 깨지도록 스왑한 변형 등
- **When**: `is_magic_square(complete_grid)` 호출
- **Then**: (1) `True`; (2)(3) `False` — **행·열·주대각·부대각** 모두 합 34일 때만 `True`
- **실패(RED) 명확화**: 임의의 합 상수 하드코딩 오류, 대각선 누락 시 GREEN 불가.
- **Scenario**: 완전 격자에 대해 10개 선(행4+열4+대각2)의 합이 34와 일치하는지 판정한다.
- **Invariant 보호 내용**: **INV-마방진 정의** — 4×4 표준 마방진 합 **34**; 한 줄이라도 어긋나면 거짓.

---

### LOGIC-RED-04 — `solution()`

- **테스트 이름(예시)**: `test_logic_ms_l_004_solution_length_six_one_indexed`, `test_logic_ms_l_004_solution_gherkin_grid_expected_placement`, `test_logic_ms_l_004_solution_filled_grid_is_magic`
- **Given**: 빈칸 2개·유효한 부분 격자; 특히 **작은 누락 수를 첫 빈칸에 넣으면 마방진이 되지 않고**, 역배치 시 성립하는 Gherkin 격자
- **When**: `solution(grid)` 호출
- **Then**:
  - 길이 6, 좌표 1~4 (**1-index**);
  - 알고리즘 규약: **작은 수→첫 빈칸(row-major 첫 0)** 시도 후 실패 시 **두 수 역순** 시도로 유일 해보장;
  - 기대 배치가 명세와 일치하면 예: `[3, 3, 6, 4, 4, 1]` (행·열은 1-index);
  - 반환값으로 격자를 채운 뒤 `is_magic_square`가 `True`
- **실패(RED) 명확화**: 시도 순서가 틀리면 잘못된 조합을 반환해 단언 실패.
- **Scenario**: 두 빈칸·두 미지수의 **유일 합법 배치**를 탐색 규약에 따라 찾는다.
- **Invariant 보호 내용**: **INV-탐색 순서·유일해·출력 계약** — FR-5와 동일하게 6-tuple·1-index·마방진 참일 것.

---

## 문서 ↔ 코드 추적

| 영역 | 자동화 테스트 파일 (참고) |
|------|---------------------------|
| Track A | `tests/boundary/test_magic_square_ui_red.py` |
| Track B | `tests/entity/test_magic_square_logic_red.py` |

본 명세는 위 파일의 **의도·ID**와 정합되도록 작성되었다. 구현이 없을 때 해당 테스트는 **의도적으로 RED**이다.

---

## 문서 이력

| 버전 | 일자 | 비고 |
|------|------|------|
| 1.0 | 2026-04-28 | Dual-Track RED 전용 명세 초안 |
