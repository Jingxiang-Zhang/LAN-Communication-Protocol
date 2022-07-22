from .core import static
from . import net_tools
from . import nat_connector
# from .core import net_tools as core_net_tools
# from .core import nat_connector as core_nat_connector

__all__ = [
    "net_tools",
    "nat_connector"
]


# globals()["net_tools"] = core_net_tools
# globals()["nat_connector"] = core_nat_connector
