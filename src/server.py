import asyncio
import socket
import sys
from .init.index import init_server
from .config.config import config
from .events.on_connection import on_connection
from .db.database import close_pools

async def main():
    try:
        # 서버 초기화
        await init_server()
        
        # 소켓 서버 생성
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # 서버 바인딩 및 리스닝
        server.bind((config['server']['host'], config['server']['port']))
        server.listen()
        server.setblocking(False)  # 비동기 소켓 설정
        
        print(f"서버가 {config['server']['host']}:{config['server']['port']}에서 실행 중입니다.")
        print(f"서버 주소: {server.getsockname()}")
        
        try:
            while True:
                try:
                    # 클라이언트 연결 수락
                    client_socket, address = await asyncio.get_event_loop().sock_accept(server)
                    print(f"새로운 연결: {address}")
                    
                    # 클라이언트 연결 처리
                    client_socket.setblocking(False)
                    asyncio.create_task(on_connection(client_socket, address))
                    
                except Exception as e:
                    print(f"연결 처리 중 오류 발생: {e}")
                    continue
        finally:
            # 서버 종료 시 정리
            server.close()
            # 데이터베이스 풀 정리
            await close_pools()
                
    except Exception as error:
        print(f"서버 오류: {error}")
        sys.exit(1)  # 오류 발생 시 프로세스 종료

if __name__ == "__main__":
    asyncio.run(main()) 