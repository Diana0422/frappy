import sys

from .core import *
import numpy as np

from .model import Observable


def interpolate_data(data_buffer: [[str, float]]) -> [[str, float]]:
    """
    Interpolate data when NaN(s) occurs\n
    :param data_buffer: list of data lists\n
    :return: interpolated data\n
    """
    i = 0
    si = []
    sk = []

    types = [int, float]
    while type(data_buffer[0][1]) not in types:
        # remove None data at the beginning
        data_buffer.pop(0)

    length = len(data_buffer)
    while type(data_buffer[length - 1][1]) not in types:
        # remove None data at the end
        data_buffer.pop(length - 1)
        length -= 1

    for data in data_buffer:
        if type(data[1]) not in types:
            # if the next value is not None, get it as the upper bridge value
            if type(data_buffer[i - 1][1]) in types:
                si.append([data_buffer[i - 1][1], i - 1])
            if i != len(data_buffer):
                try:
                    if type(data_buffer[i + 1][1]) in types:
                        sk.append([data_buffer[i + 1][1], i + 1])
                except IndexError:
                    pass
        i += 1

    i = 0
    j = 1
    k = 0
    for data in data_buffer:
        if type(data[1]) not in types:
            data[1] = si[k][0] + j * (sk[k][0] - si[k][0]) / (sk[k][1] - si[k][1])
            if type(data_buffer[i + 1][1]) not in types:
                j += 1
            else:
                k += 1
                j = 1
        i += 1
    return data_buffer


