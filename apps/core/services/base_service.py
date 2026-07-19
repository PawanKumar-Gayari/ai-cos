class BaseService:

    def success_response(self, data=None, message="success"):
        return {
            "success": True,
            "message": message,
            "data": data,
        }

    def error_response(self, message="error"):
        return {
            "success": False,
            "message": message,
        }