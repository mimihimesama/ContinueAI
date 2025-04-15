from ..utils.error.error_handler import handle_error

async def on_end(client):
    """
    소켓 연결 종료를 처리하는 함수
    
    Args:
        client: 클라이언트 소켓 래퍼
    """
    try:
        print(f"클라이언트 연결이 종료되었습니다: {client.address}")
    except Exception as e:
        print(f"연결 종료 처리 중 에러 발생: {e}") 