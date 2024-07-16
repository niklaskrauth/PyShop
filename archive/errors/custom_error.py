class CustomError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        self.classname = self.__class__.__name__
        super().__init__(message)

    def __str__(self):
        return f"{self.classname}({self.status_code}): {self.message}"
