from ..manager.interval_manager import IntervalManager
from ...utils.error.error_handler import handle_error
import time

class User:
    def __init__(self, account_id, socket):
        self.account_id = account_id
        self.socket = socket

        self.updated_at = int(time.time() * 1000)  # Date.now() 대응

        self.ping()
        IntervalManager.get_instance().add(
            self.account_id,
            self.ping,
            10000,  # PING_INTERVAL
            'ping'  # PING_INTERVAL_TYPE
        )

    async def ping(self):
        try:
            now = int(time.time() * 1000)
            if now - self.updated_at > 30000:
                # 30초 임시, timeout 처리
                pass
            self.socket.send_ping(now)
            # print(f"[{self.account_id}] PING")
        except Exception as err:
            await handle_error(self.socket, err)

    async def pong(self, data):
        try:
            now = int(time.time() * 1000)
            self.latency = (now - data['timestamp']) / 2
            # print(f"[{self.account_id}] Latency: {self.latency}ms")
        except Exception as err:
            await handle_error(self.socket, err)
