from ..constants.packet_constants import payload_types
from ..utils.error.error_codes import SuccessCode
from ..utils.error.error_handler import handle_error
from ..utils.packet_sender import send_response
from ..utils.redis.redis import GameRedis
from google.protobuf.json_format import MessageToDict

def build_support_payload(ai_result: dict) -> dict:
    """
    AI 결과를 oneof + duration 구조에 맞춰 payload로 구성
    """
    support_payload = {}

    for key, effect in ai_result.items():
        if not isinstance(effect, dict):
            continue

        duration = effect.get("duration", 0.0)

        # oneof 값 중 하나만 선택
        if "float_value" in effect and effect["float_value"] not in (None, 0):
            support_payload[key] = {
                "float_value": effect["float_value"],
                "duration": duration
            }
        elif "int_value" in effect and effect["int_value"] not in (None, 0):
            support_payload[key] = {
                "int_value": effect["int_value"],
                "duration": duration
            }
        elif "bool_value" in effect:
            if effect["bool_value"]:  # True인 경우만 전송
                support_payload[key] = {
                    "bool_value": True,
                    "duration": duration
                }

    return {"support": support_payload}


async def game_log_handler(context):
    try:
        socket = context['socket']
        account_id = context['accountId']
        packet = context['packet']
        print(f"패킷 확인: {packet}")

        data_dict = MessageToDict(packet)
        await GameRedis.push_game_log(account_id, data_dict)
        print(f"게임 로그 Redis에 저장 완료: {data_dict}\n")

        # ✅ AI 분석 로직 자리 (예시)
        logs = await GameRedis.get_filtered_logs(account_id) # Redis에서 로그 가져오는 코드
        print(f"최근 로그: {logs}\n")

        # 테스트용 더미 AI 결과
        ai_result = {
            "shield_active": {"float_value": 1.0, "duration": 5.0},
            "invincibility": {"int_value": 1, "duration": 3.0},
            "boss_buff": {"bool_value": True, "duration": 10.0},
        }

        payload = build_support_payload(ai_result)

        if not payload["support"]:
            print("\n[AI 우회] 유효한 서포트 항목 없음 → 응답 생략.\n")
            return

        await send_response(socket, SuccessCode['Success'], '서포팅 결과 전송 완료', payload_types['S_RESULT'], payload)
    except Exception as error:
        await handle_error(socket, error)
