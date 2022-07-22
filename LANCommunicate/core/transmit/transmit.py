from LANCommunicate.core.transmit.transmit_base import TransmitBase
import LANCommunicate.core.static as static
import threading
import time


class Transmit(TransmitBase):

    def send_hello(self, ip):
        """
        protocol type "hello", send hello message to the new network node that just online
        :param ip: new network node
        :return: none
        """
        self.udp_send(ip=ip, method=static.PROTOCOL_METHOD.PROTOCOL_METHOD_HELLO, data="hello")
        pass

    def broadcast_hello(self):
        """
        broadcast hello message to all of the network node to keep alive
        :return: none
        """
        self.broadcast(method=static.PROTOCOL_METHOD.PROTOCOL_METHOD_HELLO, data="hello")
        pass

    def send_list_function_name(self, ip, function_name_list):
        """
        send function name list to a appointed ip address, used when a device on line, inform
        it the function that can be execute in the device
        :param ip:
        :param function_name_list: the function name list that can execute in your device
        :return: none
        """
        func_list = list()
        for name in function_name_list:
            func_list.append(dict(name=name))
        Transmit.function_set.clear()
        self.udp_send(ip=ip, method=static.PROTOCOL_METHOD.PROTOCOL_METHOD_FUNC,
                      data=func_list)
        pass

    function_set = set()

    def broadcast_list_function_name(self, function_name_list):
        """
        broad cast a single function name of this device, happened when the function name list changed
        :param function_name_list:
        :return: none
        """
        notify = threading.Thread(target=self.__broadcast_list_function, args=(function_name_list,))
        notify.start()
        pass

    def __broadcast_list_function(self, function_name_list):
        """
        sleep for some time and do a check, if there is no change this will send broadcast
        :param function_name_list:
        :return:
        """
        Transmit.function_set.clear()
        for name in function_name_list:
            Transmit.function_set.add(name)
        current_set = Transmit.function_set.copy()
        # judge if change
        time.sleep(static.TRANSMIT.WAIT_UNTIL_SEND)
        if current_set == Transmit.function_set:
            self.__do_broadcast_single_function()
        pass

    def __do_broadcast_single_function(self):
        func_list = list()
        for name in Transmit.function_set:
            func_list.append(dict(name=name))
        Transmit.function_set.clear()
        self.broadcast(method=static.PROTOCOL_METHOD.PROTOCOL_METHOD_FUNC, data=func_list)
        pass

    def send_call(self, ip, function_name, exe_id, args, kwargs):
        """
        send a function call protocol to a appointed device to execute
        :param ip: the device ip that can execute the function
        :param function_name:
        :param exe_id: a exe_id to identify this function call
        :param args: parameter in the function
        :param kwargs: parameter in the function
        :return: none
        """
        args_dict = dict()
        for number, arg in enumerate(args):
            args_dict["p" + str(number)] = arg
        self.udp_send(ip=ip, exe_id=exe_id, method=static.PROTOCOL_METHOD.PROTOCOL_METHOD_CALL,
                      data=function_name, args=args_dict, kwargs=kwargs)
        pass

    def send_callback(self, ip, data, exe_id):
        """
        when finish function call, send the function result to the device that call this function
        :param ip:
        :param data: function data
        :param exe_id:
        :return: none
        """
        self.udp_send(ip=ip, exe_id=exe_id, method=static.PROTOCOL_METHOD.PROTOCOL_METHOD_CALLBACK,
                      data=data)
        pass
