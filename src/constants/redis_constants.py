from typing import Dict, List, Any

# 사용자 Redis 필드 정의
user_redis_fields: Dict[str, str] = {
    'UUID': 'uuid',
}

# 게임 Redis 필드 정의
game_redis_fields: Dict[str, str] = {
    'UUID': 'uuid',
    'LEVEL': 'user_level',
}

# Python에서는 Object.freeze()와 동일한 기능이 없으므로, 
# 상수처럼 사용하기 위해 frozenset으로 변환된 값 목록을 생성합니다.
user_redis_fields_array: List[str] = list(user_redis_fields.values())
game_redis_fields_array: List[str] = list(game_redis_fields.values())

def is_user_redis_field(field_name: str) -> bool:
    """
    주어진 필드 이름이 사용자 Redis 필드인지 확인합니다.
    
    Args:
        field_name (str): 확인할 필드 이름
        
    Returns:
        bool: 사용자 Redis 필드이면 True, 아니면 False
    """
    return field_name in user_redis_fields_array

def is_game_redis_field(field_name: str) -> bool:
    """
    주어진 필드 이름이 게임 Redis 필드인지 확인합니다.
    
    Args:
        field_name (str): 확인할 필드 이름
        
    Returns:
        bool: 게임 Redis 필드이면 True, 아니면 False
    """
    return field_name in game_redis_fields_array 