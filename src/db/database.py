import aiomysql
from typing import Dict, Any
from ..config.config import config

databases = config['databases']

# 데이터베이스 풀을 저장할 변수
pools = {}

async def create_pool(db_config: Dict[str, Any]) -> aiomysql.Pool:
    """
    데이터베이스 커넥션 풀을 생성하는 함수
    
    Args:
        db_config (Dict[str, Any]): 데이터베이스 설정
        
    Returns:
        aiomysql.Pool: 생성된 커넥션 풀
    """
    pool = await aiomysql.create_pool(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        db=db_config['name'],
        autocommit=True,
        maxsize=10,  # 커넥션 풀에서 최대 연결 수
        minsize=1,
    )
    
    # 쿼리 실행 시 로그를 출력하는 래퍼 함수
    async def execute_query(sql: str, params: tuple = None) -> Any:
        # 쿼리 실행시 로그
        # print(
        #     f"[{datetime.now()}] Executing query: {sql} "
        #     f"{f', {params}' if params else ''}"
        # )
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, params)
                return await cur.fetchall()
    
    # 원본 execute_query 함수를 래퍼 함수로 대체
    pool.execute_query = execute_query
    
    return pool

async def init_pools():
    """
    모든 데이터베이스 풀을 초기화하는 함수
    """
    for db_name, db_config in databases.items():
        try:
            pools[db_name] = await create_pool(db_config)
            print(f"'{db_name}' 데이터베이스 풀이 생성되었습니다.")
        except Exception as e:
            print(f"'{db_name}' 데이터베이스 풀 생성 실패: {e}")
            raise

async def close_pools():
    """
    모든 데이터베이스 풀을 종료하는 함수
    """
    for db_name, pool in pools.items():
        try:
            pool.close()
            await pool.wait_closed()
            print(f"'{db_name}' 데이터베이스 풀이 종료되었습니다.")
        except Exception as e:
            print(f"'{db_name}' 데이터베이스 풀 종료 실패: {e}")
            # 오류가 발생해도 계속 진행
            continue 