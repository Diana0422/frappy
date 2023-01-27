import json
import sys
import time

import requests

from .__core import *
from .__core import DatabaseManager
from .model import ClassType, Category, object_convert, Series, Observable


class FredApiManager:
    """
    class to interact with FRED api
    """

    def __init__(self, api_key, db_path):
        self.key = api_key
        self.children_URL = "https://api.stlouisfed.org/fred/category/children?"
        self.series_URL = "https://api.stlouisfed.org/fred/category/series?"
        self.observable_URL = "https://api.stlouisfed.org/fred/series/observations?"
        self.dbm = DatabaseManager(db_path)

    def _generate_url(self, model_type, value) -> str:
        """
        private method to generate a specific URL to request to the FRED API
        :param model_type: type of model class to retrieve
        :param value: attribute needed to build the specific URL
        :return: URL string
        """
        specific_url = ""
        if model_type is ClassType.CHILD:
            specific_url = self.children_URL + "category_id=" + str(value) + "&api_key=" + self.key + "&file_type=json"
        elif model_type is ClassType.SERIES:
            specific_url = self.series_URL + "category_id=" + str(value) + "&api_key=" + self.key + "&file_type=json"
        elif model_type is ClassType.OBSERVABLE:
            specific_url = self.observable_URL + "series_id=" + str(value) + "&api_key=" + self.key + "&file_type=json"
        return specific_url

    def _generate_request(self, model_type, attribute) -> [dict]:
        """
        Private method to make a request to the FRED API
        :param model_type: type of the model class to retrieve
        :param attribute: attribute needed to make the request
        :return: array of dictionaries that represent the objects retrieved
        """
        url = self._generate_url(model_type, attribute)
        conn = requests.get(url)
        json_data = conn.text
        dict_data = json.loads(json_data)
        ret_objects = []
        if model_type is ClassType.CHILD:
            try:
                ret_objects = dict_data['categories']
            except KeyError:
                print(dict_data['error_message'])
                sys.exit()
        elif model_type is ClassType.SERIES:
            try:
                if dict_data["count"] != 0:
                    ret_objects = dict_data['seriess']
            except KeyError:
                print(dict_data['error_message'])
                sys.exit()
        elif model_type is ClassType.OBSERVABLE:
            try:
                ret_objects = dict_data['observations']
            except KeyError:
                print(dict_data['error_message'])
                sys.exit()
        return ret_objects

    def req_cat_start(self, start_category: Category, on_api):
        # check if starting category is on database
        check = self.dbm.check_in_database(ClassType.CATEGORY, start_category.cat_id)
        if not check:
            self.dbm.insert_category(start_category)
        return self.request_categories(start_category, on_api)

    def request_categories(self, start_category: Category, on_api) -> [Category]:
        """
        request the category tree starting from a category specified
        :param start_category: the starting category from which to retrieve the tree of sub-categories
        :param on_api: a boolean that if True specifies whether the categories are to be retrieved
         from the api
        :return: list of categories retrieved
        """
        nodes_to_visit = [start_category]
        ret_categories = []
        i = 0

        while len(nodes_to_visit) != 0:
            i += 1
            node = nodes_to_visit.pop(0)
            check = self.dbm.check_in_database(ClassType.CHILD, node.cat_id)
            if not check or on_api:
                if node.leaf == 0 or node.leaf is None:
                    time.sleep(1)
                    children = self._generate_request(ClassType.CHILD, node.cat_id)
                    if len(children) == 0:
                        node.leaf = 1
                        self.dbm.update_category(node)
                else:
                    children = []
            else:
                children = self.dbm.get_subcategories(node.cat_id)
            ret_categories.append(node)
            for c in children:
                if check and not on_api:
                    is_leaf = c["is_leaf"]
                    n_children = c["n_children"]
                    n_series = c["n_series"]
                else:
                    is_leaf = 0
                    n_children = None
                    n_series = None
                print(c)
                cat = Category(c["id"], c["name"], node.cat_id, is_leaf, n_children, n_series)
                # add subcategory
                node.children.append(cat)
                # add children to the list of nodes to visit
                nodes_to_visit.append(cat)
                if not check or on_api:
                    # insert category in db
                    self.dbm.insert_category(cat)

            # update the number of children of the visited node
            if not check or on_api:
                node.n_children = len(children)
                self.dbm.update_category(node)

        # renew the root element with the collected data
        root_data = self.dbm.get_category(ret_categories[0].cat_id)
        ret_categories[0] = object_convert(ClassType.CATEGORY, root_data[0])
        return ret_categories

    def request_series(self, category: Category, on_api) -> [Series]:
        """
        request the series of a specified category
        :param category: the category whose series are to be retrieved
        :param on_api: a boolean that if True specifies whether the series are to be retrieved
        from the api
        :return: the requested series list
        """
        ret_series = []
        check = self.dbm.check_in_database(ClassType.SERIES, category.cat_id)
        if on_api or not check:

            if not category.n_series:
                time.sleep(1)
                series_list = self._generate_request(ClassType.SERIES, category.cat_id)
            else:
                series_list = []
        else:
            series_list = self.dbm.get_series_list(category.cat_id)
        # create series object and save on db
        series_len = len(series_list)
        series_number = len(series_list)
        for s in series_list:
            if s['id'] is None:
                continue
            s = Series(s['id'], s['title'], category.cat_id, s['n_observables'])
            category.series_list.append(s)
            series_len -= 1
            if on_api or not check:
                # insert series in db
                do_commit = series_len == 0
                self.dbm.insert_series(s, do_commit)
            # add series to the list
            ret_series.append(s)
        category.n_series = series_number
        self.dbm.update_category(category)
        return ret_series

    def request_observables(self, series: Series, on_api) -> [Observable]:
        """
        request the observables of a specified series
        :param series: the series whose observations are to be retrieved
        :param on_api: a boolean that if True specifies whether the observables are to be retrieved
        from the api
        :return: the requested observables list
        """
        ret_observables = []
        check = self.dbm.check_in_database(ClassType.OBSERVABLE, series.series_id)
        if on_api or not check:
            if not series.n_observables:
                time.sleep(1)
                observations = self._generate_request(ClassType.OBSERVABLE, series.series_id)
                print("from API: {}".format(observations))
            else:
                observations = []
        else:
            observations = self.dbm.get_observable_list(series.series_id)
            # print("from DB: {}".format(observations))
        # create observable object and save on db
        observations_len = len(observations)
        number_obs = len(observations)
        for o in observations:
            o = Observable(0, o['date'], o['value'], series.series_id)
            series.observables.append(o)
            observations_len -= 1
            if on_api or not check:
                # insert observable in db
                do_commit = observations_len == 0
                self.dbm.insert_observable(o, do_commit)
            # add observable to the list
            ret_observables.append(o)

        # update number of series observables on database
        series.n_observables = number_obs
        self.dbm.update_series(series)
        return ret_observables
