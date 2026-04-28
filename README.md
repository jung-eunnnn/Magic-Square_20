# Magic Square (4×4)

4×4 격자에 1~16을 각각 한 번 배치할 때, **4행·4열·주대각선 2개(총 10선)**의 합이 모두 같은지 판별하고, 값 `0`이 **정확히 두 칸**인 부분 격자에 대해 문서화된 절차로 **완성(두 순서 시도)**을 시도하는 **학습용** 프로젝트입니다.

---

## 문서 역할 (무엇을 어디서 볼지)

| 우선순위 | 경로 | 역할 |
|----------|------|------|
| **중심** | [`docs/PRD_MagicSquare_4x4.md`](docs/PRD_MagicSquare_4x4.md) | 요구사항·불변(INV)·기능 요구(FR)·계약(§10)·성공 정의(§12)·**MAP-ID 추적(§6·§13)**. **본 README의 To-Do·검증 기준의 근거**입니다. |
| 스토리·시나리오 | [`Report/MagicSquare_사용자여정_및_구현시나리오_L1-L5.md`](Report/MagicSquare_사용자여정_및_구현시나리오_L1-L5.md) | Epic → Journey → **Story 1~5 순서**, Level 4 Gherkin 참조 본문. |
| 개발 환경·구조·품질 | [`.cursorrules`](.cursorrules) | Python 3.10+, **ECB**, `tests/` 분할, pytest·AAA, **커버리지 하한 80%**, TDD 단계, 금지 패턴. |
| 맥락·배경 | [`Report/4x4_마방진_문제정의_및_배경_보고서.md`](Report/4x4_마방진_문제정의_및_배경_보고서.md) | 문제 인식, 불변 논의, TDD 채택 이유. |
| PRD 작업 요약 | [`Report/MagicSquare_4x4_PRD_DualTrack_MLOps_작업_보고서.md`](Report/MagicSquare_4x4_PRD_DualTrack_MLOps_작업_보고서.md) | PRD에 Dual-Track·MLOps 훅·MAP-ID 등이 반영된 **작업 이력·구조 요약** (정의의 단일 출처는 PRD). |

---

## 방법론 (한 줄씩)

- **Concept-to-Code:** PRD §13 추적 매트릭스와 §6.2 **MAP-ID**로 개념·규칙·테스트·컴포넌트를 연결합니다.
- **Dual-Track UI + Logic TDD:** **Boundary**는 UX Contract(메시지 키·결과 코드·CLI 종료 코드 등, PRD §10.4). **Entity·Control**은 Logic Rule(FR·INV). 테스트는 서로 구현 세부에 의존하지 않습니다(PRD §1.4).
- **ECB:** `boundary → control → entity` 단방향 의존성([`.cursorrules`](.cursorrules) `architecture`).
- **RED → GREEN → REFACTOR:** [`.cursorrules`](.cursorrules) `tdd_rules` 준수.

---

## 권장 디렉터리 구조

[`.cursorrules`](.cursorrules) `file_structure`와 동일하게 맞춥니다.

```text
.
├── boundary/          # UI, API, CLI — 도메인 규칙 직접 구현 금지
├── control/           # 유스케이스·FR-5 등 흐름 조율
├── entity/            # 격자·검증·판정 등 순수 도메인
├── tests/
│   ├── boundary/
│   ├── control/
│   └── entity/
├── docs/              # PRD 등
└── Report/            # 배경·여정·작업 보고
```

---

## 개발 환경 (`.cursorrules` 요약)

- **언어:** Python **3.10 이상**
- **스타일:** PEP 8, 행 길이 최대 **88**, **타입 힌트** 필수, public API는 **Google 스타일 docstring**
- **테스트:** **pytest**, **AAA** 패턴, 수집 규칙에 맞게 `test_` 접두사
- **커버리지:** 프로젝트 전체 라인 **최소 80%** (`testing.coverage_minimum`); Epic 문서에는 엔티티 중심 **95% 목표**가 병기되어 있으므로 PRD·L1 성공 기준과 함께 해석합니다.

의존성 선언 파일(`pyproject.toml` / `requirements.txt`)이 생기면, 가상환경 생성 후 해당 파일로 설치하고 아래 명령을 실행합니다.

```bash
pytest
pytest --cov=entity --cov=control --cov=boundary --cov-fail-under=80
```

(패키지 루트 경로는 실제 소스 레이아웃에 맞게 조정합니다.)

---

## 검증 기준 (PRD §12·NFR와 정렬)

다음을 **문서·코드·테스트**에서 동시에 만족하는 것을 완료에 가깝다고 봅니다. 상세는 [`docs/PRD_MagicSquare_4x4.md`](docs/PRD_MagicSquare_4x4.md) §12·§11을 따릅니다.

