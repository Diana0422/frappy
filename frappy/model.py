from enum import Enum


class Category:
    def __init__(self, cat_id, name, parent_id, leaf, n_children, n_series):
        self.cat_id = cat_id
        self.name = name
        self.parent_id = parent_id
        self.leaf = leaf
        self.n_children = n_children
        self.n_series = n_series
        self.children = []
        self.series_list = []

    def __str__(self):
        return "ID: " + str(self.cat_id) + " NAME: " + self.name + " parentID: " + str(self.parent_id) + " leaf: " + str(self.leaf) + " n_series: " + str(self.n_series)


class Series:
    def __init__(self, series_id, title, category_id, n_observables):
        self.series_id = series_id
        self.title = title
        self.category_id = category_id
        self.n_observables = n_observables
        self.observables = []

    def __str__(self):
        return "ID: " + str(self.series_id) + " TITLE: " + str(self.title) + " categoryID: " + str(self.category_id)


class Observable:
    def __init__(self, observable_id, date, value, series_id):
        self.observable_id = observable_id
        self.date = date
        self.value = value
        self.series = series_id

    def __str__(self):
        return "DATE: " + self.date + " VALUE: " + str(self.value) + " seriesID: " + str(self.series)


class ClassType(Enum):
    """
    enum that represents the model types
    """
    CATEGORY = 1
    SERIES = 2
    OBSERVABLE = 3
