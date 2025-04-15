import redis
from ..config.config import config

# Redis 연결
redis_client = redis.Redis(
    host=config['redis']['redisHost'],
    port=config['redis']['redisPort'],
    db=0,
    decode_responses=True,
)

# Redis 연결 이벤트 핸들러
def on_connect():
    print('Redis connected!')

def on_error(err):
    print('Redis Client Error', err)

# Redis 연결 이벤트 핸들러 등록
redis_client.ping()  # 연결 테스트
print('Redis connected!')  # 연결 성공 메시지 출력

# Redis 클라이언트 반환
redis_client = redis_client 