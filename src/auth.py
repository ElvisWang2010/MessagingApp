from database import find_user


def authenticate(username, password):

    username = username.strip()

    if not username or not password:
        return False

    user = find_user(username)

    if user is None:
        return False

    return user["password"] == password