#!/usr/bin/env python3

import os
import logging

# PlotlyGraphDrawer
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
# PltGraphDrawer
import matplotlib.pyplot as plt
import matplotlib.dates as md


class PlotlyGraphDrawer:
    """A class for creating and managing interactive graphs using Plotly.
    It supports adding subplots, drawing line plots,
    and saving the figures in HTML or PNG format.
    """
    def __init__(self, **kwargs):
        self.logger = logging.getLogger("Graph Drawer")
        self.images_directory = kwargs.get("images_directory", os.getcwd())
        self.fig_title = kwargs.get("title")
        self.subplots_layout = kwargs.get("subplots_layout")
        self.figsize = kwargs.get("figsize", (800, 600))
        self.fig = None
        self.data = []

    def add_subplot_data(self, plot_data: list):
        self.data.append(plot_data)

    def add_line_to_subplot(self, line_data, subplot_index=-1):
        if len(self.data) == 0:
            self.logger.error("No plot data available. Please initialize with add_subplot_data() method first")
            return
        elif subplot_index > len(self.data) - 1 or subplot_index < -len(self.data):
            self.logger.error("Error: Provided subplot index is out of range. Provided: %s, Valid index range: (%s ~ %s)",
                              subplot_index, -len(self.data), len(self.data) - 1)
            return

        plot_data = self.data[subplot_index]
        if "data" not in plot_data:
            plot_data["data"] = []
        plot_data["data"].append(line_data)

    def _init_subplots(self):
        if self.subplots_layout:
            nrow, ncol = self.subplots_layout
        else:
            num_subplots = len(self.data)
            nrow, ncol = num_subplots, 1
            self.subplots_layout = (nrow, ncol)

        subplot_titles = tuple(plot_data.get("title", '') for plot_data in self.data)
        self.fig = make_subplots(rows=nrow, cols=ncol, subplot_titles=subplot_titles)

    def draw_subplot(self, plot_data, row, col):
        # create line plots
        traces = []
        for line_data in plot_data.get("data", []):
            x_data = line_data.get('x', [])
            y_data = line_data.get('y', [])
            if not x_data or not y_data:
                self.logger.warning("No plot data for %s", line_data)
                continue
            label = line_data.get("label", '')
            scatter = go.Scatter(x=x_data, y=y_data, name=label, mode="lines")
            traces.append(scatter)

        # add lines to the subplot
        for trace in traces:
            self.fig.append_trace(trace, row=row, col=col)

        yaxis_label = plot_data.get("y_label")
        if yaxis_label:
            self.fig.update_yaxes(title_text=yaxis_label, row=row, col=col)

    def draw_graph(self):
        self._init_subplots()

        for row in range(self.subplots_layout[0]):
            for col in range(self.subplots_layout[1]):
                plot_index = col * self.subplots_layout[1] + row
                self.draw_subplot(self.data[plot_index], row + 1, col + 1)

        self.fig.update_layout(
            showlegend=True,
            title_text=self.fig_title)

    def save_figure(self, file_name="test", extension="html"):
        if not os.path.exists(self.images_directory):
            os.makedirs(self.images_directory)
        file_path = os.path.join(self.images_directory, '.'.join([file_name, extension]))

        if extension == "html":
            with open(file_path, 'w') as f:
                f.write(pio.to_html(self.fig, include_plotlyjs='cdn', full_html=False))
        elif extension == "png":
            self.fig.write_image(file_path, scale=3)


class PltGraphDrawer:
    """A class for creating and managing static graphs using Matplotlib.
    It supports adding subplots, drawing line plots,
    and saving the figures in PNG format.
    """
    def __init__(self, **kwargs):
        self.logger = logging.getLogger("Graph Drawer")
        self.data = []
        self.images_directory = kwargs.get("images_directory", os.getcwd())
        self.fig_title = kwargs.get("title")
        self.subplots_layout = kwargs.get('subplots_layout')
        self.figsize = kwargs.get("figsize", (20, 16))
        self.fig = None
        self.axes = None

    def _set_figure_config(self):
        plt.rcParams["figure.figsize"] = self.figsize
        plt.rcParams["figure.titlesize"] = 20
        plt.rcParams["legend.loc"] = "upper left"
        plt.rcParams['figure.dpi'] = 100

    def _init_subplots(self):
        if self.subplots_layout:
            nrow, ncol = self.subplots_layout
        else:
            num_subplots = len(self.data)
            nrow, ncol = num_subplots, 1

        self.fig, self.axes = plt.subplots(nrow, ncol)

        if self.fig_title:
            self.fig.suptitle(self.fig_title)

    def add_line_data_to_subplot(self, line_data, subplot_index=-1):
        if len(self.data) == 0:
            self.logger.error("No plot data available. Please initialize with add_subplot_data() method first")
            return
        elif subplot_index > len(self.data) - 1 or subplot_index < -len(self.data):
            self.logger.error("Error: Provided subplot index is out of range. Provided: %s, Available: %s - %s",
                              subplot_index, -len(self.data), len(self.data) - 1)
            return

        plot_data = self.data[subplot_index]
        if "data" not in plot_data:
            plot_data["data"] = []
        plot_data["data"].append(line_data)

    def add_subplot_data(self, plot_data):
        self.data.append(plot_data)

    def set_x_axis_date_formatter(self, ax, x_date_format='%Y-%m-%d %H:%M:%S'):
        xfmt = md.DateFormatter(x_date_format)
        ax.xaxis.set_major_formatter(xfmt)

    def draw_subplot(self, ax, plot_data, x_axis_type="timestamp", x_date_format='%Y-%m-%d %H:%M:%S'):
        ax_label_exist = False
        if "title" in plot_data:
            ax.set_title(plot_data.get("title"))
        if "x_label" in plot_data:
            ax.set_xlabel(plot_data.get("x_label"))
        if "y_label" in plot_data:
            ax.set_ylabel(plot_data.get("y_label"))
        if x_axis_type == "timestamp":
            self.set_x_axis_date_formatter(ax, x_date_format)

        for line_data in plot_data.get("data", []):
            x_data = line_data.get('x', [])
            y_data = line_data.get('y', [])
            label = line_data.get("label", '')
            if label:
                ax_label_exist = True
                ax.plot(x_data, y_data, label=label)
            else:
                ax.plot(x_data, y_data)

        ax.tick_params(axis='x', rotation=25)
        ax.autoscale(enable=True)
        if ax_label_exist:
            ax.legend(bbox_to_anchor=(1, 1))

    def draw_graph(self):
        self._set_figure_config()
        self._init_subplots()
        axes_list = self.fig.axes
        for i, ax in enumerate(axes_list):
            self.draw_subplot(ax, self.data[i])

    def save_figure(self, file_name="test", extension="png"):
        self.fig.tight_layout()
        self.fig.subplots_adjust(top=0.92, wspace=0.25)
        image_path = os.path.join(self.images_directory, '.'.join([file_name, extension]))
        self.fig.savefig(image_path, bbox_inches="tight")
        plt.close(self.fig)
