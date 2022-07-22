from socket import *
from . import static
from .exception import LANException
from .transmit.transmit import Transmit
import time
import threading
import traceback
import json
import time
from .receiver.receiver import Receiver


class NatConnector(Transmit, Receiver):
    equipment_list = dict()  # ip + PROTOCOL_EXPIRE_TIME
    server_function = dict()
    use_function = dict()
    waiting_list = dict()
    exe_thread = dict()
    return_data = dict()
    exe_id = 1
    """
    equipment_list = {
        "ip":time,
        "192.168.1.3":"2021-4-1 10:10:10"
    }
    server_function = {
        "function_name" : callback
    }
    use_function = {
        "function_name" : {
            "ip": address
            "description" : description
        }
    }
    """

    def __init__(self, ip):
        try:
            s = socket(AF_INET, SOCK_DGRAM)
            s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
            s.bind(('0.0.0.0', static.PROTOCAL_PORT))
        except:
            raise LANException(LANException.PORT_BEING_USED)
        self.ip = ip
        self.open = True
        self.s = s

    def start(self):
        keep_alive = threading.Thread(target=self.__keep_alive)
        receive = threading.Thread(target=self.receive, args=(self.s, self.ip))
        keep_alive.start()
        receive.start()

    def register(self, name, callback):
        assert type(name) == str
        assert callable(callback)
        NatConnector.server_function[name] = callback
        self.broadcast_list_function_name(NatConnector.server_function.keys())
        pass

    def call(self, name, *args, **kwargs):
        exe_id = NatConnector.exe_id
        NatConnector.exe_id += 1
        if NatConnector.server_function.get(name):
            callfunc = threading.Thread(target=self.__do_local_call, args=(name, exe_id, args, kwargs))
            callfunc.start()
            NatConnector.exe_thread[str(exe_id)] = callfunc
        else:
            callfunc = threading.Thread(target=self.__do_call, args=(name, exe_id, args, kwargs))
            callfunc.start()
            NatConnector.exe_thread[str(exe_id)] = callfunc
        return exe_id

    def join(self, exe_id):
        callfunc = NatConnector.exe_thread.pop(str(exe_id))
        callfunc.join()
        pass

    def get_data(self, exe_id):
        if NatConnector.return_data.get(str(exe_id)):
            return NatConnector.return_data.pop(str(exe_id))
        return False

    def receive_hello(self, addr):
        """
        receive hello method, search for equipment list, if the equipment is already in use
        and do not expire, then do nothing. else the equipment list will be refresh and send
        hello to the new equipment and new function list
        :param addr:
        :return:
        """
        last_time = NatConnector.equipment_list.get(addr)
        if (not last_time) or (time.time()-last_time > static.Connect.EXCEED_TIME_LIMIT):
            self.send_hello(addr)
            self.send_list_function_name(addr, NatConnector.server_function.keys())
        NatConnector.equipment_list[addr] = time.time()
        pass

    def receive_func(self, data, addr):
        """
        receive a function name list, delete all the function with the
            same ip address, add function to the function list
        use a dict to record newest arrive receive time, save the same time in each function name
        when call a function, compare the time record in newest arrive receive time and the time
        in function execute. if it is not the same, then the function is expire
        :param data:
        :param addr:
        :return:
        """
        for func in data:
            func_name = func.get("name")
            NatConnector.use_function[func_name] = dict(ip=addr, description="")

    def receive_call(self, addr, name, exe_id, args, kwargs):
        args_list = []
        if args:
            for key in args.keys():
                args_list.append(args[key])
        func = NatConnector.server_function.get(name)
        if args and kwargs:
            back = func(*args_list, **kwargs)
        elif args and (not kwargs):
            back = func(*args_list)
        elif (not args) and kwargs:
            back = func(*kwargs)
        else:
            back = func()
        self.send_callback(addr, back, exe_id)

    def receive_callback(self, data, exe_id):
        sem = NatConnector.waiting_list.pop(str(exe_id))
        sem.release()
        NatConnector.return_data[str(exe_id)] = data

    def __do_local_call(self, name, exe_id, args, kwargs):
        func = NatConnector.server_function.get(name)
        if args and kwargs:
            back = func(*args, **kwargs)
        elif args and (not kwargs):
            back = func(*args)
        elif (not args) and kwargs:
            back = func(*kwargs)
        else:
            back = func()
        NatConnector.return_data[str(exe_id)] = back
        pass

    def __do_call(self, name, exe_id, args, kwargs):
        if not NatConnector.use_function.get(name):
            raise LANException(LANException.FUNC_NOT_FOUND)
        ip = NatConnector.use_function.get(name).get("ip")
        self.send_call(ip, name, exe_id, args, kwargs)
        sem = threading.Semaphore(0)
        NatConnector.waiting_list[str(exe_id)] = sem
        sem.acquire(blocking=True)

    def __keep_alive(self):
        while self.open:
            self.broadcast_hello()
            time.sleep(static.Connect.SEND_HELLO_TIME)

    def close(self):
        self.open = False
        self.s.close()

    def __delete__(self, instance):
        self.close()
