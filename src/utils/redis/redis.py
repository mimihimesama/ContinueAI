import json
from typing import Dict, Any, List, Optional
from ...init.redis_init import redis_client
from ...constants.redis_constants import (
    user_redis_fields as urf,
    game_redis_fields as grf,
    is_user_redis_field,
    is_game_redis_field,
)
from ...utils.error.custom_error import CustomError
from ...utils.error.error_codes import ErrorCodes

# Redis 키 접두사
USER_PREFIX = 'user:'
GAME_DATA_PREFIX = 'game:'

class UserRedis:
    """
    사용자 Redis 관련 기능을 제공하는 클래스
    """
    
    @staticmethod
    async def create_user_data(uuid: str) -> bool:
        """
        사용자 데이터를 생성하는 함수
        
        Args:
            uuid (str): 사용자 UUID
            
        Returns:
            bool: 생성 성공 여부
        """
        try:
            key_uuid = f'{USER_PREFIX}{uuid}:{urf["UUID"]}'
            return redis_client.set(key_uuid, json.dumps(uuid))
        except Exception as error:
            print('createUserData Error Message : ', error)
            return False
    
    @staticmethod
    async def set_user_data(uuid: str, obj: Dict[str, Any]) -> None:
        """
        사용자 데이터를 설정하는 함수
        
        Args:
            uuid (str): 사용자 UUID
            obj (Dict[str, Any]): 설정할 데이터
        """
        try:
            for key, value in obj.items():
                if is_user_redis_field(key):
                    redis_key = f'{USER_PREFIX}{uuid}:{key}'
                    await redis_client.set(redis_key, json.dumps(value))
        except Exception as err:
            print('setUserData failed:', err)
    
    @staticmethod
    async def get_user_data(uuid: str) -> Optional[Dict[str, Any]]:
        """
        사용자 데이터를 조회하는 함수
        
        Args:
            uuid (str): 사용자 UUID
            
        Returns:
            Optional[Dict[str, Any]]: 사용자 데이터
        """
        try:
            result = {}
            for key in urf.values():
                redis_key = f'{USER_PREFIX}{uuid}:{key}'
                value = redis_client.get(redis_key)
                if value:
                    result[key] = json.loads(value)
            return result if result else None
        except Exception as error:
            print('getUserData Error Message : ', error)
            return None
    
    @staticmethod
    async def get_user_data_ex(uuid: str, arr: List[str]) -> Dict[str, Any]:
        """
        특정 필드의 사용자 데이터를 가져오는 함수
        
        Args:
            uuid (str): 사용자 UUID
            arr (List[str]): 가져올 필드 목록
            
        Returns:
            Dict[str, Any]: 사용자 데이터
        """
        try:
            user_data = {}
            for key_name in arr:
                if is_user_redis_field(key_name):
                    redis_key = f'{USER_PREFIX}{uuid}:{key_name}'
                    result = json.loads(redis_client.get(redis_key))
                    user_data[key_name] = result
            return user_data
        except Exception as err:
            print('getUserDataEx failed:', err)
            return {}
    
    @staticmethod
    async def remove_user_data(uuid: str) -> None:
        """
        사용자 데이터를 제거하는 함수
        
        Args:
            uuid (str): 사용자 UUID
        """
        try:
            # TODO: 유저 정보 제거 작업
            keys = redis_client.keys(f'{USER_PREFIX}{uuid}:*')
            for key in keys:
                redis_client.delete(key)
        except Exception as err:
            print('removeUserData failed:', err)

class GameRedis:
    """
    게임 Redis 관련 기능을 제공하는 클래스
    """
    
    @staticmethod
    async def create_game_data(uuid: str, level: int) -> bool:
        """
        게임 데이터를 생성하는 함수
        
        Args:
            uuid (str): 게임 UUID
            level (int): 게임 레벨
            
        Returns:
            bool: 생성 성공 여부
        """
        try:
            key_uuid = f'{GAME_DATA_PREFIX}{uuid}:{grf["UUID"]}'
            key_level = f'{GAME_DATA_PREFIX}{uuid}:{grf["LEVEL"]}'
            redis_client.set(key_uuid, json.dumps(uuid))
            return redis_client.set(key_level, json.dumps(level))
        except Exception as error:
            print('createGameData Error Message : ', error)
            return False
    
    @staticmethod
    async def set_game_data(uuid: str, obj: Dict[str, Any]) -> None:
        """
        게임 데이터를 설정하는 함수
        
        Args:
            uuid (str): 사용자 UUID
            obj (Dict[str, Any]): 설정할 데이터
        """
        try:
            for key, value in obj.items():
                if is_game_redis_field(key):
                    redis_key = f'{GAME_DATA_PREFIX}{uuid}:{key}'
                    await redis_client.set(redis_key, json.dumps(value))
        except Exception as err:
            print('setGameData failed:', err)
    
    @staticmethod
    async def get_game_data(uuid: str) -> Optional[Dict[str, Any]]:
        """
        게임 데이터를 조회하는 함수
        
        Args:
            uuid (str): 게임 UUID
            
        Returns:
            Optional[Dict[str, Any]]: 게임 데이터
        """
        try:
            result = {}
            for key in grf.values():
                redis_key = f'{GAME_DATA_PREFIX}{uuid}:{key}'
                value = redis_client.get(redis_key)
                if value:
                    result[key] = json.loads(value)
            return result if result else None
        except Exception as error:
            print('getGameData Error Message : ', error)
            return None
    
    @staticmethod
    async def get_game_data_ex(uuid: str, arr: List[str]) -> Dict[str, Any]:
        """
        특정 필드의 게임 데이터를 가져오는 함수
        
        Args:
            uuid (str): 사용자 UUID
            arr (List[str]): 가져올 필드 목록
            
        Returns:
            Dict[str, Any]: 게임 데이터
        """
        try:
            game_data = {}
            for key_name in arr:
                if is_game_redis_field(key_name):
                    redis_key = f'{GAME_DATA_PREFIX}{uuid}:{key_name}'
                    result = json.loads(redis_client.get(redis_key))
                    game_data[key_name] = result
            return game_data
        except Exception as err:
            print('getGameDataEx failed:', err)
            return {}
    
    @staticmethod
    async def patch_game_data_level(uuid: str, by_amount: int) -> None:
        """
        게임 레벨을 수정하는 함수
        
        Args:
            uuid (str): 사용자 UUID
            by_amount (int): 수정할 레벨 값
        """
        try:
            if not isinstance(by_amount, int):
                raise CustomError(ErrorCodes.GAME_REDIS_DATA_ERROR, 'byAmount 값 에러')
            key = f'{GAME_DATA_PREFIX}{uuid}:{grf["LEVEL"]}'
            await redis_client.incrby(key, by_amount)
        except Exception as err:
            print('patchGameDataLevel failed:', err)
    
    @staticmethod
    async def remove_game_data(uuid: str) -> None:
        """
        게임 데이터를 제거하는 함수
        
        Args:
            uuid (str): 사용자 UUID
        """
        try:
            keys = redis_client.keys(f'{GAME_DATA_PREFIX}{uuid}:*')
            for key in keys:
                redis_client.delete(key)
        except Exception as error:
            print('removeGameData Error Message : ', error)

# 클래스 인스턴스 생성
user_redis = UserRedis()
game_redis = GameRedis() 