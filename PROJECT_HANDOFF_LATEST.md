# PROJECT_HANDOFF_LATEST

## 프로젝트
- 새마을금고 전환직 학습 웹앱
- GitHub: `korealaw/trans`
- 현재 후보: RC4 v0.10
- 운영 원본: GitHub `main`

## RC4 구조
- 하나의 검증된 240문항 Master DB에 **Quick / Focus / Exam** 3개 학습경로를 병렬 구성
- Quick: 5문항 즉시 회상, 취약문항 우선, 정답 후 STEP 1만 기본 노출, 이유/공식근거는 선택 펼침
- Focus: 기존 Daily·Concept·단계해설·보기별 판정·공식근거·마인드맵 유지
- Exam: 20문항 실전 모의고사 유지
- 하단 메뉴: 홈 / 학습 / 모의고사 / 기록
- 첫 화면의 세부 통계·분량·지도·백업은 내부 화면으로 이동

## 데이터·기록 원칙
- 240문항 / Concept 48 / 활성 Daily 50 / 모의고사 20
- 별도 초급/중급 문제은행을 만들지 않음
- Quick 정오답은 기존 `questionStats`에 공유
- Daily 완료 판정은 Focus에 유지하여 빠르게 본 것과 집중학습 완료를 구분
- 기존 courseId와 localStorage KEY를 유지하여 RC3 v0.9.1 학습기록과 호환
- 전문 직함의 무관한 distractor 사용 금지
- `감사위원장`은 중앙회 직접 학습 문항(QRC2-176)에서만 유지

## UI 원칙
- PHONE / PERSONAL PC / INTRANET PC 3종
- PHONE은 모바일 우선, 한 화면 한 행동
- INTRANET PC는 외부 의존성 없이 중립 회색 업무형 UI 유지

## 다음 작업
1. RC4 실제기기 Quick / Focus / Exam 흐름 확인
2. PHONE 첫 화면 정보량·터치영역 확인
3. INTRANET 회색 업무형 UI 확인
4. 최신 3종 HTML을 `korealaw/trans/main`에 반영 후 Pages 검증

## 인계 정책
- 매 작업마다 원자료 포함 대형 HANDOFF ZIP을 새로 만들지 않는다.
- 이 파일과 GitHub `main`을 기본 인계수단으로 사용한다.
- 전체 ZIP은 공식 릴리스/대규모 구조변경/별도 백업이 필요할 때만 만든다.
- 원자료 PDF는 공개 저장소에 올리지 않는다.
