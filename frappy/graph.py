import frappy.stats as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as io


def set_graph_layout(figure: go.Figure, template):
    """
    changes the layout of the specified figure\n
    :param figure:\n
    :param template:\n
    :return: None\n
    """
    figure.update_layout(template=template)


class Graphs:
    """
    class to plot data\n
    """

    def __init__(self, data, graph_theme, file_type):
        self.data_original = data
        self.data_to_plot = {}
        self.stats = st.Stats()
        self.template = graph_theme
        self.file_type = file_type

    def prepare_data(self, data_dict):
        """
        prepare and import in Graphs instance original data to be used in Graphs methods\n
        :param data_dict: data to prepare\n
        :return: None\n
        """
        total = {}
        index = 0

        for dataset in data_dict:
            data_buffer = []
            for data in dataset:
                try:
                    value = float(data.value)
                except ValueError:
                    value = None
                data_buffer.append([data.date, value])
            total[data.series] = data_buffer
            index += 1
        self.data_original = total

    def _save_graph_to_file(self, figure: go.Figure):
        """
        saves the input graph to a file of a certain filetype\n
        :param figure: plot to save\n
        :return: None\n
        """
        set_graph_layout(figure, self.template)
        if self.file_type == "svg":
            figure.write_image("{}.svg".format(figure.layout.title.text))
        elif self.file_type == "png":
            figure.write_image("{}.png".format(figure.layout.title.text))
        elif self.file_type == "jpg":
            figure.write_image("{}.jpg".format(figure.layout.title.text))
        elif self.file_type == "bmp":
            figure.write_image("{}.bmp".format(figure.layout.title.text))
        else:
            # default: html
            figure.write_html("{}.html".format(figure.layout.title.text))

    def print_covariance(self):
        """
        calculates covariance and prints it on screen\n
        :return: None\n
        """
        cov = self.stats.covariance()
        print("covariance: {}".format(cov))

    def plot_series(self, interpolate):
        """
        plot a time series\n
        :return: figure\n
        """
        # just plot the series observables
        data = self.data_original.copy()
        self.data_to_plot = self.stats.parse_to_dict(data)

        # check if there are multiple datasets to plot
        layout = dict(xaxis=dict(title="Date"), yaxis=dict(title="Value"), title="Series Over Time")
        fig = go.Figure(layout=layout)
        series_titles = list(self.data_to_plot.keys())

        for index in range(0, len(self.data_to_plot)):
            dataset = self.data_to_plot[series_titles[index]]
            if interpolate:
                inter_dataset = st.interpolate_data(dataset)
            else:
                inter_dataset = dataset.copy()
            inter_dataset.sort()
            df = pd.DataFrame(inter_dataset, columns=["Date", "Value"])
            data = go.Scatter(x=df['Date'], y=df['Value'], name=series_titles[index])
            fig.add_traces([data])
        # save plot image on file
        self._save_graph_to_file(fig)
        return fig

    def plot_moving_average(self, step, interpolate):
        """
        plot the moving average of the series\n
        :return: figure\n
        """
        # calculate the moving avg
        self.data_to_plot = self.stats.moving_average(step, interpolate)

        # plot the results
        layout = dict(xaxis=dict(title="Date"), yaxis=dict(title="Value"), title="Series Moving Average")
        fig = go.Figure(layout=layout)
        series_titles = list(self.data_to_plot.keys())
        x = 0
        for index in range(0, len(self.data_to_plot)):
            dataset = self.data_to_plot[series_titles[index]]
            print(dataset)
            df = pd.DataFrame(dataset, columns=["Date", "Value"])
            data = go.Scatter(x=df['Date'], y=df['Value'], name=series_titles[index])
            fig.add_traces([data])
            x += 1
        # save plot image on file
        self._save_graph_to_file(fig)
        return fig

    def plot_prime_differences(self):
        """
        plot the prime differences of the series specified\n
        :return: figure\n
        """
        # calculate the prime differences
        self.data_to_plot = self.stats.prime_differences()

        # plot the result
        layout = dict(xaxis=dict(title="Date"), yaxis=dict(title="Value"), title="Series Prime Differences")
        fig = go.Figure(layout=layout)
        series_titles = list(self.data_to_plot.keys())
        x = 0
        for index in range(0, len(self.data_to_plot)):
            dataset = self.data_to_plot[series_titles[index]]
            print(dataset)
            df = pd.DataFrame(dataset, columns=["Date", "Value"])
            data = go.Scatter(x=df['Date'], y=df['Value'], name=series_titles[index])
            fig.add_traces([data])
            x += 1
        # save plot image on file
        self._save_graph_to_file(fig)
        return fig

    def plot_prime_differences_percent(self):
        """
        plot the prime differences of the series specified\n
        :return: figure\n
        """
        # calculate the prime difference percentage
        self.data_to_plot = self.stats.percent_prime_differences()

        # plot the result
        layout = dict(xaxis=dict(title="Date"), yaxis=dict(title="Value"), title="Series Percent Prime Differences")
        fig = go.Figure(layout=layout)
        series_titles = list(self.data_to_plot.keys())
        x = 0
        for index in range(0, len(self.data_to_plot)):
            dataset = self.data_to_plot[series_titles[index]]
            df = pd.DataFrame(dataset, columns=["Date", "Value"])
            data = go.Scatter(x=df['Date'], y=df['Value'], name=series_titles[index])
            fig.add_traces([data])
            x += 1
        # save plot image on file
        self._save_graph_to_file(fig)
        return fig


    def plot_linear_regression(self):
        """
        plot the linear regression of the series specified\n
        :return: figure\n
        """
        # calculate the linear regression
        self.data_to_plot = self.stats.linear_regression()

        # plot the result
        layout = dict(xaxis=dict(title="Date"), yaxis=dict(title="Value"), title="Series Linear Regression")
        fig = go.Figure(layout=layout)
        series_titles = list(self.data_to_plot.keys())
        colors = px.colors.qualitative.Plotly
        for index in range(0, len(self.data_to_plot)):
            dataset = self.data_to_plot[series_titles[index]]
            data_table_lr = []
            data_table_or = []
            for i in range(len(dataset[6])):
                date = dataset[7][i]
                lr_value = dataset[6][i]
                or_value = dataset[5][i]
                data_table_lr.append([date, lr_value])
                data_table_or.append([date, or_value])
            df_lr = pd.DataFrame(data_table_lr, columns=["Date", "Value"])
            df_or = pd.DataFrame(data_table_or, columns=["Date", "Value"])
            data_lr = go.Scatter(x=df_lr['Date'], y=df_lr['Value'], name="LR-" + series_titles[index],
                                 marker=dict(color=colors[index]))
            data_or = go.Scatter(x=df_or['Date'], y=df_or['Value'], name=series_titles[index],
                                 marker=dict(color=colors[index], size=1), opacity=0.3)
            fig.add_traces([data_lr])
            fig.add_traces([data_or])
        # save plot image on file
        self._save_graph_to_file(fig)
        return fig
