import json
from google.protobuf.json_format import MessageToDict
from ..constants.packet_constants import packet_types, payload_key_names
from ..init.proto_init import get_proto_messages
from .error.custom_error import CustomError
from .error.error_codes import ErrorCodes

def _get_message_type_by_packet_type(packet_type):
    """패킷 타입을 통해 메시지 타입을 반환하는 유틸리티 함수"""
    for name, value in packet_types.items():
        if value == packet_type:
            return get_proto_messages()['packet'][name]
    raise CustomError(
        ErrorCodes.INVALID_PACKET,
        f"유효하지 않은 패킷 타입: {packet_type}"
    )

def serialize(message_type, data):
    """
    메시지 타입과 데이터를 직렬화하는 함수
    
    Args:
        message_type: 프로토콜 버퍼 메시지 타입
        data: 직렬화할 데이터
        
    Returns:
        bytes: 직렬화된 데이터
        
    Raises:
        CustomError: 직렬화 과정에서 오류 발생 시
    """
    if not message_type:
        raise CustomError(
            ErrorCodes.INVALID_PACKET,
            f"직렬화 에러: empty messageType {message_type}."
        )
    
    try:
        # message_type이 정수인 경우 처리
        if isinstance(message_type, int):
            message_type = _get_message_type_by_packet_type(message_type)
            
        # 더미 메시지 클래스를 사용하는 경우
        if hasattr(message_type, 'SerializeToString'):
            message = message_type(**data)
            return message.SerializeToString()
        else:
            # 기존 코드
            message_type.verify(data)
            created = message_type.create(data)
            return message_type.encode(created).finish()
    except Exception as msg:
        error_message = f"직렬화 검증 실패11: {msg}\r\nfailed data: {json.dumps(data, indent=2)}\r\n"
        raise CustomError(ErrorCodes['INVALID_PACKET'], error_message)

def serialize_ex(packet_type, payload_type, data):
    """
    패킷 타입과 페이로드 타입을 포함한 확장 직렬화 함수
    
    Args:
        packet_type: 패킷 타입 (PING, PONG, REQUEST, RESPONSE)
        payload_type: 페이로드 타입 (C_ENTER, S_ENTER, C_LOG, S_RESULT)
        data: 직렬화할 데이터
        
    Returns:
        bytes: 직렬화된 데이터
    """
    try:
        # payload 필드가 있는 경우에만 처리
        if 'payload' in data:
            data[payload_key_names[payload_type]] = data.pop('payload')
        
        return serialize(packet_type, data)
        
    except Exception as e:
        error_message = f"직렬화 검증 실패: {str(e)}\nfailed data: {json.dumps(data, indent=2, ensure_ascii=False)}"
        raise CustomError(ErrorCodes['INVALID_PACKET'], error_message)

def deserialize(message_type, data):
    """
    직렬화된 데이터를 역직렬화하는 함수
    
    Args:
        message_type: 프로토콜 버퍼 메시지 타입
        data: 역직렬화할 데이터
        
    Returns:
        dict: 역직렬화된 데이터
        
    Raises:
        CustomError: 역직렬화 과정에서 오류 발생 시
    """
    if not message_type:
        raise CustomError(
            ErrorCodes.INVALID_PACKET,
            f"역직렬화 에러: empty messageType ({message_type})"
        )
    # 더미 메시지 클래스를 사용하는 경우
    if hasattr(message_type, 'ParseFromString'):
        message = message_type()
        message.ParseFromString(bytes(data)) 
        return message
    else:
        # 기존 코드
        result = message_type.decode(data)
        print(f"decode 역직렬화 완료: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return result

def deserialize_by_packet_type(packet_type, data):
    """
    패킷 타입에 따른 역직렬화 함수
    
    Args:
        packet_type: 패킷 타입
        data: 역직렬화할 데이터
        
    Returns:
        protobuf.Message: 역직렬화된 메시지 객체 (dict 아님, 필요 시 MessageToDict로 변환)
    """
    # 패킷 타입 이름 찾기
    packet_type_name = None
    for name, value in packet_types.items():
        if value == packet_type:
            packet_type_name = name
            break
    
    print(f"패킷 타입 이름: {packet_type_name}")
    
    message_type = get_proto_messages()['packet'][packet_type_name]
    print(f"메시지 타입: {message_type.__name__ if hasattr(message_type, '__name__') else str(message_type)}")
    
    decoded = deserialize(message_type, data)
    
    return decoded 