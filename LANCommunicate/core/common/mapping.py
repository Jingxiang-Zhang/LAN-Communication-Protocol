from LANCommunicate.core.nat_connector import NatConnector
from LANCommunicate.core.net_tools import get_host_ip


def global_mapping(globals_list, name):
    assert type(name) == str
    assert type(globals_list) == dict
    if name == "nat_connector":
        globals_list["NatConnector"] = NatConnector
    elif name == "net_tools":
        globals_list["get_host_ip"] = get_host_ip
