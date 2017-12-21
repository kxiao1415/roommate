from pyws.data.user_data import UserData

_user_data = UserData()


def get_user_by_user_id(user_id):
    user = _user_data.get(user_id)
    if user is None or user.deleted:
        return None
    return user

def create_user(user_info):
    return _user_data.create(user_info)

def update_user(user, user_info):
    return _user_data.update(user, user_info)

def delete_user(user):
    return _user_data.delete(user)
