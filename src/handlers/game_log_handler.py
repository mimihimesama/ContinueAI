from ..constants.packet_constants import payload_types
from ..utils.error.error_codes import SuccessCode
from ..utils.error.error_handler import handle_error
from ..utils.packet_sender import send_response
from ..utils.redis.redis import GameRedis
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import random
import time
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime, timedelta
from google.protobuf.json_format import MessageToDict

FEATURES = [
    "survivalTime", "killMonsters", "kpm", "totalDamage", "totalDamageTaken",
    "level", "hitCount", "usedHPitems", "totalHealAmount",
    "atkPower", "atkSpeed", "criticalChance", "criticalMultiplier",
    "cooldown", "defensivePower", "healSpeed", "numEquipments", "numOrnaments"
]


BUFF_COOLDOWNS = {
    "shield_active": 15,
    "invincibility": 60,
    "boss_buff": 15,
    "hp_guard": 45,
    "periodic_heal": 15,
    "speed_up": 15,
    "attack_speed_up": 15,
    "attack_up": 15,
    "defense_up": 15,
    "cooldown_reduction": 15,
    "berserk_mode": 15,
    "crit_boost": 15,
    "xp_boost": 15,
    "area_slow": 15,
}


last_buff_times={}
last_global_buff_time = None
GLOBAL_BUFF_COOLDOWN = 20 #sec
active_buffs = {}



def coerce_numeric_fields(context: dict, fields: list):
    for key in fields:
        if key in context:
            try:
                context[key] = float(context[key])
            except (ValueError, TypeError):
                print(f"[WARN] {key} 변환 실패 → 원본값: {context.get(key)}")
                context[key] = 0.0
        else:
            context[key] = 0.0



def get_or_default(context: dict, key: str, default: float = 0.0):
    try:
        return float(context[key])
    except (KeyError, TypeError, ValueError):
        return default



def danger_score(context):
    def get_or_default(key, default=0.0):
        val = context.get(key)
        try:
            return float(val)
        except (TypeError, ValueError):
            print(f"[WARN] {key} 변환 실패 → 원본값: {val}")
            return default

    hp = get_or_default("currentHp", 80.0)
    max_hp = max(get_or_default("maxHp", 80.0), 1.0)
    hp_ratio = hp / max_hp

    near_monsters = get_or_default("nearMonsters", context.get("numMonsters", 0.0))
    hit_count = get_or_default("hitCount", 0.0)
    used_hp_items = get_or_default("usedHPitems", 0.0)
    total_heal = get_or_default("totalHealAmount", 0.0)
    kpm = get_or_default("kpm", 1.0)
    defense = get_or_default("defensivePower", 10.0)


    # 계산 항목
    d1 = near_monsters * 1.0
    d2 = (1 - hp_ratio) * 20
    d3 = min(hit_count, 10) * 1.5
    d4 = used_hp_items * 1.0
    d5 = (total_heal / 10) * 0.5
    d6 = (1 / max(kpm, 0.1)) * 0.5
    d7 = 5 if defense < 10 else 0

    danger = d1 + d2 + d3 + d4 + d5 + d6 + d7

    return round(danger, 2)



def is_buff_on_cooldown(account_id, buff_name):
    now = time.time()
    cooldown = BUFF_COOLDOWNS.get(buff_name)
    if cooldown is None:
        return False
    last_time = last_buff_times.get((account_id, buff_name), 0)
    return now - last_time < cooldown

def set_buff_timestamp(account_id, buff_name):
    last_buff_times[(account_id, buff_name)] = time.time()





def recommend_buff(context):
    global last_global_buff_time
    now = datetime.now()

    if last_global_buff_time and (now - last_global_buff_time).total_seconds() < GLOBAL_BUFF_COOLDOWN:
        remaining = GLOBAL_BUFF_COOLDOWN - (now - last_global_buff_time).total_seconds()
        print(f"[INFO] 글로벌 버프 쿨다운 중 - 남은 시간: {remaining:.1f}s")
        print_active_buffs()
        return None

    danger = danger_score(context)
    context["danger_score"] = danger
    hp_ratio = context.get("currentHp", 0) / max(context.get("maxHp", 1), 1)

    if danger > 40:
        buff = "invincibility"
    elif danger > 25 and hp_ratio < 0.2:
        buff = "hp_guard"
    elif context.get("boss_exists", True) and random.random() < 0.5:
        buff = "boss_buff"
    else:
        buff = random.choice([
            "shield_active", "periodic_heal", "speed_up", "attack_speed_up",
            "attack_up", "defense_up", "cooldown_reduction", "berserk_mode",
            "crit_boost", "xp_boost", "area_slow"
        ])

    last_global_buff_time = now
    return buff


def apply_buff(buff_name: str, duration: float):
    global active_buffs, last_buff_times, last_global_buff_time
    now = datetime.now()
    active_buffs[buff_name] = (now, duration)
    last_buff_times[buff_name] = now
    last_global_buff_time = now
    print_active_buffs()
    


