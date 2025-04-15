from ..constants.packet_constants import header_constants
from ..constants.env_constants import (
    PORT, HOST, CLIENT_VERSION,
    DB1_NAME, DB1_USER, DB1_PASSWORD, DB1_HOST, DB1_PORT,
    DB2_NAME, DB2_USER, DB2_PASSWORD, DB2_HOST, DB2_PORT,
    REDIS_HOST, REDIS_PORT, REDIS_USERNAME, REDIS_PASSWORD
)

# 설정값 로드
config = {
    'server': {
        'port': PORT,
        'host': HOST,
    },
    'client': {
        'version': CLIENT_VERSION,
    },
    'packet': {
        'totalLength': header_constants['TOTAL_LENGTH'],
        'typeLength': header_constants['PACKET_TYPE_LENGTH'],
    },
    'databases': {
        'GAME_CHAR_DB': {
            'name': DB1_NAME,
            'user': DB1_USER,
            'password': DB1_PASSWORD,
            'host': DB1_HOST,
            'port': DB1_PORT,
        },
        'USER_DB': {
            'name': DB2_NAME,
            'user': DB2_USER,
            'password': DB2_PASSWORD,
            'host': DB2_HOST,
            'port': DB2_PORT,
        },
    },
    'redis': {
        'redisHost': REDIS_HOST,
        'redisPort': REDIS_PORT,
        'redisUsername': REDIS_USERNAME,
        'redisPassword': REDIS_PASSWORD,
    },
} 