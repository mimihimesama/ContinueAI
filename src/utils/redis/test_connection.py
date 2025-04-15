import uuid
from .redis import game_redis, user_redis

async def test_user_redis_connection() -> None:
    """
    사용자 Redis 연결을 테스트하는 함수
    """
    try:
        user_uuid = str(uuid.uuid4())
        
        # 사용자 데이터 생성
        created = await user_redis.create_user_data(user_uuid)
        if not created:
            print('유저 데이터 생성 실패')
            return
            
        # 사용자 데이터 조회
        user_data = await user_redis.get_user_data(user_uuid)
        print('유저 레디스 테스트 결과:', user_data)
    except Exception as error:
        print('유저 레디스 실행 중 오류 발생: ', error)

async def test_game_redis_connection() -> None:
    """
    게임 Redis 연결을 테스트하는 함수
    """
    try:
        game_uuid = str(uuid.uuid4())
        level = 1
        
        # 게임 데이터 생성
        created = await game_redis.create_game_data(game_uuid, level)
        if not created:
            print('게임 데이터 생성 실패')
            return
            
        # 게임 데이터 조회
        game_data = await game_redis.get_game_data(game_uuid)
        print('게임 레디스 테스트 결과:', game_data)
    except Exception as error:
        print('게임 레디스 실행 중 오류 발생: ', error)

async def test_all_redis_connections() -> None:
    """
    모든 Redis 연결을 테스트하는 함수
    """
    await test_user_redis_connection()
    await test_game_redis_connection() 