class AIcosException(Exception):

    default_message = "Application Error"

    def __init__(self, message=None):
        self.message = message or self.default_message
        super().__init__(self.message)