import asyncio
from ..constants.packet_constants import header_constants, packet_types
from ..handlers.index import get_handler_by_payload_type
from ..utils.error.error_codes import ErrorCodes
from ..utils.error.error_handler import handle_error
from ..utils.packet_header import read_header
from ..utils.packet_serializer import deserialize_by_packet_type
from ..utils.error.custom_error import CustomError
from ..session.user_session import get_user_by_socket

header_size = header_constants['TOTAL_LENGTH'] + header_constants['PACKET_TYPE_LENGTH']

async def on_data(socket):
    async def handle_data(data):
        try:
            socket.buffer.extend(data)
            while len(socket.buffer) >= header_size:
                header_info = read_header(socket.buffer)
                total_length = header_info['totalLength']
                packet_type = header_info['packetType']

                if total_length > len(socket.buffer):
                    break

                packet = socket.buffer[header_size:total_length]
                socket.buffer = socket.buffer[total_length:]

                if packet_type == packet_types['PING']:
                    user = get_user_by_socket(socket)
                    if not user:
                        raise CustomError(ErrorCodes.USER_NOT_FOUND, 'Ping을 수신할 유저가 없습니다.')
                    user.pong(deserialize_by_packet_type(packet_types['PING'], packet))

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
