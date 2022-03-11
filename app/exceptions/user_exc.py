class TypeFieldError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
     


class EmailAlreadyExist(Exception):
    def __init__(self, status_code=409):
        self.message = "User already exists."
        self.status_code = status_code
           