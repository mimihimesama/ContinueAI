import uuid
import random
from ..constants.packet_constants import payload_types
from ..session.user_session import add_user
from ..utils.error.error_codes import SuccessCode
from ..utils.error.error_handler import handle_error
from ..utils.packet_sender import send_response

async def auto_login_handler(socket):
    try:
        # socket이 딕셔너리인 경우 실제 소켓 객체를 가져옴
        if isinstance(socket, dict):
            real_socket = socket.get('socket')
            if real_socket is None:
                raise Exception("Real socket not found")
            account_id = real_socket.session_id
        else:
            account_id = socket.session_id
            
        # 유저 세션에 추가
        user = add_user(socket, account_id)
        print(f"자동 로그인: {account_id}")

        # PlayerData 초기값 생성
        player_data = {
            'playerId': account_id,
            'level': 1,
            'exp': 0,
            'posX': 0,
            'posY': 0,
            'posZ': 0,
            'moveSpeed': 10,
            'currentHp': 80,
            'maxHp': 80,
            'healSpeed': 0.03,
            'atkPower': 1.2,
            'atkSpeed': 1,
            'maxSpeed': 3.5,
            'criticalChance': 5,
            'criticalMultiplier': 1.75,
            'defensivePower': 0,
            'cooldown': 0,
            'magnet': 1.5,
            'hitCount': 0,
            'totalDamageTaken': 0,
            'totalDamage': 0,
            'numMonsters': 0,
            'nearMonsters': 0,
            'killMonsters': 0,
            'kpm': 0,
            'usedHPitems': 0,
            'deletedItems': 0,
            'numEquipments': 0,
            'numOrnaments': 0,
            'equipmentSlot': [],
            'ornamentSlot': [],
            'score': 0.0,
            'survivalTime': 0.0,
            'soulCont': 0,
            'keyCount': 0,
            'IsAlive': True
        }

        payload = {
            'player': player_data  # 필드명은 프로토버퍼 파일 참고
        }

        # User 객체의 socket을 사용하여 응답 전송
        await user.socket.send_response(SuccessCode['Success'], '계정 생성 성공', payload_types['S_ENTER'], payload)
    except Exception as error:
        await handle_error(socket, error)
