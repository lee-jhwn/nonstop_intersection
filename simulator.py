from vehicle import vehicle
from config import *
from intersection import *
import os
from convex_solver import get_match_acc, get_match_acc_cvnx
from jss_solver import optimize_signals
from gurobi import optimize_signals_gurobi
import csv
from datetime import datetime
from generate_signals import *
from tqdm import tqdm

# now = datetime.now().strftime('%Y%m%d-%H%M%S')


def find_front_car_id(cars, car):

    for c in cars:
        if c.start_loc == car.start_loc and c.lane == car.lane:
            if (c.start_loc == 'E' or c.start_loc == 'W') and np.abs(c.dx) < np.abs(car.dx):

                if car.front_car_distance > np.abs(car.dx - c.dx):

                    car.front_car_distance = np.abs(car.dx - c.dx) #- car.size[1] - c.size[1]
                    car.front_car_id = c.id

            elif (c.start_loc == 'S' or c.start_loc == 'N') and np.abs(c.dy) < np.abs(car.dy):

                if car.front_car_distance > np.abs(car.dy - c.dy):
                    car.front_car_distance = np.abs(car.dy - c.dy) #- car.size[1] - c.size[1]
                    car.front_car_id = c.id

def generate_random_car(i, traffic_const, pattern_num):



    st_rnd_int = np.random.randint(4)
    start_loc = loc_list[st_rnd_int]
    end_loc = None
    lane_x = np.random.randint(ins_type[0]) + 1
    rdn_v = np.random.randint(9,18)

    if ins_type[0] == 2:
        if lane_x == 1:
            if pattern_num in [21,22,23,0]:
                end_loc = loc_list[(st_rnd_int + np.random.randint(1,3)) % 4] # left + straight
            elif pattern_num in [24,25,26]:
                end_loc = loc_list[(st_rnd_int + 1) % 4] # left turn only
        elif lane_x == 2:
            # end_loc = loc_list[(st_rnd_int + np.random.randint(2, 4)) % 4]
            end_loc = loc_list[(st_rnd_int + 2) % 4]


    elif ins_type[0] == 3:
        if pattern_num in [31, 32,0]:
            if lane_x == 1:
                end_loc = loc_list[(st_rnd_int + 1) % 4] # left turn only
            elif lane_x in [2,3]:
                end_loc = loc_list[(st_rnd_int + 2) % 4]
        if pattern_num in [33, 34]:
            if lane_x in [1,2]:
                end_loc = loc_list[(st_rnd_int+1) % 4]
            elif lane_x == 3:
                end_loc = loc_list[(st_rnd_int + 2) % 4]

    elif ins_type[0] == 1:
        # print(np.random.randint(1,3))
        end_loc = loc_list[(st_rnd_int + np.random.randint(1,3)) % 4]


    if start_loc == 'N':
        # return vehicle(i, dirc[0], dirc[1], (-ins_size/2, stop_line + i*10/traffic_const), (0, -rdn_v), ans)
        return vehicle(i, start_loc, end_loc, size + 1 + i * 10 / traffic_const, (0, -rdn_v), ans, lane=lane_x)
    elif start_loc == 'S':
        # return vehicle(i, dirc[0], dirc[1], (ins_size/2, -stop_line - i*10/traffic_const), (0, rdn_v), asn)
        return vehicle(i, start_loc, end_loc, -size -1 - i * 10 / traffic_const, (0, rdn_v), asn, lane=lane_x)
    elif start_loc == 'W':
        # return vehicle(i, dirc[0], dirc[1], (-stop_line - i*10/traffic_const, -ins_size/2), (rdn_v, 0), awe)
        return vehicle(i, start_loc, end_loc, -size -1 - i * 10 / traffic_const, (rdn_v, 0), awe, lane=lane_x)

    elif start_loc == 'E':
        # return vehicle(i, dirc[0], dirc[1], (stop_line + i*10/traffic_const, ins_size/2), (-rdn_v,0), aew)
        return vehicle(i, start_loc, end_loc, size + 1 + i * 10 / traffic_const, (-rdn_v, 0), aew, lane=lane_x)


