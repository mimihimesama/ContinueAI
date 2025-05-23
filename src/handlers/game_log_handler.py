from ..constants.packet_constants import payload_types
from ..utils.error.error_codes import SuccessCode
from ..utils.error.error_handler import handle_error
from ..utils.packet_sender import send_response
from ..utils.redis.redis import GameRedis
from google.protobuf.json_format import MessageToDict

def build_support_payload(ai_result: dict) -> dict:
    """
    AI 결과에서 의미 있는 support 효과만 추출하여 payload 형식으로 구성
    """
    support_payload = {}

    for key, value in ai_result.items():
        # area_* 계열 (dict 타입 필수)
        if key.startswith("area_") and isinstance(value, dict):
            if "range" in value and "value" in value:
                support_payload[key] = {
                    "range": value["range"],
                    "value": value["value"]
                }
            continue

        if value is None:
            continue

        if isinstance(value, (int, float)) and value == 0:
            continue

        support_payload[key] = value

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
        # logs = await GameRedis.get_recent_logs(account_id) // Redis에서 로그 가져오는 코드
        # ai_result = await run_ai(logs)

        # 테스트용 더미 AI 결과
        ai_result = {
            "shield_active": 1.0,
            "speed_up": 2.5,
            "area_slow": {"range": 5.0, "value": 0.3},
            "crit_boost": None,
            "cooldown_reduction": 0
        }

        payload = build_support_payload(ai_result)

        if not payload["support"]:
            print("\n[AI 우회] 유효한 서포트 항목 없음 → 응답 생략.\n")
            return

        await send_response(socket, SuccessCode['Success'], '서포팅 결과 전송 완료', payload_types['S_RESULT'], payload)
    except Exception as error:
        await handle_error(socket, error)
