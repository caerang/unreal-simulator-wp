# 시스템 아키텍처 다이어그램 (System Architecture Diagram)

본 문서는 **Unreal Engine 임무 비행 시뮬레이터 & gRPC 강화학습 에이전트 파이프라인** 프로젝트의 전체 시스템 구조를 시각화합니다.

---

## 1. 전체 시스템 구조 (Full System Overview)

```mermaid
graph TB
    subgraph UE5["Unreal Engine 5 Simulator"]
        direction TB
        CSV["Scenario_List.csv<br/>(시나리오 데이터)"]
        DT["Data Table<br/>(S_ScenarioData)"]
        LBP["Level Blueprint<br/>(For Each Loop 스폰)"]
        CSV --> DT --> LBP

        subgraph SCENARIOS["Multi-Scenario Instances (최대 256+)"]
            direction LR
            subgraph S1["Scenario A (Drone)"]
                F1["BP_Fighter (Pawn)"]
                AI1["AIC_Fighter"]
                BB1["BB_Fighter"]
                BT1["BT_Fighter"]
                F1 --- AI1
                AI1 --- BB1
                AI1 --- BT1
            end
            subgraph S2["Scenario B (Jet)"]
                F2["BP_Fighter (Pawn)"]
                AI2["AIC_Fighter"]
                BB2["BB_Fighter"]
                BT2["BT_Fighter"]
                F2 --- AI2
                AI2 --- BB2
                AI2 --- BT2
            end
            subgraph S3["Scenario N ..."]
                FN["BP_Fighter (Pawn)"]
                AIN["AIC_Fighter"]
                BBN["BB_Fighter"]
                BTN["BT_Fighter"]
                FN --- AIN
                AIN --- BBN
                AIN --- BTN
            end
        end

        LBP --> S1
        LBP --> S2
        LBP --> S3
    end

    subgraph GRPC["gRPC Pipeline (FighterRL.proto)"]
        direction LR
        STATE["AgentState<br/>(UE -> Python)<br/>환경ID, 좌표, 방향, 타겟거리"]
        ACTION["AgentAction<br/>(Python -> UE)<br/>Thrust, Steering"]
    end

    subgraph PYTHON["Python RL Agent"]
        direction TB
        SERVER["gRPC Server"]
        ENV["Environment Wrapper<br/>(State 수신 / Action 응답)"]
        MODEL["RL Model<br/>(PyTorch / RLlib)"]
        TRAIN["Training Loop<br/>(학습 루프)"]
        SERVER --- ENV
        ENV --- MODEL
        MODEL --- TRAIN
    end

    S1 -- "State" --> STATE
    S2 -- "State" --> STATE
    S3 -- "State" --> STATE
    STATE --> SERVER
    SERVER --> ACTION
    ACTION -- "Action" --> S1
    ACTION -- "Action" --> S2
    ACTION -- "Action" --> S3

    style UE5 fill:#1a1a2e,stroke:#e94560,stroke-width:2px,color:#eee
    style GRPC fill:#0f3460,stroke:#e94560,stroke-width:2px,color:#eee
    style PYTHON fill:#16213e,stroke:#e94560,stroke-width:2px,color:#eee
    style SCENARIOS fill:#162447,stroke:#1b6ca8,stroke-width:1px,color:#eee
    style S1 fill:#1b2838,stroke:#1b6ca8,stroke-width:1px,color:#eee
    style S2 fill:#1b2838,stroke:#1b6ca8,stroke-width:1px,color:#eee
    style S3 fill:#1b2838,stroke:#1b6ca8,stroke-width:1px,color:#eee
```

---

## 2. 시뮬레이터 내부 구조 (UE5 Simulator Detail)

```mermaid
graph TD
    subgraph DATA_LAYER["데이터 레이어"]
        CSV["Scenario_List.csv"]
        DT["UE Data Table<br/>(S_ScenarioData)"]
        CSV -- "Import" --> DT
    end

    subgraph SPAWN_LAYER["스폰 시스템"]
        LBP["Level Blueprint"]
        LOOP["For Each Loop<br/>(Row 순회)"]
        SPAWN["Spawn Actor<br/>(Always Spawn,<br/>Ignore Collisions)"]
        OFFSET["Geographic Offset<br/>(거점 좌표 기반<br/>환경 격리)"]
        LBP --> LOOP --> SPAWN
        OFFSET --> SPAWN
    end

    subgraph FIGHTER["전투기 (BP_Fighter)"]
        PAWN["Pawn<br/>(Auto Possess AI)"]
        AIC["AIC_Fighter<br/>(AI Controller)"]
        BB["BB_Fighter<br/>(Blackboard)"]
        BT["BT_Fighter<br/>(Behavior Tree)"]

        PAWN -- "1. OnPossess<br/>(빙의 확인)" --> AIC
        AIC -- "2. Use Blackboard<br/>(생성 및 할당)" --> BB
        AIC -- "3. Set Value as Name<br/>(MissionTarget 기록)" --> BB
        AIC -- "4. Run Behavior Tree<br/>(판단 시작)" --> BT
    end

    subgraph BT_LOGIC["행위 트리 분기 로직"]
        SEL["Selector"]
        SEQ_D["Sequence: Drone"]
        SEQ_J["Sequence: Jet"]
        SEQ_S["Sequence: Ship"]
        FALL["Fallback<br/>(Wait 500s)"]
        SEL --> SEQ_D
        SEL --> SEQ_J
        SEL --> SEQ_S
        SEL --> FALL
    end

    DT -- "시나리오 파라미터" --> LBP
    SPAWN -- "BP_Fighter 인스턴스" --> PAWN
    BT --> SEL
    BB -- "MissionTarget 값<br/>(Drone/Jet/Ship)" --> SEL

    style DATA_LAYER fill:#2d3436,stroke:#00b894,stroke-width:2px,color:#eee
    style SPAWN_LAYER fill:#2d3436,stroke:#0984e3,stroke-width:2px,color:#eee
    style FIGHTER fill:#2d3436,stroke:#e17055,stroke-width:2px,color:#eee
    style BT_LOGIC fill:#2d3436,stroke:#fdcb6e,stroke-width:2px,color:#eee
```

