class Session:
    def __init__(self):
        self.current_user = None
        self.user_key = None

    def login(self, user, user_key):
        self.current_user = user
        self.user_key = user_key

    def logout(self):
        self.current_user = None
        self.user_key = None

    def is_logged_in(self):
        return self.current_user is not None

    def get_current_user(self):
        return self.current_user

    def get_user_key(self):
        return self.user_key