PROTOCOL = dict.fromkeys([
    "type",
    "method",
    "version",
    "data",
    "exe_id",
    "args",
    "kwargs",
    "encrypted",
    "compress"
])
PROTOCOL_TYPE = "LANC"
PROTOCOL_VERSION = 0.01


class PROTOCOL_METHOD:
    PROTOCOL_METHOD_HELLO = 1  # hello method used to inform other node
    PROTOCOL_METHOD_FUNC = 2  # func method inform other node the function name that can be execute
    PROTOCOL_METHOD_CALL = 3  # function call method
    PROTOCOL_METHOD_CALLBACK = 4  # function call return result


class TRANSMIT:
    WAIT_UNTIL_SEND = 1  # wait for this time to see if there are any change in send function list


class Connect:
    SEND_HELLO_TIME = 5
    EXCEED_TIME_LIMIT = 30


PROTOCOL_FUCNTION = dict.fromkeys([
    "name",
    "description"
])

PROTOCOL_ENCRYPTED_NONE = 0

PROTOCOL_COMPRESS_NONE = 0

PROTOCAL_PORT = 5127
