# GEMINI.md (Project Context & Instructions)

이 파일은 **Unreal Engine 임무 비행 시뮬레이터 & gRPC 강화학습 에이전트 파이프라인 연동 프로젝트**의 핵심 아키텍처, 기술 스택, 그리고 에이전트가 준수해야 할 작업 규칙을 정의합니다. 

> [!NOTE]
> 이 파일은 Antigravity CLI 세션이 시작될 때 자동으로 로드되어 에이전트의 컨텍스트와 규칙을 강제하는 역할을 합니다.

---

## 📖 프로젝트 개요 (Overview)
강화학습(RL) 기반의 전투기 임무 비행 세부 작전 기동 학습을 수행하기 위해, **언리얼 엔진 기반 시뮬레이터(환경)**와 **파이썬 기반 에이전트(모델)**를 **gRPC 파이프라인**으로 연결하고, **대규모 병렬 시나리오(32~64개)**가 동시에 실행될 수 있도록 개발하는 프로젝트입니다.

---

## 🧩 아키텍처 및 요구사항 (Key Requirements)
1.  **시뮬레이터 (Unreal Engine 5)**
    *   **임무 비행 시나리오:** 행위 트리(Behavior Tree) 기반 제어.
    *   **환경 동적 변경:** 전투기의 시작 위치, 타격 대상 종류 및 위치 등을 동적으로 설정하고 변경 가능해야 합니다.
2.  **임무 비행 에이전트 (Python)**
    *   강화학습 기반으로 작동하며, 최적의 세부 작전 기동을 학습합니다.
3.  **gRPC 연동 파이프라인**
    *   언리얼 시뮬레이터(C++ / Blueprint)와 파이썬 강화학습 에이전트가 gRPC를 사용하여 상태(State) 데이터와 행동(Action) 데이터를 실시간 송수신합니다.
4.  **병렬성 (Multi-Scenario)**
    *   최소 32개~64개의 시나리오 인스턴스가 독립적으로 동시 실행되어야 합니다.

---

## 📂 프로젝트 구조 및 핵심 파일 (Directory Structure)
*   **[PROGRESS.md](file:///D:/workspace/simulator_wp/PROGRESS.md):** 프로젝트 진행 상황 및 개발 로드맵 관리 파일.
*   **[GEMINI.md](file:///D:/workspace/simulator_wp/GEMINI.md):** 프로젝트 컨텍스트 및 에이전트 작업 지침 가이드 (본 파일).
*   **[docs/design.md](file:///D:/workspace/simulator_wp/docs/design.md):** 프로젝트 상위 기획 및 설계 사양서.
*   **`Content/` (언리얼 에셋 폴더):**
    *   `BP_Fighter.uasset`: 전투기 액터 블루프린트.
    *   `AIC_Fighter.uasset`: 전투기 AI 컨트롤러.
    *   `BB_Fighter.uasset`: 전투기 블랙보드.
    *   `BP_ScenarioData.umap`: 임무 비행 테스트 및 학습용 시나리오 맵/레벨.
    *   `S_ScenarioData.uasset`: 시나리오 매개변수 구조체 데이터.

---

## 🛠️ 기술 스택 및 도구 (Tech Stack)
*   **3D Environment:** Unreal Engine
*   **Agent / ML:** Python (가상환경 관리는 `uv` 사용)
*   **IPC Protocol:** gRPC / Protocol Buffers
*   **Version Control:** Git (Branch: `main`)

---

## 📜 에이전트 작업 규칙 (Agent Instruction Rules)
*   **가상환경 사용:** 파이썬 실행 및 라이브러리 설치 시 전역 파이썬 대신 반드시 `uv`를 사용해 생성한 가상환경(`.venv` 또는 지정 가상환경) 내부에서 실행할 것.
*   **진행 상태 동기화:** 작업을 마칠 때마다 또는 주요 마일스톤 완료 시 [PROGRESS.md](file:///D:/workspace/simulator_wp/PROGRESS.md)의 작업 내역 및 상태를 주기적으로 업데이트할 것.
*   **코드 컨벤션:** 언리얼 엔진 명명 규칙 및 PEP 8 파이썬 코딩 스타일을 준수할 것.
