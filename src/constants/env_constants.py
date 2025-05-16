import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 서버 설정
PORT = int(os.getenv('PORT', 3000))
HOST = os.getenv('HOST', '127.0.0.1')
CLIENT_VERSION = os.getenv('CLIENT_VERSION', '1.0.0')

# 게임 캐릭터 데이터베이스 설정
DB1_NAME = os.getenv('DB1_NAME', 'GAME_CHAR_DB')
DB1_USER = os.getenv('DB1_USER', 'user1')
DB1_PASSWORD = os.getenv('DB1_PASSWORD', 'password1')
DB1_HOST = os.getenv('DB1_HOST', 'localhost')
DB1_PORT = int(os.getenv('DB1_PORT', 3306))

# 사용자 데이터베이스 설정
DB2_NAME = os.getenv('DB2_NAME', 'USER_DB')
DB2_USER = os.getenv('DB2_USER', 'user2')
DB2_PASSWORD = os.getenv('DB2_PASSWORD', 'password2')
DB2_HOST = os.getenv('DB2_HOST', 'localhost')
DB2_PORT = int(os.getenv('DB2_PORT', 3306))

# Redis 설정
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6380))
REDIS_USERNAME = os.getenv('REDIS_USERNAME', '')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '') 