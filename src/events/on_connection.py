import asyncio
import uuid
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
        self.session_id = str(uuid.uuid4())  # 세션 ID 생성
        self.last_ping_time = asyncio.get_event_loop().time()
        self.is_connected = True
    
    def send_ping(self):
        return send_ping(self.socket)
    
    def send_response(self, data):
        return send_response(self.socket, data)
    
    def send(self, data):
        try:
            # Windows에서는 일반 send를 사용
            self.socket.send(data)
        except Exception as e:
            print(f"소켓 전송 오류: {e}")
            raise
    
    def close(self):
        if self.is_connected:
            try:
                self.socket.close()
            except:
                pass
            self.is_connected = False

async def check_ping_timeout(client):
    """PING 타임아웃을 체크하는 함수"""
    while client.is_connected:
        current_time = asyncio.get_event_loop().time()
        if current_time - client.last_ping_time > 3.0:  # 3초 이상 PING이 없으면 연결 종료
            print(f"\n{'='*50}")
            print(f"PING 타임아웃: {client.address} (Session ID: {client.session_id})")
            print(f"마지막 PING 수신: {current_time - client.last_ping_time:.1f}초 전")
            print(f"{'='*50}\n")
            
            client.close()
            break
        await asyncio.sleep(0.5)  # 0.5초마다 체크

async def on_connection(socket, address):
    # 클라이언트 소켓 래퍼 생성
    client = ClientSocketWrapper(socket, address)

    print(f"\n{'='*50}")
    print(f'클라이언트가 연결되었습니다: {address[0]}, {address[1]} (Session ID: {client.session_id})')
    print(f"{'='*50}\n")

    try:
        # 데이터 처리 핸들러 준비
        handler = await on_data(client)
        
        # PING 타임아웃 체크 태스크 시작
        ping_check_task = asyncio.create_task(check_ping_timeout(client))
        
        while client.is_connected:
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
                
            except ConnectionAbortedError:
                print(f"\n{'='*50}")
                print(f"클라이언트 연결 강제 종료: {address} (Session ID: {client.session_id})")
                print(f"{'='*50}\n")
                break
            except Exception as e:
                print(f"데이터 처리 중 오류 발생: {e}")
                await on_error(client, e)
                break
                
    except Exception as e:
        print(f"연결 처리 중 오류 발생: {e}")
    finally:
        print(">> finally 블록 진입")
        # PING 체크 태스크 취소
        if 'ping_check_task' in locals():
            try:
                await ping_check_task
            except asyncio.CancelledError:
                pass
                
        # 연결 종료 처리
        await on_end(client)
        client.close()
        print(f"소켓 닫힘: {address}")