class ResponseInfo(object):
    def __init__(self, status=True, status_code=200, message='', data={}, errors={}):
        self.response = {
            "success": status,
            "status_code": status_code,
            "message": message,
            "data": data,
            "error": errors,
        }

class ResponseHandler:
    def response_info(self, status=True, status_code=200, message='', data={}, errors={}):
        return ResponseInfo(status=status, status_code=status_code, message=message, data=data, errors=errors).response
