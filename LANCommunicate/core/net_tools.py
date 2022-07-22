import os
from .exception import LANToolException
import warnings
import sys


def get_host_ip():
    """
    this function used to get host ip, only can be used in windows OS or Linux OS
    return a tuple, eg: ("192.168.1.1", "255.255.255.0")
    :return host ip, subnet_mask
    """
    system = sys.platform
    if system == "win32":
        return _get_host_ip_windows()
    elif system == "linux":
        return _get_host_ip_linux()
    else:
        LANToolException("your OS system is not support ip finding")


def _get_host_ip_linux():
    """
    get linux OS ip
    :return: ip
    """
    warnings.warn("_get_host_ip_linux function is not accuracy")
    for line in os.popen('/sbin/route').readlines():
        if "192.168" in line:
            net = line.split()[0]
            if len(net.split(".")) == 4:
                return net, "255,255,255,0"
    raise LANToolException("get linux LAN host ip failed")


def _get_host_ip_windows():
    """
    get windows OS ip
    :return: ip
    """
    for line in os.popen("route print"):
        line = line.strip()
        if line.startswith("0.0.0.0"):
            ip = line.split()[3]
            mask = line.split()[1]
            return ip, mask
    else:
        raise LANToolException("get windows LAN host ip failed")
