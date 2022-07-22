def get_host_ip():
    """
    this function used to get host ip, only can be used in windows OS or Linux OS
    return a tuple, eg: ("192.168.1.1", "255.255.255.0")
    :return host ip, subnet_mask
    """
    pass


from .core.common.mapping import global_mapping

global_mapping(globals(), "net_tools")
del global_mapping
