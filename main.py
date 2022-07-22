"""
this is a demo
"""

import time
import LANCommunicate
def addfunc(tc, td, a, b):
    print("a", tc, td, a, b)
    time.sleep(1)
    return tc + td + a + b


ip = LANCommunicate.net_tools.get_host_ip()
a = LANCommunicate.nat_connector.NatConnector(ip[0])
a.start()
a.register("addfunc", addfunc)

time.sleep(2)
id = a.call("addfunc", 10, 20, a=10, b=30)
print(a.get_data(id))
a.join(id)
print(a.get_data(id))
time.sleep(2)
a.close()


