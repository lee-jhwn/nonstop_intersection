from config import *
# import cvxpy as cp
from sig_op_param import *
# from getConstant.getConstants import machine_data_straight, machine_data_left

class Intersection():
    def __init__(self, total_size, intrsctn_size, margin=0, intrsc_type=[1,1]):

        self.total_size = total_size
        self.intrsctn_size = intrsctn_size
        self.margin = margin
        self.type = intrsc_type

    def init_draw(self): ### !!!! same x, y intersection size
        fig, ax = plt.subplots()
        ax.set_xlim((-self.total_size, self.total_size))
        ax.set_ylim((-self.total_size, self.total_size))
        ax.set_facecolor('g')

        rect = patches.Rectangle((-self.intrsctn_size * self.type[1], -self.total_size), 2 * self.intrsctn_size * self.type[1], 2 * self.total_size,
                                 linewidth=0, edgecolor='w', facecolor='gray')
        ax.add_patch(rect)
        rect = patches.Rectangle((-self.total_size, -self.intrsctn_size * self.type[0]), 2 * self.total_size, 2 * self.intrsctn_size * self.type[0],
                                 linewidth=0, edgecolor='w', facecolor='gray')
        ax.add_patch(rect)

        x = np.linspace(-self.total_size, self.total_size)
        y = np.zeros(len(x))
        ins_loc_x, = np.where(abs(x) < self.intrsctn_size * self.type[0] + self.margin)
        # ins_loc_y, = np.where(abs(y) < self.intrsctn_size * self.type[1] + self.margin)
        x[ins_loc_x] = None
        y[ins_loc_x] = None  # x,y 교차로 크기 달라지면 조정 필요
        ax.plot(x, y, c='orange', linestyle='solid')
        ax.plot(y, x, c='orange', linestyle='solid')

        # if self.type[0]-1:
        for i in range(self.type[0]-1):
            y1 = np.full(len(x), (i+1)*self.intrsctn_size)
            ax.plot(x, y1, c='white', linestyle='--')
            ax.plot(x, -y1, c='white', linestyle='--')
            ax.plot(y1, x, c='white', linestyle='--')
            ax.plot(-y1, x, c='white', linestyle='--')


        ax.scatter(-ins_size*self.type[1]-1.5, matching_dist, marker='*', s=10, c='r', zorder=4)
        ax.scatter(ins_size*self.type[1]+1.5, -matching_dist, marker='*', s=10, c='r', zorder=4)
        ax.scatter(matching_dist, ins_size*self.type[0]+1.5, marker='*', s=10, c='r', zorder=4)
        ax.scatter(-matching_dist, -ins_size*self.type[0]-1.5, marker='*', s=10, c='r', zorder=4)


        return fig, ax




