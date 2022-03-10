"""
This module is private and contains the definitions of classes and exceptions
used in this package to interact with the FRED API.
"""
import sqlite3
from sqlite3 import Error
from model import *
from api import *

__database_conf = {'tables': ['Category', 'Series', 'Observable'],
                   'attributes': {'Category': [('id', 'INTEGER PRIMARY KEY'),
                                               ('name', 'TEXT NOT NULL'),
                                               ('parent_id', 'INTEGER REFERENCES Category(id) '
                                                             'ON DELETE CASCADE ON UPDATE CASCADE'),
                                               ('is_leaf', 'INTEGER'),
                                               ],
                                  'Series': [('id', 'TEXT PRIMARY KEY'),
                                             ('title', 'TEXT NOT NULL'),
                                             ('category_id', 'INTEGER REFERENCES Category(id) '
                                                             'ON DELETE CASCADE ON UPDATE CASCADE')],
                                  'Observable': [('id', 'INTEGER PRIMARY KEY AUTOINCREMENT'),
                                                 ('date', 'TEXT NOT NULL'),
                                                 ('value', 'INTEGER'),
                                                 ('series_id', 'INTEGER REFERENCES Series(id) '
                                                               'ON DELETE CASCADE ON UPDATE CASCADE')]}
                   }


def _read_creation_conf() -> str:
    """
    Reads the database configuration entries to build a
    database query
    :return: a database query
    """
    tables = __database_conf['tables']
    creation_query = ""
    for i in range(len(tables)):
        first_time = True
        query = "CREATE TABLE IF NOT EXISTS "
        attrs = __database_conf['attributes'][tables[i]]
        query += tables[i] + "("
        for a in attrs:
            if not first_time:
                query += ","
            query += a[0] + " " + a[1]
            first_time = False
        query += ");"
        creation_query += query
        creation_query += " "
    return creation_query


