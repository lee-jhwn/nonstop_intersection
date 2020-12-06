import numpy as np
import cvxpy as cp
from config import *


def get_match_acc_cvnx(car, signal, i):

    if car.start_loc == 'S':
        t = (-ins_size*ins_type[0] - signal.dy) / signal.vy
        t_idx = int(t / dt)

        a = cp.Variable(t_idx)
        v = cp.Variable(t_idx)
        d = cp.Variable(t_idx)

        objective = cp.Minimize(cp.sum_squares(a[:t_idx-1]-a[1:]) + (car.ay[i-1]-a[0])**2 +(car.ay[i+t_idx+1]-a[-1])**2)
        constraints = [a <= max_a, a >= -max_a, v[0] == car.vy, d[0] == car.dy, v[-1] == signal.vy, d[-1] == -ins_size*ins_type[0]-car.size[1]/2]#, v>=0]

        for j in range(t_idx-1):
            constraints.append(v[j+1] == v[j] + a[j]*dt)
            constraints.append(d[j+1] == d[j] + v[j]*dt)

        prob = cp.Problem(objective, constraints)
        prob.solve()
        if a.value is not None:
            car.ay[i:i+t_idx] = a.value
            return True
        else:
            return False

    elif car.start_loc == 'N':

        t = (ins_size*ins_type[0] - signal.dy) / signal.vy
        t_idx = int(t / dt)

        a = cp.Variable(t_idx)
        v = cp.Variable(t_idx)
        d = cp.Variable(t_idx)

        objective = cp.Minimize(cp.sum_squares(a[:t_idx-1]-a[1:]) + (car.ay[i-1]-a[0])**2 +(car.ay[i+t_idx+1]-a[-1])**2)
        constraints = [a <= max_a, a >= -max_a, v[0] == car.vy, d[0] == car.dy, v[-1] == signal.vy, d[-1] == ins_size*ins_type[0]+car.size[1]/2]#, v<=0]

        for j in range(t_idx-1):
            constraints.append(v[j+1] == v[j] + a[j]*dt)
            constraints.append(d[j+1] == d[j] + v[j]*dt)

        prob = cp.Problem(objective, constraints)
        prob.solve()
        if a.value is not None:
            car.ay[i:i+t_idx] = a.value
            return True
        else:
            return False

    elif car.start_loc == 'E':

        t = (ins_size*ins_type[0] - signal.dx) / signal.vx
        t_idx = int(t / dt)

        a = cp.Variable(t_idx)
        v = cp.Variable(t_idx)
        d = cp.Variable(t_idx)

        objective = cp.Minimize(cp.sum_squares(a[:t_idx-1]-a[1:]) + (car.ay[i-1]-a[0])**2 +(car.ay[i+t_idx+1]-a[-1])**2)
        constraints = [a <= max_a, a >= -max_a, v[0] == car.vx, d[0] == car.dx, v[-1] == signal.vx, d[-1] == ins_size*ins_type[0]+car.size[1]/2]#, v<=0]

        for j in range(t_idx-1):
            constraints.append(v[j+1] == v[j] + a[j]*dt)
            constraints.append(d[j+1] == d[j] + v[j]*dt)

        prob = cp.Problem(objective, constraints)
        prob.solve()
        if a.value is not None:
            car.ax[i:i+t_idx] = a.value
            return True
        else:
            return False
        # print(a.value)

    elif car.start_loc == 'W':

        t = (-ins_size*ins_type[0] - signal.dx) / signal.vx
        t_idx = int(t / dt)

        a = cp.Variable(t_idx)
        v = cp.Variable(t_idx)
        d = cp.Variable(t_idx)

        objective = cp.Minimize(cp.sum_squares(a[:t_idx-1]-a[1:]) + (car.ay[i-1]-a[0])**2 +(car.ay[i+t_idx+1]-a[-1])**2)
        constraints = [a <= max_a, a >= -max_a, v[0] == car.vx, d[0] == car.dx, v[-1] == signal.vx, d[-1] == -ins_size*ins_type[0]-car.size[1]/2]#, v>=0]

        for j in range(t_idx-1):
            constraints.append(v[j+1] == v[j] + a[j]*dt)
            constraints.append(d[j+1] == d[j] + v[j]*dt)

        prob = cp.Problem(objective, constraints)
        prob.solve()
        if a.value is not None:
            car.ax[i:i+t_idx] = a.value
            return True
        else:
            return False

