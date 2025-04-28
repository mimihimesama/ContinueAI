import asyncio
from .on_end import on_end
from .on_error import on_error
from .on_data import on_data
from ..utils.packet_sender import send_ping, send_response

# 클라이언트 소켓 래퍼 클래스
class ClientSocketWrapper:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.buffer = bytearray()
    
    def send_ping(self):
        return send_ping(self.socket)
    
    def send_response(self, data):
        return send_response(self.socket, data)
    
    async def send(self, data):
        try:
            # Windows에서는 일반 send를 사용
            self.socket.send(data)
        except Exception as e:
            print(f"소켓 전송 오류: {e}")
            raise
    
    def close(self):
        self.socket.close()

async def on_connection(socket, address):
    print(f"\n{'='*50}")
    print(f'클라이언트가 연결되었습니다: {address[0]}, {address[1]}')
    print(f"{'='*50}\n")
    
    # 클라이언트 소켓 래퍼 생성
    client = ClientSocketWrapper(socket, address)
    
    try:
        # 데이터 처리 핸들러 준비
        handler = await on_data(client)
        
        while True:
            try:
                # 데이터 수신
                data = await asyncio.get_event_loop().sock_recv(client.socket, 1024)
                if not data:
                    print(f"클라이언트 연결 종료: {address}")
                    break
                
                print(f"\n{'='*50}")
                print(f"데이터 수신: {address}")
                print(f"Raw data: {data.hex()}")
                print(f"Length: {len(data)} bytes")
                
                # 데이터 처리
                await handler(data)
                
            except Exception as e:
                print(f"데이터 처리 중 오류 발생: {e}")
                await on_error(client, e)
                break
                
    except Exception as e:
        print(f"연결 처리 중 오류 발생: {e}")
    finally:
        # 연결 종료 처리
        await on_end(client)
        client.close()
        print(f"소켓 닫힘: {address}")