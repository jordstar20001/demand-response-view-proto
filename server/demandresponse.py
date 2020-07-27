import json

class User():
    username = ""
    password = ""
    acc_type = ""
    permissions = []
    def __init__(self, _username, _password, _acc_type, _permissions):
        self.username = _username
        self.password = _password
        self.acc_type = _acc_type
        self.permissions = _permissions


class PermissionManager():
    auth_perms = {}
    def __init__(self, auth_fn):
        with open(auth_fn, "r") as f:
            self.auth_perms = json.loads(f.read())
    
    def user_permitted(self, user, auth_str):
        if self.is_anonymous_action(auth_str) or "all" in user["permissions"]: return True
        perms = self.auth_perms[auth_str]
        for perm in perms:
            if perm in user.permissions: return True
        return False
    
    def is_anonymous_action(self, auth_str):
        if auth_str not in self.auth_perms: return True
        return False




class UserManager():
    users = []
    filename = ""
    def __init__(self, fn):
        self.filename = fn
        self.get_users()

    def get_users(self):
        with open(self.filename, "r") as f:
            self.users = json.loads(f.read())
        
    def add_user(self, user):
        self.users.append(user)
        self.__update__()

    def remove_user(self, username):
        i = 0
        try:
            i = self.users.index(self.get_user_by_username(username))
        except:
            raise ValueError(f"No user found with username: {username}")

        self.users.pop(i)
        self.__update__()

    def edit_user(self, username, new_user_details):
        i = 0
        try:
            i = self.users.index(self.get_user_by_username(username))
        except:
            raise ValueError(f"No user found with username: {username}")

        self.users[i] = new_user_details
        self.__update__()


    def get_user_by_username(self, username):
        for u in self.users:
            if u["username"] == username:
                return u
        return None
        
    def valid_user(self, username, password):
        for u in self.users:
            if u["username"] == username and u["password"] == password:
                return True
        return False

    def __update__(self):
        users_str = json.dumps(users, indent=4)
        with open(filename, "w") as f:
            f.write(users_str)

