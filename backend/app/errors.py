from fastapi import status

class ApiBotException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

def handle_error(exc):
    if exc.code is None:
        raise ApiBotException(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Internal server error")
    else:
        raise ApiBotException(code=exc.code, message=exc.message)

def raise_not_found_error():
    raise ApiBotException(code=status.HTTP_404_NOT_FOUND, message="Specified resource(s) was not found")