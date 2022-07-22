class LANException(Exception):
    LAN_IP_NOT_FIND = "get linux LAN host ip failed"
    LAN_IP_FINDING_OS_NOT_SUPPORT = "your OS system is not support ip finding"
    PROTOCOL_NOT_COMPLETE = "PROTOCOL is not complete"

    def __init__(self, error_message):
        assert type(error_message) == str
        self.error_message = error_message

    def __str__(self):
        return self.error_message
