from api import *
from frappy import *

if __name__ == '__main__':

    f_api = FredApiManager("e5889c59144fa74e5235e15a0d1037ff")
    #root = Category(0, "root", None, 0, 0)
    #categories = f_api.req_cat_start(root, 0)
    root = Category(154, "Missouri", 27281, 0, 0)
    categories = f_api.request_categories(root, 0)
    series = []
    #series.append(f_api.request_series(categories[35],False))
    for i in categories:
        series.append(f_api.request_series(i, False))



