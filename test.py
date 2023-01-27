import sys
import time
from frappy.api import FredApiManager
from frappy.graph import Graphs
from frappy.model import Category

if __name__ == '__main__':

    f_api = FredApiManager("e5889c59144fa74e5235e15a0d1037ff", './frappy.db')
    # root = Category(0, "root", None, None, None, None)
    root = Category(154, "Missouri", None, None, None, None)

    # get category tree
    categories = []
    t0 = time.time()
    categories += f_api.req_cat_start(root, 0)
    print(time.time()-t0)
    series = []
    obs = []

    # get SERIES - OK
    t0 = time.time()
    for i in categories:
        if i.n_series != 0:
            series.append(f_api.request_series(i, False))
    print(time.time()-t0)

    print(series)

    # get OBSERVABLES
    t0 = time.time()
    index = 0
    array = series[0]
    #sto prendendo TUTTE le osservabili da 16 serie relative a una categoria.
    for i in array:
        #obs.append([])
        if i.n_observables != 0:
            obs.append(f_api.request_observables(i, False))
        index += 1
        print(index)
        if index > 15:
            break
    f_api.dbm.close_db()
    print(time.time()-t0)

    # GRAPHS
    first_list = obs[10]
    second_list = obs[8]
    third_list = obs[7]
    data_to_plot = [first_list, second_list, third_list]
    print(data_to_plot)

    # INIZIO TEST stats.py

    print("time series")
    graphs = Graphs(data_to_plot, "ggplot2", "svg")
    graphs.plot_series(True)
    graphs.plot_moving_average(5, False)
    graphs.plot_linear_regression()
    sys.exit()



#possible themes: plotly_dark, plotly_white, plotly, ggplot2, seaborn, simple_white, none

