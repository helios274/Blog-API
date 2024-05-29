from rest_framework.response import Response
from rest_framework import status


class CustomResponse(Response):
    def __init__(self, success: bool, message: str = "", error_type: str = "", error_message: str = "", status_code=None, data=None):
        response_data = {}
        response_data["success"] = success
        if success:
            response_data["message"] = message
            if data is not None:
                response_data["data"] = data
        else:
            response_data["error"] = {}
            response_data["error"]["type"] = error_type
            response_data["error"]["message"] = error_message

        super().__init__(response_data, status=status_code)


class SuccessResponse(Response):
    def __init__(self, message: str = "", data: any = None, data_name: str = "data", status_code=status.HTTP_200_OK):
        success_res = {
            "success": True,
            "message": message,
        }
        if data:
            success_res[data_name] = data

        super().__init__(success_res, status=status_code)


class ValidationErrorResponse(Response):
    def __init__(self, error_message: str):
        error_res = {
            "success": False,
            "error": {
                "type": "Validation Error",
                "message": error_message
            }
        }
        super().__init__(error_res, status=status.HTTP_400_BAD_REQUEST)
