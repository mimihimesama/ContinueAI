from ..manager.interval_manager import IntervalManager
from ...utils.error.error_handler import handle_error
from ...utils.packet_sender import send_ping, send_response
import time
import asyncio

class User:
    def __init__(self, account_id, socket):
        self.account_id = account_id
        # socket이 딕셔너리인 경우 처리
        if isinstance(socket, dict):
            # 딕셔너리를 소켓 래퍼로 변환
            class SocketWrapper:
                def __init__(self, socket_dict):
                    self.socket_dict = socket_dict
                
                def send_response(self, code, message, type, payload):
                    return send_response(self.socket_dict, code, message, type, payload)
            
            self.socket = SocketWrapper(socket)
        else:
            self.socket = socket