class DatabaseManager:
    """
    This is a class to interact with the database of the package
    """

    def __init__(self, db_name: str):
        self.conn = None
        if self.conn is None:
            if db_name.endswith(".db"):
                self.db_name = db_name
            else:
                self.db_name = db_name + ".db"
            self.conn = sqlite3.connect(self.db_name)
            self.conn.execute('pragma journal_mode=wal')
            # create tables in the database configuration
            cur = self.conn.cursor()
            queries = _read_creation_conf().split(";")
            for q in queries:
                cur.execute(q)
                self.conn.commit()

    def insert_category(self, category: Category):
        """
        insert a new Category in the database
        :param category: the category to insert
        :return: None
        """
        insert_category_query = "REPLACE INTO Category VALUES(?,?,?,?)"
        values = [category.cat_id, category.name]
        if category.parent_id is not None:
            values.append(category.parent_id)
        else:
            values.append(None)
        values.append(category.leaf)
        try:
            cur = self.conn.cursor()
            cur.execute(insert_category_query, values)
            self.conn.commit()
        except Error as e:
            print(e)

    def insert_series(self, series: Series):
        """
        insert a new Series object in the database
        :param series: the series to insert
        :return: None
        """
        insert_series_query = "REPLACE INTO Series VALUES(?,?,?)"
        values = [series.series_id, series.title, series.category_id]
        try:
            cur = self.conn.cursor()
            cur.execute(insert_series_query, values)
            self.conn.commit()
        except Error as e:
            print(e)

    def insert_observable(self, observable: Observable):
        """
        insert a new Observable object in the database
        :param observable: the observable to insert
        :return: None
        """
        insert_observable_query = "REPLACE INTO Observable VALUES(?,?,?)"
        values = [observable.date, observable.value, observable.series]
        try:
            cur = self.conn.cursor()
            cur.execute(insert_observable_query, values)
            self.conn.commit()
        except Error as e:
            print(e)

    def get_subcategories(self, category_id) -> [Category]:
        """
        get a list of children for the given category
        :param category_id: the id of the category whose children are to be retrieved
        :return: list of Category type children
        """
        get_subcategory_query = "SELECT * FROM Category WHERE parent_id=?"
        sub = []
        try:
            cur = self.conn.cursor()
            cur.execute(get_subcategory_query, [category_id])
            columns = [col[0] for col in cur.description]
            sub = [dict(zip(columns, row)) for row in cur.fetchall()]
        except Error as e:
            print(e)
        return sub

    def get_series_list(self, category_id) -> [Series]:
        """
        get a list of series of a given category
        :param category_id: the given category
        :return: list of Series
        """
        get_series_list_query = "SELECT * FROM Series WHERE category_id=?"
        series_list = []
        try:
            cur = self.conn.cursor()
            cur.execute(get_series_list_query, [category_id])
            columns = [col[0] for col in cur.description]
            series_list = [dict(zip(columns, row)) for row in cur.fetchall()]
        except Error as e:
            print(e)
        return series_list

    def get_observable_list(self, series_id) -> [Observable]:
        """
        get a list of observables of a given series
        :param series_id: the given series
        :return: list of Observable
        """
        get_observables_query = "SELECT *  FROM Observable WHERE series_id=?"
        observables = []
        try:
            cur = self.conn.cursor()
            cur.execute(get_observables_query, [series_id])
            columns = [col[0] for col in cur.description]
            observables = [dict(zip(columns, row)) for row in cur.fetchall()]
        except Error as e:
            print(e)
        return observables

    def get_series(self, series_id) -> Series:
        """
        get the series with the specified id in the database
        :param series_id: series id
        :return: a Series object
        """
        get_series_query = "SELECT * FROM Series WHERE series_id=?"
        series = []
        try:
            cur = self.conn.cursor()
            cur.execute(get_series_query, [series_id])
            columns = [col[0] for col in cur.description]
            series = [dict(zip(columns, row)) for row in cur.fetchall()]
        except Error as e:
            print(e)
        return series

    def update_category(self, category: Category):
        """
        update the category specified in the database
        :param category: the new state of the Category
        :return: None
        """
        update_category_query = "UPDATE Category SET name=?, parent_id=?, is_leaf=? where id=?"
        values = [category.name, category.parent_id, category.leaf, category.cat_id]
        try:
            c = self.conn.cursor()
            c.execute(update_category_query, values)
            self.conn.commit()
        except Error as e:
            print(e)

    def update_series(self, series: Series):
        """
        update the series specified in the database
        :param series: the new state of the Series
        :return: None
        """
        update_series_query = "UPDATE Series SET title=?, category_id=? where id=?"
        values = [series.title, series.category_id, series.series_id]
        try:
            cur = self.conn.cursor()
            cur.execute(update_series_query, values)
            self.conn.commit()
        except Error as e:
            print(e)

    def update_observable(self, observable: Observable):
        """
        update the observable specified in the database
        :param observable: the new state of the Observable
        :return: None
        """
        update_observable_query = "UPDATE Observable SET date=?, value=?, series_id=? where id=?"
        values = [observable.date, observable.value, observable.series, observable.observable_id]
        try:
            cur = self.conn.cursor()
            cur.execute(update_observable_query, values)
            self.conn.commit()
        except Error as e:
            print(e)

    def check_in_database(self, model_type: ClassType, attribute) -> int:
        """
        checks if a certain instance with the given attributes is already present
        into the database. This is used to check if an object is to be retrieved from the FRED api
        or not (see more on documentation)
        :param model_type: the type of the object to check
        :param attribute: the attributes of the object
        :return: the number of elements present in the database. If 0, then the object is not present.
        """
        ret = None
        if model_type is ClassType.CATEGORY:
            ret = self.get_subcategories(attribute)
        elif model_type is ClassType.SERIES:
            ret = self.get_series_list(attribute)
        elif model_type is ClassType.OBSERVABLE:
            ret = self.get_observable_list(attribute)
        return len(ret) != 0

