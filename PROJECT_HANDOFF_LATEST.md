# PROJECT_HANDOFF_LATEST

## 프로젝트
- 제품명: **새마을금고 학습**
- 기준 후보: **RC4 v0.18**
- GitHub: `korealaw/trans`

## 절대 유지 정책
1. 제품명은 `새마을금고 학습`으로만 표기한다.
2. 집중학습 전에 **5분 문제 10문항을 반드시 완료**한다.
3. 5분 문제와 집중학습 문제는 서로 겹치지 않는다.
4. 집중학습 기본 목표는 **40문항**이다.
5. 집중학습 Daily는 5개, 각 약 40문항 규모를 유지한다.
6. PHONE은 카카오톡 계열 UI를 유지한다.
7. INTRANET은 전면 회색조이며 홈/학습/모의고사/기록을 항상 사용할 수 있어야 한다.
8. INTRANET은 중첩 스크롤을 만들지 않고 `.main` 단일 스크롤을 유지한다.
9. Quick 저장상태가 손상되거나 큐가 비면 빈 화면을 보여주지 말고 자동 복구한다.
10. 공식 원자료 PDF는 공개 GitHub에 올리지 않는다.

## 데이터
- ACTIVE 260
- Master DB 300
- Quick 전용 52
- Focus 전용 208
- Daily 5

## v0.18 회귀방지
- `FLOW_SCHEMA_VERSION=18`
- `QUESTION_INDEX` 기반 문제 lookup
- `validQuickIds()` 예상값 52
- `buildQuickQueue(10)` 예상값 10
- `state.view='quick' + empty queue` 저장상태는 `learnHub`로 자동 복구
- 복구 후 `startQuick()`은 다시 10문항을 구성해야 함

## 다음 검증
1. 실제 사내 PC에서 이전 v0.17 학습기록을 남긴 상태로 v0.18 실행
2. 학습 → 5분 문제 시작 시 1/10 문항이 정상 표시되는지 확인
3. 홈 / 학습 / 모의고사 / 기록 왕복 확인
4. 문제·해설 최하단까지 스크롤 확인
5. 통과 후 GitHub main 최신 앱 반영 및 Pages 검증
