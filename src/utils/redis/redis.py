import json
from typing import Dict, Any, List
from datetime import datetime
from ...init.redis_init import redis_client

class GameRedis:
    """
    게임 Redis 관련 기능을 제공하는 클래스
    """

    @staticmethod
    async def push_game_log(account_id: str, log_data: Dict[str, Any]) -> None:
        try:
            key = f"logs:{account_id}"
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                **log_data
            }
            await redis_client.rpush(key, json.dumps(log_entry))
            await redis_client.ltrim(key, -60, -1)
        except Exception as e:
            print(f"GameRedis.push_game_log 에러: {e}")

    @staticmethod
    async def get_recent_class_logs(account_id: str) -> List[Dict[str, Any]]:
        """
        Redis에서 최근 로그 7개를 가져옴
        """
        try:
            key = f"logs:{account_id}"
            logs = await redis_client.lrange(key, -7, -1)
            return [json.loads(log) for log in logs]
        except Exception as e:
            print(f"GameRedis.get_recent_class_logs 에러: {e}")

    @staticmethod
    async def get_recent_buff_logs(account_id: str) -> List[Dict[str, Any]]:
        """
        Redis에서 최근 로그 18개를 가져옴
        """
        try:
            key = f"logs:{account_id}"
            logs = await redis_client.lrange(key, -18, -1)
            return [json.loads(log) for log in logs]
        except Exception as e:
            print(f"GameRedis.get_recent_buff_logs 에러: {e}")

    @staticmethod
    async def remove_log_data(account_id: str) -> None:
        try:
            key = f'logs:{account_id}'
            await redis_client.delete(key)
            print(f"{key} 삭제 완료")
        except Exception as error:
            print('remove_log_data Error Message : ', error)


# 클래스 인스턴스 생성
game_redis = GameRedis()