def simulate(intersection, traffic_const, pattern_num):

    print('simulating...')
    fig, ax = None, None


    cars = []

    for i in range(int(end_sec*traffic_const)*5):
        cars.append(generate_random_car(i, traffic_const, pattern_num))

    print(f'{len(cars)*3600/end_sec} cars per hour')

    # print(pattern_num)
    if usual:
        signals = generate_usual_signals()

    else:
        signals = generate_signals(pattern_num=pattern_num)
        signals, c_max = optimize_signals_gurobi(signals)
        c_max = c_max

        signals = signals + repeat_signals(signals, c_max, end_sec)

    # print('signals:', signals)

    signal_log = []


    logs_head = ['index', 'time']

    for i, car in enumerate(cars):

        logs_head.append((f'car_{i+1}:(x,y,angle); size - ',car.size))
        find_front_car_id(cars, car)



    logs = [logs_head]

    logs.append([0,0])
    logs[-1] = logs[-1] + [(car.dx, car.dy, car.angle) for car in cars] ## record at time 0
    signal_log.append([0])
    # print(signal_log[-1])
    # print(signals)
    signal_log[-1] = signal_log[-1] + [(s.dx, s.dy) for s in signals if not s.idx]

    # print(logs)

    for i,ti in tqdm(enumerate(t), desc='time', total=len(t)): ######### time loop ################

        # if not (i % 10):
        print(f'pattern {pattern_num}, traffic {traffic_const}\n')


        logs.append([i+1, ti]) #### log head
        signal_log.append([i+1])

        signal_update(signals, i)
        assign_signal(cars, signals, i)
        # match_signal(cars, signals, i)
        match_signal_cnvx(cars, signals, i)
        slow_unassigned(cars, i)

        # print(cars[4].dx, cars[4].dy, cars[4].vx, cars[4].vy)

        front_car_distance_update(cars)
        avoid_collision(cars, i)

        set_exit_acc(cars, i)
        loc_update(intersection, cars, i)

        del_signal(signals)

        signal_log[-1] = signal_log[-1] + [(s.dx, s.dy) for s in signals if s.idx < i]
        logs[-1] = logs[-1] + [(car.dx, car.dy, car.angle) for car in cars] ###record

    save_delay_log(cars, pattern_num, traffic_const)


    return logs, signal_log

