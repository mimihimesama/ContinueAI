import ollama
import random
from ..protobuf import packet_pb2

def generate_quest_text(player: packet_pb2.PlayerData) -> str:
    player_status_prompt = f"""
    [플레이어 현재 상태]
    - 현재 체력: {player.currentHp:.1f} / 최대 체력: {player.maxHp:.1f}
    - 처치한 몬스터 수: {player.killMonsters}
    - 경험치: {player.exp}
    - 현재 장비 수: {player.numEquipments}
    - 현재 장신구 수: {player.numOrnaments}
    - 생존 여부: {'생존' if player.IsAlive else '사망'}
    """

    prompt = f"""
    {player_status_prompt}

    [퀘스트 생성 규칙 - 중요: 이 규칙을 **절대적으로 엄수**하세요]
    - **어떤 추가적인 설명이나 문장도 없이, 오직 퀘스트 문장 하나만 생성해야 합니다.** "Here is the quest:", "새로운 퀘스트 시작:", "퀘스트:" 등의 서두 문구를 **절대 포함하지 마세요.**
    - **아래 [퀘스트 예시]에 있는 문장 구조와 단어를 그대로 사용하고, 숫자만 변경하여 퀘스트를 생성하세요.**
    - **숫자는 오직 정수만 사용하세요. (예: 10초, 80%) 소수점은 절대 사용하지 마세요. 1.4초, 80.0% 같은 형식은 절대 불가합니다.**
    - **다른 문장 구조, 새로운 표현, 다른 단어, 또는 새로운 단위는 절대 사용하지 마세요.**
    - **[퀘스트 예시]에 없는 새로운 유형의 퀘스트는 절대 생성하지 마세요.**
    - **퀘스트 문장 외에 설명, 해설, Note, 추가 지시사항 등 다른 내용은 절대 포함하지 마세요.**
    - **"이상" 이라는 단어는 절대 사용하지 마세요.**
    - 퀘스트 예시 중 다양한 퀘스트를 고르려고 노력하세요.

    [퀘스트 예시]
    - 10초 동안 계속 움직이세요.
    - 체력이 80% 이하인 상태에서 10초 동안 생존하세요.
    - 적을 처치하지 않고 10초 동안 생존하세요.
    - 10초 동안 가만히 멈춰 있으세요.
    - 적 5명에게 둘러싸인 상태에서 7초 생존하세요.
    - 10초 동안 생존하세요.
    - 체력 회복 없이 10초 동안 살아남으세요.
    - 피해를 입지 않고 10초 동안 살아남으세요.

    - 적 2명을 10초 이내에 처치하세요.
    - 엘리트 몬스터를 10초 안에 처치하세요.
    - 체력이 80% 이하일 때 적 10명을 처치하세요.
    - 보스를 40초 안에 처치하세요.

    - S등급 아이템을 2개 수집하세요.

    답변 형식:
    퀘스트 문장 한 문장만 출력해주세요.
    """

    possible_quests = []
    num_attempts = 5 # 퀘스트 생성 시도 횟수

    print("--- 퀘스트 생성 후보군 시작 ---") # 후보군 출력 시작 알림
    for i in range(num_attempts):
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 1.2}
        )
        quest_text = response["message"]["content"].strip()

        if quest_text not in possible_quests:
            possible_quests.append(quest_text)
            print(f"후보 {len(possible_quests)}: {quest_text}") # 각 후보 출력

    print("--- 퀘스트 생성 후보군 종료 ---") # 후보군 출력 종료 알림

    if possible_quests:
        return random.choice(possible_quests)
    else:
        return "새로운 퀘스트를 생성할 수 없습니다."