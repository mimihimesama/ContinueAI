from ..constants.packet_constants import header_constants

def read_header(packet, is_reverse=False):
    """
    패킷 헤더를 읽는 함수
    
    Args:
        packet (bytes): 패킷 데이터
        is_reverse (bool): 바이트 순서를 역순으로 읽을지 여부
        
    Returns:
        dict: totalLength와 packetType을 포함하는 딕셔너리
    """
    print(f"패킷 헤더 읽기 시작: 패킷 길이={len(packet)}바이트, 역순={is_reverse}")
    
    # totalLength 읽기 (4바이트)
    if is_reverse:
        total_length = int.from_bytes(packet[:header_constants['TOTAL_LENGTH']], byteorder='big')
    else:
        total_length = int.from_bytes(packet[:header_constants['TOTAL_LENGTH']], byteorder='little')
    
    # packetType 읽기 (1바이트)
    packet_type = packet[header_constants['TOTAL_LENGTH']]
    
    print(f"패킷 헤더 읽기 완료: 총 길이={total_length}바이트, 패킷 타입={packet_type}")
    
    return {
        'totalLength': total_length,
        'packetType': packet_type
    }

def write_header(data_length, packet_type):
    """
    패킷 헤더를 작성하는 함수
    
    Args:
        data_length (int): 데이터 길이
        packet_type (int): 패킷 타입
        
    Returns:
        bytes: 작성된 헤더
    """
    print(f"패킷 헤더 작성 시작: 데이터 길이={data_length}바이트, 패킷 타입={packet_type}")
    
    header_size = header_constants['TOTAL_LENGTH'] + header_constants['PACKET_TYPE_LENGTH']
    header = bytearray(header_size)
    
    # totalLength 작성 (4바이트)
    total_length_bytes = (header_size + data_length).to_bytes(
        header_constants['TOTAL_LENGTH'],
        byteorder='big'
    )
    header[:header_constants['TOTAL_LENGTH']] = total_length_bytes
    
    # packetType 작성 (1바이트)
    header[header_constants['TOTAL_LENGTH']] = packet_type
    
    print(f"패킷 헤더 작성 완료: 총 길이={header_size + data_length}바이트")
    
    return header 