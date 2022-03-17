from frappy.stats import interpolate_data
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as io


class Graphs:
    """
    class to plot data
    """

    def __init__(self, data_to_plot):
        self.data_to_plot = data_to_plot
        self.fig = go.Figure()

    def plot_series(self):
        """
        plot a time series
        :return: figure
        """
        # check if there are multiple datasets to plot
        series_titles = list(self.data_to_plot.keys())

        for index in range(0, len(self.data_to_plot)):
            dataset = self.data_to_plot[series_titles[index]]
            inter_dataset = interpolate_data(dataset)
            inter_dataset.sort()
            df = pd.DataFrame(inter_dataset, columns=["Date", "Value"])
            self.fig.add_traces([go.Scatter(x=df['Date'], y=df['Value'], name=series_titles[index])])
            # save plot image on file
        #io.write_image(fig=self.fig, file='series_plot.png', format="png")

        return self.fig

    def plot_moving_average(self):
        """
        plot the moving average of the series
        :return: figure
        """
        series_titles = list(self.data_to_plot.keys())
        x = 0
        for index in range(0, len(self.data_to_plot)):
            array = []
            dataset = self.data_to_plot[series_titles[index]]
            for x in range(1, len(dataset) + 1):
                array.append(x)
            df = pd.DataFrame(dataset, columns=["Value"])
            self.fig.add_traces([go.Scatter(x=array, y=df['Value'], name=series_titles[index])])
            x += 1
        io.write_image(fig=self.fig, file='moving_avg_plot.png', format="png")
        return self.fig

    def plot_linear_regression(self):
        """
        plot the linear regression of the series specified
        :return: figure
        """
        series_titles = list(self.data_to_plot.keys())
        colors = px.colors.qualitative.Plotly
        for index in range(0, len(self.data_to_plot)):
            dataset = self.data_to_plot[series_titles[index]]
            # df = pd.DataFrame(dataset, columns=["Value"])
            x = [1, dataset[3]]
            y = [dataset[0], dataset[0] + dataset[1] * dataset[3]]
            self.fig.add_traces(
                [go.Scatter(x=x, y=y, name="LR-" + series_titles[index], marker=dict(color=colors[index]))])
            self.fig.add_traces([go.Scatter(x=dataset[4], y=dataset[5], name=series_titles[index],
                                            marker=dict(color=colors[index], size=1), opacity=0.3)])
        io.write_image(fig=self.fig, file='linear_regression_plot.png', format="png")
        return self.fig

