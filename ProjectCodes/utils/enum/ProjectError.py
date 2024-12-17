from enum import Enum

class DatabaseError(Enum):
    CONNECTION_FAILED = "Connection Failed."
    USER_ALREADY_EXISTS = "User Already Exists."
    USER_NOT_FOUND = "User not Found."
    INCORRECT_PASSWORD = "Incorrect Password"
    INSERT_FAILED = "There is an error in registered failed."
    QUERY_FAILED = "Query Failed."
    UNKNOWN_ERROR = "Unknown Error."

    def __str__(self):
        return self.value