class Stats:
    """
    a class that implements some statistic methods to work with FRED data\n
    """

    def __init__(self):
        self.data_dict = {}
        self.titles_map = {}
        self.number_of_series = 0
        self.dbm = DatabaseManager('frappy.db')

    def parse_to_dict(self, dataset_list: [[Observable]]) -> dict:
        """
        add the specified dataset to the dictionary of series to study\n
        :param dataset_list: data added to the workflow\n
        :return: None\n
        """
        total = {}
        index = 0
        obs = None

        for dataset in dataset_list:
            data_buffer = []
            for data in dataset:
                try:
                    value = float(data.value)
                except ValueError:
                    value = None
                data_buffer.append([data.date, value])
            total[data.series] = data_buffer
            index += 1
            data_buffer.append([data.date, value])
            obs = data
            self.data_dict[data.series] = data_buffer
            self._map_position(self.number_of_series, data.series)
            self.number_of_series += 1
        return self.data_dict

    def _map_position(self, index, series_title):
        """
        map the position of the series data in the dictionary with the title of the series\n
        :param index: position\n
        :param series_title: title of the series\n
        :return: None\n
        """
        self.titles_map[index] = series_title

    def covariance(self) -> dict:
        """
        calculate the covariance between the series in the workflow\n
        :return: dictionary with the variance-covariance matrix\n
        """
        ret_data = {}
        series_titles = list(self.data_dict.keys())

        for index1 in range(len(self.data_dict)):
            dataset1 = interpolate_data(self.data_dict[series_titles[index1]])
            values1 = []
            for data in dataset1:
                values1.append(data[1])
            # check if there are multiple datasets
            if self.number_of_series > 1:
                for index2 in range(index1, len(self.data_dict)):
                    # calculate covariance only for series with same length
                    if len(self.data_dict[series_titles[index1]]) == len(self.data_dict[series_titles[index2]]):
                        if index2 == index1:
                            # same series: skip series
                            continue
                        values2 = []
                        dataset2 = interpolate_data(self.data_dict[series_titles[index2]])
                        for data in dataset2:
                            values2.append(data[1])

                        cov_mat = np.stack((values1, values2), axis=0)
                        # print(cov_mat)
                        # calculate covariance of the series
                        covariance = np.cov(cov_mat)
                        # print("covariance: {}".format(covariance))
                        ret_data[series_titles[index1] + "-" + series_titles[index2]] = covariance.tolist()
            else:
                # TODO return error
                print("error: insufficient number of series to calculate covariance")
        return ret_data

    def prime_differences(self) -> dict:
        """
        calculate the prime differences of the series in the workflow\n
        :return: dictionary with the prime differences results\n
        """
        ret_data = {}
        series_titles = list(self.data_dict.keys())
        for index in range(len(self.data_dict)):
            diffs = []
            dataset = interpolate_data(self.data_dict[series_titles[index]])
            for i in range(len(dataset) - 1):
                diff = dataset[i + 1][1] - dataset[i][1]
                diffs.append([dataset[i][0], diff])  # [data, value_diff]
            ret_data[series_titles[index]] = diffs
        return ret_data

    def percent_prime_differences(self) -> dict:
        """
        calculate the percentual prime differences of the series in the workflow\n
        :return: dictionary with the percentual prime differences results\n
        """
        ret_data = {}
        series_titles = list(self.data_dict.keys())
        for index in range(len(self.data_dict)):
            diffs = []
            dataset = interpolate_data(self.data_dict[series_titles[index]])
            print(dataset)
            for i in range(len(dataset)-1):
                try:
                    diff = (dataset[i + 1][1] - dataset[i][1]) / dataset[i][1]
                except ZeroDivisionError:
                    diff = None
                diffs.append([dataset[i][0], diff])
            ret_data[series_titles[index]] = diffs
        return ret_data

    def moving_average(self, n, interpolate) -> dict:
        """
        calculate the moving average of the series in the workflow\n
        :param n: window size\n
        :param interpolate: boolean to set the interpolation of NaN data\n
        :return: dictionary with the moving average of the series in the workflow\n
        """
        ret_data = {}
        series_titles = list(self.data_dict.keys())

        for index in range(0, len(self.data_dict)):
            window = 0
            values = []
            dataset = self.data_dict[series_titles[index]]
            date_index = 0

            # check n
            print(len(dataset))
            print(n)
            if n > len(dataset):
                #TODO exception
                print("n is too big")
                sys.exit(-1)

            if interpolate:
                dataset = interpolate_data(dataset)
            for i in range(n):
                window += dataset[i][1]
                date_index += 1

            date = dataset[i][0]
            values.append([date, window / n])
            for i in range(n, len(dataset)):
                window = window + dataset[i][1] - dataset[i - n][1]
                date_index += 1
                date = dataset[i][0]
                values.append([date, window / n])
            ret_data[series_titles[index]] = values
        return ret_data

    def linear_regression(self) -> dict:
        """
        calculate the linear regression of the series in the workflow\n
        :return: dictionary with the linear regression parameters calculated\n
        """
        ret_data = {}
        series_titles = list(self.data_dict.keys())

        for index in range(0, len(self.data_dict)):
            y_or = []
            y_lr = []
            x = []
            dates = []
            n = 0
            dataset = self.data_dict[series_titles[index]]
            for i in range(len(dataset)):
                if dataset[i][1] is None:
                    continue
                else:
                    y_or.append(dataset[i][1])
                    n += 1
                    x.append(n)
                    dates.append(dataset[i][0])

            # calculate linear regression parameters
            b1_num = 0
            b1_den = 0

            y_arr = np.array(y_or)
            x_mean = sum(x) / len(x)
            y_mean = np.average(y_arr)

            for i in range(len(x)):
                b1_num += ((x[i] - x_mean) * (y_or[i] - y_mean))
                b1_den += ((x[i] - x_mean) ** 2)

            b1 = np.around((b1_num / b1_den), 5)
            b0 = np.around((y_mean - (b1 * x_mean)), 5)

            reg_line = "y = {} + {}β".format(b0, b1)

            for i in range(len(x)):
                x_val = x[i]
                y_lr_val = b0 + b1 * x_val
                y_lr.append(y_lr_val)

            ret_data[series_titles[index]] = (b0, b1, reg_line, len(x), x, y_or, y_lr, dates)
        return ret_data

    def __str__(self):
        return "Dict: {}".format(self.data_dict) + " Indexes: {}".format(self.titles_map)
