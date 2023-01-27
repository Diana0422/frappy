import sys
from pprint import pprint

from frappy.api import *
from frappy import *
from frappy.__core import DatabaseManager
from frappy.graph import Graphs

if __name__ == '__main__':

    f_api = FredApiManager("e5889c59144fa74e5235e15a0d1037ff")
    dbm = DatabaseManager('frappy.db')
    # root = Category(0, "root", None, None, None, None)
    root = Category(154, "Missouri", None, None, None, None)

    # get category tree
    categories = []
    t0 = time.time()
    print("STAMPA CATEGORIE")
    categories += f_api.req_cat_start(root, 0)
    print(time.time()-t0)
    series = []
    obs = []

    # get SERIES - OK
    t0 = time.time()
    print("STAMPA SERIES")
    for i in categories:
        if i.n_series != 0:
            series.append(f_api.request_series(i, False))
    print(time.time()-t0)

    # get OBSERVABLES
    t0 = time.time()
    print("STAMPA OBSERVABLES")
    count = 0
    for i in series:
        obs.append([])
        for j in i:
            if j.n_observables != 0:
                obs[count].append(f_api.request_observables(j, False))
        count += 1
    f_api.dbm.close_db()
    print(time.time()-t0)

    # GRAPHS
    first_list = obs[4][0]
    second_list = obs[4][1]
    third_list = obs[4][2]
    data_to_plot = [first_list, second_list, third_list]
    print(data_to_plot)

    # INIZIO TEST stats.py

    print("time series")
    graphs = Graphs(data_to_plot)
    graphs.plot_series()
    graphs.plot_moving_average(5, False)
    graphs.plot_linear_regression()
    sys.exit()





