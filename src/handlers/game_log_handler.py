from ..constants.packet_constants import payload_types
from ..utils.error.error_codes import SuccessCode
from ..utils.error.error_handler import handle_error
from ..utils.packet_sender import send_response
from ..utils.redis.redis import GameRedis
from google.protobuf.json_format import MessageToDict

async def game_log_handler(context):
    try:
        socket = context['socket']
        account_id = context['accountId']
        packet = context['packet']
        print(f"패킷 확인: {packet}")

        data_dict = MessageToDict(packet)
        await GameRedis.push_game_log(account_id, data_dict)
        print(f"게임 로그 Redis에 저장 완료: {data_dict}")

        # ✅ AI 분석 로직 자리 (예시)
        # logs = await GameRedis.get_recent_logs(account_id) // Redis에서 로그 가져오는 코드
        # result = await run_ai(logs)
        # if result["need_support"]:
        #     payload에 해당 값 담아서 send_response

        need_support = False  # send_response 우회 // AI 추가 전 로그 확인용

        if not need_support:
            print("\n[AI 우회] 지원 불필요 판단, 응답 생략.\n")
            return

        payload = {
            # 필요한 값 담아서
            # packet.proto 파일에서 S_RESULT 타입 수정 필요 (현재는 빈 객체)
        }

        await send_response(SuccessCode['Success'], '서포팅 결과 전송 완료', payload_types['S_RESULT'], payload)
    except Exception as error:
        await handle_error(socket, error)
