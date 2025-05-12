import uuid
import random
from ..constants.packet_constants import payload_types
from ..session.user_session import add_user
from ..utils.error.error_codes import SuccessCode
from ..utils.error.error_handler import handle_error
from ..utils.packet_sender import send_response
from ..utils.redis.redis import UserRedis, GameRedis

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

        # 유저 레디스 데이터 생성
        await UserRedis.create_user_data(account_id)
        
        # 게임 레디스 데이터 생성 (레벨 1로 시작)
        await GameRedis.create_game_data(account_id, 1)

        # 레디스 데이터 확인
        user_data = await UserRedis.get_user_data(account_id)
        game_data = await GameRedis.get_game_data(account_id)
        print(f"\n{'='*50}")
        print(f"유저 레디스 데이터: {user_data}")
        print(f"게임 레디스 데이터: {game_data}")
        print(f"{'='*50}\n")

        # PlayerData 생성 (테스트 용도 무작위값)
        player_data = {
            'playerId': account_id,
            'level': random.randint(1, 100),
            'exp': random.uniform(0, 1000),
            'posX': random.uniform(-10, 10),
            'posY': random.uniform(-10, 10),
            'posZ': random.uniform(-10, 10),
            'moveSpeed': random.uniform(1, 10),
            'currentHp': random.uniform(50, 100),
            'maxHp': random.uniform(100, 200),
            'healSpeed': random.uniform(1, 5),
            'atkPower': random.uniform(10, 50),
            'atkSpeed': random.uniform(1, 3),
            'maxSpeed': random.uniform(5, 15),
            'criticalChance': random.uniform(0, 0.5),
            'criticalMultiplier': random.uniform(1.5, 3),
            'defensivePower': random.uniform(5, 20),
            'cooldown': random.uniform(0.5, 2),
            'magnet': random.uniform(1, 5),
            'hitCount': random.randint(0, 1000),
            'totalDamageTaken': random.uniform(0, 5000),
            'totalDamage': random.uniform(0, 10000),
            'numMonsters': random.randint(0, 100),
            'nearMonsters': random.randint(0, 20),
            'killMonsters': random.randint(0, 500),
            'kpm': random.uniform(0, 10),
            'usedHPitems': random.randint(0, 50),
            'deletedItems': random.randint(0, 100),
            'numEquipments': random.randint(0, 10),
            'numOrnaments': random.randint(0, 5),
            'equipmentSlot': [{'equipment': random.randint(1, 100)} for _ in range(random.randint(0, 5))],
            'ornamentSlot': [{'ornament': random.randint(1, 50)} for _ in range(random.randint(0, 3))],
            'score': random.uniform(0, 10000),
            'survivalTime': random.uniform(0, 3600),
            'soulCont': random.randint(0, 1000),
            'keyCount': random.randint(0, 10),
            'IsAlive': random.choice([True, False])
        }

        payload = {
            'player': player_data  # 필드명은 프로토버퍼 파일 참고
        }

        # User 객체의 socket을 사용하여 응답 전송
        await user.socket.send_response(SuccessCode['Success'], '계정 생성 성공', payload_types['S_ENTER'], payload)
    except Exception as error:
        await handle_error(socket, error)
