from ..classes.models.user_class import User

# JS의 Map은 Python에서는 dict로 대체
user_session = {}
user_socket_session = {}

def add_user(socket, account_id):
    user = get_user_by_id(account_id)
    user = User(account_id, socket)
    user_session[account_id] = user
    user_socket_session[socket] = user
    return user

def get_user_by_id(account_id):
    return user_session.get(account_id)

def get_user_by_socket(socket):
    return user_socket_session.get(socket)
