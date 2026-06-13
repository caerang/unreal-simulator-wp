# 프로젝트 진행 상황 (Progress Log)

이 파일은 **Unreal Engine 임무 비행 시뮬레이터 & gRPC 강화학습 에이전트 파이프라인 연동 프로젝트**의 작업 이력과 상태를 관리하는 파일입니다.

---

## 📌 현재 프로젝트 상태

*   **현재 단계:** 초기 환경 구성 및 기본 언리얼 에셋 배치 단계 (Scaffolding & Initial Setup)
*   **통신 파이프라인 상태:** 미구축 (gRPC 명세 설계 예정)
*   **버전 관리:** Git 초기화 및 첫 커밋 완료 (`Initialize Unreal Engine project`)

---

## 🛠️ 작업 내역 (Work History)

### 1단계: 프로젝트 환경 구성 (2026-06-13)
*   [x] 프로젝트 명세서 [design.md](file:///D:/workspace/simulator_wp/docs/design.md) 분석 완료.
*   [x] 언리얼 엔진 프로젝트 맞춤형 [.gitignore](file:///D:/workspace/simulator_wp/.gitignore) 파일 생성.
*   [x] 초기 핵심 에셋(전투기 블루프린트 및 맵 에셋) 스테이징 및 Git 첫 커밋(Initial Commit) 생성.
*   [x] 상태 표시줄 스크립트([status.py](file:///C:/Users/mylov/.antigravity/status.py))의 Windows/Console UTF-8 호환성 패치 및 이모지 제거 렌더링 최적화 작업 완료.
*   [x] 기본 Git 작업 브랜치를 `master`에서 `main`으로 변경하고, 프로젝트 문서의 브랜치 참조 정합성 업데이트 완료.

---

## 🎯 향후 작업 로드맵 (Roadmap)

### [ ] 1단계: gRPC 인터페이스 설계 및 명세 정의
*   임무 비행 상태(State) 데이터 및 에이전트 행동(Action) 데이터의 Protobuf 메시지 구조 정의 (`.proto` 파일 생성).
*   시뮬레이터-에이전트 간 서비스 명세서 작성.

### [ ] 2단계: 파이썬 gRPC 에이전트 스텁(Stub) 구현
*   가상환경(`uv`)에서 protobuf 컴파일 및 gRPC 서비스 서버/클라이언트 기본 뼈대 코드 작성.

### [ ] 3단계: 언리얼 엔진 gRPC 클라이언트/서버 연동
*   언리얼 엔진 내 gRPC 플러그인 또는 C++ 모듈 추가.
*   블루프린트/C++에서 파이썬 에이전트로 상태 데이터를 전송하고 행동 데이터를 수신하는 단일 에이전트 연동 테스트 완료.

### [ ] 4단계: 멀티 시나리오(동시 실행) 파이프라인 확장
*   32개/64개 이상의 다수 시나리오를 병렬로 구동하고, 각각의 인스턴스가 독립된 gRPC 채널을 통해 상태/행동 데이터를 비동기 송수신할 수 있도록 통신 모듈 아키텍처 확장.

### [ ] 5단계: 행위 트리(Behavior Tree) 기반 시나리오 통합
*   언리얼 엔진 행위 트리(`AIC_Fighter`, `BB_Fighter`)와 강화학습 행동 데이터를 매핑하여 기동/타격 임무 비행 시나리오 시뮬레이션 및 학습 루프 완성.
