__all__ = [
    "NatConnector"
]


class NatConnector:

    def __init__(self, ip):
        """
        create a NatConnector object, used to execute function in other equipment that in the same LAN.

        A device can register a function named "add". Then under the same WiFi range,
        device B can use call function, input name "add" and the necessary parameter, this
        NatConnector can help you auto locate device A and execute "add" function in A.
        return the result after a while.

        all of the device under this protocol is in peer status, all of the device can donate it
        function or use the function in other device.

        for example:
        in device A:
        def add(a, b, c):
            return a + b + c
        A = NatConnector(ip = "192.168.1.31") # A's ip address
        A.start()
        A.register("add", add)
        A.loop_forever()

        in device B:
        B = NatConnector(ip = "192.168.1.28") # B's ip address
        B.start()
        exe_id = B.call("add", 10, 20, c=30)
        B.join(exe_id)  # block the thread until get data
        result = B.get_result(exe_id)

        :param ip: ip address of this device
        """
        pass

    def start(self):
        """
        start nat_connector, inform other device that you are on line,
        you must start before do other operate,
        :return: none
        """
        pass

    def close(self):
        """
        close nat_connector
        :return: none
        """
        pass

    def register(self, name, callback):
        """
        register a function, all of the device can use this function in your device.
        multiple register the same name function in different device can cause overwrite. your device
        can only save the last register information.
        :param name: the function name you want to register
        :param callback: a function that is callable
        :return: none
        """
        pass

    def call(self, name, *args, **kwargs):
        """
        use the function that already been registered under the same LAN..
        this function is non-blocking type, therefore a execute id is needed to identified this process

        when searching device that can execute this function,
        :param name: the function name that you want to call
        :param args: parameter in that function
        :param kwargs: parameter in that function
        :return: an execute id that unique identified this call
        """
        pass

    def join(self, exe_id):
        """
        wait until this function call finished
        :param exe_id: the exe_id of this function call
        :return: none
        """
        pass

    def get_data(self, exe_id):
        """
        get the data. the data can only get one time. If the data is not return then the return
        message will be none.
        :param exe_id: the exe_id of this function call
        :return: data
        """
        pass


from .core.common.mapping import global_mapping
global_mapping(globals(), "nat_connector")
del global_mapping
