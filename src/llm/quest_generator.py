import ollama
from ..protobuf import packet_pb2

def generate_quest_text(player: packet_pb2.PlayerData) -> str:
    player_status_prompt = f"""
    [플레이어 상태 요약]
    - 현재 체력: {player.currentHp} / {player.maxHp}
    - 이동 속도: {player.moveSpeed}
    - 생존 시간: {player.survivalTime:.1f}초
    - 적 처치 수: {player.killMonsters}
    - 현재 레벨: {player.level}
    """

    prompt = f"""
    {player_status_prompt}

    [퀘스트 생성 규칙]
    - 반드시 한국어로 출력
    - 오직 퀘스트 문장만 출력
    - 줄바꿈 없이 한 줄만 출력
    - 설명, 해설, Note, [플레이어 상태] 등 포함하지 마세요
    - 퀘스트는 하나만 생성

    [생존 퀘스트 예시]
    - 10초 동안 생존하세요.
    - 체력 회복 없이 15초 동안 살아남으세요.
    - 피해를 입지 않고 20초 동안 살아남으세요.
    - 10초 동안 계속 움직이세요.
    - 체력이 70% 이하인 상태에서 8초 동안 생존하세요.
    - 적을 처치하지 않고 12초 동안 생존하세요.
    - 5초 동안 가만히 멈춰 있으세요.
    - 적 3명에게 둘러싸인 상태에서 7초간 생존하세요.

    [전투 퀘스트 예시]
    - 적 5명을 10초 이내에 처치하세요.
    - 엘리트 몬스터를 20초 안에 처치하세요.
    - 체력이 70% 이하일 때 적 3명을 처치하세요.
    - 보스를 30초 안에 처치하세요.

    [점수/아이템 퀘스트 예시]
    - S등급 아이템을 2개 수집하세요.

    [생성 시 주의사항]
    - 너무 쉽거나 반복적인 퀘스트는 피해주세요.
    - 다양한 숫자 값과 조건을 조합하여 퀘스트를 생성해주세요.

    답변 형식:
    자연어 한 문장 퀘스트만 출력해주세요.
    """

    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"].strip()
