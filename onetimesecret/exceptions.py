class PreventModelUpdateException(Exception):
    def __init__(self, message=None):

        if not message:
            message = "Updating the instance is not allowed"

        super().__init__(message)
