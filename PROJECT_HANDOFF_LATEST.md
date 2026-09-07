# PROJECT_HANDOFF_LATEST

## 프로젝트
- 제품명: **새마을금고 학습**
- 기준 후보: **RC4 v0.21 RELEASE CANDIDATE**
- GitHub: `korealaw/trans`

## 절대 유지 정책
1. 제품명은 `새마을금고 학습`으로만 표기한다.
2. 집중학습 전에 **5분 문제 10문항을 반드시 완료**한다.
3. 기본 집중학습 목표는 **40문항**이다.
4. 집중학습 Daily는 5개, 각 약 40문항 규모를 유지한다.
5. PHONE은 카카오톡 계열 UI를 유지한다.
6. INTRANET은 전면 회색조이며 사내 업무프로그램 수준의 작은 글꼴·사각형 버튼·얇은 경계선을 유지한다.
7. INTRANET은 홈/학습/모의고사/기록을 항상 사용할 수 있어야 한다.
8. INTRANET은 `.main` 단일 스크롤 구조를 유지한다.
9. 공식 원자료 PDF는 공개 GitHub에 올리지 않는다.
10. 별도 마인드맵 기능은 다시 추가하지 않는다.

## 오답 회복 정책
- 오답은 문제번호보다 **취약 개념 단위**로 누적한다.
- 다음 학습일의 1단계 10문항에 회복개념을 최대 6개 우선 배치한다.
- 같은 개념의 다른 문항을 원문항보다 우선한다.
- 대체문항이 없을 때만 동일 문항 재사용을 허용한다.
- 2회 회복 확인 시 안정화 처리한다.
- 모의고사 오답도 동일 reviewBank에 반영한다.

## 데이터
- ACTIVE 260
- Master DB 300
- Quick 전용 52
- Focus 전용 208
- Daily 5
- Mock 20
- Concepts 58

## v0.21 최종 QA
- 3종 앱 Chromium E2E: PASS
- Quick 10문항: PASS
- Focus 40문항: PASS
- 오답 reviewBank: PASS
- concept variant 재출제: PASS
- INTRANET nav 4개: PASS
- INTRANET scroll: PASS
- runtime pageerror: 0

## 다음 단계
실제 사용자 기기에서 1회 시범운영 후 GitHub `main` 앱 본체 3종을 RC4 v0.21로 교체하고 Pages 실URL을 최종 확인한다.
