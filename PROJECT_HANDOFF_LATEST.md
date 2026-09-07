# PROJECT_HANDOFF_LATEST — 새마을금고 학습

## 새 채팅 시작 키워드
사용자가 새 채팅에서 **`다음 작업 진행`**이라고만 입력하면 아래 순서로 즉시 이어서 작업한다.

### 새 채팅의 첫 행동
1. GitHub `korealaw/trans`의 `PROJECT_HANDOFF_LATEST.md`와 `README.md`를 먼저 읽는다.
2. `RC4_V023_FINAL_QA.md`를 함께 확인한다.
3. 이 문서를 현재 작업의 기준으로 삼는다.
4. 사용자에게 프로젝트 설명을 다시 요구하지 않는다.
5. 이미 확정된 정책을 재논의하지 말고 아래 **다음 작업**부터 진행한다.

## 현재 프로젝트 기준
- 제품명: **새마을금고 학습**
- 현재 후보: **RC4 v0.23 INTEGRITY UPDATE**
- GitHub: `korealaw/trans`
- 최신 패키지명: `MG_saemaeul_learning_RC4_v0_23_INTEGRITY_UPDATE.zip`
- 앱 3종: `01_PHONE.html`, `02_PERSONAL_PC.html`, `03_INTRANET_PC.html`
- 실제기기 점검: `C23_DEVICE_SELFTEST.html`
- 최종 QA: `RC4_V023_FINAL_QA.md`

## GitHub 배포 현황 — 2026-09-08
- RC4 v0.23 앱 본체 3개를 GitHub `main`에 업로드 완료.
- 문제 DB `MG_MASTER_QUESTION_DB_300.csv`, `MG_RESERVE_40.csv` 업로드 완료.
- 로컬 `trans-main.zip`과 GitHub 핵심 파일의 size + Git blob SHA 일치 재확인 완료.
- 실패한 임시 `.payload` 디렉터리 제거 완료.
- 앱/DB 배포 커밋: `128457c3be8b3391a9bce7754423257d2bebe6f8`.
- `index.html`의 PHONE / PERSONAL PC / INTRANET PC / C23 링크 정상.
- 3종 HTML JavaScript 정적 구문검사 PASS.
- INTRANET 외부 URL/CDN/fetch/service worker 의존성 정적 검색 0건.
- GitHub Pages 정적 배포 준비용 `.nojekyll` 추가 완료.
- `RC4_V023_FINAL_QA.md` 생성 완료.
- 저장소 메타데이터 기준 현재 `has_pages=false`.
- 현재 ChatGPT GitHub 연결 권한은 `push=true`, `admin=false`이므로 파일 수정은 가능하지만 Pages 설정 활성화는 수행할 수 없다.
- 현재 확인된 유일한 공개 배포 차단점: **GitHub Pages 미활성화**.

## 사용자가 GitHub 웹에서 1회 수행할 작업
`korealaw/trans` → `Settings` → `Pages` → `Build and deployment` → `Source: Deploy from a branch` → `Branch: main` → `Folder: /(root)` → `Save`

Pages가 켜진 뒤 바로 아래 공개 경로를 실검증한다.
- `/trans/`
- `/trans/01_PHONE.html`
- `/trans/02_PERSONAL_PC.html`
- `/trans/03_INTRANET_PC.html`
- `/trans/C23_DEVICE_SELFTEST.html`

## 절대 유지 정책
1. 제품명은 **새마을금고 학습**만 사용한다.
2. 이전 프로젝트명/시험 직군명은 앱 화면·문서·배포물에 다시 쓰지 않는다.
3. `마인드맵` 기능은 완전 삭제 상태를 유지하며 다시 추가하지 않는다.
4. 학습 순서는 **1단계 5분 문제 10문항 필수 → 2단계 집중학습 기본 40문항**이다.
5. Quick과 Focus 문제군은 중복시키지 않는다.
6. 집중학습 Daily는 5개, 각 약 40문항 단위의 큰 주제 묶음으로 유지한다.
7. PHONE은 카카오톡 계열 시각언어를 유지한다.
8. INTRANET은 전면 회색조, 작은 업무형 폰트, 사각 버튼, 얇은 경계선, 단일 `.main` 스크롤을 유지한다.
9. INTRANET은 외부 CDN·웹폰트·API·네트워크 의존성 0을 유지한다.
10. INTRANET도 PHONE과 동일하게 홈 / 학습 / 모의고사 / 기록 라우팅이 항상 동작해야 한다.
11. 오답은 단순 문제 재출제가 아니라 **취약 개념 회복 DB**로 관리한다.
12. 다음 학습일 5분 문제에는 회복 대상 개념을 우선 반영하고, 같은 문제보다 같은 개념의 다른 문제를 우선 출제한다.
13. 동일 원문항 반복정답 또는 단일문항 개념만으로 MASTERED 처리하지 않는다.
14. JavaScript 함수는 동일 이름을 여러 번 override하지 않고 1회 정의한다.
15. 공개 GitHub에는 공식 원자료 PDF 10종을 올리지 않는다.

