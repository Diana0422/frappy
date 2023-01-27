import sqlite3
from sqlite3 import Error
from .model import *
from .api import *


"""
This module is private and contains the definitions of classes and exceptions
used in this package to interact with the FRED API.
"""
__database_conf = {'tables': ['Category', 'Series', 'Observable'],
                   'attributes': {'Category': [('id', 'INTEGER PRIMARY KEY'),
                                               ('name', 'TEXT NOT NULL'),
                                               ('parent_id', 'INTEGER REFERENCES Category(id) '
                                                             'ON DELETE CASCADE ON UPDATE CASCADE'),
                                               ('is_leaf', 'INTEGER'),
                                               ('n_children', 'INTEGER'),
                                               ('n_series', 'INTEGER')],
                                  'Series': [('id', 'TEXT PRIMARY KEY'),
                                             ('title', 'TEXT NOT NULL'),
                                             ('category_id', 'INTEGER REFERENCES Category(id) '
                                                             'ON DELETE CASCADE ON UPDATE CASCADE'),
                                             ('n_observables', 'INTEGER')],
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

    def commit(self):
        self.conn.commit()

    def insert_category(self, category: Category):
        """
        insert a new Category in the database
        :param category: the category to insert
        :return: None
        """
        insert_category_query = "REPLACE INTO Category (id, name, parent_id, is_leaf, n_children, n_series) VALUES(?,?,?,?,?,?)"
        values = [category.cat_id, category.name]
        # TODO probabilemte si può levare il controllo sul parent id
        if category.parent_id is not None:
            values.append(category.parent_id)
        else:
            values.append(None)
        values.append(category.leaf)
        values.append(category.n_children)
        values.append(category.n_series)
        try:
            cur = self.conn.cursor()
            cur.execute(insert_category_query, values)
            self.conn.commit()
        except Error as e:
            print(e)

    def insert_series(self, series: Series, commit_flag):
        """
        insert a new Series object in the database
        :param commit_flag:
        :param series: the series to insert
        :return: None
        """
        insert_series_query = "REPLACE INTO Series (id, title, category_id, n_observables) VALUES(?,?,?,?)"
        values = [series.series_id, series.title, series.category_id, series.n_observables]
        try:
            cur = self.conn.cursor()
            cur.execute(insert_series_query, values)
            if commit_flag == 1:
                self.conn.commit()
        except Error as e:
            print(e)

    def insert_observable(self, observable: Observable, commit_flag):
        """
        insert a new Observable object in the database
        :param observable: the observable to insert
        :return: None
        """
        insert_observable_query = "REPLACE INTO Observable(date, value, series_id) VALUES(?,?,?)"
        values = [observable.date, observable.value, observable.series]
        try:
            cur = self.conn.cursor()
            cur.execute(insert_observable_query, values)
            if commit_flag == 1:
                self.conn.commit()
        except Error as e:
            print(e)

    def get_category(self, category_id) -> Category:
        """
        retrieve a category with given id from the database
        :param category_id: the id of the category to fetch
        :return: Category object
        """
        get_category_query = "SELECT * FROM Category WHERE id=?"
        sub = []
        try:
            cur = self.conn.cursor()
            cur.execute(get_category_query, [category_id])
            columns = [col[0] for col in cur.description]
            sub = [dict(zip(columns, row)) for row in cur.fetchall()]
        except Error as e:
            print(e)
        return sub

    def get_series(self, series_id) -> Series:
        """
        retrieve a series with given id from the database
        :param series_id: the id of the series to fetch
        :return: Series object
        """
        get_series_query = "SELECT * FROM Series WHERE id=?"
        try:
            cur = self.conn.cursor()
            cur.execute(get_series_query, [series_id])
            columns = [col[0] for col in cur.description]
            sub = [dict(zip(columns, row)) for row in cur.fetchall()]
        except Error as e:
            print(e)
        return sub

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

    def get_category_list(self) -> [Category]:
        """
        get a list of categories
        :return: list of Category
        """
        get_category_list_query = "SELECT * FROM Category"
        category_list = []
        try:
            cur = self.conn.cursor()
            cur.execute(get_category_list_query)
            columns = [col[0] for col in cur.description]
            category_list = [dict(zip(columns, row)) for row in cur.fetchall()]
        except Error as e:
            print(e)
        return category_list

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

    def get_series_number(self, category_id):
        """
        get number of series of a given category
        :param category_id: the given category
        :return: number of Series integer
        """
        get_series_number_query = "SELECT n_series FROM Category WHERE id=?"
        series_number = -1
        try:
            cur = self.conn.cursor()
            cur.execute(get_series_number_query, [category_id])
            series_number = cur.fetchone()[0]
        except Error as e:
            print(e)
        return series_number

    def get_children_number(self, category_id):
        """
        get the number of children of a given category
        :param category_id:
        :return:
        """
        get_children_number_query = "SELECT n_children FROM Category WHERE id=?"
        children_number = -1
        try:
            cur = self.conn.cursor()
            cur.execute(get_children_number_query, [category_id])
            children_number = cur.fetchone()[0]
        except Error as e:
            print(e)
        return children_number

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

    def get_observables_number(self, category_id):
        """
                get number of series of a given category
                :param category_id: the given category
                :return: number of Series integer
                """
        get_observables_number_query = "SELECT n_observables FROM Series WHERE id=?"
        observables_number = -1
        try:
            cur = self.conn.cursor()
            cur.execute(get_observables_number_query, [category_id])
            observables_number = cur.fetchone()[0]
        except Error as e:
            print(e)
        return observables_number

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
        update_category_query = "UPDATE Category SET name=?, parent_id=?, is_leaf=?, n_children=?, n_series=? where id=?"
        values = [category.name, category.parent_id, category.leaf, category.n_children, category.n_series, category.cat_id]
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
        update_series_query = "UPDATE Series SET title=?, category_id=?, n_observables=? where id=?"
        values = [series.title, series.category_id, series.n_observables, series.series_id]
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
        if model_type is ClassType.CHILD:
            children = self.get_subcategories(attribute)
            n_children = self.get_children_number(attribute)
            return len(children) == n_children
        elif model_type is ClassType.CATEGORY:
            cat = self.get_category(attribute)
            return len(cat) != 0
        elif model_type is ClassType.SERIES:
            n_series = self.get_series_number(attribute)
            series_list = self.get_series_list(attribute)
            result = len(series_list) == n_series and n_series is not None
            return result
        elif model_type is ClassType.OBSERVABLE:
            obs_list = self.get_observable_list(attribute)
            n_observables = self.get_observables_number(attribute)
            return len(obs_list) == n_observables and n_observables is not None

    def close_db(self):
        """
        procedure to close the database connection
        :return:
        """
        self.conn.close()

