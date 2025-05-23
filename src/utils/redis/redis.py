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
    async def get_filtered_logs(account_id: str, count: int = 60) -> List[Dict[str, Any]]:
        """
        Redis에서 최근 로그를 가져오되, player 필드 내 특정 key만 추출하여 반환
        """
        try:
            target_keys = [
                "survival_time", "kill_monsters", "kpm", "total_damage", "totalDamageTaken",
                "level", "hit_count", "used_hp_items", "total_heal_amount",
                "atkPower", "atkSpeed", "criticalChance", "criticalMultiplier",
                "cooldown", "defensivePower", "healSpeed", "numEquipments", "numOrnaments"
            ]

            key = f"logs:{account_id}"
            logs = await redis_client.lrange(key, -count, -1)
            parsed_logs = [json.loads(log) for log in logs]

            filtered_logs = []
            for log in parsed_logs:
                player_data = log.get("player", {})
                extracted = {key: player_data.get(key) for key in target_keys}
                filtered_logs.append(extracted)

            return filtered_logs

        except Exception as e:
            print(f"GameRedis.get_filtered_logs 에러: {e}")

# 클래스 인스턴스 생성
game_redis = GameRedis()