| ID | 조건 |
|----|------|
| **S-01** | INV-01~INV-04가 구현·테스트·문서에서 동일 해석 |
| **S-02** | FR-1~FR-5 각 AC에 대응하는 자동화 테스트 존재 (권장: **MAP-ID ↔ `test_*` 함수명** 링크 표) |
| **S-03** | `pytest` 전체 통과, **라인 커버리지 ≥ 80%** |
| **S-04** | `tests/boundary`, `tests/control`, `tests/entity` **분리·병존** |
| **S-05** | L1–L5 Level 4 Gherkin 시나리오와 **동일 조건**의 pytest 대응 |

---

## 사용자 스토리 순서 (L1–L5 Level 3)

구현·To-Do 진행 순서는 [`Report/MagicSquare_사용자여정_및_구현시나리오_L1-L5.md`](Report/MagicSquare_사용자여정_및_구현시나리오_L1-L5.md) Level 3과 PRD §9를 맞춥니다.

1. **Story 1** — 입력 검증 (FR-1, MAP-01~04)  
2. **Story 2** — 빈칸 탐색 (FR-2, MAP-05)  
3. **Story 3** — 누락 두 수 (FR-3, MAP-06)  
4. **Story 4** — 완전 격자 마방진 판정 (FR-4, MAP-07~08)  
5. **Story 5** — 두 순서 시도 완성 (FR-5, MAP-09~10)

---

## MAP-ID 빠른 참조 (PRD §6.2)

| MAP-ID | 요약 | FR |
|--------|------|-----|
| MAP-01 | 격자가 4×4 아님 | FR-1.1 |
| MAP-02 | 빈칸(`0`) 개수 ≠ 2 | FR-1.2 |
| MAP-03 | 0 제외 중복 | FR-1.3 |
| MAP-04 | 채워진 값이 1~16 밖 | FR-1.4 |
| MAP-05 | 빈칸 좌표(row-major) | FR-2 |
| MAP-06 | 누락 두 수(오름차순) | FR-3 |
| MAP-07 | 완전 격자, 비마방진 | FR-4 |
| MAP-08 | 완전 격자, 마방진 | FR-4, INV |
| MAP-09 | 두 순서 시도 후 성공 | FR-5 |
| MAP-10 | 두 시도 모두 실패(명시적 실패) | FR-5.4 |

---

## To-Do (구현 보드)

아래 보드는 **체크박스 · 단계 번호(Epic → US → Task) · 요구사항 추적**을 한데 묶은 형태입니다. 요구·불변·MAP-ID의 **단일 출처**는 [`docs/PRD_MagicSquare_4x4.md`](docs/PRD_MagicSquare_4x4.md)이고, 스토리 순서·Level 시나리오는 본문 **사용자 스토리 순서 (L1–L5)** 및 [`Report/MagicSquare_사용자여정_및_구현시나리오_L1-L5.md`](Report/MagicSquare_사용자여정_및_구현시나리오_L1-L5.md), 구조·TDD·품질은 [`.cursorrules`](.cursorrules)입니다.

항목을 닫을 때는 **Task ID / Req ID / MAP-ID**와 대응 테스트명을 커밋·PR에 남겨 **요구사항 추적성(traceability)**을 유지합니다.

### 번호·체크박스 체계 (슬라이드 1.3과 동일 구조)

| 레벨 | 의미 |
|------|------|
| **Epic-xxx** | 제품 단위 목표(예: 마방진 검증 시스템 전체). |
| **US-xxx** | 사용자 가치 단위(User Story). |
| **TASK-xxx** | 구현·검증 가능한 작업 묶음. |
| **TASK-002-1 … -3** | TDD: **RED** → **GREEN** → **REFACTOR** 순서 고정. |

- **RED:** 실패하는 테스트를 먼저 추가(요구가 테스트로 표현됨).
- **GREEN:** 통과할 만큼만 구현.
- **REFACTOR:** 동작 유지한 채 구조·이름·중복 정리.

아래 체크 상태는 **보드 기준 스냅샷**이며, 구현이 진행되면 이 섹션을 갱신합니다.

---

### Epic-001: 마방진 검증 시스템 (Magic Square Verification System)

#### US-001: 합 검증 (Sum Verification)

행·열·주대각선 등 **합 일치 여부**를 도메인 계층에서 판별하는 흐름입니다. PRD의 완전 격자 판정·부분 격자 이후 검증과 맞물립니다.

- [x] **TASK-001** — MagicSquare 엔티티 정의 (Define MagicSquare Entity)  
  - 격자 표현, 매직 합·차원 등 **도메인 상수·불변**을 엔티티 쪽에 모읍니다(ECB: `entity/`).  
  - **추적:** Req **REQ-001**, 시나리오 **L1 Happy**, 테스트 `test_valid_ms` → 상태 **PASS**(완료).

