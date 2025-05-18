import asyncio
import socket
import sys
import subprocess
from .init.index import init_server
from .config.config import config
from .events.on_connection import on_connection
from .db.database import close_pools

ollama_process = None

# Ollama 모델도 서버가 켜질 때 같이 켜지도록
async def start_ollama():
        global ollama_process
        try:
            # 이미 실행 중인지 확인 
            ollama_process = subprocess.Popen(
                ["ollama", "run", "llama3"],
                stdout=subprocess.DEVNULL,  # 필요하면 로그 출력 제거
                stderr=subprocess.DEVNULL
            )
            print("🦙 Ollama 모델(Llama3)이 백그라운드에서 실행되었습니다.")
        except Exception as e:
            print(f"⚠️ Ollama 실행 실패: {e}")

async def main():
        try:
            # LLM 실행
            await start_ollama()

            # 서버 초기화
            await init_server()

            # 소켓 서버 생성
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            server.bind((config['server']['host'], config['server']['port']))
            server.listen()
            server.setblocking(False)

            print(f"🚀 서버가 {config['server']['host']}:{config['server']['port']} 에서 실행 중입니다.")

            try:
                while True:
                    try:
                        # 클라이언트 연결 수락
                        client_socket, address = await asyncio.get_event_loop().sock_accept(server)
                        print(f"새로운 연결: {address}")

                        # 클라리언트 연결 처리
                        client_socket.setblocking(False)
                        asyncio.create_task(on_connection(client_socket, address))

                        
                    except Exception as e:
                        print(f"연결 처리 중 오류: {e}")
                        continue
            finally:
                # 서버 종료 시 정리
                server.close()
                # 데이터베이스 풀 정리
                # await close_pools()

                if ollama_process:
                    ollama_process.terminate()
                    print("🛑 Ollama 프로세스를 종료했습니다.")

        except Exception as error:
            print(f"서버 오류: {error}")
            sys.exit(1) # 오류 발생 시 프로세스 종료

if __name__ == "__main__":
        asyncio.run(main())
