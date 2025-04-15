import os
import sys
import asyncio
from pathlib import Path
from typing import Any

from ..database import pools

async def execute_sql_file(pool: Any, file_path: str) -> None:
    """
    SQL 파일을 실행하는 함수
    
    Args:
        pool: 데이터베이스 연결 풀
        file_path (str): SQL 파일 경로
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    queries = [query.strip() for query in sql.split(';') if query.strip()]
    
    for query in queries:
        await pool.execute(query)

async def create_schemas() -> None:
    """
    데이터베이스 스키마를 생성하는 함수
    """
    sql_dir = Path(__file__).parent.parent / 'sql'
    try:
        await execute_sql_file(pools.USER_DB, sql_dir / 'user_db.sql')
        await execute_sql_file(pools.GAME_CHAR_DB, sql_dir / 'game_char_db.sql')
        print('데이터베이스 테이블이 성공적으로 생성되었습니다.')
    except Exception as error:
        print('데이터베이스 테이블 생성 중 오류가 발생했습니다:', error)
        raise

async def main() -> None:
    """
    메인 함수
    """
    try:
        await create_schemas()
        print('마이그레이션이 완료되었습니다.')
        sys.exit(0)  # 마이그레이션 완료 후 프로세스 종료
    except Exception as error:
        print('마이그레이션 중 오류가 발생했습니다:', error)
        sys.exit(1)  # 오류 발생 시 프로세스 종료

if __name__ == '__main__':
    asyncio.run(main()) 