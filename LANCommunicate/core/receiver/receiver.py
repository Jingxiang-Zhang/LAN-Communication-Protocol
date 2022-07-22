import json
import LANCommunicate.core.static as static

class Receiver:
    def receive(self, s, ip):
        """
        listen port with udp protocol, distribute receive data
        :param s: socket
        :param ip: localhost ip
        :return:
        """
        assert type(ip) == str
        while True:
            try:
                msg, addr = s.recvfrom(1024)
                addr = addr[0]
                if addr == ip:
                    continue
                msg = msg.decode('utf-8').replace("\'", "\"")
                msg = json.loads(msg)
                if msg["method"] == static.PROTOCOL_METHOD.PROTOCOL_METHOD_HELLO:
                    self.receive_hello(addr)
                elif msg["method"] == static.PROTOCOL_METHOD.PROTOCOL_METHOD_FUNC:
                    self.receive_func(msg["data"], addr)
                elif msg["method"] == static.PROTOCOL_METHOD.PROTOCOL_METHOD_CALL:
                    self.receive_call(addr, msg["data"],
                                        msg["exe_id"], msg.get("args"), msg.get("kwargs"))
                elif msg["method"] == static.PROTOCOL_METHOD.PROTOCOL_METHOD_CALLBACK:
                    self.receive_callback(msg["data"], msg["exe_id"])
            except OSError as e:
                if str(e) == "[WinError 10038] 在一个非套接字上尝试了一个操作。":
                    break
                else:
                    raise e

    def receive_hello(self, addr):
        """
        receive hello method
        :param addr: ip address of the sender
        :return: none
        """
        pass

    def receive_func(self, data, addr):
        """
        receive a function name list
        :param data: function name list
        :param addr: ip address of the sender
        :return: none
        """
        pass

    def receive_call(self, addr, name, exe_id, args, kwargs):
        """
        receive a function call from other host, execute the function, and send back the result
        :param addr: ip address of the sender
        :param name: function name
        :param exe_id: function execute id in the sender side
        :param args: function parameter args
        :param kwargs: function parameter kwargs
        :return: none
        """
        pass

    def receive_callback(self, data, exe_id):
        """
        receive the function result, save the result in the result list,
        then unblock the execute thread
        :param data: function result
        :param exe_id: execute id of this call
        :return: none
        """
        pass