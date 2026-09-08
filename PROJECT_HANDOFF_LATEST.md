# PROJECT_HANDOFF_LATEST — 새마을금고 학습

## 현재 기준 · 2026-09-08
저장소: `korealaw/trans`, 브랜치 `main`.
- PHONE / PERSONAL PC 공개 웹앱: **RC4 v0.24.2**, 표시명 **오다영과장 공부하기**.
- INTRANET: **RC4 v0.24.1**, 단일 HTML 오프라인판.
- 공개 URL: `https://korealaw.github.io/trans/`.
- GitHub Pages: 활성화 완료, `pages build and deployment` 실행 `34175300561` 성공.
- Pages에 배포된 기준 커밋: `d908221cc4218ad76d2acc93f74b61baf3c7603e`.
- 공개 런처는 PHONE / PERSONAL PC만 노출한다. INTRANET은 별도 파일 전달용이다.

## 최종 확인 상태
- 자동 Chromium DOM 검사: 171/171 PASS.
- 공개 앱 명칭/메인 제목: `오다영과장 공부하기` 반영 완료.
- PHONE blob: `7eb064417f9bc6ae1777aba968e2c12c3eee5439`.
- PERSONAL PC blob: `e192490725bf607773546a6c42b7cb59b6f6d681`.
- INTRANET blob: `9042cffb25e5d84de29c1cbf0f86cd3c29a15b7b`.
- INTRANET 실사내 PC 사용자 확인: **PASS**. 화면/문제/실행 정상으로 보고됨.
- Pages build/deploy: **PASS**.

## 절대 유지 정책
1. 로그인 추가 금지. 삭제한 마인드맵 복원 금지.
2. 1단계 Quick 10문항 필수 → 2단계 Focus 기본 40문항. Quick/Focus 전용 문제군 비중복.
3. PHONE 대화형 UI와 PERSONAL PC 현재 구조 유지.
4. 공개 PHONE/PERSONAL PC의 앱명은 **오다영과장 공부하기**.
5. INTRANET은 별도 오프라인판이며 기존 시각 기준 유지: 좌측·상단·호스트 프레임은 이전 사진 원색, 실제 실행영역 `.main`만 회색 업무형 UI. 전체 `#app` grayscale 필터 금지.
6. INTRANET은 작은 업무형 글씨·사각형 버튼·단일 `.main` 스크롤·외부 런타임 통신 0 유지.
7. 공식 원자료 PDF 10종은 공개 GitHub에 올리지 않는다.

## 데이터
활성 260 = Quick 52 + Focus 208. Daily 5(40/38/42/42/46), 개념 58, 모의 20 Focus 전용. Master 300에 Reserve 40 포함. 340으로 중복 합산하지 않는다.

## 남은 작업
1. 공개 URL을 실제 Galaxy와 개인 PC에서 열어 제목/메뉴/학습 시작/새로고침 후 기록 유지 여부를 사용자 실기기로 최종 확인한다.
2. 법령·규정 300문항의 실질 최신성 전수감수는 코드 QA와 별개로 진행한다.
3. 실기기 이상이 없으면 RC4 v0.24.2 공개판을 배포 확정 상태로 동결한다.

새 채팅에서 사용자가 `다음 작업 진행`이라고 하면 이 문서를 기준으로 공개 URL 실기기 검증 또는 콘텐츠 최신성 감수로 이어간다.
