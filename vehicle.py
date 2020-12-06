from config import *

class vehicle():
    def __init__(self, id, start_loc, end_loc, init_d, init_v, acc, lane=1, size=car_size, color=None):

        self.start_loc = start_loc # NEWS
        self.end_loc = end_loc # NEWS

        self.id = id
        self.front_car_id = None
        self.front_car_distance = 10e5
        self.lane = lane

        self.map = False
        # self.check_map_init()
        self.map_enter = None
        self.map_leave = None
        self.optimal_travel_time = None
        self.actual_travel_time = None

        self.matchzone = False
        self.matched = False
        self.assignzone = False
        self.assigned = False
        self.assigned_signal_id = None

        self.intersection = False # if in intersection
        self.passed = False
        self.turning = not (self.start_loc + self.end_loc) in ['SN', 'NS', 'EW', 'WE']
        self.turntype = self.turning
        self.right = (self.start_loc + self.end_loc) in ['SE', 'EN', 'NW', 'WS']
        self.left = (self.start_loc + self.end_loc) in ['SW', 'WN', 'NE', 'ES']

        self.size = size # car size; default 2 * 5
        self.color = color

        self.dx, self.dy = None, None
        self.init_loc(init_d)

        # self.dx, self.dy = init_d[0], init_d[1]
        self.vx, self.vy = init_v[0], init_v[1]
        self.ax, self.ay = np.copy(acc[0]), np.copy(acc[1])

        if self.start_loc == 'W' or self.start_loc == 'E':
            self.angle = np.deg2rad(90)
        else:
            self.angle = 0
        # self.get_path()

    def init_loc(self, init_d):

        if self.start_loc == 'N':
            self.dx = -ins_size/2 - (self.lane-1)*ins_size
            self.dy = init_d
        elif self.start_loc == 'S':
            self.dx = ins_size/2 + (self.lane-1)*ins_size
            self.dy = init_d
        elif self.start_loc == 'W':
            self.dy = -ins_size/2 - (self.lane-1)*ins_size
            self.dx = init_d
        elif self.start_loc == 'E':
            self.dy = ins_size/2 + (self.lane-1)*ins_size
            self.dx = init_d



    # def init_draw(self, fig=None, ax=None):
    #
    #     if fig == None and ax == None:
    #         fig, ax = plt.subplots()
    #
    #     if self.start_loc == 'S' or self.start_loc == 'N':
    #
    #         rect = patches.Rectangle((self.dx-self.size[0]*0.5, self.dy-self.size[1]*0.5), self.size[0], self.size[1], linewidth=0, edgecolor='w', facecolor='r')
    #         ax.add_patch(rect)
    #
    #     else:
    #
    #         rect = patches.Rectangle((self.dx - self.size[1] * 0.5, self.dy - self.size[0] * 0.5), self.size[1],
    #                                  self.size[0], linewidth=0, edgecolor='w', facecolor='r')
    #         ax.add_patch(rect)
    #
    #
    # def car_draw(self, fig, ax):
    #     rect = patches.Rectangle((self.dx - self.size[0] * 0.5, self.dy - self.size[1] * 0.5), self.size[0],
    #                              self.size[1], linewidth=0, edgecolor='w', facecolor='r')
    #     ax.add_patch(rect)




    # def turn(self, mode):
    #
    #     if mode=='SE':
    #         turn_t, = np.where(abs(self.dy)<ins_size/2)
    #         turn_t = turn_t[0]
    #         print(turn_t)
    #
    #         print(self.ax)
    #         print(self.ay)
    #
    #         temp = np.copy(self.ax[turn_t:])
    #         self.ax[turn_t:] = np.copy(self.ay[turn_t:])
    #         self.ay[turn_t:] = temp
    #
    #         temp = np.copy(self.vx[turn_t:])
    #         self.vx[turn_t:] = np.copy(self.vy[turn_t:])
    #         self.vy[turn_t:] = temp
    #
    #         del temp
    #
    #         # self.ax[turn_t[0]:], self.ay[turn_t[0]:] = self.ay[turn_t[0]:], self.ax[turn_t[0]:]
    #
    #         print(self.ax)
    #         print(self.ay)
    #
    #
    #         # self.vx[turn_t[0]:], self.vy[turn_t[0]:] = self.vy[turn_t[0]:], self.vx[turn_t[0]:]
    #
    #         for i, _ in enumerate(self.vx[turn_t:len(t) - 1]):
    #             # self.vx[i + 1] = self.vx[i] + dt * self.ax[i]
    #             # self.vy[i + 1] = self.vy[i] + dt * self.ay[i]
    #
    #             self.dx[i + 1] = self.dx[i] + dt * self.vx[i]
    #             self.dy[i + 1] = self.dy[i] + dt * self.vy[i]
    #
    #         # self.vx, self.vy = self.vx, selfvy
    #         # self.dx, self.dy = x, y
    #
    #
    #     return

    def turn(self, intrs_size):

        mode = self.start_loc + self.end_loc

        if mode == 'SW' or mode == 'WS':
            r = ((self.dx+intrs_size*ins_type[0])**2 + (self.dy+intrs_size*ins_type[0])**2)**0.5
            v = (self.vx**2 + self.vy**2)**0.5
            a = v*v/r

            ax = -a * (self.dx+intrs_size*ins_type[0]) / r
            ay = -a * (self.dy+intrs_size*ins_type[0]) / r

            self.angle = np.arctan((self.dy + intrs_size*ins_type[0]) / (self.dx + intrs_size*ins_type[0]))

        elif mode == 'SE' or mode == 'ES':
            r = ((self.dx-intrs_size*ins_type[0])**2 + (-self.dy-intrs_size*ins_type[0])**2)**0.5
            v = (self.vx**2 + self.vy**2)**0.5
            a = v*v/r

            ax = a * (intrs_size*ins_type[0] - self.dx) / r
            ay = a * (-intrs_size*ins_type[0] - self.dy) / r

            self.angle = np.arctan((-intrs_size*ins_type[0] - self.dy) / (intrs_size*ins_type[0] - self.dx))

        elif mode == 'NE' or mode == 'EN':
            r = ((intrs_size*ins_type[0]-self.dx)**2 + (intrs_size*ins_type[0]-self.dy)**2)**0.5
            v = (self.vx**2 + self.vy**2)**0.5
            a = v*v/r

            ax = a * (intrs_size*ins_type[0] - self.dx) / r
            ay = a * (intrs_size*ins_type[0] - self.dy) / r

            self.angle = np.arctan((intrs_size*ins_type[0] - self.dy) / (intrs_size*ins_type[0] - self.dx))

        elif mode == 'NW' or mode == 'WN':
            r = ((-intrs_size*ins_type[0]-self.dx)**2 + (intrs_size*ins_type[0]-self.dy)**2)**0.5
            v = (self.vx**2 + self.vy**2)**0.5
            a = v*v/r

            ax = a * (-intrs_size*ins_type[0] - self.dx) / r
            ay = a * (intrs_size*ins_type[0] - self.dy) / r

            self.angle = np.arctan((intrs_size*ins_type[0] - self.dy) / (-intrs_size*ins_type[0] - self.dx))

        self.dx = self.dx + dt * self.vx
        self.dy = self.dy + dt * self.vy

        self.vx = self.vx + dt * ax
        self.vy = self.vy + dt * ay



    def get_next_vd(self, a, intrs_size):

        if self.turning and self.intersection and not self.passed:
            self.turn(intrs_size)

        else:
            self.dx = self.dx + dt * self.vx
            self.dy = self.dy + dt * self.vy

            self.vx = self.vx + dt * a[0]
            self.vy = self.vy + dt * a[1]


        if self.passed:

            self.turning = False

            if self.end_loc == 'W':

                self.angle = np.deg2rad(90)
                self.dy = intrs_size/2 + intrs_size * (self.lane - 1)
                self.vy = 0

            elif self.end_loc == 'E':

                self.angle = np.deg2rad(-90)
                self.dy = -intrs_size/2 - intrs_size * (self.lane - 1)
                self.vy = 0

            elif self.end_loc == 'N':

                self.angle = 0
                self.dx = intrs_size/2 + intrs_size * (self.lane - 1)
                self.vx = 0

            elif self.end_loc == 'S':
                self.angle = 0
                self.dx = -intrs_size / 2 - intrs_size * (self.lane - 1)
                self.vx = 0


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

        # if abs(self.dx) < size and abs(self.dy) < size:
        #     self.map = True
        # else:
        #     self.map = False

    # def check_map_init(self):
    #     if abs(self.dx) < size and abs(self.dy) < size:
    #         self.map = True
    #     else:
    #         self.map = False

    def check_map(self, i):
        # print(self.map, self.dy, self.dx)
        # print(not self.map and abs(self.dx) < size and abs(self.dy) < size)
        if not self.map and abs(self.dx) < size and abs(self.dy) < size: ## enter map
            self.map = True
            self.map_enter = i
            self.get_fastest_travel_time()
            print(f'car{self.id} enters the map')
        elif self.map and (abs(self.dx) > size or abs(self.dy) > size): ## leave map
            self.map = False
            self.map_leave = i
            self.actual_travel_time = (self.map_leave - self.map_enter) * dt
            print(f'actual travel time of car{self.id}: {self.actual_travel_time}')
            print(f'optimal travel time of car{self.id}: {self.optimal_travel_time}')
            print(f'delay of car{self.id}: {self.actual_travel_time - self.optimal_travel_time}')

    def get_fastest_travel_time(self):
        d1 = (size - ins_size * ins_type[0])
        if self.turntype:
            if self.left:
                remain_dist = ((size - ins_size * ins_type[0])) + (ins_size * ins_type[0] + car_size[0]/2)**2 * pi /4
            elif self.right:
                remain_dist = ((size - ins_size * ins_type[0])) + (car_size[0]/2)**2 * pi /4
        else:
            remain_dist = 2 * size - d1

        # tm = abs(v_intersection - abs(self.vy) - abs(self.vx)) / max_a
        # self.optimal_travel_time = (remain_dist - 0.5 * tm * (v_intersection + abs(self.vx) + abs(self.vy)))/v_intersection + tm
        vm = ((2*d1*max_a + self.vx**2 + self.vy**2 + v_intersection**2)/2)**0.5
        t1 = (vm - abs(self.vy) - abs(self.vx)) / max_a
        tm = t1 + (vm - v_intersection) / max_a
        self.optimal_travel_time = v_intersection / remain_dist + tm







    def get_path(self):
        vx = np.zeros(len(t))
        vy = np.zeros(len(t))

        x = np.zeros(len(t))
        y = np.zeros(len(t))

        vx[0], vy[0] = self.vx, self.vy
        x[0], y[0] = self.dx, self.dy


        for i,_ in enumerate(vx[:len(t)-1]):
            vx[i+1] = vx[i] + dt * self.ax[i]
            vy[i+1] = vy[i] + dt * self.ay[i]

            x[i+1] = x[i] + dt * vx[i]
            y[i+1] = y[i] + dt * vy[i]

        self.vx, self.vy = vx, vy
        self.dx, self.dy = x, y





