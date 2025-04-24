import asyncio
from ..constants.packet_constants import header_constants, packet_types
from ..handlers.index import get_handler_by_payload_type
from ..utils.error.error_codes import ErrorCodes
from ..utils.error.error_handler import handle_error
from ..utils.packet_header import read_header
from ..utils.packet_serializer import deserialize_by_packet_type
from ..utils.error.custom_error import CustomError
from ..session.user_session import get_user_by_socket
from ..utils.packet_sender import send_ping

header_size = header_constants['TOTAL_LENGTH'] + header_constants['PACKET_TYPE_LENGTH']

async def on_data(socket):
    async def handle_data(data):
        try:
            socket.buffer.extend(data)

            print(f"버퍼 길이: {len(socket.buffer)}")
            print(f"버퍼 내용: {socket.buffer.hex()}")

            while len(socket.buffer) >= header_size:
                print(f"\n헤더 파싱:")
                header_info = read_header(socket.buffer)
                total_length = header_info['totalLength']
                packet_type = header_info['packetType']
                print(f"Total Length: {total_length}")
                print(f"Packet Type: {packet_type}")

                if total_length > len(socket.buffer):
                    break

                packet = socket.buffer[header_size:total_length]
                socket.buffer = socket.buffer[total_length:]

                print(f"패킷 내용: {packet.hex()}")

                if packet_type == packet_types['PING']:
                    print(f"[PING] 패킷 수신됨!")

                    decoded = deserialize_by_packet_type(packet_types['PING'], packet)
                    print(f"[PING] 디코딩된 데이터: {decoded}")
                    
                    # PONG 응답 전송 (유저 체크 없이)
                    await send_ping(socket.socket, decoded.timestamp)
                    print("[PONG] 응답 전송 완료")

                elif packet_type == packet_types['REQUEST']:
                    result = deserialize_by_packet_type(packet_type, packet)
                    payload_type = result.get('payloadType')
                    payload = result.get('payload')
                    handler = get_handler_by_payload_type(payload_type or 0)
                    await handler({
                        'socket': socket,
                        'accountId': getattr(socket, 'accountId', None),
                        'packet': payload
                    })

        except Exception as err:
            await handle_error(socket, err)

    return handle_data
