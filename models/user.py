class User:
    """Domain Model representing an application User."""
    def __init__(self, user_id, username, password_hash, salt, created_at=None):
        self.__id = user_id
        self.__username = username
        self.__password_hash = password_hash
        self.__salt = salt
        self.__created_at = created_at

    # Getters (Encapsulation Demonstration)
    @property
    def id(self): return self.__id
    @property
    def username(self): return self.__username
    @property
    def password_hash(self): return self.__password_hash
    @property
    def salt(self): return self.__salt