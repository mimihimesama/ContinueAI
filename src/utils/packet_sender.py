import time
import asyncio
from ..constants.packet_constants import packet_types, payload_key_names
from .packet_header import read_header, write_header
from .packet_serializer import serialize_ex, serialize
from .error.error_handler import handle_error
from ..init.proto_init import get_proto_messages

class SocketWrapper:
    """딕셔너리 소켓/일반 소켓 모두 지원하는 전송용 래퍼"""
    def __init__(self, socket):
        self.socket = socket

    async def send(self, data):
        try:
            if isinstance(self.socket, dict):
                real_socket = self.socket.get('socket')
            else:
                real_socket = self.socket

            if real_socket is None:
                raise Exception("Real socket not found")

            if hasattr(real_socket, 'fileno'):
                await asyncio.get_running_loop().sock_sendall(real_socket, data)
            else:
                await real_socket.send(data)
        except Exception as e:
            print(f"Socket 전송 실패: {e}")
            raise

async def send_packet(socket, packet):
    """공통 전송 함수"""
    try:
        wrapper = SocketWrapper(socket)
        await wrapper.send(packet)
    except Exception as err:
        await handle_error(socket, err)

async def send_ping(socket, timestamp=None, dont_send=False):
    try:
        if timestamp is None:
            print("timestamp is None")
            timestamp = int(time.time() * 1000)  # JavaScript의 Date.now()와 동일

        PingPacketClass = get_proto_messages()['packet']['PONG']
        
        packet_data = {
            'timestamp': timestamp,
            'serverTimestamp': int(time.time() * 1000)
        }

        print(f"{'='*50}")
        print(f"[PONG] 응답 전송!")
        
        serialized = serialize(PingPacketClass, packet_data)
        header = write_header(len(serialized), packet_types['PONG'])
        packet = header + serialized
        
        if dont_send:
            return packet
            
        await send_packet(socket, packet)

        print(f"[send_ping] 완료 - timestamp: {timestamp}")
        print(f"{'='*50}\n")
            
    except Exception as err:
        await handle_error(socket, err)

async def send_response(socket, code, message, type, payload=None):
    try:
        # 응답 패킷 데이터 구성
        packet_data = {
            'code': code,
            'message': message,
            'timestamp': int(time.time() * 1000),
            'payloadType': type  # payloadType은 payload_types의 값을 사용
        }
        
        # payload가 있는 경우에만 추가
        if payload is not None:
            # payloadType에 따른 필드명 동적 매핑
            field_name = payload_key_names.get(type)
            if field_name:
                packet_data[field_name] = payload
        
        print(f"[RESPONSE] 전송 시작")
        print(f"Code: {code}")
        print(f"Message: {message}")
        print(f"Payload Type: {type}")
        print(f"Packet Type: {packet_types['RESPONSE']}")  # 항상 RESPONSE(4)를 사용
        print(f"Payload: {payload}")
        
        # 패킷 직렬화 (패킷 타입은 항상 RESPONSE(4)를 사용)
        serialized_packet = serialize_ex(packet_types['RESPONSE'], type, packet_data)
        header = write_header(len(serialized_packet), packet_types['RESPONSE'])  # 헤더에도 RESPONSE(4) 사용
        packet = header + serialized_packet
        
        await send_packet(socket, packet)
        
        print(f"\n[RESPONSE] 전송 완료")
        print(f"\n{'='*50}\n")
        
    except Exception as error:
        print(f"\n{'='*50}")
        print(f"[RESPONSE] 전송 실패")
        print(f"Error: {error}")
        print(f"{'='*50}\n")
        await handle_error(socket, error)

def log_packet(packet_type, payload_type, serialized_packet):
    header_info = read_header(serialized_packet)
    print(f"sending: [{payload_type}] {get_payload_key_name(payload_type)}")