---

## 3. 에이전트 내부 구조 (Python RL Agent Detail)

```mermaid
graph TD
    subgraph COMM_LAYER["통신 레이어"]
        PROTO["FighterRL.proto<br/>(Protocol Buffers)"]
        GRPC_SRV["gRPC Server<br/>(포트 대기)"]
        PROTO -- "pb2.py 컴파일" --> GRPC_SRV
    end

    subgraph ENV_LAYER["환경 래퍼 레이어"]
        RECV["State 수신<br/>(AgentState)"]
        DECODE["관측 데이터 디코딩<br/>(환경ID, 좌표, 방향,<br/>타겟거리)"]
        ENCODE["행동 데이터 인코딩<br/>(Thrust, Steering)"]
        SEND["Action 응답<br/>(AgentAction)"]
        RECV --> DECODE --> MODEL_IN
        MODEL_OUT --> ENCODE --> SEND
    end

    subgraph ML_LAYER["강화학습 레이어"]
        MODEL_IN["Observation<br/>(관측 벡터)"]
        POLICY["Policy Network<br/>(정책 신경망)"]
        MODEL_OUT["Action<br/>(행동 벡터)"]
        REWARD["Reward 계산"]
        BUFFER["Experience Buffer<br/>(경험 저장)"]
        OPTIM["Optimizer<br/>(모델 업데이트)"]

        MODEL_IN --> POLICY --> MODEL_OUT
        MODEL_IN --> BUFFER
        MODEL_OUT --> BUFFER
        REWARD --> BUFFER
        BUFFER --> OPTIM --> POLICY
    end

    GRPC_SRV --> RECV
    SEND --> GRPC_SRV

    style COMM_LAYER fill:#2d3436,stroke:#a29bfe,stroke-width:2px,color:#eee
    style ENV_LAYER fill:#2d3436,stroke:#74b9ff,stroke-width:2px,color:#eee
    style ML_LAYER fill:#2d3436,stroke:#ff7675,stroke-width:2px,color:#eee
```

---

## 4. 대규모 병렬 실행 구조 (Geographic Offset)

```mermaid
graph LR
    subgraph WORLD["UE5 Large World Coordinates"]
        direction TB
        subgraph R1["거점 A (강릉)"]
            E1_1["Env 1"]
            E1_2["Env 2"]
            E1_3["Env ..."]
        end
        subgraph R2["거점 B (평양)"]
            E2_1["Env 33"]
            E2_2["Env 34"]
            E2_3["Env ..."]
        end
        subgraph R3["거점 C (대구)"]
            E3_1["Env 65"]
            E3_2["Env 66"]
            E3_3["Env ..."]
        end
        subgraph RN["거점 N"]
            EN_1["Env 225"]
            EN_2["Env 226"]
            EN_3["Env ...256+"]
        end
    end

    TICK["Shared Time Step<br/>(단일 틱 동기화)"]
    NULLRHI["-nullrhi<br/>(헤드리스 모드)"]

    TICK --> WORLD
    NULLRHI --> WORLD

    style WORLD fill:#1a1a2e,stroke:#e94560,stroke-width:2px,color:#eee
    style R1 fill:#1b2838,stroke:#00b894,stroke-width:1px,color:#eee
    style R2 fill:#1b2838,stroke:#0984e3,stroke-width:1px,color:#eee
    style R3 fill:#1b2838,stroke:#e17055,stroke-width:1px,color:#eee
    style RN fill:#1b2838,stroke:#a29bfe,stroke-width:1px,color:#eee
    style TICK fill:#0f3460,stroke:#eee,stroke-width:1px,color:#eee
    style NULLRHI fill:#0f3460,stroke:#eee,stroke-width:1px,color:#eee
```

---

## 5. 데이터 흐름 시퀀스 (State-Action Loop)

```mermaid
sequenceDiagram
    participant CSV as Scenario_List.csv
    participant LBP as Level Blueprint
    participant Fighter as BP_Fighter + AIC
    participant BT as BT_Fighter
    participant gRPC as gRPC Channel
    participant Agent as Python RL Agent

    CSV->>LBP: 시나리오 데이터 로드
    LBP->>Fighter: 동적 스폰 (Geographic Offset 적용)
    Fighter->>BT: OnPossess → Blackboard 초기화 → Run BT

    loop 매 Time Step
        BT->>gRPC: AgentState 전송 (환경ID, 좌표, 방향, 타겟거리)
        gRPC->>Agent: State 수신
        Agent->>Agent: Policy Network 추론
        Agent->>gRPC: AgentAction 응답 (Thrust, Steering)
        gRPC->>BT: Action 수신
        BT->>Fighter: Action 적용 (Add Actor Local Offset)
    end
```
