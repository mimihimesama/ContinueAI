import logging
from google.protobuf.message import DecodeError
from google.protobuf import descriptor_pool
from google.protobuf import message_factory
from google.protobuf import text_format
from google.protobuf.internal.decoder import _DecodeVarint32
from ..utils.packet_sender import send_response
from ..protobuf.packet_pb2 import PlayerData, S_QuestResponse
from ..llm.quest_generator import generate_quest_text
from ..constants.packet_constants import packet_types, payload_types  # payload_types도 필요함



async def handle_generate_quest(context: dict):
    try:
        client = context['socket']
        data = context['packet']  # 이건 이미 역직렬화된 `C_QuestRequest` protobuf 객체

        player_data = data.player  # data: C_QuestRequest
        quest_text = generate_quest_text(player_data)

        # QuestResult 메시지 생성
        quest_result = S_QuestResponse()
        quest_result.questText = quest_text

        # 응답 전송 (code=200, message="success", payloadType=QUEST_RESULT)
        await send_response(
            socket=client.socket,                   # 실제 소켓
            code=200,
            message="success",
            type=payload_types['S_QUEST_RESPONSE'],     # ← S_QUEST_RESPONSE 타입
            payload=quest_result                    # ← payload로 보낼 protobuf 메시지
        )

    except DecodeError as e:
        logging.error(f"[에러] PlayerData 파싱 실패: {e}")
    except Exception as e:
        logging.error(f"[에러] 퀘스트 생성 처리 중 문제 발생: {e}")