from ..constants.packet_constants import payload_types
from ..utils.error.custom_error import CustomError
from ..utils.error.error_codes import ErrorCodes
from .auto_login_handler import auto_login_handler
from .game_log_handler import game_log_handler
from .quest_handler import handle_generate_quest  # ← 추가

# 패킷 타입에 따른 핸들러 매핑
handlers = {
    payload_types['C_ENTER']: auto_login_handler,
     payload_types['C_LOG']: game_log_handler,
    payload_types['C_QUEST_REQUEST']: handle_generate_quest,  # ← 이 줄 추가
}

def get_handler_by_payload_type(payload_types):
    if payload_types not in handlers:
        raise CustomError(
            ErrorCodes.UNKNOWN_HANDLER_ID,
            f'핸들러를 찾을 수 없습니다: ID {payload_types}',
        )
    return handlers[payload_types] 