from typing import Dict, Any

async def test_db_connection(pool: Any, db_name: str) -> None:
    """
    데이터베이스 연결을 테스트하는 함수
    
    Args:
        pool: 데이터베이스 연결 풀
        db_name (str): 데이터베이스 이름
    """
    try:
        result = await pool.execute_query('SELECT 1 + 1 AS solution')
        if result and len(result) > 0:
            print(f'{db_name} 테스트 쿼리 결과:', result[0][0])  # 튜플의 첫 번째 요소 사용
        else:
            print(f'{db_name} 테스트 쿼리 결과가 없습니다.')
    except Exception as error:
        print(f'{db_name} 테스트 쿼리 실행 중 오류 발생:', error)

async def test_all_db_connections(pools: Dict[str, Any]) -> None:
    """
    모든 데이터베이스 연결을 테스트하는 함수
    
    Args:
        pools (Dict[str, Any]): 데이터베이스 연결 풀 딕셔너리
    """
    await test_db_connection(pools['GAME_CHAR_DB'], 'GAME_CHAR_DB')
    await test_db_connection(pools['USER_DB'], 'USER_DB') 