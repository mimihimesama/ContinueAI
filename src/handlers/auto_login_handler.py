import uuid
from ..constants.packet_constants import payload_types
from ..session.user_session import add_user
from ..utils.error.error_codes import SuccessCode
from ..utils.error.error_handler import handle_error

async def auto_login_handler(socket):
    try:
        account_id = str(uuid.uuid4())  # UUID 생성
        await add_user(socket, account_id)  # User 객체 생성 및 세션에 저장
        print(f"자동 로그인: {account_id}")

        payload = {
            'accountId': account_id
        }
        socket.send_response(SuccessCode.Success, '계정 생성 성공', payload_types['S_ENTER'], payload)
    except Exception as error:
        await handle_error(socket, error)
