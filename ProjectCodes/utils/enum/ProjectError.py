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
    
class ValidateError(Enum):
    LEAST_EIGHT_CHATACTER = "Password must be least 8 character."
    MUST_CONTAIN_NUMBER = "Password must contain at least one number."
    MUST_CONTAIN_LOWERCASE = "Password must contain at least one lowercase letter."
    MUST_CONTAIN_UPPERCASE = "Password must contain at least one uppercase letter."
    MUST_CONTAIN_SPECIAL_CHAR = "Password must contain at least one special character."
    EMPTY_FIELD = "There is not can be empty field."
   