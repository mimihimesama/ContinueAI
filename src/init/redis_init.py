from ..config.config import config
import redis.asyncio as aioredis

# Redis 연결
redis_client = aioredis.Redis(
    host=config['redis']['redisHost'],
    port=config['redis']['redisPort'],
    db=0,
    decode_responses=True,
    protocol=3,
)

# 연결 테스트용 함수만 정의 (실행은 X)
async def test_redis_connection():
    try:
        await redis_client.ping()
        print('Redis connected!')
    except Exception as e:
        print('Redis connection failed:', e)

# Redis 클라이언트 반환
redis_client = redis_client 