- [ ] **TASK-002** — SquareValidator 구현 (Implement SquareValidator)  
  - `is_valid()`(또는 동등 API)로 **10선·공통합·INV**와 일치하는 검증을 제공합니다.  
  - **추적:** Req **REQ-002**, 시나리오 **L3 Fail**, 테스트 `test_invalid` → 상태 **RED**(실패 테스트가 요구를 끌고 감; GREEN까지 미완).  
  - [ ] **TASK-002-1** — `is_valid()` **RED:** 비정상·비마방진 입력에 대해 **의도적으로 실패**하는 테스트 추가.  
  - [ ] **TASK-002-2** — `is_valid()` **GREEN:** 위 테스트를 만족하는 최소 구현.  
  - [ ] **TASK-002-3** — **REFACTOR:** 중복 제거, 경계·이름 정리, PRD 10.2에 맞는 **실패 구분**(광범위 예외 삼키기 금지, `.cursorrules` `forbidden` 준수).

#### US-002: 빈칸 탐색 (Search Empty Spaces)

값 `0`인 칸 등 **빈칸 위치**를 결정적으로 찾아 후속 FR(누락 수·완성 시도)으로 넘깁니다.

- [ ] **TASK-003** — MissingFinder 구현 (Implement MissingFinder)  
  - **선택:** 좌표·제약 탐색에 **N-Queen** 계열(백트래킹·가지치기) 아이디어를 **참고·재사용**할 수 있습니다. 4×4·빈칸 2개 제약에 맞게 단순 탐색으로 충분하면 과도한 일반화는 피합니다.  
  - **\[Checkpoint\]** 해당 탐색 경로(및 PRD에서 정한 단위 작업)가 **100ms 미만**인지 측정·기록합니다(환경·NFR는 PRD 11절과 정렬).  
  - **추적:** Req **REQ-003**, 시나리오 **L2 Edge**, 테스트 `test_missing` → 상태 **TODO**.

##### US-001 보조 · UI 경계 (매트릭스에만 명시된 Task)

- [ ] **TASK-004** — REQ-001 **L1 UI** 격자 표현·관측 규약  
  - 동일 Req **REQ-001**을 **Boundary**에서 다시 검증합니다(메시지 키·결과 코드·CLI 종료 코드 등 PRD 10.4, Dual-Track에서 Logic 테스트와 독립).  
  - **추적:** 테스트 `test_grid_ui` → 상태 **TODO**.

---

### 요구사항 추적 매트릭스 (Requirements Traceability)

Task ↔ 요구 ↔ 시나리오 레벨 ↔ 테스트 케이스 ↔ 현재 판정을 한 표에 둡니다. 저장소가 커지면 PRD 6절 **MAP-ID** 열을 이 표에 병기하는 것을 권장합니다.

| Task ID | Req ID | Scenario | Test Case | 상태 |
|:--------|:-------|:---------|:----------|:-----|
| TASK-001 | REQ-001 | L1 Happy | `test_valid_ms` | **PASS** |
| TASK-002 | REQ-002 | L3 Fail | `test_invalid` | **RED** |
| TASK-003 | REQ-003 | L2 Edge | `test_missing` | **TODO** |
| TASK-004 | REQ-001 | L1 UI | `test_grid_ui` | **TODO** |

**상태 읽는 법:** **PASS** = 해당 테스트가 녹색·요구 충족으로 간주됨. **RED** = TDD RED 단계이거나 회귀로 실패 중(의도적 실패 포함). **TODO** = 테스트 미작성 또는 미연결.

---

### PRD Phase·스토리와의 대응 (보조)

Epic 보드만으로는 ECB·FR-5·품질 게이트가 드러나지 않으므로, **세부 체크리스트**는 PRD 9·12절과 상단 **사용자 스토리 순서**를 그대로 따릅니다. 요약만 둡니다.

| 구분 | 할 일(요약) |
|------|-------------|
| 스캐폴딩·추적 | ECB 디렉터리, `tests/boundary`·`control`·`entity`, MAP-01~10 ↔ `test_*` 링크 표 |
| Entity | FR-1~4 (**MAP-01~08**), 상수·Validator·빈칸·누락 두 수 |
| Control | FR-5 두 순서 시도·성공/명시적 실패 (**MAP-09~10**) |
| Boundary | PRD 10.4 관측 규약, TASK-004·`test_grid_ui`와 합류 |
| 품질 게이트 | **S-01~S-05**, `pytest` 녹색, 커버리지 ≥ 80%, Gherkin 대응 표기 |

---

## 배경을 더 읽으려면

- [4×4 마방진 문제 정의·배경](Report/4x4_마방진_문제정의_및_배경_보고서.md) — 왜 이 크기·규칙·TDD인지.  
- [PRD Dual-Track·MLOps 작업 보고](Report/MagicSquare_4x4_PRD_DualTrack_MLOps_작업_보고서.md) — PRD 구조·보강 요약 (요구 정의 본문은 PRD).

---

## 라이선스

저장소에 `LICENSE`가 추가되면 이 섹션을 갱신합니다.