def print_active_buffs():
    now = datetime.now()
    expired = []
    print("\n[ACTIVE BUFFS 상태]")
    for buff, (start_time, duration) in active_buffs.items():
        elapsed = (now - start_time).total_seconds()
        remaining = round(duration - elapsed, 2)
        if remaining > 0:
            print(f" - {buff}: 남은 시간 {remaining:.2f}초")
        else:
            print(f" - {buff}: 종료됨 → 제거 예정")
            expired.append(buff)
    for buff in expired:
        del active_buffs[buff]
        print(f"[INFO] '{buff}' 버프가 만료되어 제거되었습니다.")



def build_support_payload(ai_result: dict) -> dict:
    support_payload = {}
    for key, effect in ai_result.items():
        if not isinstance(effect, dict):
            continue
        duration = effect.get("duration", 0.0)
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
            if effect["bool_value"]:
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

        logs = await GameRedis.get_filtered_logs(account_id)
        raw_user = logs[-1] if logs else {}
        user = raw_user.get("player", raw_user)
        
        
        def calculate_score(user):
            score = (
                user.get("survivalTime", 0)
                + user.get("killMonsters", 0) * 5
                + user.get("totalDamage", 0) / 100
                + user.get("level", 0) * 50
                - user.get("hitCount", 0) * 5
                - user.get("usedHPitems", 0) * 10
                - user.get("totalHealAmount", 0) * 0.5
            )
            return round(max(score, 0), 2)

        user["score"] = calculate_score(user)

        def train_model(sample_user, n_samples=1000):
            data = []
            for _ in range(n_samples):
                noisy_user = {}
                for feature in FEATURES:
                    base_value = sample_user.get(feature) or 0.0
                    noise = random.uniform(-1, 1)
                    noisy_user[feature] = base_value + noise
                noisy_user["score"] = calculate_score(noisy_user)
                data.append(noisy_user)
            df = pd.DataFrame(data)
            try:
                df["class"] = pd.qcut(df["score"], 7, labels=False, duplicates='drop')
            except ValueError:
                df["class"] = 0
            df = df.dropna(subset=["class"])
            X = df[FEATURES]
            y = df["class"].astype(int)
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X, y)
            return model

        def predict_user_class(user_data, model):
            user_input = [[user_data.get(feature, 0) for feature in FEATURES]]
            return model.predict(user_input)[0]

        model = train_model(user)
        predicted_class = predict_user_class(user, model)
        print(f"예측된 사용자 클래스: {predicted_class}")

        def generate_ai_support(predicted_class: int, context: dict, selected_buff: str) -> dict:
            def scale(value, base_min=0.4, base_max=1.0):
                scale_factor = 1 - (predicted_class / 6)
                strength = base_min + (base_max - base_min) * scale_factor
                return round(value * strength, 2)

            base_buffs = {
                "shield_active": {"float_value": 30.0, "duration": 15.0},
                "invincibility": {"int_value": 1, "duration": 5.0},
                "boss_buff": {"bool_value": True, "duration": 15.0},
                "hp_guard": {"int_value": 1, "duration": 8.0},
                "periodic_heal": {"float_value": 0.15, "duration": 15.0},
                "speed_up": {"float_value": 0.2, "duration": 16.0},
                "attack_speed_up": {"float_value": 0.2, "duration": 16.0},
                "attack_up": {"float_value": 0.3, "duration": 16.0},
                "defense_up": {"int_value": 5, "duration": 16.0},
                "cooldown_reduction": {"float_value": 0.25, "duration": 16.0},
                "berserk_mode": {"float_value": 0.3, "duration": 15.0},
                "crit_boost": {"float_value": 0.2, "duration": 15.0},
                "xp_boost": {"float_value": 1.5, "duration": 20.0},
                "area_slow": {"float_value": 0.3, "duration": 15.0},
            }

            base = base_buffs.get(selected_buff)
            if not base:
                return {}

            buff = {}
            if "float_value" in base:
                buff["float_value"] = scale(base["float_value"])
            if "int_value" in base:
                buff["int_value"] = int(scale(base["int_value"]))
            if "bool_value" in base:
                buff["bool_value"] = base["bool_value"]
            buff["duration"] = scale(base["duration"])

            return {selected_buff: buff}

        selected_buff = recommend_buff(user)
        ai_result = generate_ai_support(predicted_class, user, selected_buff)
        payload = build_support_payload(ai_result)
        
        if selected_buff and selected_buff in ai_result:
            duration = ai_result[selected_buff].get("duration", 0)
            apply_buff(selected_buff, duration)
            print_active_buffs()

        if not payload["support"]:
            print("\n[AI 우회] 유효한 서포트 항목 없음 → 응답 생략.\n")
            return

        await send_response(socket, SuccessCode['Success'], '서포팅 결과 전송 완료', payload_types['S_RESULT'], payload)

    except Exception as error:
        await handle_error(socket, error)
