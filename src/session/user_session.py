from ..classes.models.user_class import User

# JS의 Map은 Python에서는 dict로 대체
user_session = {}
user_socket_session = {}

def add_user(socket, account_id):
    user = get_user_by_id(account_id)
    user = User(account_id, socket)
    user_session[account_id] = user
    # 소켓 객체의 ID를 키로 사용
    user_socket_session[id(socket)] = user
    return user

def get_user_by_id(account_id):
    return user_session.get(account_id)

def get_user_by_socket(socket):
    # 소켓 객체의 ID로 사용자 조회
    return user_socket_session.get(id(socket))
