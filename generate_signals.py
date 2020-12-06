from intersection import signal
from config import *
import copy
import gurobi

def generate_usual_signals(type=None, interval=28, pause=2):
    signals = []
    repeat_num = int((end_sec)/(4*(interval+pause))) + 1
    print(end_sec, 4 * (interval+pause), repeat_num)
    t_step_str = (min_dist_bt_cars / v_intersection)
    t_max_str = int(interval / t_step_str)
    if ins_type[0] == 1:
        for i in range(repeat_num):
            for t in range(t_max_str):
                print(t*t_step_str)
                print(4 * (interval+pause) * i + t * t_step_str, (interval+pause) * (4*i+1) + t * t_step_str, (interval+pause) * (4*i+2) + t * t_step_str, (interval+pause) * (4*i+3) +t * t_step_str)
                signals.append(signal(len(signals)+1, 'SN', (interval+pause) * 4 * i + t * t_step_str))
                signals.append(signal(len(signals)+1, 'SW', (interval+pause) * 4*i + t * t_step_str))

                signals.append(signal(len(signals)+1, 'EW', (interval+pause) * (4*i+1) + t * t_step_str))
                signals.append(signal(len(signals)+1, 'ES', (interval+pause) * (4*i+1) + t * t_step_str))

                signals.append(signal(len(signals)+1, 'NS', (interval+pause) * (4*i+2) + t * t_step_str))
                signals.append(signal(len(signals)+1, 'NE', (interval+pause) * (4*i+2) +t * t_step_str))

                signals.append(signal(len(signals)+1, 'WE', (interval+pause) * (4*i+3) +t * t_step_str))
                signals.append(signal(len(signals)+1, 'WN', (interval+pause) * (4*i+3) +t * t_step_str))

        print(end_sec)

    elif ins_type[0] == 2:
        for i in range(repeat_num):
            for t in range(t_max_str):
                print(t * t_step_str)
                print(4 * (interval + pause) * i + t * t_step_str, (interval + pause) * (4 * i + 1) + t * t_step_str,
                      (interval + pause) * (4 * i + 2) + t * t_step_str,
                      (interval + pause) * (4 * i + 3) + t * t_step_str)
                signals.append(signal(len(signals) + 1, 'SN', (interval + pause) * 4 * i + t * t_step_str, lane=2))
                signals.append(signal(len(signals) + 1, 'SW', (interval + pause) * 4 * i + t * t_step_str, lane=1))
                signals.append(signal(len(signals) + 1, 'SN', (interval + pause) * 4 * i + t * t_step_str, lane=1))

                signals.append(signal(len(signals) + 1, 'EW', (interval + pause) * (4 * i + 1) + t * t_step_str, lane=1))
                signals.append(signal(len(signals) + 1, 'ES', (interval + pause) * (4 * i + 1) + t * t_step_str, lane=1))
                signals.append(signal(len(signals) + 1, 'EW', (interval + pause) * (4 * i + 1) + t * t_step_str, lane=2))


                signals.append(signal(len(signals) + 1, 'NS', (interval + pause) * (4 * i + 2) + t * t_step_str, lane=1))
                signals.append(signal(len(signals) + 1, 'NE', (interval + pause) * (4 * i + 2) + t * t_step_str, lane=1))
                signals.append(signal(len(signals) + 1, 'NS', (interval + pause) * (4 * i + 2) + t * t_step_str, lane=2))


                signals.append(signal(len(signals) + 1, 'WE', (interval + pause) * (4 * i + 3) + t * t_step_str, lane=1))
                signals.append(signal(len(signals) + 1, 'WN', (interval + pause) * (4 * i + 3) + t * t_step_str, lane=1))
                signals.append(signal(len(signals) + 1, 'WE', (interval + pause) * (4 * i + 3) + t * t_step_str, lane=2))

    elif ins_type[0] == 3:
        for i in range(repeat_num):
            for t in range(t_max_str):
                print(t * t_step_str)
                print(4 * (interval + pause) * i + t * t_step_str, (interval + pause) * (4 * i + 1) + t * t_step_str,
                      (interval + pause) * (4 * i + 2) + t * t_step_str,
                      (interval + pause) * (4 * i + 3) + t * t_step_str)
                signals.append(signal(len(signals) + 1, 'SN', (interval + pause) * 4 * i + t * t_step_str, lane=2))
                signals.append(signal(len(signals) + 1, 'SN', (interval + pause) * 4 * i + t * t_step_str, lane=3))
                signals.append(signal(len(signals) + 1, 'SW', (interval + pause) * 4 * i + t * t_step_str, lane=1))
                # signals.append(signal(len(signals) + 1, 'SW', (interval + pause) * 4 * i + t * t_step_str, lane=2))

                signals.append(signal(len(signals) + 1, 'ES', (interval + pause) * (4 * i + 1) + t * t_step_str, lane=1))
                # signals.append(signal(len(signals) + 1, 'ES', (interval + pause) * (4 * i + 1) + t * t_step_str, lane=2))
                signals.append(signal(len(signals) + 1, 'EW', (interval + pause) * (4 * i + 1) + t * t_step_str, lane=2))
                signals.append(signal(len(signals) + 1, 'EW', (interval + pause) * (4 * i + 1) + t * t_step_str, lane=3))

                signals.append(signal(len(signals) + 1, 'NE', (interval + pause) * (4 * i + 2) + t * t_step_str, lane=1))
                signals.append(signal(len(signals) + 1, 'NS', (interval + pause) * (4 * i + 2) + t * t_step_str, lane=2))
                # signals.append(signal(len(signals) + 1, 'NE', (interval + pause) * (4 * i + 2) + t * t_step_str, lane=2))
                signals.append(signal(len(signals) + 1, 'NS', (interval + pause) * (4 * i + 2) + t * t_step_str, lane=3))

                signals.append(signal(len(signals) + 1, 'WN', (interval + pause) * (4 * i + 3) + t * t_step_str, lane=1))
                # signals.append(signal(len(signals) + 1, 'WN', (interval + pause) * (4 * i + 3) + t * t_step_str, lane=2))
                signals.append(signal(len(signals) + 1, 'WE', (interval + pause) * (4 * i + 3) + t * t_step_str, lane=2))
                signals.append(signal(len(signals) + 1, 'WE', (interval + pause) * (4 * i + 3) + t * t_step_str, lane=3))

    return signals



