# import numpy as np
import cvxpy as cp
from config import *
from intersection import signal


# def gurobi_test(signals):
#
#     m = Model()
#
#     start_time_sum = m.addVar()
#
#     for signal in signals:
#         signal.set_operation_t(m)
#         return

def optimize_signals_gurobi(signals):
    print('optimizaing signals with gurobi ....')

    m = Model("Signal_Optimizer")

    tau_init(signals, m)
    c_max = m.addVar(vtype=GRB.CONTINUOUS, name='C_max')
    lamda = m.addVars(len(signals), len(signals), vtype=GRB.BINARY)

    for signal in signals:
        signal.set_operation_t(m)

        if signal.operation_t:

            m.addConstr(c_max >= signal.operation_t[len(signal.operation_t)-1] + signal.delta[-1] + car_size[1]/v_intersection)

            for i,p in enumerate(signal.operation_t):
                if not i:
                    # print(signal.t_ip[i])
                    # print(signal.operation_t[i], p)
                    m.addConstr(signal.operation_t[i] >= signal.t_ip[i])
                    # print(i)
                else:
                    # print(p)
                    m.addConstr(signal.operation_t[i] == signal.operation_t[i-1] + signal.t_ip[i])

    # for signal in signals:



        # for _,t in enumerate(signal.tau):
        #     for j,v in enumerate(t):
        #         for k,__ in enumerate(v):
        #             for w in range(k):
        #                 temp = (signal.operation_t[w] <= signals[j].operation_t[k])
        #                 # print(temp)
        #                 m.addConstr(v[w] == temp)

    for i,signal in enumerate(signals):
        for p, tv in enumerate(signal.tau):
            for j, s in enumerate(tv):
                for q, v in enumerate(s):
                    # m.addConstr(v == (signal.operation_t[p] <= signals[j].operation_t[q]))
                    # temp = signal.tau[p][j][q]
                    # print(temp)
                    # print(v)
                    # m.addConstr((signal.operation_t[p] <= signals[j].operation_t[q]), GRB.EQUAL, signal.tau[p][j][q])


                    if conflict_zone(signals, i, p, j, q):
                        # print('conflict')
                        try:
                            m.addConstr(signal.operation_t[p] + signal.delta[p] <= signals[j].operation_t[q] + (1-signal.tau[p][j][q])*big_num)
                            # m.addConstr(signals[j].operation_t[q] + signals[j].delta[q] <= signal.operation_t[p] + signal.tau[p][j][q]*big_num)
                        except:
                            pass

        for j, signalj in enumerate(signals):
            if same_destination(i, j, signals):
                try:
                    # print('adddddd')
                    m.addConstr(signals[j].operation_t[0] - signals[j].t_ip[0] + signals[j].travel_time - (signals[i].operation_t[0]- signals[i].t_ip[0] + signals[i].travel_time) >= 1 + big_num * (lamda[i][j] - 1))
                except:
                    pass

    for i,s1 in enumerate(signals):
        for j,s2 in enumerate(signals[i+1:]):
            if s1.operation_t and s2.operation_t:
                m.addConstr(s1.operation_t[0] + 0.3 <= s2.operation_t[0]) ### i added this.... ????????????






    # print(m.getVars())


    m.setObjective(c_max, GRB.MINIMIZE)

    m.optimize()

    # print(signals[0].operation_t[1])
    # print(c_max)

    # for v in m.getVars():
    #     print('%s %g' % (v.varName, v.x))
    # print(m.getVars())

    for signal in signals:
        signal.update_start_time()
        print(signal.start_t)


    return signals, c_max.x

def same_destination(i,j, signals):
    if i == j:
        return False

    return signals[i].type[1] == signals[j].type[1]

def conflict_zone(signals, i,p,j,q):
    if i == j: #and p == q:
        return False

    return signals[i].operation_index[p] == signals[j].operation_index[q]

    # return True


def tau_init(signals, m):

    # if ins_type[0] == 1:
        # temp = [m.addVars(len(s.operation_index), vtype=GRB.BINARY) for s in signals]
    for i,signal in enumerate(signals):
        # signal.tau = [temp.copy() for _ in enumerate(signal.operation_index)]
        signal.tau = [[m.addVars(len(s.operation_index), vtype=GRB.BINARY, name=f'tau{i}_{j}_{_[0]}') for j,s in enumerate(signals)] for _ in enumerate(signal.operation_index)] ## i,j,p,q

    # print(signals[0].tau[1][0][0])
    # print(signals[0].tau)
    # print(signals[0].tau[1][0])

    # print(lamda.shape)



if __name__=='__main__':

    # test()
    # print(cp.installed_solvers())
    signals = []

    if ins_type[0] == 1:
        for i in range(1):
            signals.append(signal(12 * i, 'SN', 12 * i))
            signals.append(signal(12 * i + 1, 'SW', 12 * i + 1))
            signals.append(signal(12 * i + 2, 'SE', 12 * i + 2))
            #
            signals.append(signal(12 * i + 3, 'EW', 12 * i + 3))
            signals.append(signal(12 * i + 4, 'EN', 12 * i + 4))
            signals.append(signal(12 * i + 5, 'ES', 12 * i + 5))
            #
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
        for i in range(1):
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

    optimize_signals_gurobi(signals)









'''

# z = None


def test(m):

    z = m.addVar(vtype=GRB.BINARY, name="z")

    return z

try:
    # Create a new model
    m = Model("mip1")

    # Create variables
    x = m.addVar(vtype=GRB.BINARY, name="x")
    y = m.addVar(vtype=GRB.BINARY, name="y")
    z = test(m)

    print(x)
    print(z)

    print(m.getVars())

    # Set objective
    m.setObjective(x + y + 2 * z, GRB.MAXIMIZE)

    # Add constraint: x + 2 y + 3 z <= 4
    m.addConstr(x + 2 * y + 3 * z <= 4, "c0")

    # Add constraint: x + y >= 1
    m.addConstr(x + y >= 1, "c1")

    # Optimize model
    m.optimize()

    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % m.objVal)

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')
    
'''
