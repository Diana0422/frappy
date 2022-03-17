from pprint import pprint

from api import *
from frappy import *

if __name__ == '__main__':

    f_api = FredApiManager("e5889c59144fa74e5235e15a0d1037ff")
    dbm = DatabaseManager('frappy.db')
    #root = Category(0, "root", None, 0, 0)
    #root = Category(154, "Missouri", 27281, 0, 0)
    root = dbm.get_category_list()[0]
    root = Category(root["id"], root["name"], root["parent_id"], root["is_leaf"], root["n_children"], root["n_series"])
    categories = []
    categories += f_api.req_cat_start(root, 0)
    series = []
    obs=[]

    #series.append(f_api.request_series(categories[35],False))
    for i in categories:
        if i.n_series != 0:
            series.append(f_api.request_series(i, False))
    count = 0
    for i in series:
        obs.append([])
        for j in i:
            if j.n_observables != 0:
                obs[count].append(f_api.request_observables(j, False))
        count+=1
    print(obs[0][0][0])
    first_list = obs[0][0]
    second_list = obs[0][1]
    third_list = obs[0][2]
    data_to_plot = []
    data_to_plot.append(first_list)
    data_to_plot.append(second_list)
    data_to_plot.append(third_list)
    #print(data_to_plot)

    #INIZIO TEST stats.py

    data_buffer=[]
    total = {}
    index = 0

    for dataset in data_to_plot:
        data_buffer = []
        for data in dataset:
            print(data)
            try:
                value = float(data.value)
            except ValueError:
                value = None
            data_buffer.append([data.date, value])
        total[data.series] = data_buffer
        index += 1
    print(total)
    print("time series")
    graphs = Graphs(total)
    graphs.plot_series().show()
    print("moving average:")
    #avg = moving_average(total, 250, True)





