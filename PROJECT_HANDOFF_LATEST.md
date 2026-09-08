# PROJECT_HANDOFF_LATEST — 새마을금고 학습

## 현재 기준 · 2026-09-08
제품: **새마을금고 학습**. 저장소: `korealaw/trans`, 브랜치 `main`. 최신 앱: **RC4 v0.24.1 INTRANET COLOR-BOUNDARY HOTFIX**. 앱 반영 커밋: `bbda1eaa4ff1b3b683da655f8158a2231b8a9a27`. GitHub Actions 실행 `34172620809` 성공.

## 절대 유지 정책
1. 제품명은 새마을금고 학습만 사용. 로그인 추가 금지. 삭제한 마인드맵 복원 금지.
2. 1단계 Quick 10문항 필수 → 2단계 Focus 기본 40문항. Quick/Focus 전용 문제군은 중복시키지 않는다.
3. PHONE 대화형 UI와 PERSONAL PC 현재 구조 유지.
4. **INTRANET의 비실행 좌측·상단·호스트 프레임은 이전 사내화면 사진의 원래 색상을 유지한다.**
5. **INTRANET의 실제 실행영역 `.main`만 회색/중성 업무형 UI로 유지한다.** 전체 `#app` grayscale 필터를 다시 추가하지 않는다.
6. INTRANET은 작은 업무형 글씨·사각형 버튼·단일 `.main` 스크롤·외부 네트워크 의존성 0 유지.
7. 공식 원자료 PDF 10종은 공개 GitHub에 올리지 않는다.

## 데이터
활성 260 = Quick 52 + Focus 208. Daily 5(40/38/42/42/46), 개념 58, 모의 20 Focus 전용. Master 300에 Reserve 40 포함. Reserve를 더해 340으로 계산하지 않는다.

## v0.24.1 수정 이유
v0.24에서 `#app{filter:grayscale(1)}`가 적용되어 실행영역뿐 아니라 좌측·상단의 호스트 배경 사진까지 회색화됐다. 사용자 의도는 ‘호스트 화면은 이전 사진 색상 유지 / 실제 학습 패널만 회색’이므로 전체 필터를 제거했다. 내장 배경 이미지는 이전 v0.6과 원래부터 동일했으며 SHA256 `3bea84654e733a6b45a887e139cd8f528eff90e11b1d237bb8897dfaf020e097`로 재확인했다.

## 검증
- Chromium DOM: 171/171 PASS.
- 앱 3종 JavaScript 구문 / 함수중복 / 260문항 CSV 정합성 / 외부 런타임 통신: PASS.
- INTRANET 실행 패널 내부 샘플: 비회색 픽셀 0.
- 호스트 상단: 비회색 픽셀 비율 약 79%, 좌측 약 46%, 우측 배경 100%로 색상 유지 확인.
- GitHub 정적 검증 파일: `qa/static_results_v0241.json`.

## 아직 미확인
실제 Galaxy, 실제 사내 PC 보안정책, 브라우저 재시작 후 네이티브 저장 지속성, 법령·규정 300문항의 실질 최신성 전수감수.

## 다음 작업
GitHub Pages가 아직 비활성이라면 Pages를 `main` / `/(root)`로 켠 뒤 공개 URL을 실검증한다. 그 다음 실제 Galaxy 및 사내 PC에서 `C24_DEVICE_SELFTEST.html`을 실행한다.

새 채팅에서 사용자가 `다음 작업 진행`이라고 하면 이 문서와 `qa/static_results_v0241.json`을 우선 기준으로 바로 이어간다.
