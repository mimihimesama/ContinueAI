import time
import asyncio
from ..constants.packet_constants import packet_types, payload_key_names
from .packet_header import read_header, write_header
from .packet_serializer import serialize_ex, serialize
from .error.error_handler import handle_error
from ..init.proto_init import get_proto_messages

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

        print(f"\n{'='*50}")
        print(f"[PONG] 응답 전송!")
        print(f"[PONG] Timestamp: {timestamp}")
        print(f"{'='*50}\n")
        
        serialized = serialize(PingPacketClass, packet_data)
        header = write_header(len(serialized), packet_types['PONG'])
        packet = header + serialized
        
        if dont_send:
            return packet
            
        # socket.send(packet)
        await asyncio.get_running_loop().sock_sendall(socket, packet)
        print(f"[send_ping] socket type: {type(socket)}")  # <class 'socket.socket'> 이어야 정상
        
    except Exception as err:
        await handle_error(socket, err)

async def send_response(socket, code, message, payload_type, payload, dont_send=False):
    try:
        packet_data = {
            'code': code,
            'message': message,
            'timestamp': int(time.time() * 1000),  # JavaScript의 Date.now()와 동일
            'payloadType': payload_type,
            'payload': payload
        }
        
        serialized_packet = serialize_ex(packet_types['RESPONSE'], payload_type, packet_data)
        
        log_packet(packet_types['RESPONSE'], payload_type, serialized_packet)
        
        header = write_header(len(serialized_packet), packet_types['RESPONSE'])
        packet = header + serialized_packet
        
        if dont_send:
            return packet
            
        socket.send(packet)
        
    except Exception as err:
        handle_error(socket, err)

def log_packet(packet_type, payload_type, serialized_packet):
    header_info = read_header(serialized_packet)
    print(f"sending: [{payload_type}] {get_payload_key_name(payload_type)}")