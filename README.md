# 새마을금고 학습 · RC4 v0.11

## 현재 구조
- 문제은행 240문항
- 48 Concepts / 50 Daily / 모의고사 20문항
- PHONE / PERSONAL PC / INTRANET PC 3종

## 영구 운영 원칙
1. 제품·프로젝트 화면 명칭은 **새마을금고 학습**으로만 사용합니다.
2. 5분 빠른학습과 집중학습은 **같은 문항을 교차 출제하지 않습니다.**
   - 5분 빠른학습 전용: 52문항
   - 집중학습 전용: 188문항
   - 실전 모의고사는 별도 시험 흐름으로 운영합니다.
3. INTRANET PC 버전은 **회색조 전용 UI**로 유지합니다. 이후 기능 추가 시에도 유채색을 사용하지 않습니다.
4. 사내판은 외부 CDN·웹폰트·네트워크 의존성 없이 동작해야 합니다.
5. 문제·정답·해설·공식근거의 기준 데이터는 하나만 유지합니다.

## 파일
- `index.html` / `00_VERSION_SELECTOR.html`: 버전 선택
- `01_PHONE.html`: 모바일
- `02_PERSONAL_PC.html`: 개인 PC
- `03_INTRANET_PC.html`: 사내 PC 회색조·오프라인
- `C11_DEVICE_SELFTEST.html`: 실제 기기 점검
- `PROJECT_HANDOFF_LATEST.md`: 다음 작업 인계

## 원자료
공식 원자료 PDF 10종은 공개 GitHub 저장소에 업로드하지 않습니다.
