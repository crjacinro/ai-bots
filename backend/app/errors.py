class ApiBotException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

def handle_error(exc):
    if exc.code is None:
        raise ApiBotException(code=500, message="Internal server error")
    else:
        raise ApiBotException(code=exc.code, message=exc.message)