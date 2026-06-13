# GEMINI.md (Project Context & Instructions)

이 파일은 **Unreal Engine 임무 비행 시뮬레이터 & gRPC 강화학습 에이전트 파이프라인 연동 프로젝트**의 핵심 아키텍처, 기술 스택, 그리고 에이전트가 준수해야 할 작업 규칙을 정의합니다. 

> [!NOTE]
> 이 파일은 Antigravity CLI 세션이 시작될 때 자동으로 로드되어 에이전트의 컨텍스트와 규칙을 강제하는 역할을 합니다.

---

## 📖 프로젝트 개요 (Overview)
강화학습(RL) 기반의 전투기 임무 비행 세부 작전 기동 학습을 수행하기 위해, **언리얼 엔진 5 기반 시뮬레이터(환경)**와 **파이썬 기반 에이전트(모델)**를 **gRPC 파이프라인**으로 연결하고, **대규모 병렬 시나리오(최대 256개+)**가 동시에 실행될 수 있도록 개발하는 프로젝트입니다.

**현재 단계:** gRPC 파이프라인 연동용 C++ 하이브리드 모듈 및 플러그인(TurboLink) 빌드 완료, 파이썬 gRPC 서버 구축 완료 / 언리얼 블루프린트(행위 트리) 및 통신 노드 연동 대기

---

## 🧩 아키텍처 및 요구사항 (Key Requirements)
1.  **시뮬레이터 (Unreal Engine 5)**
    *   **임무 비행 시나리오:** 행위 트리(Behavior Tree) 기반 제어.
    *   **데이터 주도형 스폰:** 외부 CSV(`Scenario_List.csv`)에서 시나리오 데이터를 읽어 전투기를 동적 스폰.
    *   **환경 동적 변경:** 전투기의 시작 위치, 타격 대상 종류(Drone/Jet/Ship) 및 위치 등을 동적으로 설정하고 변경 가능.
    *   **AI 제어 구조:** `AIC_Fighter`(AI 컨트롤러) → `BB_Fighter`(블랙보드) → `BT_Fighter`(행위 트리) 3종 연동.
2.  **임무 비행 에이전트 (Python)**
    *   강화학습 기반으로 작동하며, 최적의 세부 작전 기동을 학습합니다.
    *   PyTorch, RLlib 등 프레임워크 활용.
3.  **gRPC 연동 파이프라인**
    *   **Python(에이전트) = gRPC Server** / **UE5(시뮬레이터) = gRPC Client** 구조.
    *   UE5가 매 Tick마다 State를 Python 서버로 전송하고, Python이 Action을 응답하는 방식.
    *   **AgentState (UE → Python):** 환경 ID, 에이전트 종류, 3차원 좌표, 방향, 타겟 거리 등 관측 정보.
    *   **AgentAction (Python → UE):** 엔진 추진력(Thrust), 조향(Steering) 등 제어 수치.
    *   배치 추론: 다수 환경의 State를 모아 GPU에서 한 번에 처리하여 학습 효율 극대화.
4.  **병렬성 (Multi-Scenario)**
    *   최소 32개~64개, 최대 256개+ 시나리오 인스턴스가 독립적으로 동시 실행.
    *   **지형 기반 오프셋(Geographic Offset):** 시나리오별 거점 좌표를 중심으로 에이전트를 스폰하여 환경 격리.
    *   **UE5 LWC(Large World Coordinates)** 활용, 모든 환경이 동일한 Time Step 공유.
    *   학습 시 `-nullrhi` 헤드리스 모드로 GPU 렌더링 부하 제거.

---

## 📂 프로젝트 구조 및 핵심 파일 (Directory Structure)
*   **[PROGRESS.md](file:///D:/workspace/simulator_wp/PROGRESS.md):** 프로젝트 진행 상황 및 개발 로드맵 관리 파일.
*   **[GEMINI.md](file:///D:/workspace/simulator_wp/GEMINI.md):** 프로젝트 컨텍스트 및 에이전트 작업 지침 가이드 (본 파일).
*   **`docs/` (문서 폴더):**
    *   [design.md](file:///D:/workspace/simulator_wp/docs/design.md): 프로젝트 상위 기획 및 설계 사양서.
    *   [UE5_MultiAgent_Simulator_Architecture.md](file:///D:/workspace/simulator_wp/docs/UE5_MultiAgent_Simulator_Architecture.md): 상세 아키텍처 설계 및 구현 이력 문서.
    *   [architecture_diagram.md](file:///D:/workspace/simulator_wp/docs/architecture_diagram.md): 전체 시스템 구조 Mermaid 다이어그램.
    *   [grpc_server_placement_analysis.md](file:///D:/workspace/simulator_wp/docs/grpc_server_placement_analysis.md): gRPC 서버 배치 위치 분석 문서.
*   **[Scenario_List.csv](file:///D:/workspace/simulator_wp/Scenario_List.csv):** 시나리오 데이터 (ID, 타겟 종류, 스폰 위치).
*   **`Content/` (언리얼 에셋 폴더):**
    *   `BP_Fighter.uasset`: 전투기 Pawn 블루프린트.
    *   `AIC_Fighter.uasset`: 전투기 AI 컨트롤러.
    *   `BB_Fighter.uasset`: 전투기 블랙보드.
    *   `BT_Fighter.uasset`: 전투기 행위 트리.
    *   `BP_ScenarioData.umap`: 임무 비행 테스트 및 학습용 시나리오 맵/레벨.
    *   `S_ScenarioData.uasset`: 시나리오 매개변수 구조체 데이터.

---

## 🛠️ 기술 스택 및 도구 (Tech Stack)
*   **3D Environment:** Unreal Engine 5 (LWC 활용)
*   **Agent / ML:** Python (가상환경 관리는 `uv` 사용, PyTorch / RLlib)
*   **IPC Protocol:** gRPC / Protocol Buffers (`FighterRL.proto`)
*   **Version Control:** Git (Branch: `main`)
*   **Repository:** [github.com/caerang/unreal-simulator-wp](https://github.com/caerang/unreal-simulator-wp)

---

## 📜 에이전트 작업 규칙 (Agent Instruction Rules)
*   **가상환경 사용:** 파이썬 실행 및 라이브러리 설치 시 전역 파이썬 대신 반드시 `uv`를 사용해 생성한 가상환경(`.venv` 또는 지정 가상환경) 내부에서 실행할 것.
*   **진행 상태 동기화:** 작업을 마칠 때마다 또는 주요 마일스톤 완료 시 [PROGRESS.md](file:///D:/workspace/simulator_wp/PROGRESS.md)의 작업 내역 및 상태를 주기적으로 업데이트할 것.
*   **코드 컨벤션:** 언리얼 엔진 명명 규칙 및 PEP 8 파이썬 코딩 스타일을 준수할 것.
*   **문서 정합성:** 아키텍처나 설계 변경 시 관련 문서([design.md](file:///D:/workspace/simulator_wp/docs/design.md), [UE5_MultiAgent_Simulator_Architecture.md](file:///D:/workspace/simulator_wp/docs/UE5_MultiAgent_Simulator_Architecture.md))도 함께 갱신할 것.
