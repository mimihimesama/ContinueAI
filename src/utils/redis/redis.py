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
    async def get_recent_logs(account_id: str, count: int = 60) -> List[Dict[str, Any]]:
        try:
            key = f"logs:{account_id}"
            logs = await redis_client.lrange(key, -count, -1)
            return [json.loads(log) for log in logs]
        except Exception as e:
            print(f"GameRedis.get_recent_logs 에러: {e}")

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