class signal():
    def __init__(self, id, type, start_t, lane=1, v=v_intersection, ax=0, ay=0):

        self.id = id
        self.ax = ax
        self.ay = ay
        self.start_t = start_t
        self.idx = self.start_t / dt # dt
        self.type = type # NS, SN, EW, WE,
        self.passed = False
        self.assigned = False
        self.assignzone = False
        self.matchzone = False
        self.assigned_car_id = None
        self.intersection = False
        self.turning = not self.type in ['SN', 'NS', 'EW', 'WE']
        self.right = self.type in ['SE', 'EN', 'NW', 'WS']
        self.left = self.type in ['SW', 'WN', 'NE', 'ES']

        self.lane = lane


        self.operation_index = None
        self.set_operation_index()
        self.operation_t = None
        # self.set_operation_t()
        self.tau = None
        self.delta = None
        self.set_delta()
        self.t_ip = None
        self.set_t_ip()
        self.travel_time = None
        self.set_travel_time()

        if self.type[0] == 'W' or self.type[0] == 'E':
            self.angle = np.deg2rad(90)
        else:
            self.angle = 0

        if self.type[0] == "S":
            self.dx = ins_size / 2 + (self.lane - 1) * ins_size
            self.dy = - ins_size - stop_line
            self.vx = 0
            self.vy = v

        elif self.type[0] =="N":
            self.dx = - ins_size / 2 - (self.lane - 1) * ins_size
            self.dy = ins_size + stop_line
            self.vx = 0
            self.vy = -v

        elif self.type[0] == "E":
            self.dx = ins_size + stop_line
            self.dy = ins_size / 2 + (self.lane - 1) * ins_size
            self.vx = -v
            self.vy = 0

        elif self.type[0] == "W":
            self.dx = - ins_size - stop_line
            self.dy = - ins_size / 2 - (self.lane - 1) * ins_size
            self.vx = v
            self.vy = 0

    def update_start_time(self):
        # self.start_t = self.operation_t[0].value
        # print(self.operation_t[0].X)
        if self.operation_t:
            self.start_t = self.operation_t[0].x
            self.idx = self.start_t / dt  # dt

    def set_operation_index(self):
        self.operation_index = op_index[self.type]
        '''
        if ins_type[0] == 1:
            if self.type == 'SN':
                self.operation_index = [3, 0]
            elif self.type == 'SE':
                self.operation_index = [3]
            elif self.type == 'SW':
                self.operation_index = [3, 2, 0, 1]
            elif self.type == 'EW' :
                self.operation_index = [0,1]
            elif self.type == 'EN':
                self.operation_index = [0]
            elif self.type == 'ES':
                self.operation_index = [0, 3, 1, 2]
            elif self.type == 'NS':
                self.operation_index = [1, 2]
            elif self.type == 'NW':
                self.operation_index = [1]
            elif self.type == 'NE':
                self.operation_index = [1, 2, 0, 3]
            elif self.type == 'WE' :
                self.operation_index = [2,3]
            elif self.type == 'WS':
                self.operation_index = [2]
            elif self.type == 'WN':
                self.operation_index = [2, 3, 1, 0]

        elif ins_type[0] == 3:
            if self.type == 'SN':
                self.operation_index = [14, 11, 19, 7, 4] #,  18,  20,  31,  10,  12, 5]
            elif self.type == 'SE':
                self.operation_index = []
            elif self.type == 'SW':
                self.operation_index = [16, 20, 12, 8, 18, 6] #27, 28, 32, 21, 23, 13, 19, 30, 9, 15]
            elif self.type == 'EW':
                self.operation_index = [4, 3, 17, 2, 1]
            elif self.type == 'EN':
                self.operation_index = []
            elif self.type == 'ES':
                self.operation_index = [7, 19, 9, 12, 20, 15] #, 16, 31, 14, 20, 21, 24, 32, 26, 28]
            elif self.type == 'NS':
                self.operation_index = [1, 6, 18, 10, 13]# 2, 9, 30, 17, 22]
            elif self.type == 'NW':
                self.operation_index = []
            elif self.type == 'NE':
                self.operation_index = [2, 17, 5, 9, 19, 11] #1, 2, 0, 3]
            elif self.type == 'WE':
                self.operation_index = [13, 15, 20, 16, 14]#2, 3]
            elif self.type == 'WS':
                self.operation_index = []
            elif self.type == 'WN':
                self.operation_index = [10, 18, 8, 5, 17, 3]#2, 3, 1, 0]
                '''

    def set_operation_t(self, m):
        # if ins_type[0] == 1:
        if self.operation_index:
            self.operation_t = m.addVars(len(self.operation_index), vtype=GRB.CONTINUOUS, name=f'x{self.id}') # real, gt 0
        # m.addConstrs(self.operation_t >= 0)
            # print(self.operation_t)
            # self.operation_t = cp.Variable(len(self.operation_index))
            # if not self.turning:
            #     self.operation_t = cp.Variable(2)
            # elif self.right:
            #     self.operation_t = cp.Variable(1)
            # elif self.left:
            #     self.operation_t = cp.Variable(4)

    def set_delta(self):
        # if ins_type[0] == 1:
        #     if not self.turning:
        #         temp = (ins_size + car_size[1]) / v_intersection
        #         self.delta = [temp, temp]
        #     elif self.right:
        #         self.delta = [ins_size*pi/(v_intersection*4)]
        #     elif self.left:
        #         temp = (1.5*ins_size*pi/(4*v_intersection))
        #         temp2 = (1.5*ins_size*pi/(6*v_intersection))
        #         self.delta = [temp, temp2, temp2, temp]
        #
        # elif ins_type[0] == 3:
        #     if not self.turning:
        #         self.delta = [0.504, 0.4629, 0.4937, 0.4629, 0.504]
        #     elif self.left:
        #         self.delta = [0.4771,  0.5551,  0.4771,  0.4771,  0.5421,  0.4771]
        #     elif self.right:
        #         self.delta = []
        if self.left :
            self.delta = deltas['left']
        elif not self.turning:
            self.delta = deltas['straight']

    def set_t_ip(self):

        if self.left :
            self.t_ip = t_ips['left']
        elif not self.turning:
            self.t_ip = t_ips['straight']
        # self.t_ip = []
        # if ins_type[0] == 1:
        #     self.t_ip = np.ones(len(self.operation_index)+1)#, dtype=float)
        #     # if not self.turning:
        #
        # elif ins_type[0] == 3:
        #     if not self.turning:
        #         # self.t_ip = [0.24685714285714283, 0.3908571428571428, 0.22628571428571426, 0.06171428571428571, 0.2674285714285714, 0.09257142857142855]
        #         self.t_ip = [  0.2469,   0.2674,   0.0617,   0.0926,   0.2263, 0.3909]
        #     elif self.left:
        #         # self.t_ip = [0.26012387171723483, 0.37717961398999056, 0.05202477434344696, 0.32515483964654357, 0.03901858075758522, 0.11705574227275567, 0.13006193585861742]
        #         self.t_ip = [ 0.2601,  0.039 ,  0.1301,  0.3252,  0.052 ,  0.1171,  0.3772]
        #     elif self.right:
        #         self.t_ip = []


        # print(self.t_ip)
        return

    def set_travel_time(self):
        if not self.turning:
            self.travel_time = ins_size * ins_type[0] * 2 / v_intersection

        elif self.left:
            r = ins_size * ins_type[0] + 0.5 * ins_size
            self.travel_time = pi * r / (2 * v_intersection)

        elif self.right:
            self.travel_time = pi * ins_size / (4 * v_intersection)




    def turn(self):

        mode = self.type

        if mode == 'SW' or mode == 'WS':
            r = ((self.dx+ins_size*ins_type[0])**2 + (self.dy+ins_size*ins_type[0])**2)**0.5
            v = (self.vx**2 + self.vy**2)**0.5
            a = v*v/r

            ax = -a * (self.dx+ins_size*ins_type[0]) / r
            ay = -a * (self.dy+ins_size*ins_type[0]) / r

            self.angle = np.arctan((self.dy + ins_size*ins_type[0]) / (self.dx + ins_size*ins_type[0]))

        elif mode == 'SE' or mode == 'ES':
            r = ((self.dx-ins_size*ins_type[0])**2 + (-self.dy-ins_size*ins_type[0])**2)**0.5
            v = (self.vx**2 + self.vy**2)**0.5
            a = v*v/r

            ax = a * (ins_size*ins_type[0] - self.dx) / r
            ay = a * (-ins_size*ins_type[0] - self.dy) / r

            self.angle = np.arctan((-ins_size*ins_type[0] - self.dy) / (ins_size*ins_type[0] - self.dx))

        elif mode == 'NE' or mode == 'EN':
            r = ((ins_size*ins_type[0]-self.dx)**2 + (ins_size*ins_type[0]-self.dy)**2)**0.5
            v = (self.vx**2 + self.vy**2)**0.5
            a = v*v/r

            ax = a * (ins_size*ins_type[0] - self.dx) / r
            ay = a * (ins_size*ins_type[0] - self.dy) / r

            self.angle = np.arctan((ins_size*ins_type[0] - self.dy) / (ins_size*ins_type[0] - self.dx))

        elif mode == 'NW' or mode == 'WN':
            r = ((-ins_size*ins_type[0]-self.dx)**2 + (ins_size*ins_type[0]-self.dy)**2)**0.5
            v = (self.vx**2 + self.vy**2)**0.5
            a = v*v/r

            ax = a * (-ins_size*ins_type[0] - self.dx) / r
            ay = a * (ins_size*ins_type[0] - self.dy) / r

            self.angle = np.arctan((ins_size*ins_type[0] - self.dy) / (-ins_size*ins_type[0] - self.dx))

        self.dx = self.dx + dt * self.vx
        self.dy = self.dy + dt * self.vy

        self.vx = self.vx + dt * ax
        self.vy = self.vy + dt * ay



    def get_next_vd(self):

        if self.turning and self.intersection and not self.passed:
            self.turn()

        else:

            self.dx = self.dx + dt * self.vx
            self.dy = self.dy + dt * self.vy

            self.vx = self.vx + dt * self.ax
            self.vy = self.vy + dt * self.ay


    def loc_bools_update(self, intrs_size):


        if not self.intersection:
            if abs(self.dy) < matching_dist and abs(self.dx) < matching_dist:
                self.matchzone = True
            elif abs(self.dy) < assign_dist+matching_dist and abs(self.dx) < assign_dist+matching_dist:
                self.assignzone = True

        if (not self.intersection) and (abs(self.dx) < intrs_size*ins_type[0] and abs(self.dy) < intrs_size*ins_type[0]):
            self.intersection = True

        elif self.intersection and (abs(self.dx) > intrs_size*ins_type[0] or abs(self.dy) > intrs_size*ins_type[0]):
            self.passed = True




def signal_update(signals, i):

    for s in signals:
        if s.idx < i:
            if s.type[1] == "N":
                if s.dy < ins_size*ins_type[0]:
                    s.get_next_vd()
                else:
                    s.passed = True
            elif s.type[1] == "S":
                if s.dy > -ins_size*ins_type[0]:
                    s.get_next_vd()
                else:
                    s.passed = True
            elif s.type[1] == "E":
                if s.dx < ins_size*ins_type[0]:
                    s.get_next_vd()
                else:
                    s.passed = True
            elif s.type[1] == "W":
                if s.dx > -ins_size*ins_type[0]:
                    s.get_next_vd()
                else:
                    s.passed = True

        s.loc_bools_update(ins_size)


def signal_draw(fig, ax, x, y):

    ax.scatter(x,y, s=10, c='r', zorder=4)


def del_signal(signals):

    for i,s in enumerate(signals):
        if s.passed:
            del signals[i]



