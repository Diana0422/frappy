from api import *
from frappy import *

if __name__ == '__main__':

    f_api = FredApiManager("e5889c59144fa74e5235e15a0d1037ff")
    root = Category(0, "root", None, 0)
    categories = f_api.request_categories(root, 1)