def save_delay_log(cars, pattern_num, traffic_const):
    delay_measure_log = [['configuration', f'instruction type: {ins_type}', f'traffic const: {traffic_const}', f'{len(cars)*3600/end_sec} cars / hour'],
                         ['car id', 'turn type', 'lane', 'optimal travel time', 'actual travel time', 'delay']]
    for car in cars:
        # print(car.turning)
        if not car.turntype:
            turning_type = 'straight'
        elif car.left:
            turning_type = 'left'
        elif car.right:
            turning_type = 'right'

        # print(turning_type)

        try:
            delay = car.actual_travel_time - car.optimal_travel_time
        except:
            delay = None

        delay_measure_log.append([car.id, car.lane, turning_type, car.optimal_travel_time, car.actual_travel_time, delay])

    with open(f'./delay_log/delay_log_{ins_type}_{pattern_num}_{traffic_const}.csv', 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(delay_measure_log)

    return



def match_signal(cars, signals, i):
    for car in cars:
        if car.assigned and not car.matched:
            for signal in signals:
                if car.assigned_signal_id == signal.id:
                    # t = 2 * (matching_dist - car.size[1]/2) / abs(car.vx + car.vy + signal.vx + signal.vy)
                    # t_idx = int(t / dt)
                    # if car.start_loc == 'N':
                    #     car.ay[i:i+t_idx] = (signal.vy - car.vy) / t
                    # elif car.start_loc == 'S':
                    #     car.ay[i:i+t_idx] = (signal.vy - car.vy) / t
                    #     print(t_idx)
                    #     print(car.ay[i:i+t_idx])
                    # elif car.start_loc == 'E':
                    #     car.ax[i:i+t_idx] = (signal.vx - car.vx) / t
                    # elif car.start_loc == 'W':
                    #     car.ax[i:i + t_idx] = (signal.vx - car.vx) / t

                    if get_match_acc(car, signal, i):
                        car.matched = True


    return

def match_signal_cnvx(cars, signals, i):
    for car in cars:
        if car.assigned and not car.matched:
            for signal in signals:
                if car.assigned_signal_id == signal.id:
                    try:
                        if get_match_acc_cvnx(car, signal, i):
                            car.matched = True
                            print(f'car{car.id} and signal{signal.id} matched!!!!!!!')

                        else:
                            car.assigned = False
                            signal.assigned = False
                            print(f'car{car.id} and signal{signal.id} not matched, unassigned.')
                        # car.matched = get_match_acc_cvnx(car, signal, i)
                        # car.matched = True
                    except:
                        print(f'car{car.id} and signal{signal.id} matched but time index out of range')
                        car.matched = True






def slow_unassigned(cars, i):
    for car in cars:
        if car.assignzone and not car.assigned:
            stop_d = 0.5 * abs(car.vy + car.vx)**2 / max_a
            if car.start_loc == 'N' and stop_d + matching_dist > abs(car.dy) - car.size[1]/2 and car.vy:
                car.ay[i] = max_a
            elif car.start_loc == 'S' and stop_d + matching_dist > abs(car.dy) - car.size[1] / 2 and car.vy:
                car.ay[i] = -max_a
            elif car.start_loc == 'W' and stop_d + matching_dist > abs(car.dx) - car.size[1] / 2 and car.vx:
                car.ax[i] = -max_a
            elif car.start_loc == 'E' and stop_d + matching_dist > abs(car.dx) - car.size[1] / 2 and car.vx:
                car.ax[i] = max_a

            # print('slow not assigned')
            # if car.start_loc == 'N':
            #     car.ay[i] = 0.5 * car.vy ** 2 / (car.dy - matching_dist)# - car.size[1]/2)
            # elif car.start_loc == 'S':
            #     car.ay[i] = 0.5 * car.vy ** 2 / (car.dy + matching_dist)# + car.size[1]/2)
            # elif car.start_loc == 'E':
            #     car.ax[i] = 0.5 * car.vx ** 2 / (car.dx - matching_dist)# - car.size[1]/2)
            # elif car.start_loc == 'W':
            #     car.ax[i] = 0.5 * car.vx ** 2 / (car.dx + matching_dist)# + car.size[1]/2)

            if car.start_loc in ['N', 'S'] and abs(car.dy) - car.size[1]/2 < matching_dist:# + car.size[1]/2 :
                car.vy = 0
            elif car.start_loc in ['E', 'W'] and abs(car.dx) - car.size[1]/2 < matching_dist:# + car.size[1]/2 :
                car.vx = 0

    return

def match(car, signal):
    car.assigned_signal_id = signal.id
    signal.assigned_car_id = car.id
    car.assigned = True
    signal.assigned = True

    return


def front_car_assigned(me, cars):
    for front in cars:
        if me.front_car_id == front.id:
            return front.intersection

    return me.front_car_distance > 9.99e5

# def matchzone_enter_t(car, i):
#     vx, vy = car.vx, car.vy
#     dx, dy = car.dx, car.dy
#
#     for j, ax in enumerate(car.ax[i:]):
#         vx = vx + ax * dt
#         vy = vy + car.ay[i+j] * dt
#         dx = dx + vx * dt
#         dy = dy + vy * dt
#         # print(j)
#         if car.start_loc in 'SN':
#             if abs(dy) < matching_dist:
#                 return j, dy, vy
#         elif car.start_loc in 'EW':
#             if abs(dx) < matching_dist:
#                 return j, dx, vx
#
#     return -1, -1, -1

def check_assign_possible(car, signal, i):
    # mtch_tidx, cd, cv = matchzone_enter_t(car, i)
    # mtch_t = mtch_tidx * dt
    # # print(mtch_tidx)
    # if mtch_tidx == -1:
    #     return False


    if car.start_loc == 'S':

        t = (-ins_size*ins_type[0] - signal.dy) / signal.vy
        tm = (signal.vy - car.vy + max_a*t) / (2*max_a)
        dist = 0.5 * (2*car.vy + max_a*tm)*tm + 0.5 * (car.vy + signal.vy + max_a * tm)*(t-tm)
        #
        # print(dist)
        # print(-ins_size - car.dy)
        return abs(dist) > abs(-ins_size*ins_type[0] - car.dy)

    elif car.start_loc == 'N':

        t = (ins_size*ins_type[0] - signal.dy) / signal.vy
        tm = (signal.vy - car.vy - max_a*t) / (2*-max_a)
        dist = 0.5 * (2*car.vy - max_a*tm)*tm + 0.5 * (car.vy + signal.vy - max_a * tm)*(t-tm)
        # print(t, tm)
        # print(dist)
        # print(ins_size - car.dy)

        return abs(dist) > abs(ins_size*ins_type[0] - car.dy)

    elif car.start_loc == 'E':

        t = (ins_size*ins_type[0] - signal.dx) / signal.vx
        tm = (signal.vx - car.vx - max_a * t) / (2 * -max_a)
        dist = 0.5 * (2 * car.vx - max_a * tm) * tm + 0.5 * (car.vx + signal.vx - max_a * tm) * (t - tm)

        return abs(dist) > abs(ins_size*ins_type[0] - car.dx)

    elif car.start_loc == 'W':

        t = (-ins_size*ins_type[0] - signal.dx) / signal.vx
        tm = (signal.vx - car.vx + max_a * t) / (2 * max_a)
        dist = 0.5 * (2 * car.vx + max_a * tm) * tm + 0.5 * (car.vx + signal.vx + max_a * tm) * (t - tm)

        return abs(dist) > abs(-ins_size*ins_type[0] - car.dx)






        # t = ((24*max_a*(signal.dy+signal.vy*mtch_t-cd)+13*(cv - signal.vy)**2)**0.5 -3*cv + 3*signal.vy )/(2*max_a)
        # dist = signal.vy * t + (signal.dy + signal.vy*mtch_t - cd)
        # print(dist)
        # return dist < matching_dist
        # tm = ((24*max_a*(signal.dy+signal.vy*mtch_t-cd)+13*(cv - signal.vy)**2)**0.5 -5*cv + 5*signal.vy )/(6*max_a)
            # ((24*max_a*(signal.dy-car.dy)+13*(car.vy - signal.vy)**2)**0.5 -5*car.vy + 5*signal.vy )/(6*max_a)
        # tm_idx = int(tm/dt)
        # t_idx = int(t/dt)
        # print(mtch_t, tm, t, cv)
        # print(0.5 * (2*cv + max_a*tm) * tm + 0.5*(cv + signal.vy + max_a*tm) * (t - tm) )
        # print(matching_dist)

        # return 0.5 * (2*cv + max_a*tm) * tm + 0.5*(cv + signal.vy + max_a*tm) * (t - tm) < matching_dist


def assign_signal(cars, signals, i):

    for i,c in enumerate(cars):
        if (not cars[i].assigned) and cars[i].assignzone and front_car_assigned(cars[i], cars):
            for signal in signals:
                if not signal.assigned and signal.assignzone and not signal.matchzone and cars[i].start_loc+cars[i].end_loc == signal.type and signal.lane == cars[i].lane:
                    if check_assign_possible(cars[i], signal, i):
                        if not cars[i].assigned:
                            # print('before match', cars[i].assigned)
                            match(cars[i], signal)
                            # print('before match', cars[i].assigned)
                            # print(i)
                            # print(cars[i])

                        # if car.assigned:
                        #     print('after match', car.assigned)
                    # if car.start_loc in ['S', 'N']:
                    #     if abs(car.dy - signal.dy) - car.size[1]/2 < 0.5 * abs((car.vy**2 - signal.vy**2)/max_a):
                    #         match(car, signal)
                    # elif car.start_loc in ['E', 'W']:
                    #     if abs(car.dx - signal.dx) - car.size[1]/2 < 0.5 * abs((car.vx**2 - signal.vx**2)/max_a):
                    #         match(car, signal)
                    # elif car.vx == 0 and car.vy == 0:
                    #     if abs(car.dx - signal.dx) + abs(car.dy - signal.dy) < 10e-2:
                    #         match(car, signal)
                        print(f'car{cars[i].id} assigned to signal{signal.id}')
                        break

    return

def front_car_distance_update(cars):

    for me in cars:
        if not me.passed:
            for front in cars:
                if front.id == me.front_car_id:
                    if not front.intersection:
                        if me.start_loc =='S' or me.start_loc == 'N':
                            me.front_car_distance = np.abs(me.dy-front.dy) - me.size[1]/2 - front.size[1]/2
                        elif me.start_loc == 'W' or me.start_loc == 'E':
                            me.front_car_distance = np.abs(me.dx-front.dx) - me.size[1]/2 - front.size[1]/2
                    elif front.passed or front.intersection or front.matched:
                        me.front_car_distance = big_num

        elif me.intersection or me.passed:
            me.front_car_distance = big_num


def avoid_collision(cars, i):


    for car in cars:
        if not car.passed: #and  car.front_car_distance < 20:
            for front in cars:
                if front.id == car.front_car_id and not front.intersection and not front.passed:
                    df = min_dist_bt_cars + 0.5 * (front.vx + front.vy - car.vx - car.vy)**2 / max_a
                    if car.front_car_distance < df:
                    # a = (front.vx**2 + front.vy**2 - car.vy**2 - car.vy**2) / (2*(car.front_car_distance-min_dist_bt_cars))
                    # a = 0.5 * ((front.vx + front.vy - car.vx - car.vy)**2) / (car.front_car_distance - min_dist_bt_cars)


                        if car.start_loc == 'S':
                            car.ay[i] = -max_a
                            if car.vy < 0:
                                car.vy = 0
                        elif car.start_loc == 'N':
                            car.ay[i] = max_a
                            if car.vy > 0:
                                car.vy = 0
                        elif car.start_loc == 'W':
                            car.ax[i] = -max_a
                            if car.vx < 0:
                                car.vx = 0
                        elif car.start_loc == 'E':
                            car.ax[i] = max_a
                            if car.vx > 0:
                                car.vx = 0

                    if car.front_car_distance < min_dist_bt_cars and not car.matchzone:
                        car.vx = front.vx
                        car.vy = front.vy


def set_exit_acc(cars, i, exit_speed=exit_speed):
    for car in cars:
        if car.passed:
            if np.abs(car.vx) + np.abs(car.vy) < exit_speed:
                if car.end_loc == 'N':
                    car.ay[i] = max_a
                elif car.end_loc == 'S':
                    car.ay[i] = -max_a




def loc_update(intersection, cars, i):

    for car in cars:
        car.get_next_vd((car.ax[i], car.ay[i]), intersection.intrsctn_size)
        car.loc_bools_update(intersection.intrsctn_size)
        car.check_map(i)
        # print(car.vy)

    return

def car_draw(fig, ax, dx, dy, size, angle=0):

    rect = patches.Rectangle((dx - size[0] * 0.5, dy - size[1] * 0.5), size[0], size[1], linewidth=0, edgecolor='w', facecolor='b')

    if angle:
        rotate = matplotlib.transforms.Affine2D().rotate_deg_around(dx, dy, np.rad2deg(angle)) + ax.transData
        rect.set_transform(rotate)

    ax.add_patch(rect)



def sim_draw(intersection, logs, signal_log, pattern_num, traffic_const):

    # path = f'./sim_draw/int_{ins_type[0]}_P{pattern_num}_T{traffic_const}'
    path = f'../../../../home_kahlo/jihwan.lee/2019-2_jolproj/data/sim_draw/int_{ins_type[0]}_P{pattern_num}_T{traffic_const}'

    if not os.path.isdir(path):
        os.mkdir(path)


    for i, line in tqdm(enumerate(logs[1:]), desc='item', total=len(logs[1:])):

        if i % 10 == 0:
            fig, ax = intersection.init_draw()

            for j, car in enumerate(line[2:]):

                car_draw(fig, ax, car[0], car[1], logs[0][j+2][1], car[2])

            for s in signal_log[i][1:]:
                signal_draw(fig, ax, s[0], s[1])

            plt.savefig(f'{path}/test{i}.png')
            plt.close('all')






# if __name__ == '__main__':

def run(traffic_const, pattern_num):
    print('main begins')

    intersection1 = Intersection(size, ins_size, intrsc_type=ins_type)

    print('recording logs...')
    logs, signal_log = simulate(intersection1, traffic_const=traffic_const, pattern_num=pattern_num)

    if visualize:

        print('visualizing...')


        sim_draw(intersection1, logs, signal_log, pattern_num, traffic_const)

        print('visualization finished')

    # plt.show()
    return

if __name__ == '__main__':
    for patt in pattern_nums:
        # global pattern_num
        # pattern_num = p
        for trff in traffic_consts:
            # global traffic_const
            # traffic_const= t
            print(f'Pattern {patt}, Traffic {trff}')
            run(pattern_num=patt,traffic_const=trff)





'''
a1 = (np.ones(len(t)), np.zeros(len(t)))
car1 = vehicle(None, None, (-10, -ins_size/2), (0, 0), a1)

a2 = (2*np.sin(t), np.zeros(len(t)))
car2 = vehicle(None, None, (5, -ins_size/2), (0, 0), a2)


a3 = (np.zeros(len(t)), np.ones(len(t)))
car3 = vehicle(None, None, (ins_size/2, 5), (0, 0), a3)

a4 = (np.zeros(len(t)), np.zeros(len(t)))
car4 = vehicle(None, None, (ins_size/2, -30), (0, 5), a3)
car4.turn("SE")




cars = [car1, car2, car3, car4]

carloc = []

for car in cars:
    carloc.append([car.dx, car.dy])


carloc = np.transpose(carloc, [2,0,1])

print(carloc.shape)

fig, ax = plt.subplots()
ax.set_xlim((-size,size))
ax.set_ylim((-size,size))
ax.set_facecolor('g')


rect = patches.Rectangle((-ins_size,-size),2*ins_size,2*size,linewidth=0,edgecolor='w',facecolor='gray')
ax.add_patch(rect)
rect = patches.Rectangle((-size,-ins_size),2*size,2*ins_size,linewidth=0,edgecolor='w',facecolor='gray')
ax.add_patch(rect)


x = np.linspace(-size,size)
y = np.zeros(len(x))
ins_loc, = np.where(abs(x)<ins_size)
x[ins_loc] = None
y[ins_loc] = None
ax.plot(x,y, c='orange', linestyle='dashed')
ax.plot(y,x, c='orange', linestyle='dashed')


scat = ax.scatter(None, None, c='r', zorder=5)


# print(carloc)

# plt.scatter(car2.dx[2000], car2.dy[2000])

#
# def simulate():
#
#     a1 = (np.ones(len(t)), np.zeros(len(t)))
#     car1 = vehicle((0,0),(0,0),a1)
#     car1.get_path()
#
#     a2 = (np.sin(t), np.zeros(len(t)))
#     car2 = vehicle((0,0),(0,0),a2)
#     car2.get_path()
#graph([car1, car2])
#
#     anim = animation.FuncAnimation(fig, animate, init_func=ani_init, frames=30, interval=20, blit=True)

def ani_init():
    scat.set_offsets(carloc[0])

    # line.set_data([], [])
    # return (line,)

def animate(i):
    scat.set_offsets(carloc[i])
    # print(i)

    # line.set_data([car2.dx[i]],[car2.dy[i]])



    # return (line,)

def graph(cars):

    figxy = plt.figure()

    figx = figxy.add_subplot(2,1,1)
    figy = figxy.add_subplot(2,1,2)

    for car in cars:
        figx.plot(t, car.dx)
        figy.plot(t, car.dy)

    # plt.show()

# graph([car2])

anim = animation.FuncAnimation(fig, animate, init_func=ani_init, frames=len(t), interval=1, blit=False)

plt.show()


# if __name__=='__main__':

    # simulate()



    # gurobi int
    # LP scipy

    # integer programming solver

    # 회전
    # collision avodiance size 2-3*5 알아서 멈추도록 차간의 distance에 따라서 acceleration
    # intersection heuristic patterns v=50km/h
    # acc profile - intersection simulation / 교차로까진 acc profile, 나간 후에는 등속으로, 좌화전우회전직진

    # signal에 타는 (LP)


    # 회전
    
    #


'''



# matching assign
# signal optimize
# intersection expand



# delay measure 얼마나 효율적인지? 차가 많을때, 적을때, 등등 일반 신호등과 비교
# 논문?





# matching ts 초에 vs라는 속도를 가지면 댐, 한대씩,, 매칭 가능 여부판별, acc profile 정하기
# acc 어떻게 정하는가? convex solver
# assign - 어떤 신호와 매칭할지 정하고, matching zone 에서 매칭, assign 실패시 matching zone에서 기다림.


# signal optimize - gurobi, interger software
# conflict zones, 차 - job, conflict zone 지나는거 operation, 무슨 j가 무슨 o 를 할지 정함
# prececent constraint, collision aviod, 어떤 잡이 어떤 시간에 교차로 진입할


# Q1 time length unknown?
# Q2 assign after change? # assign only when front car at intersection



# convex solver t index out of range


# more lanes
# trajectory pattern
# signal start time optimization
# solver coding
# find conflict zones/parameters
# order ofconflict zones of a signal
# data structure




# intereection in out time of car
# statistics
# delay - 한대가 들어오고 나가는데 실제걸린시간
# 최단시간(혼자) 일때랑 비교

# 여러 차량의 평균



# delay measure - data, statistics; optimal : analytic; real time: map in/out
# scenarios patterns; traffic scenarios; intersection dimension (l,s,r:111, 222) repeat;;