def get_match_acc(car, signal, i):

    if car.start_loc == 'S':




        pass

    #s = c + 2*a*m - a*(t-m), 0.5*(c + c+ a*m)*m + 0.5*(c+a*m+s)*(t-m) = s*t+d, find t, m


    # if car.start_loc == 'S':
    #
    #     # tm = (-2*car.vy + 2*signal.vy + (2*(2*max_a*(signal.dy - car.dy) + (car.vy - signal.vy)**2))**0.5 ) / (2*max_a)
    #     # t = (-car.vy + signal.vy + (2*(2*max_a*(signal.dy - car.dy) + (car.vy - signal.vy)**2))**0.5 ) / (2*max_a)
    #
    #     t = ((24*max_a*(signal.dy-car.dy)+13*(car.vy - signal.vy)**2)**0.5 -3*car.vy + 3*signal.vy )/(2*max_a)
    #     tm = ((24*max_a*(signal.dy-car.dy)+13*(car.vy - signal.vy)**2)**0.5 -5*car.vy + 5*signal.vy )/(6*max_a)
    #
    #     tm_idx = int(tm/dt)
    #     t_idx = int(t/dt)
    #
    #     car.ay[i:i+tm_idx] = max_a
    #     car.ay[i+tm_idx:i+t_idx] = -max_a
    #
    # elif car.start_loc == 'N':
    #     t = ((24 * -max_a * (signal.dy - car.dy) + 13 * (
    #                 car.vy - signal.vy) ** 2) ** 0.5 - 3 * -car.vy + 3 * -signal.vy) / (2 * max_a)
    #     tm = ((24 * -max_a * (signal.dy - car.dy) + 13 * (
    #                 car.vy - signal.vy) ** 2) ** 0.5 - 5 * -car.vy + 5 * -signal.vy) / (6 * max_a)
    #
    #     tm_idx = int(tm / dt)
    #     t_idx = int(t / dt)
    #
    #     car.ay[i:i + tm_idx] = -max_a
    #     car.ay[i + tm_idx:i + t_idx] = max_a
    #
    # elif car.start_loc == 'E':
    #     t = ((24 * -max_a * (signal.dx - car.dx) + 13 * (
    #                 car.vx - signal.vx) ** 2) ** 0.5 - 3 * -car.vx + 3 * -signal.vx) / (2 * max_a)
    #     tm = ((24 * -max_a * (signal.dx - car.dx) + 13 * (
    #                 car.vx - signal.vx) ** 2) ** 0.5 - 5 * -car.vx + 5 * -signal.vx) / (6 * max_a)
    #
    #     tm_idx = int(tm / dt)
    #     t_idx = int(t / dt)
    #
    #     car.ax[i:i + tm_idx] = -max_a
    #     car.ax[i + tm_idx:i + t_idx] = max_a
    #
    # elif car.start_loc == 'W':
    #     t = ((24 * max_a * (signal.dx - car.dx) + 13 * (
    #                 car.vx - signal.vx) ** 2) ** 0.5 - 3 * car.vx + 3 * signal.vx) / (2 * max_a)
    #     tm = ((24 * max_a * (signal.dx - car.dx) + 13 * (
    #                 car.vx - signal.vx) ** 2) ** 0.5 - 5 * car.vx + 5 * signal.vx) / (6 * max_a)
    #
    #     tm_idx = int(tm / dt)
    #     t_idx = int(t / dt)
    #
    #     car.ax[i:i + tm_idx] = max_a
    #     car.ax[i + tm_idx:i + t_idx] = -max_a

    return

if __name__=='__main__':

    x = cp.Variable()
