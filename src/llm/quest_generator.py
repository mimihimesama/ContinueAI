import ollama
from ..protobuf import packet_pb2

def generate_quest_text(player: packet_pb2.PlayerData) -> str:
    player_status_prompt = f"""
[플레이어 현재 상태]
- 레벨: {player.level}
- 현재 체력: {player.currentHp:.1f} / 최대 체력: {player.maxHp:.1f}
- 이동 속도: {player.moveSpeed:.1f}
- 생존 시간: {player.survivalTime:.1f}초
- 처치한 몬스터 수: {player.killMonsters}
- 경험치: {player.exp}
- 총 피해량: {player.totalDamage:.1f}
- 받은 총 피해량: {player.totalDamageTaken:.1f}
- 현재 장비 수: {player.numEquipments}
- 현재 장신구 수: {player.numOrnaments}
- 현재 점수: {player.score}
- 생존 여부: {'생존' if player.IsAlive else '사망'}
"""

    prompt = f"""
{player_status_prompt}

[퀘스트 생성 규칙]
- **반드시 아래 [퀘스트 예시]에 있는 문장 구조와 단어를 그대로 사용하고, 오직 숫자만 변경하여 플레이어에게 적합한 퀘스트를 한국어로 한 문장만 생성해주세요.**
- **변경하는 숫자는 int 타입으로 생성하세요**
- **다른 문장 구조, 표현, 단어, 단위는 절대 사용하지 마세요.**
- 퀘스트 예시에 없는 새로운 유형의 퀘스트는 생성하지 마세요.
- 설명, 해설, Note, 추가 지시사항 등 퀘스트 문장 외의 다른 내용은 절대 포함하지 마세요.
- 퀘스트는 반드시 한 줄로 요약된 한국어 자연어 문장으로만 출력되어야 합니다.
- "이상" 이라는 단어를 사용하지 마세요.
- 너무 쉽거나 반복적인 퀘스트는 피하고, 플레이어의 현재 상태에 맞춰 적절히 난이도를 조절하여 새로운 도전 과제를 제시해주세요.

[퀘스트 예시]
- 10초 동안 생존하세요.
- 체력 회복 없이 15초 동안 살아남으세요.
- 피해를 입지 않고 20초 동안 살아남으세요.
- 10초 동안 계속 움직이세요.
- 체력이 70% 이하인 상태에서 8초 동안 생존하세요.
- 적을 처치하지 않고 12초 동안 생존하세요.
- 5초 동안 가만히 멈춰 있으세요.
- 적 3명에게 둘러싸인 상태에서 7초간 생존하세요.

- 적 5명을 10초 이내에 처치하세요.
- 엘리트 몬스터를 20초 안에 처치하세요.
- 체력이 70% 이하일 때 적 3명을 처치하세요.
- 보스를 30초 안에 처치하세요.

- S등급 아이템을 2개 수집하세요.

답변 형식:
퀘스트 문장 한 문장만 출력해주세요.
"""

    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"].strip()