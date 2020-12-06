import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint

def get_mean_delay(filename, type='all'):
    data = pd.read_csv(filename)
    # print(data)

    for s in data.columns.values[3].split():
        try:
            traffic = float(s)
        except:
            pass
    data = pd.read_csv(filename, skiprows=1)
    # print(data)


    traffic = int(traffic)
    # print(traffic)
    # print(data['delay'])
    # data = data['delay']
    # print(data)
    data = data.dropna() #.iloc[1:]
    # print(data)
    if type != 'all':
        data = data[data['lane']==type]
        # data = data[data.iloc[:,0]==type]
        print(data)
    data = data.iloc[:,-1].astype('float64')
    # print(data.mean())

    return traffic, data.mean()

def draw_graph(input, filename, patterns, type='all'):

    # p = 'I'
    for i, line in enumerate(input):
        x = [d[0] for d in line]
        y = [d[1] for d in line]

        if patterns[i]:
            plt.plot(x,y, 's--', label=f'Pattern {patterns[i]}')
        else:
            plt.plot(x,y, 's--', label=f'baseline')
        # p = p + 'I'
        # print(p)
    if type == 'all':
        plt.title('Average Delay of Vehicles', fontsize=16)
    elif type == 'left':
        plt.title('Average Delay of Vehicles (left turn)', fontsize=14)
    elif type == 'straight':
        plt.title('Average Delay of Vehicles (no turn)', fontsize=14)

    plt.xlabel('Traffics (vehicles per hour)')
    plt.ylabel('Delay time (seconds)')
    plt.legend(loc='upper left')
    plt.savefig(filename)
    plt.close()
    plt.clf()
    # plt.show()




#################### main ######################
def main(intersection_size, type, patterns):
    file_names = []
    stats = []


    for p in patterns:
        temp = []
        for j in ['1','25','5','75']:
            file = f'./delay_log/delay_log_[{intersection_size}, {intersection_size}]_{p}_0.{j}.csv'
            # print(file)
            # file_names.append(file)
            temp.append(get_mean_delay(file, type=type))
        stats.append(temp)

    pprint(stats)

    draw_graph(stats, f'./delay_log/plots/{intersection_size}-{type}.png', patterns=patterns, type=type)

    # print(file_names)


    # get_mean_delay('P1T01.csv')

    return

if __name__ == '__main__':

    patterns = {
        1: [0, 11, 12, 13],
        2: [0, 21,22,23,24,25,26],
        3: [0, 31,32]
    }

    for n in range(3):
        for t in ['all', 'left', 'straight']:
            main(intersection_size=n+1, type=t, patterns=patterns[n+1])


    # main(intersection_size=3, type='all', patterns=[0,31,32])
    # main(intersection_size=3, type='left', patterns=[0,31,32])
    # main(intersection_size=3, type='straight', patterns=[0,31,32])