import time
from ..constants.packet_constants import packet_types, payload_key_names
from .packet_header import read_header, write_header
from .packet_serializer import serialize_ex
from .error.error_handler import handle_error

async def send_ping(socket, timestamp=None, dont_send=False):
    try:
        if timestamp is None:
            timestamp = int(time.time() * 1000)  # JavaScript의 Date.now()와 동일
        
        packet_data = {
            'timestamp': timestamp
        }
        
        serialized = serialize_ex(packet_types['PING'], 0, packet_data)
        header = write_header(len(serialized), packet_types['PING'])
        packet = header + serialized
        
        if dont_send:
            return packet
            
        socket.send(packet)
        
    except Exception as err:
        handle_error(socket, err)

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