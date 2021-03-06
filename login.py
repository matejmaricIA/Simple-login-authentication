import sys
import getpass
import hashlib
from usermgmt import load_json, check_duplicate, passwd, update_json, MIN_LEN
import base64

def change_password(username):
    new_password = getpass.getpass('New password: ')
    repeat_new_password = getpass.getpass('Repeat new password: ')

    if new_password != repeat_new_password:
        print('Password change failed. Password mismatch.')
        return 2
    elif len(new_password) < MIN_LEN:
        print('Password change failed. Password too short.')
        return 2

    passwd(username, new_password)
    data = load_json()
    data[username][2] = 0
    user = {username : data[username]}
    update_json(user)
    return 1


def login(username, password):
    if not check_duplicate(username):
        return 0
    data = load_json()

    real_hashed_key = base64.b64decode(data[username][1])
    salt = base64.b64decode(data[username][0])
    new_hashed = hashlib.scrypt(password.encode(), salt = salt, n = 2**14,r = 8, p = 1)

    if real_hashed_key != new_hashed:
        return 0

    if data[username][2] == 1:
        return change_password(username)

    return 1

def main():
    username = sys.argv[1]
    password = input()
    log = login(username, password)
    while not log:
        print('Username or password incorrect.')
        password = getpass.getpass('Password: ')
        log = login(username, password)
    if log != 2:
        print('Login succesful.')


if __name__ == '__main__':
    main()


