import grpc
from concurrent import futures
import time
import random

import FighterRL_pb2
import FighterRL_pb2_grpc

class FighterServiceServicer(FighterRL_pb2_grpc.FighterServiceServicer):
    def SendState(self, request, context):
        # 1. State 정보 수신 및 로그 출력 (너무 잦은 출력 방지를 위해 시나리오 1 위주로 찍거나 간단하게 찍음)
        # 256개 병렬 실행 시 너무 많은 출력이 발생하므로, 간단하게 1줄 포맷으로 출력하거나 특정 시나리오만 디버그 출력
        if request.env_id == "Scenario_1" or random.random() < 0.01:
            print(f"[{request.env_id}] Pos: ({request.pos_x:.1f}, {request.pos_y:.1f}, {request.pos_z:.1f}) | Target: {request.target_type} | Dist: {request.target_dist:.1f} | Reward: {request.reward:.2f}")

        # 2. 더미 액션 결정 로직
        # 디폴트 전진 기동, 타겟 방향 선회를 흉내내거나 더미 액션 지정
        thrust = 0.85
        steering_yaw = random.uniform(-0.2, 0.2)
        steering_pitch = random.uniform(-0.1, 0.1)
        steering_roll = random.uniform(-0.1, 0.1)
        
        # 거리가 매우 가까우면(예: 1500m 이내) 무장 발사 시도
        fire = request.target_dist > 0 and request.target_dist < 1500.0
        
        # 3. Action 응답 생성
        action = FighterRL_pb2.AgentAction(
            thrust=thrust,
            steering_yaw=steering_yaw,
            steering_pitch=steering_pitch,
            steering_roll=steering_roll,
            fire=fire
        )
        return action

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=32))
    FighterRL_pb2_grpc.add_FighterServiceServicer_to_server(FighterServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("========================================")
    print("  Fighter RL gRPC Dummy Server Started  ")
    print("  Listening on port: 50051             ")
    print("========================================")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("\nStopping gRPC Server...")
        server.stop(0)

if __name__ == '__main__':
    serve()
