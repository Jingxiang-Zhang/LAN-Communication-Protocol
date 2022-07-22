import LANCommunicate.core.static as static
import socket
from LANCommunicate.core.exception import LANException


class TransmitBase:

    def broadcast(self, method, data, exe_id=None, args=None, kwargs=None,
                  encrypted=static.PROTOCOL_ENCRYPTED_NONE,
                  compress=static.PROTOCOL_COMPRESS_NONE):

        ip = "255.255.255.255"
        protocol = self.__encapsulate(method, data, exe_id, args, kwargs, encrypted, compress)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            destination = (ip, static.PROTOCAL_PORT)
            # 加入到发送队列
            s.sendto(protocol, destination)

    def udp_send(self, ip, method, data, exe_id=None, args=None, kwargs=None,
                 encrypted=static.PROTOCOL_ENCRYPTED_NONE,
                 compress=static.PROTOCOL_COMPRESS_NONE):

        assert type(ip) == str
        protocol = self.__encapsulate(method, data, exe_id, args, kwargs, encrypted, compress)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            destination = (ip, static.PROTOCAL_PORT)
            # 加入到发送队列
            s.sendto(protocol, destination)

    def __encapsulate(self, method, data,
                      exe_id=None,
                      args=None,
                      kwargs=None,
                      encrypted=static.PROTOCOL_ENCRYPTED_NONE,
                      compress=static.PROTOCOL_COMPRESS_NONE):
        """
        encapsulate a protocol to a bit stream type
        :param method: protocol method type
        :param data: protocol body
        :param exe_id:
        :param args:
        :param kwargs:
        :param encrypted:
        :param compress:
        :return: bit stream of a protocol
        """
        try:
            protocol = dict()
            protocol["type"] = static.PROTOCOL_TYPE
            protocol["method"] = method
            protocol["version"] = static.PROTOCOL_VERSION
            protocol["data"] = data
            protocol["encrypted"] = encrypted
            protocol["compress"] = compress
            if exe_id:
                protocol["exe_id"] = exe_id
            if args:
                protocol["args"] = args
            if kwargs:
                protocol["kwargs"] = kwargs
            protocol = str(protocol).encode('utf-8')

        except Exception as e:
            raise LANException("error happened in encapsulate protocol: " + str(e))
        return protocol
