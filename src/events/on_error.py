from ..utils.error.custom_error import CustomError
from ..utils.error.error_handler import handle_error

async def on_error(client, err):
    """
    소켓 에러를 처리하는 함수
    
    Args:
        client: 클라이언트 소켓 래퍼
        err: 에러 객체
    """
    try:
        await handle_error(client.socket, err)
    except Exception as e:
        print(f"에러 처리 중 추가 에러 발생: {e}") 