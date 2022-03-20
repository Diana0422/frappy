import frappy.stats as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as io


class Graphs:
    """
    class to plot data
    """

    def __init__(self, data):
        self.data_original = data
        self.data_to_plot = {}
        self.stats = st.Stats()

    def prepare_data(self, data_dict):
        total = {}
        index = 0

        for dataset in data_dict:
            data_buffer = []
            for data in dataset:
                print(data)
                try:
                    value = float(data.value)
                except ValueError:
                    value = None
                data_buffer.append([data.date, value])
            total[data.series] = data_buffer
            index += 1
        self.data_original = total
        print(total)

    def plot_series(self):
        """
        plot a time series
        :return: figure
        """
        # just plot the series observables
        data = self.data_original.copy()
        self.data_to_plot = self.stats.parse_to_dict(data)

        # check if there are multiple datasets to plot
        fig = go.Figure()
        series_titles = list(self.data_to_plot.keys())

        for index in range(0, len(self.data_to_plot)):
            dataset = self.data_to_plot[series_titles[index]]
            inter_dataset = st.interpolate_data(dataset)
            inter_dataset.sort()
            df = pd.DataFrame(inter_dataset, columns=["Date", "Value"])
            fig.add_traces([go.Scatter(x=df['Date'], y=df['Value'], name=series_titles[index])])
        # save plot image on file
        fig.write_html('series_plot.html')
        return fig

    def plot_moving_average(self, step, interpolate):
        """
        plot the moving average of the series
        :return: figure
        """
        # calculate the moving avg
        self.data_to_plot = self.stats.moving_average(step, interpolate)

        # plot the results
        fig = go.Figure()
        series_titles = list(self.data_to_plot.keys())
        x = 0
        for index in range(0, len(self.data_to_plot)):
            array = []
            dataset = self.data_to_plot[series_titles[index]]
            for x in range(1, len(dataset) + 1):
                array.append(x)
            df = pd.DataFrame(dataset, columns=["Value"])
            fig.add_traces([go.Scatter(x=array, y=df['Value'], name=series_titles[index])])
            x += 1
        # save plot image on file
        fig.write_html('moving_avg_plot.html')
        return fig

    def plot_linear_regression(self):
        """
        plot the linear regression of the series specified
        :return: figure
        """
        # calculate the linear regression
        self.data_to_plot = self.stats.linear_regression()

        # plot the result
        fig = go.Figure()
        series_titles = list(self.data_to_plot.keys())
        colors = px.colors.qualitative.Plotly
        for index in range(0, len(self.data_to_plot)):
            dataset = self.data_to_plot[series_titles[index]]
            # df = pd.DataFrame(dataset, columns=["Value"])
            x = [1, dataset[3]]
            y = [dataset[0], dataset[0] + dataset[1] * dataset[3]]
            fig.add_traces(
                [go.Scatter(x=x, y=y, name="LR-" + series_titles[index], marker=dict(color=colors[index]))])
            fig.add_traces([go.Scatter(x=dataset[4], y=dataset[5], name=series_titles[index],
                                       marker=dict(color=colors[index], size=1), opacity=0.3)])
        # save plot image on file
        fig.write_html('linear_regression_plot.html')
        return fig
