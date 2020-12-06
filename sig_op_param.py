from config import *
from getConstant.getConstants import *

straight_types = ['NS', 'SN', 'EW', 'WE']
left_types = ['SW', 'WN', 'NE', 'ES']

op_index = {}
t_ips = {}
deltas = {}

for v in straight_types:
    op_index[v] = [int(_) for _ in findMachineStraight_WE(mac_array, mode=v)[0][0][0] if _]

for v in left_types:
    op_index[v] = [int(_) for _ in findMachineLeft_NE(mac_array, mode=v)[0][0][0] if _]

print(op_index)

machine_str = findMachineStraight(mac_array)
machine_left = findMachineLeft( mac_array )

t_ips['straight'] = get_t_ip(machine_str)
t_ips['left'] = get_t_ip(machine_left)

deltas['straight'] = [_ for _ in machine_str[0][0][3] if _]
deltas['left'] = [_ for _ in machine_left[0][0][3] if _]



print(t_ips)
print(deltas)
