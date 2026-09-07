# PROJECT_HANDOFF_LATEST

## 프로젝트
- 제품명: **새마을금고 학습**
- 기준 후보: **RC4 v0.23 INTEGRITY UPDATE**
- 저장소: `korealaw/trans`

## 절대 유지 정책
1. 제품명은 `새마을금고 학습`만 사용한다.
2. 1단계 5분 문제 10문항을 완료해야 2단계 집중학습으로 들어간다.
3. 집중학습 기본 목표는 40문항, Daily는 5개 약 40문항 단위다.
4. PHONE은 카카오톡 계열 시각언어 + 단순한 모바일 정보구조를 유지한다.
5. INTRANET은 전면 회색조, 업무형 작은 폰트, 단일 `.main` 스크롤, 외부 의존성 0을 유지한다.
6. Quick/Focus 문제군은 겹치지 않는다.
7. 오답 회복은 개념 단위이며 같은 문항보다 같은 개념의 다른 문항을 우선한다.
8. 단일문항 개념 또는 동일 원문항 재정답만으로 MASTERED 처리하지 않는다.
9. 각 JavaScript 함수는 **한 번만 정의**한다. 레이어드 override 방식으로 같은 함수명을 뒤에 추가하지 않는다.
10. 공개 GitHub에는 공식 원자료 PDF를 올리지 않는다.

## v0.23 데이터
- ACTIVE 260 / Master 300 / Reserve 40
- Quick 52 / Focus 208
- Daily 5 / Concepts 58
- Mock 20: Focus-only, Quick overlap 0, 11개 영역, 20개 개념
- FLOW_SCHEMA_VERSION=23

## 보기 순서 규칙
원본/CSV에서 정답위치가 기계적으로 순환하지 않도록 **빌드 시점에 결정론적으로 재배열**한다.

1. CSV `answer`는 1-based, 앱 JSON `answer`는 0-based다.
2. 문항 ID의 FNV-1a 32-bit hash를 이용한다.
3. `qid + '|ans'` hash mod 4로 정답 표시 위치를 결정한다.
4. 나머지 3개 오답은 `qid + '|dist'` seed로 결정론적 Fisher-Yates를 적용한다.
5. `options`와 `optionReasons`를 같은 순서로 이동한다.
6. 동일 문항은 버전 내에서 항상 같은 순서를 유지한다.
7. 보기 순서를 바꾸는 버전은 FLOW_SCHEMA_VERSION을 올리고 진행 중 pick/mock transient state를 초기화한다.

## Mock 선발 규칙
- Focus 전용 문제만 사용한다.
- Quick ID와 교집합은 0이어야 한다.
- 활성 Concept의 전체 영역을 최소 1문항씩 포함한다.
- 가능하면 Concept 중복 없이 선발한다.
- 현 v0.23: 20문항 / 11영역 / 20개념.

## 콘텐츠 후속 과제
단일문항 개념 13개에는 대체문항을 각 1개 이상 공식자료와 대조해 추가한다. 그 전까지 엔진이 허위 MASTERED 승격을 차단한다.

## 빌드/QA 절차
1. `question_db/MG_MASTER_QUESTION_DB_300.csv`를 canonical DB로 관리한다.
2. active 260을 앱 JSON으로 생성할 때 answer 1-based → 0-based 변환을 확인한다.
3. 결정론적 보기 재배열을 CSV와 HTML JSON에 동일 적용한다.
4. Quick 52 / Focus 208 / 교집합 0 검증.
5. Mock 20의 Focus-only / 영역 / 개념 검증.
6. JS에서 중복 함수명 0 검증.
7. `node --check`로 세 앱 구문검사.
8. Chromium에서 PHONE/PC/INTRANET 학습 흐름 회귀시험.
9. INTRANET 비회색 색상·외부 URL·스크롤을 별도 검사.
10. 실제 Galaxy와 사내 PC에서 최종 1회 확인 후 배포한다.
