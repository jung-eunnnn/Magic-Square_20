# MagicSquare — `.cursorrules` 설정 작업 보고서

**작성 목적:** 프로젝트 루트의 `.cursorrules` 파일을 설계·작성·검토·확장한 과정과 결과를 한 문서로 보존한다.  
**범위:** YAML 뼈대 작성, `tdd_rules` 초기 입력, 규칙 파일 검토, MagicSquare 기준 전 섹션 완성. 소스 코드 구현은 포함하지 않는다.  
**프로젝트 경로:** `c:\DEV\Magic Square_01`  
**문서 이력:** 2026-04-27

---

## 1. 산출물

| 항목 | 경로 |
|------|------|
| Cursor 규칙 파일 | 프로젝트 루트 `.cursorrules` |
| 문제 정의·배경(기존) | `Report/4x4_마방진_문제정의_및_배경_보고서.md` |
| 본 작업 보고서 | `Report/MagicSquare_Cursorrules_작업_보고서.md` |

---

## 2. 작업 단계 요약

### 2.1 YAML 뼈대

- 최상위 키: `project`, `code_style`, `architecture`, `tdd_rules`, `testing`, `forbidden`, `file_structure`, `ai_behavior`
- 각 최상위 블록 앞에 **80자** `#` 구분선 주석 배치
- 당시 빈 값은 `~`(YAML null)로 둠

### 2.2 `tdd_rules` 1차 입력

- `red_phase`, `green_phase`, `refactor_phase`를 각각 **한 줄 문자열**로 기술(이후 구조화 단계에서 대체됨).

### 2.3 검토(수정 없음)

요청에 따라 파일을 수정하지 않고 아래만 점검함.

1. **YAML 문법:** PyYAML `safe_load` 기준 오류 없음.
2. **필수 섹션:** 합의된 8개 키 모두 존재. Cursor 공식 필수 스키마는 비공개로 추가 판단 불가.
3. **`tdd_rules` vs `forbidden`:** `forbidden`이 비어 있어 당시 기준으로 충돌 없음.
4. **`ai_behavior`:** 비어 있어 “따를 수 없는 규칙” 검토 대상 없음.

### 2.4 MagicSquare 기준 전 섹션 완성

다음 규칙에 맞춰 `.cursorrules`를 재작성함.

- **`code_style`:** Python 3.10+, PEP 8, 전 함수 타입 힌트, Google docstring(public), 행 길이 88(Black).
- **`architecture`:** ECB 3레이어(`boundary` / `control` / `entity`) 정의 및 **의존성 방향** `boundary → control → entity` 명시. entity의 상위 레이어 참조 금지 등.
- **`tdd_rules`:** 각 phase별 `description`, `rules`, `must_not` 목록으로 세분화.
- **`testing`:** pytest, AAA, 커버리지 최소 80%, `fixture_scope` 정책, `test_` 접두사 명명.
- **`forbidden`:** 항목마다 `pattern` / `reason` / `alternative`. 최소 포함: `print()` 남용, 도메인 하드코딩, `except` 단독·광범위 삼키기.
- **`file_structure`:** ECB 기준 디렉터리 트리를 블록 문자열 내 주석 형태로 기술(`boundary/`, `control/`, `entity/`, `tests/` 하위 미러, `Report/`).
- **`ai_behavior`:** 작성 전·중·후 행동, ECB 위반 금지, 타입 힌트 없는 함수 금지, `tdd_rules` 위반 시 사용자에게 경고 후 단계 분할 제안.
- **`project`:** 기존 `Report/4x4_마방진_문제정의_및_배경_보고서.md`와 맞는 불변(1~16, 10선, 매직 합 34, 역할 명시 등) 요약.

YAML 전체는 PyYAML으로 파싱 검증 완료.

---

## 3. 설계상 참고 사항

- **테스트 명명:** 규칙에 `test_` 접두사를 명시함. pytest는 클래스 기반 테스트에서 관례적으로 `Test*` 접두 클래스명을 사용하므로, 클래스 스타일 테스트 도입 시 `testing.naming_convention` 문구를 보완할 수 있음.
- **`.cursorrules` 해석:** Cursor가 이 파일을 엄격한 YAML이 아닌 자연어 지침으로 병행 해석할 가능성은 있으나, 본 프로젝트는 사람·도구 모두 읽기 쉬운 단일 소스로 유지하는 것을 목표로 함.

---

## 4. 이후 권장 작업

- `boundary/`, `control/`, `entity/`, `tests/` 실제 디렉터리 생성 및 첫 테스트·엔티티 스켈레톤 추가 시, 본 보고서 §2.4와 디렉터리 실물이 일치하는지 점검.
- 역할(검증 전용 / 생성 / 부분 채움)이 확정되면 `project`·`Report` 문제 정의 문서를 동시에 개정.

---

*본 보고서는 대화 기반으로 수행된 `.cursorrules` 관련 작업을 옮긴 것이다.*
