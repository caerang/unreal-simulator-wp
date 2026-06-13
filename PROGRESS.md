# 프로젝트 진행 상황 (Progress Log)

이 파일은 **Unreal Engine 임무 비행 시뮬레이터 & gRPC 강화학습 에이전트 파이프라인 연동 프로젝트**의 작업 이력과 상태를 관리하는 파일입니다.

---

## 현재 프로젝트 상태

*   **현재 단계:** 언리얼 시뮬레이터 기본 구조 구현 완료 / gRPC 파이프라인 구축 대기
*   **통신 파이프라인 상태:** 미구축 (`.proto` 초안 설계 완료, 플러그인 연동 예정)
*   **버전 관리:** Git (`main` 브랜치), GitHub 원격 저장소 연결 완료

---

## 작업 내역 (Work History)

### 1단계: 프로젝트 환경 구성 (2026-06-13)
*   [x] 프로젝트 명세서 [design.md](file:///D:/workspace/simulator_wp/docs/design.md) 분석 완료.
*   [x] 언리얼 엔진 프로젝트 맞춤형 [.gitignore](file:///D:/workspace/simulator_wp/.gitignore) 파일 생성.
*   [x] 초기 핵심 에셋(전투기 블루프린트 및 맵 에셋) 스테이징 및 Git 첫 커밋(Initial Commit) 생성.
*   [x] 기본 Git 작업 브랜치를 `master`에서 `main`으로 변경하고, 프로젝트 문서의 브랜치 참조 정합성 업데이트 완료.

### 2단계: 데이터 주도형 동적 스폰 시스템 구축
*   [x] 엑셀(CSV) 형식의 시나리오 데이터([Scenario_List.csv](file:///D:/workspace/simulator_wp/Scenario_List.csv))를 언리얼 엔진 데이터 테이블로 임포트 완료.
*   [x] 레벨 블루프린트에서 `For Each Loop`를 활용해 CSV 행(Row) 데이터를 읽고, 각 좌표에 독립적인 전투기 객체(`BP_Fighter`)를 동적 스폰하는 로직 구현.
*   [x] 스폰 시 바닥 충돌로 인한 누락 현상 해결 — Z축 좌표 상향 조정 및 `Always Spawn, Ignore Collisions` 옵션 적용.

### 3단계: AI 컨트롤러 및 행위 트리 연동
*   [x] 전투기를 단순 Actor에서 AI가 탑승 가능한 `Pawn`으로 업그레이드.
*   [x] AI 3종 세트 생성 및 연동 완료:
    *   `AIC_Fighter` (AI 컨트롤러 / 조종사)
    *   `BB_Fighter` (블랙보드 / 기억 장치)
    *   `BT_Fighter` (행위 트리 / 판단 로직)
*   [x] Pawn에 `Auto Possess AI` 설정 완료.

### 4단계: 비동기 타이밍(Race Condition) 에러 해결
*   [x] **문제:** AI가 Pawn에 빙의하기 전에 블랙보드를 호출하여 `Accessed None` 오류 발생.
*   [x] **해결:** 불안정한 `Delay` 노드를 폐기하고, `AIC_Fighter` 중심의 명시적 초기화 아키텍처로 전면 개편:
    1.  `Event OnPossess` (빙의 확인)
    2.  `Use Blackboard` (블랙보드 생성 및 할당)
    3.  `Set Value as Name` (Pawn의 임무 데이터를 블랙보드에 기록)
    4.  `Run Behavior Tree` (데이터 준비 완료 후 판단 시작)

### 5단계: 규칙 기반(Rule-based) 행동 분기 구현
*   [x] 블랙보드 `MissionTarget` 변수 값("Drone", "Jet", "Ship")에 따라 행동을 분기하는 `Selector` 및 3개의 `Sequence` 분기점 구축 완료.
*   [x] 조건 불일치 시 행위 트리 강제 종료 방지를 위한 `Wait 500s` Fallback 안전망 노드 적용.
*   [x] 디버그 목록 실시간 모니터링 성공.

### 6단계: 대규모 확장 아키텍처 설계
*   [x] 256개+ 동시 실행을 위한 **지형 기반 오프셋(Geographic Offset)** 방식 설계 합의:
    *   시나리오별 거점(예: 강릉, 평양, 대구)의 절대 좌표를 중심으로 에이전트를 스폰하여 논리적/물리적 환경 격리.
    *   UE5 거대 월드 좌표(LWC)를 활용한 오차 제거.
    *   256개 환경이 동일한 Time Step을 공유하여 파이썬 측 데이터 노이즈 원천 차단.
*   [x] 학습 시 `-nullrhi` 헤드리스 모드 구동 정책 결정 (GPU 렌더링 부하 제거).
*   [x] 통신 규약으로 **gRPC** 채택 결정 (클라우드 분산 학습, 프레임워크 호환성, 스케일업 용이성).
*   [x] **gRPC 서버 배치 위치 결정: Python(에이전트) = Server / UE5(시뮬레이터) = Client** — 배치 추론 효율, 시스템 안정성, 확장성 분석 기반. ([분석 문서](file:///D:/workspace/simulator_wp/docs/grpc_server_placement_analysis.md))

### 7단계: 프로토콜 버퍼(.proto) 초안 설계
*   [x] `FighterRL.proto` 규약 초안 설계 완료:
    *   **AgentState (UE -> Python):** 환경 ID, 에이전트 종류, 3차원 좌표(X/Y/Z), 방향, 타겟 거리 등 관측 정보.
    *   **AgentAction (Python -> UE):** 엔진 추진력(Thrust), 조향(Steering) 등 제어 수치.

### 8단계: 시스템 아키텍처 다이어그램 및 분석 문서 작성 (2026-06-13)
*   [x] 전체 시스템 구조 Mermaid 다이어그램 작성 ([architecture_diagram.md](file:///D:/workspace/simulator_wp/docs/architecture_diagram.md)).
*   [x] gRPC 서버 배치 위치 기술 분석 문서 작성 및 승인 ([grpc_server_placement_analysis.md](file:///D:/workspace/simulator_wp/docs/grpc_server_placement_analysis.md)).

---

## 향후 작업 로드맵 (Roadmap)

### [ ] 다음 단계: gRPC 파이프라인 구축 (Python=Server / UE5=Client)
*   [ ] `FighterRL.proto` 파일 정식 작성 및 파이썬(pb2.py) / 언리얼(C++) 환경으로 컴파일.
*   [ ] **Python gRPC Server** 구축 (State 수신 → 배치 추론 → Action 응답).
*   [ ] 언리얼 엔진에 gRPC **Client** 통신 모듈 구현 (플러그인 또는 C++ 모듈).
*   [ ] 행위 트리(BT)에서 gRPC Client 노드를 호출하여 State 전송 / Action 수신 핵심 루프 완성.

### [ ] 단일 에이전트 E2E 통합 테스트
*   [ ] 단일 전투기 시나리오에서 UE <-> Python 간 State/Action 실시간 송수신 검증.

### [ ] 멀티 시나리오 파이프라인 확장
*   [ ] 32개/64개 이상의 시나리오가 독립된 gRPC 채널을 통해 비동기 송수신할 수 있도록 통신 모듈 확장.
*   [ ] 지형 기반 오프셋 아키텍처를 실제 레벨에 적용하여 256개+ 환경 동시 구동 검증.

### [ ] 강화학습 모델 연동 및 학습 루프 완성
*   [ ] 행위 트리와 강화학습 행동 데이터를 매핑하여 기동/타격 임무 비행 시뮬레이션 학습 루프 완성.
*   [ ] `-nullrhi` 헤드리스 모드에서의 대규모 학습 실행 검증.