def generate_signals(pattern_num):
    signals = []
    if ins_type[0] == 1:
        for i in range(1):
            if pattern_num == 11:
                signals.append(signal(12*i, 'SN', 12*i))
                signals.append(signal(12*i+1, 'SW', 12*i+1))
                # signals.append(signal(12*i+2, 'SE', 12*i+2))

                signals.append(signal(12*i+3, 'EW', 12*i+3))
                # signals.append(signal(12*i+4, 'EN', 12*i+4))
                signals.append(signal(12*i+5, 'ES', 12*i+5))

                signals.append(signal(12*i+6, 'NS', 12*i+6))
                # signals.append(signal(12*i+7, 'NW', 12*i+7))
                signals.append(signal(12*i+8, 'NE', 12*i+8))

                signals.append(signal(12*i+9, 'WE', 12*i+9))
                signals.append(signal(12*i+10, 'WN', 12*i+10))
                # signals.append(signal(12*i+11, 'WS', 12*i+11))
            elif pattern_num == 12:
                signals.append(signal(12 * i, 'SN', 12 * i))
                signals.append(signal(12 * i + 1, 'SW', 12 * i + 1))

                signals.append(signal(12*i+2, 'SN', 12*i+2))

                signals.append(signal(12 * i + 3, 'EW', 12 * i + 3))
                signals.append(signal(12*i+4, 'EW', 12*i+4))
                signals.append(signal(12 * i + 5, 'ES', 12 * i + 5))

                signals.append(signal(12 * i + 6, 'NS', 12 * i + 6))
                signals.append(signal(12*i+7, 'NS', 12*i+7))
                signals.append(signal(12 * i + 8, 'NE', 12 * i + 8))

                signals.append(signal(12 * i + 9, 'WE', 12 * i + 9))
                signals.append(signal(12 * i + 10, 'WN', 12 * i + 10))
                signals.append(signal(12*i+11, 'WE', 12*i+11))
            elif pattern_num == 13:
                signals.append(signal(12 * i, 'SN', 12 * i))
                signals.append(signal(12 * i + 1, 'SW', 12 * i + 1))
                signals.append(signal(12*i+2, 'SW', 12*i+2))

                signals.append(signal(12 * i + 3, 'EW', 12 * i + 3))
                signals.append(signal(12*i+4, 'ES', 12*i+4))
                signals.append(signal(12 * i + 5, 'ES', 12 * i + 5))

                signals.append(signal(12 * i + 6, 'NS', 12 * i + 6))
                signals.append(signal(12*i+7, 'NE', 12*i+7))
                signals.append(signal(12 * i + 8, 'NE', 12 * i + 8))

                signals.append(signal(12 * i + 9, 'WE', 12 * i + 9))
                signals.append(signal(12 * i + 10, 'WN', 12 * i + 10))
                signals.append(signal(12*i+11, 'WN', 12*i+11))


    elif ins_type[0] == 2:
        for i in range(1):
            if pattern_num == 21:
                idx = 0
                signals.append(signal(16*i + idx, 'SN', 8*i, lane=1))
                idx = idx+1
                signals.append(signal(16*i+idx, 'SN', 8*i, lane=2))
                idx = idx+1
                signals.append(signal(16*i+idx, 'SW', 8*i+1, lane=1))
                idx += 1
                # signals.append(signal(16*i+3, 'SE', 8*i+1, lane=2))

                signals.append(signal(16 * i+idx, 'EW', 8 * i + 2, lane=1))
                idx += 1
                signals.append(signal(16 * i + idx, 'EW', 8 * i + 2, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'ES', 8 * i + 3, lane=1))
                idx +=1
                # signals.append(signal(16 * i + 7, 'EN', 8 * i + 3, lane=2))

                signals.append(signal(16 * i + idx, 'NS', 8 * i + 4, lane=1))
                idx +=1
                signals.append(signal(16 * i + idx, 'NS', 8 * i + 4, lane=2))
                idx +=1
                signals.append(signal(16 * i + idx, 'NE', 8 * i + 5, lane=1))
                idx +=1
                # signals.append(signal(16 * i + 11, 'NW', 8 * i + 5, lane=2))

                signals.append(signal(16 * i + idx, 'WE', 8 * i + 6, lane=1))
                idx +=1
                signals.append(signal(16 * i + idx, 'WE', 8 * i + 6, lane=2))
                idx +=1
                signals.append(signal(16 * i + idx, 'WN', 8 * i + 7, lane=1))
                idx +=1
                # signals.append(signal(16 * i + 15, 'WS', 8 * i + 7, lane=2))

            elif pattern_num == 22:
                idx=0
                signals.append(signal(16 * i + idx, 'SN', 8 * i, lane=1))
                idx = idx + 1
                signals.append(signal(16 * i + idx, 'SN', 8 * i, lane=1))
                idx = idx + 1
                signals.append(signal(16 * i + idx, 'SN', 8 * i, lane=2))
                idx = idx + 1
                signals.append(signal(16 * i + idx, 'SN', 8 * i, lane=2))
                idx = idx + 1
                signals.append(signal(16 * i + idx, 'SW', 8 * i + 1, lane=1))
                idx += 1
                # signals.append(signal(16*i+3, 'SE', 8*i+1, lane=2))

                signals.append(signal(16 * i + idx, 'EW', 8 * i + 2, lane=1))
                idx += 1
                signals.append(signal(16 * i + idx, 'EW', 8 * i + 2, lane=1))
                idx += 1
                signals.append(signal(16 * i + idx, 'EW', 8 * i + 2, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'EW', 8 * i + 2, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'ES', 8 * i + 3, lane=1))
                idx += 1
                # signals.append(signal(16 * i + 7, 'EN', 8 * i + 3, lane=2))

                signals.append(signal(16 * i + idx, 'NS', 8 * i + 4, lane=1))
                idx += 1
                signals.append(signal(16 * i + idx, 'NS', 8 * i + 4, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'NS', 8 * i + 4, lane=1))
                idx += 1
                signals.append(signal(16 * i + idx, 'NS', 8 * i + 4, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'NE', 8 * i + 5, lane=1))
                idx += 1
                # signals.append(signal(16 * i + 11, 'NW', 8 * i + 5, lane=2))

                signals.append(signal(16 * i + idx, 'WE', 8 * i + 6, lane=1))
                idx += 1
                signals.append(signal(16 * i + idx, 'WE', 8 * i + 6, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'WE', 8 * i + 6, lane=1))
                idx += 1
                signals.append(signal(16 * i + idx, 'WE', 8 * i + 6, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'WN', 8 * i + 7, lane=1))
                idx += 1
                # signals.append(signal(16 * i + 15, 'WS', 8 * i + 7, lane=2))
            elif pattern_num == 23:
                idx=0
                signals.append(signal(16 * i + idx, 'SN', 8 * i, lane=1))
                idx = idx + 1
                signals.append(signal(16 * i + idx, 'SN', 8 * i, lane=2))
                idx = idx + 1
                signals.append(signal(16 * i + idx, 'SN', 8 * i, lane=2))
                idx = idx + 1
                signals.append(signal(16 * i + idx, 'SW', 8 * i + 1, lane=1))
                idx += 1
                signals.append(signal(16 * i + idx, 'SW', 8 * i + 1, lane=1))
                idx += 1
                # signals.append(signal(16*i+3, 'SE', 8*i+1, lane=2))

                signals.append(signal(16 * i + idx, 'EW', 8 * i + 2, lane=1))
                idx += 1
                signals.append(signal(16 * i + idx, 'EW', 8 * i + 2, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'EW', 8 * i + 2, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'ES', 8 * i + 3, lane=1))
                idx += 1
                signals.append(signal(16 * i + idx, 'ES', 8 * i + 3, lane=1))
                idx += 1
                # signals.append(signal(16 * i + 7, 'EN', 8 * i + 3, lane=2))

                signals.append(signal(16 * i + idx, 'NS', 8 * i + 4, lane=1))
                idx += 1
                signals.append(signal(16 * i + idx, 'NS', 8 * i + 4, lane=1))
                idx += 1
                signals.append(signal(16 * i + idx, 'NS', 8 * i + 4, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'NE', 8 * i + 5, lane=1))
                idx += 1
                signals.append(signal(16 * i + idx, 'NE', 8 * i + 5, lane=1))
                idx += 1
                # signals.append(signal(16 * i + 11, 'NW', 8 * i + 5, lane=2))

                signals.append(signal(16 * i + idx, 'WE', 8 * i + 6, lane=1))
                idx += 1
                signals.append(signal(16 * i + idx, 'WE', 8 * i + 6, lane=1))
                idx += 1
                signals.append(signal(16 * i + idx, 'WE', 8 * i + 6, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'WN', 8 * i + 7, lane=1))
                idx += 1
                signals.append(signal(16 * i + idx, 'WN', 8 * i + 7, lane=1))
                idx += 1
                # signals.append(signal(16 * i + 15, 'WS', 8 * i + 7, lane=2))
            elif pattern_num == 24:
                idx = 0
                # signals.append(signal(16*i + idx, 'SN', 8*i, lane=1))
                # idx = idx+1
                signals.append(signal(16*i+idx, 'SN', 8*i, lane=2))
                idx = idx+1
                signals.append(signal(16*i+idx, 'SW', 8*i+1, lane=1))
                idx += 1
                # signals.append(signal(16*i+3, 'SE', 8*i+1, lane=2))

                # signals.append(signal(16 * i+idx, 'EW', 8 * i + 2, lane=1))
                # idx += 1
                signals.append(signal(16 * i + idx, 'EW', 8 * i + 2, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'ES', 8 * i + 3, lane=1))
                idx +=1
                # signals.append(signal(16 * i + 7, 'EN', 8 * i + 3, lane=2))

                # signals.append(signal(16 * i + idx, 'NS', 8 * i + 4, lane=1))
                # idx +=1
                signals.append(signal(16 * i + idx, 'NS', 8 * i + 4, lane=2))
                idx +=1
                signals.append(signal(16 * i + idx, 'NE', 8 * i + 5, lane=1))
                idx +=1
                # signals.append(signal(16 * i + 11, 'NW', 8 * i + 5, lane=2))

                # signals.append(signal(16 * i + idx, 'WE', 8 * i + 6, lane=1))
                # idx +=1
                signals.append(signal(16 * i + idx, 'WE', 8 * i + 6, lane=2))
                idx +=1
                signals.append(signal(16 * i + idx, 'WN', 8 * i + 7, lane=1))
                idx +=1

            elif pattern_num == 25:
                idx = 0
                signals.append(signal(16*i + idx, 'SN', 8*i, lane=2))
                idx = idx+1
                signals.append(signal(16 * i + idx, 'SN', 8 * i, lane=2))
                idx = idx + 1
                signals.append(signal(16 * i + idx, 'SW', 8 * i + 1, lane=1))
                idx += 1
                # signals.append(signal(16*i+3, 'SE', 8*i+1, lane=2))

                signals.append(signal(16 * i+idx, 'EW', 8 * i + 2, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'EW', 8 * i + 2, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'ES', 8 * i + 3, lane=1))
                idx += 1
                # signals.append(signal(16 * i + 7, 'EN', 8 * i + 3, lane=2))

                signals.append(signal(16 * i + idx, 'NS', 8 * i + 4, lane=2))
                idx +=1
                signals.append(signal(16 * i + idx, 'NS', 8 * i + 4, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'NE', 8 * i + 5, lane=1))
                idx += 1
                # signals.append(signal(16 * i + 11, 'NW', 8 * i + 5, lane=2))

                signals.append(signal(16 * i + idx, 'WE', 8 * i + 6, lane=2))
                idx +=1
                signals.append(signal(16 * i + idx, 'WE', 8 * i + 6, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'WN', 8 * i + 7, lane=1))
                idx += 1

            elif pattern_num == 26:
                idx = 0
                signals.append(signal(16*i + idx, 'SW', 8*i, lane=1))
                idx = idx+1
                signals.append(signal(16 * i + idx, 'SN', 8 * i, lane=2))
                idx = idx + 1
                signals.append(signal(16 * i + idx, 'SW', 8 * i + 1, lane=1))
                idx += 1
                # signals.append(signal(16*i+3, 'SE', 8*i+1, lane=2))

                signals.append(signal(16 * i+idx, 'ES', 8 * i + 2, lane=1))
                idx += 1
                signals.append(signal(16 * i + idx, 'EW', 8 * i + 2, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'ES', 8 * i + 3, lane=1))
                idx += 1
                # signals.append(signal(16 * i + 7, 'EN', 8 * i + 3, lane=2))

                signals.append(signal(16 * i + idx, 'NE', 8 * i + 4, lane=1))
                idx +=1
                signals.append(signal(16 * i + idx, 'NS', 8 * i + 4, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'NE', 8 * i + 5, lane=1))
                idx += 1
                # signals.append(signal(16 * i + 11, 'NW', 8 * i + 5, lane=2))

                signals.append(signal(16 * i + idx, 'WN', 8 * i + 6, lane=1))
                idx +=1
                signals.append(signal(16 * i + idx, 'WE', 8 * i + 6, lane=2))
                idx += 1
                signals.append(signal(16 * i + idx, 'WN', 8 * i + 7, lane=1))
                idx += 1

    elif ins_type[0] == 3:
        for i in range(1):
            if pattern_num == 31:
                signals.append(signal(12 * i, 'SN', 4 * i, lane=2))
                signals.append(signal(12 * i + 1, 'SW', 4 * i, lane=1))
                signals.append(signal(12 * i + 2, 'SN', 4 * i, lane=3))

                signals.append(signal(12 * i + 3, 'EW', 4 * i+1, lane=2))
                signals.append(signal(12 * i + 4, 'EW', 4 * i + 1, lane=3))
                signals.append(signal(12 * i + 5, 'ES', 4 * i + 1, lane=1))

                signals.append(signal(12 * i + 6, 'NS', 4 * i + 2, lane=2))
                signals.append(signal(12 * i + 7, 'NS', 4 * i + 2, lane=3))
                signals.append(signal(12 * i + 8, 'NE', 4 * i + 2, lane=1))

                signals.append(signal(12 * i + 9, 'WE', 4 * i + 3, lane=2))
                signals.append(signal(12 * i + 10, 'WN', 4 * i + 3, lane=1))
                signals.append(signal(12 * i + 11, 'WE', 4 * i + 3, lane=3))

            elif pattern_num == 32:
                signals.append(signal(12 * i, 'SN', 4 * i, lane=2))
                signals.append(signal(12 * i + 1, 'SW', 4 * i, lane=1))
                signals.append(signal(12 * i + 2, 'SN', 4 * i, lane=3))
                signals.append(signal(12 * i + 12, 'SW', 4 * i + 1, lane=1))


                signals.append(signal(12 * i + 3, 'EW', 4 * i + 1, lane=2))
                signals.append(signal(12 * i + 4, 'EW', 4 * i + 1, lane=3))
                signals.append(signal(12 * i + 5, 'ES', 4 * i + 1, lane=1))
                signals.append(signal(12 * i + 13, 'ES', 4 * i + 2, lane=1))


                signals.append(signal(12 * i + 6, 'NS', 4 * i + 2, lane=2))
                signals.append(signal(12 * i + 7, 'NS', 4 * i + 2, lane=3))
                signals.append(signal(12 * i + 8, 'NE', 4 * i + 2, lane=1))
                signals.append(signal(12 * i + 14, 'NE', 4 * i + 3, lane=1))


                signals.append(signal(12 * i + 9, 'WE', 4 * i + 3, lane=2))
                signals.append(signal(12 * i + 10, 'WN', 4 * i + 3, lane=1))
                signals.append(signal(12 * i + 11, 'WE', 4 * i + 3, lane=3))
                signals.append(signal(12 * i + 15, 'WN', 4 * i + 4, lane=1))

            elif pattern_num == 33:
                idx=0
                signals.append(signal(12 * idx, 'SW', 4 * i, lane=2))
                idx +=1
                signals.append(signal(12 * idx, 'SW', 4 * i, lane=1))
                signals.append(signal(12 * i + 2, 'SN', 4 * i, lane=3))

                signals.append(signal(12 * i + 3, 'ES', 4 * i + 1, lane=2))
                signals.append(signal(12 * i + 4, 'EW', 4 * i + 1, lane=3))
                signals.append(signal(12 * i + 5, 'ES', 4 * i + 1, lane=1))

                signals.append(signal(12 * i + 6, 'NE', 4 * i + 2, lane=2))
                signals.append(signal(12 * i + 7, 'NS', 4 * i + 2, lane=3))
                signals.append(signal(12 * i + 8, 'NE', 4 * i + 2, lane=1))

                signals.append(signal(12 * i + 9, 'WN', 4 * i + 3, lane=2))
                signals.append(signal(12 * i + 10, 'WN', 4 * i + 3, lane=1))
                signals.append(signal(12 * i + 11, 'WE', 4 * i + 3, lane=3))

            elif pattern_num == 34:
                signals.append(signal(12 * i, 'SW', 4 * i, lane=2))
                signals.append(signal(12 * i + 1, 'SW', 4 * i, lane=1))
                signals.append(signal(12 * i + 2, 'SN', 4 * i, lane=3))
                signals.append(signal(12 * i + 12, 'SN', 4 * i+1, lane=3))


                signals.append(signal(12 * i + 3, 'ES', 4 * i + 1, lane=2))
                signals.append(signal(12 * i + 4, 'EW', 4 * i + 1, lane=3))
                signals.append(signal(12 * i + 13, 'EW', 4 * i + 2, lane=3))
                signals.append(signal(12 * i + 5, 'ES', 4 * i + 1, lane=1))

                signals.append(signal(12 * i + 6, 'NE', 4 * i + 2, lane=2))
                signals.append(signal(12 * i + 7, 'NS', 4 * i + 2, lane=3))
                signals.append(signal(12 * i + 8, 'NE', 4 * i + 2, lane=1))
                signals.append(signal(12 * i + 14, 'NS', 4 * i + 3, lane=3))


                signals.append(signal(12 * i + 9, 'WN', 4 * i + 3, lane=2))
                signals.append(signal(12 * i + 10, 'WN', 4 * i + 3, lane=1))
                signals.append(signal(12 * i + 11, 'WE', 4 * i + 3, lane=3))
                signals.append(signal(12 * i + 12, 'WE', 4 * i + 4, lane=3))


    return signals

def repeat_signals(signals, interval, repeat_num):
    total_signals = []
    sig_nums = len(signals) + 10
    for i in range(repeat_num):
        # new_signals = copy.deepcopy(signals)
        # new_signals = []
        for os in signals:
            total_signals.append(signal(os.id + (i+1)*sig_nums, os.type, os.start_t + interval * (i+1), lane=os.lane))

        # for ns in new_signals:
        #     ns.id = ns.id + i
        #     ns.start_time = ns.start_t + interval * (i+1)

        # total_signals.append(new_signals)

    # for ns in total_signals:
    #     print(ns.id)

    return total_signals


if __name__ == "__main__":
    print('test')
    generate_usual_signals(repeat_num=10)
    print('test')