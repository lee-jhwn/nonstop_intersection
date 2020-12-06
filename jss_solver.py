import numpy as np
import cvxpy as cp
from config import *
from intersection import signal
from gurobipy import *

def optimize_signals(signals):

    print('optimizaing signals....')

    tau_init(signals)

    c_max = cp.Variable()
    lamda = cp.Variable((len(signals), len(signals)))
    print(len(signals))


    objective = cp.Minimize(c_max)
    constraints = []

    for signal in signals:
        # for i,p in enumerate(signal.operation_t):
        constraints.append(c_max >= signal.operation_t[-1] + signal.delta[-1] + car_size[1]/v_intersection)

        temp = None
        for i,p in enumerate(signal.operation_t):
            if not i:
                constraints.append(p >= signal.delta[i])
                temp = p
            else:
                constraints.append(p == temp + signal.delta[i]) # delta index check
                temp = p


    for signal in signals: ## tau....???
        for _, t in enumerate(signal.tau):
            for j,v in enumerate(t):
                for k in range(v.shape[0]):

                    # print(j)
                    print(signals[j].operation_t.shape)
                    # temp =
                    print(v.shape)
                    print(v[k])
                    constraints.append(v[k] == (signal.operation_t[k] <= signals[j].operation_t[k]))
                    # if signal.operation_t[k] <= signals[j].operation_t[k]:
                    #     constraints.append(v[k] == 1)
                    # else:
                    #     constraints.append(v[k] == 0)



    prob = cp.Problem(objective, constraints)
    prob.solve()


    for signal in signals:
        signal.update_start_time()
        print(signal.start_t)

    return


def tau_init(signals):

    if ins_type[0] == 1:
        # x = cp.Variable((len(signals), 4))
        # print(x.shape)
        # tau = cp.Variable((len(signals), 4, len(signals), 4))
        # print(tau.shape)
        temp = [cp.Variable(s.operation_t.shape[0], boolean=True) for s in signals]
        for signal in signals:
            signal.tau = [temp.copy() for _ in enumerate(signal.operation_index)]
    print(signals[0].tau[1][0].shape)

    # print(lamda.shape)

def test():
    x = cp.Variable(boolean=True)
    y = cp.Variable()
    z = cp.Variable()
    # z = True

    c = []
    c.append(x == (1))


if __name__=='__main__':

    # test()
    print(cp.installed_solvers())
    signals = []

    if ins_type[0] == 1:
        for i in range(200):
            signals.append(signal(12 * i, 'SN', 12 * i))
            signals.append(signal(12 * i + 1, 'SW', 12 * i + 1))
            signals.append(signal(12 * i + 2, 'SE', 12 * i + 2))

            signals.append(signal(12 * i + 3, 'EW', 12 * i + 3))
            signals.append(signal(12 * i + 4, 'EN', 12 * i + 4))
            signals.append(signal(12 * i + 5, 'ES', 12 * i + 5))

            signals.append(signal(12 * i + 6, 'NS', 12 * i + 6))
            signals.append(signal(12 * i + 7, 'NW', 12 * i + 7))
            signals.append(signal(12 * i + 8, 'NE', 12 * i + 8))

            signals.append(signal(12 * i + 9, 'WE', 12 * i + 9))
            signals.append(signal(12 * i + 10, 'WN', 12 * i + 10))
            signals.append(signal(12 * i + 11, 'WS', 12 * i + 11))

    elif ins_type[0] == 2:
        for i in range(200):
            signals.append(signal(16 * i, 'SN', 8 * i, lane=1))
            signals.append(signal(16 * i + 1, 'SN', 8 * i, lane=2))
            signals.append(signal(16 * i + 2, 'SW', 8 * i + 1, lane=1))
            signals.append(signal(16 * i + 3, 'SE', 8 * i + 1, lane=2))

            signals.append(signal(16 * i + 4, 'EW', 8 * i + 2, lane=1))
            signals.append(signal(16 * i + 5, 'EW', 8 * i + 2, lane=2))
            signals.append(signal(16 * i + 6, 'ES', 8 * i + 3, lane=1))
            signals.append(signal(16 * i + 7, 'EN', 8 * i + 3, lane=2))

            signals.append(signal(16 * i + 8, 'NS', 8 * i + 4, lane=1))
            signals.append(signal(16 * i + 9, 'NS', 8 * i + 4, lane=2))
            signals.append(signal(16 * i + 10, 'NE', 8 * i + 5, lane=1))
            signals.append(signal(16 * i + 11, 'NW', 8 * i + 5, lane=2))

            signals.append(signal(16 * i + 12, 'WE', 8 * i + 6, lane=1))
            signals.append(signal(16 * i + 13, 'WE', 8 * i + 6, lane=2))
            signals.append(signal(16 * i + 14, 'WN', 8 * i + 7, lane=1))
            signals.append(signal(16 * i + 15, 'WS', 8 * i + 7, lane=2))

    elif ins_type[0] == 3:
        for i in range(200):
            signals.append(signal(12 * i, 'SN', 4 * i, lane=2))
            signals.append(signal(12 * i + 1, 'SW', 4 * i, lane=1))
            signals.append(signal(12 * i + 2, 'SE', 4 * i, lane=3))

            signals.append(signal(12 * i + 3, 'EW', 4 * i + 1, lane=2))
            signals.append(signal(12 * i + 4, 'EN', 4 * i + 1, lane=3))
            signals.append(signal(12 * i + 5, 'ES', 4 * i + 1, lane=1))

            signals.append(signal(12 * i + 6, 'NS', 4 * i + 2, lane=2))
            signals.append(signal(12 * i + 7, 'NW', 4 * i + 2, lane=3))
            signals.append(signal(12 * i + 8, 'NE', 4 * i + 2, lane=1))

            signals.append(signal(12 * i + 9, 'WE', 4 * i + 3, lane=2))
            signals.append(signal(12 * i + 10, 'WN', 4 * i + 3, lane=1))
            signals.append(signal(12 * i + 11, 'WS', 4 * i + 3, lane=3))

    optimize_signals(signals)