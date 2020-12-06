import numpy as np
from gurobipy import *
import matplotlib.pyplot as plt
# from matplotlib import animation
import matplotlib.patches as patches
import matplotlib
pi = 3.142
big_num = 10e5

loc_list = ['N', 'E', 'S', 'W']
end_sec = 60 * 15
# end_sec = 10
eps = 0.1
dt = 0.1
t = np.arange(0, end_sec, dt)
size = 100
ins_size = 6
ins_type = [1,1]
car_size = [2,5]
min_dist_bt_cars = 2

aew = (np.minimum(np.sin(t), np.zeros(len(t))), np.zeros(len(t)))
awe = (np.maximum(np.sin(t), np.zeros(len(t))), np.zeros(len(t)))
ans = (np.zeros(len(t)), np.minimum(np.sin(t), np.zeros((len(t)))))
asn = (np.zeros(len(t)), np.maximum(np.sin(t), np.zeros((len(t)))))

max_a = 3
v_intersection = 50 * 1000 / 3600 #16.6667 # 60km/h 14
exit_speed = v_intersection
print(v_intersection)
v_inter_right = 8.33333 # 30km/h
v_inter_left = 8.33333

matching_dist = 0.6 * v_intersection * v_intersection / max_a + ins_type[0]*ins_size
assign_dist = matching_dist
stop_line = matching_dist + assign_dist


traffic_consts = [0.75, 0.5, 0.25, 0.1] #(0~2) # 0.1, 0.25, 0.5, 0.75
pattern_nums = [13]

visualize = True

usual = False

# print(matching_dist)