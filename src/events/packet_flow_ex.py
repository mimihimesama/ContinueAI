# 패킷 수신 및 버퍼에 추가
client.buffer.extend(data)

# 패킷 헤더 읽기
header_info = read_header(client.buffer)
total_length = header_info['totalLength']
packet_type = header_info['packetType']

# 패킷 데이터 추출
packet_data = client.buffer[:total_length]
client.buffer = client.buffer[total_length:]

# 패킷 타입에 따른 처리
if packet_type == packet_types['PING']:
    # PING 패킷 처리
    await send_ping(client.socket)
else:
    # REQUEST 패킷 처리
    deserialized_data = deserialize_by_packet_type(packet_type, packet_data)
    payload_type = deserialized_data.get('payloadType')
    
    # 핸들러 실행
    handler = get_handler_by_payload_type(payload_type)
    await handler(client, deserialized_data)  # 응답 생성 및 전송 