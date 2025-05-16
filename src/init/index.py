import sys
import asyncio
from ..db.database import pools, init_pools
from ..utils.db.test_connection import test_all_db_connections
from .proto_init import load_proto_files
from .redis_init import test_redis_connection

async def init_server() -> None:
    """
    서버 초기화 함수
    """
    try:
        # 데이터베이스 풀 초기화
        await init_pools()
        
        await load_proto_files()
        await test_all_db_connections(pools)
        await test_redis_connection()
    except Exception as e:
        print(e)
        sys.exit(1)  # 오류 발생 시 프로세스 종료

# 서버 초기화 함수 반환
init_server = init_server 