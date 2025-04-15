from ..utils.transform_case import string_to_camel_case, string_to_pascal_case

# 프로토콜 관련 상수
PROTOCOL_PREFIX = 'Google.Protobuf.Protocol.'
PACKET_SUFFIX = 'Packet'

# 헤더 관련 상수
header_constants = {
    'TOTAL_LENGTH': 4,  # bytes
    'PACKET_TYPE_LENGTH': 1,
}

# 패킷 타입 정의
packet_types = {
    'PING': 1,
    'REQUEST': 2,
    'RESPONSE': 3,
}

# 페이로드 타입 정의
payload_types = {
    'C_ENTER': 1,
    'S_ENTER': 2,
    'C_LOG': 3,
    'S_RESULT': 4,
}

# 패킷 이름 매핑
packet_names = {
    value: PROTOCOL_PREFIX + string_to_pascal_case(key) + PACKET_SUFFIX
    for key, value in packet_types.items()
}

# 페이로드 이름 매핑
payload_names = {
    value: PROTOCOL_PREFIX + key[:2] + string_to_pascal_case(key[2:])
    for key, value in payload_types.items()
}

# 타입 매핑
type_mappings = {
    value: packet_types['RESPONSE'] if key.startswith('S') else packet_types['REQUEST']
    for key, value in payload_types.items()
}

# 페이로드 키 타입 매핑
payload_key_to_types = {}

# 페이로드 키 이름 매핑
payload_key_names = {}
for key, value in payload_types.items():
    payload_key = string_to_camel_case(key)
    payload_key_to_types[payload_key] = value
    payload_key_names[value] = payload_key

def get_payload_name_by_payload_type(payload_type):
    """
    페이로드 타입에 해당하는 메시지 이름을 반환하는 함수
    
    Args:
        payload_type (int): payload_types에 매핑된 타입
        
    Returns:
        str: payload_type에 맞는 Message 이름, 없으면 None
    """
    if payload_type in payload_names:
        return payload_names[payload_type]
    return None 