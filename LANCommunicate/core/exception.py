class LANException(Exception):
    PROTOCOL_NOT_COMPLETE = "PROTOCOL is not complete"
    PORT_BEING_USED = "Nat protocol port has already being used"
    FUNC_NOT_FOUND = "the function you call is not found"

    def __init__(self, error_message):
        assert type(error_message) == str
        self.error_message = error_message

    def __str__(self):
        return self.error_message

class LANToolException(Exception):
    def __init__(self, error_message):
        assert type(error_message) == str
        self.error_message = error_message

    def __str__(self):
        return self.error_message