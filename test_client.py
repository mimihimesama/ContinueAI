# test_client.py
import asyncio
import socket
import json
import uuid
import struct

async def test_connection():
    # 소켓 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setblocking(False)
    
    try:
        # 서버에 연결
        await asyncio.get_event_loop().sock_connect(client_socket, ('127.0.0.1', 3000))
        print("서버에 연결되었습니다.")
        
        # 간단한 메시지 전송 (PING 패킷)
        # 패킷 헤더: [총 길이(2바이트), 패킷 타입(1바이트)]
        # PING 패킷 타입은 1로 가정
        packet_type = 1  # PING 패킷 타입
        total_length = 3  # 헤더 길이 (2 + 1)
        
        # 패킷 헤더 생성
        header = struct.pack('>HB', total_length, packet_type)
        
        # 패킷 전송
        await asyncio.get_event_loop().sock_sendall(client_socket, header)
        
        # 응답 수신
        response = await asyncio.get_event_loop().sock_recv(client_socket, 1024)
        print(f"서버로부터 응답: {response}")
        
    except Exception as e:
        print(f"연결 오류: {e}")
    finally:
        # 소켓 닫기
        client_socket.close()

asyncio.run(test_connection())