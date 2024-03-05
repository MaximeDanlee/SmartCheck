class Response:
    def __init__(self, success=False, message="", data=None, test_name=""):
        if data is None:
            data = {}
        self.success = success
        self.message = message
        self.data = data
        self.test_name = test_name

    def __str__(self):
        return f"Success: {self.success}, Message: {self.message}, Data: {self.data}"

    def set_success(self, success):
        self.success = success

    def set_message(self, message):
        self.message = message

    def set_data(self, data):
        self.data = data

    def set_test_name(self, test_name):
        self.test_name = test_name

    def to_json(self):
        return {
            "test_name": self.test_name,
            "success": self.success,
            "message": self.message,
            "data": self.data
        }
