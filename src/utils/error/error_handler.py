import traceback
from .error_codes import ErrorCodes

async def handle_error(socket, error):
    try:
        if hasattr(error, 'code'):
            response_code = error.code
            message = error.message
            err = (
                f"{type(error).__name__}\r\n"
                f"Code: {error.code}\r\n"
                f"Message: {error.message}\r\n"
                f"{traceback.format_exc()}"
            )
        else:
            response_code = ErrorCodes['SOCKET_ERROR']
            message = str(error)
            err = (
                f"{type(error).__name__}\r\n"
                f"Message: {str(error)}\r\n"
                f"{traceback.format_exc()}"
            )
        print(err)

    except Exception as err:
        print('Error in errorHandler:', err)