## 현재 데이터
- ACTIVE 260
- Master DB 300
- Reserve 40
- Quick 52
- Focus 208
- Daily 5
- Concepts 58
- Mock 20: Focus-only / Quick overlap 0 / 11개 영역 / 20개 서로 다른 개념
- `FLOW_SCHEMA_VERSION=23`

## 보기/정답 무결성 규칙
- CSV `answer`: 1-based
- HTML JSON `answer`: 0-based
- 문항 ID의 FNV-1a 32-bit hash를 이용해 보기 순서를 결정론적으로 재배열한다.
- `options`와 `optionReasons`는 항상 같은 순서로 이동한다.
- 동일 문항은 동일 버전에서 항상 같은 보기 순서를 유지한다.
- 현재 Master 300 정답 위치: ①76 / ②76 / ③74 / ④74.

## 현재 QA 통과 상태
- 3종 JavaScript `node --check`: PASS
- 중복 함수: 0
- CSV ↔ HTML active 260 옵션/정답 일치: PASS
- Quick 10문항 생성: PASS
- Quick 완료 전 Focus Gate 잠금: PASS
- Quick 완료 후 Focus Gate 해제: PASS
- Focus 기본 target 40 / queue 40: PASS
- 오답 개념 DB 생성: PASS
- 다음 회차 같은 개념의 다른 문제 우선: PASS
- 동일 문제 반복만으로 MASTERED 방지: PASS
- 단일문항 개념 MASTERED 방지: PASS
- INTRANET 홈/학습/모의고사/기록: PASS
- INTRANET 휠 스크롤: PASS
- INTRANET 비회색 색상: 0
- INTRANET 외부 URL/CDN/API: 0

## 아직 남은 실제 배포 게이트
1. GitHub Pages를 `main` / `/(root)`로 활성화.
2. Pages 공개 URL 5종 실검증.
3. 실제 Galaxy에서 `C23_DEVICE_SELFTEST.html` 최종 1회 확인.
4. 실제 사내 PC에서 `03_INTRANET_PC.html` 오프라인 실행 최종 1회 확인.
5. 실제기기 통과 후 RC4 v0.23 배포 확정.

## 새 채팅에서 `다음 작업 진행` 입력 시 바로 할 일
사용자가 별도 오류 스크린샷이나 새 요구를 함께 주지 않았다면:

### A. GitHub 상태부터 읽는다
- `PROJECT_HANDOFF_LATEST.md`
- `RC4_V023_FINAL_QA.md`
- 저장소 메타데이터의 `has_pages`

### B. `has_pages=false`라면
- 다른 코드 수정부터 하지 않는다.
- 사용자에게 GitHub 웹에서 Pages를 켜는 정확한 클릭 경로를 제시한다.
- Pages 활성화가 확인될 때까지 배포 장애를 코드 오류로 오인하지 않는다.

### C. `has_pages=true`라면
- Pages 공개 URL 5종 실검증
- Galaxy / 사내 PC 최종기기 점검으로 진행한다.

## 문제 콘텐츠 후속 과제 — 배포 후 v0.24 후보
- 단일문항 Concept 13개에 공식자료 대조 후 대체문항을 각 1개 이상 추가.
- Reserve 40을 검증하여 Master DB 340+로 확장.
- 오답 Family를 중요 FACT별 2~4문항으로 확장하여 같은 문제 반복률을 낮춘다.
- 난이도는 단순 암기형보다 사례·경계값·비교·역방향형 비중을 늘리되 공식 근거 QA 후 활성화한다.

## 원자료
공식 원자료는 최초 프로젝트 handoff/source ZIP의 10개 PDF다. 공개 GitHub에는 올리지 않는다. 콘텐츠 수정 시 원자료와 다시 대조한다.

## 새 채팅 응답 원칙
- 사용자가 `다음 작업 진행`이라고 하면 **“무엇을 진행할까요?”라고 묻지 않는다.**
- 최신 GitHub handoff와 이 문서 기준으로 곧바로 다음 작업을 수행한다.
