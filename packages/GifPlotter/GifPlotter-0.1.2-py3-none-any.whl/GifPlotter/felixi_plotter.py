import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import imageio.v3 as imageio
from typing import Dict, Any


class FlexiPlotter:
    def __init__(self, payload: Dict[str, Any], dataframe: pd.DataFrame):
        """
        Initialize the class instance with the given payload and dataframe.

        :param payload: A dictionary containing the payload information.
        :param dataframe: A pandas DataFrame that represents the data.

        """
        self.payload = payload
        self.df = dataframe
        self.fig = None
        self.axes = []

    def create_figure(self):
        """
        Create a figure with the specified size and layout.

        :return: None
        """
        fig_size = self.payload.get('figure_size', (16, 12))
        self.fig, self.axes = plt.subplots(nrows=len(self.payload['layout']),
                                           ncols=max(len(row) for row in self.payload['layout']),
                                           figsize=fig_size)
        self.fig.tight_layout(pad=3.0)  # Adjust padding as needed

    def arrange_plots(self, num_rows):
        """

        :param num_rows: The number of rows in the plot grid.
        :return: None

        This method arranges plots in a grid based on the specified number of rows. It takes a parameter `num_rows` indicating the desired number of rows in the grid. It internally uses the `payload` attribute of the object to access the plot data.

        The method iterates over the plot data and calculates the row and column positions for each plot based on the current index. If the `layout` attribute of the object has a length greater than 1, it uses a 2D array of axes to position the plots, otherwise it uses a 1D array. The `plot_data` method is called to plot each plot on the corresponding axis.

        After plotting all the plots, any unused subplots are hidden by setting their axis to 'off'. This is done by iterating over the range from the length of the plot data to the total number of axes in the grid, and calculating the row and column positions for each subplot based on the current index.

        Example usage:
            obj = MyClass()
            obj.arrange_plots(3)  # Arranges the plots in a grid with 3 rows

        """
        plot_data = self.payload['plots']

        for i, plot_info in enumerate(plot_data):
            row = i // len(self.axes[0])
            col = i % len(self.axes[0])
            ax = self.axes[row][col] if len(self.payload['layout']) > 1 else self.axes[col]
            self.plot_data(ax, plot_info, num_rows)

        # Hide unused subplots
        for i in range(len(plot_data), self.axes.size):
            row = i // len(self.axes[0])
            col = i % len(self.axes[0])
            ax = self.axes[row][col] if len(self.payload['layout']) > 1 else self.axes[col]
            ax.axis('off')

    def plot_data(self, ax: plt.Axes, plot_info: Dict[str, Any], num_rows: int):
        """
        Method to plot data on a given axes.

        :param ax: The matplotlib axes to plot the data on.
        :param plot_info: A dictionary containing information about the plot. It should have the following keys:
            - 'type': The type of plot to be created. Can be 'line', 'scatter', or 'bar'.
            - 'x': The column in the dataframe to be used as the x-axis.
            - 'y': The column in the dataframe to be used as the y-axis.
            - 'color' (optional): The color of the plot. If not provided, a default color is used.
            - 'title' (optional): The title of the plot. If not provided, no title is set.
            - 'xlabel' (optional): The label for the x-axis. If not provided, the x-column name is used.
            - 'ylabel' (optional): The label for the y-axis. If not provided, the y-column name is used.
        :param num_rows: The number of rows to be plotted from the dataframe.
        :return: None
        """
        plot_type = plot_info['type']
        x_col = plot_info['x']
        y_col = plot_info['y']
        color = plot_info.get('color', None)

        if plot_type == 'line':
            ax.plot(self.df[x_col][:num_rows], self.df[y_col][:num_rows], color=color)
        elif plot_type == 'scatter':
            ax.scatter(self.df[x_col][:num_rows], self.df[y_col][:num_rows], color=color)
        elif plot_type == 'bar':
            ax.bar(self.df[x_col][:num_rows], self.df[y_col][:num_rows], color=color)

        ax.set_title(plot_info.get('title', ''))
        ax.set_xlabel(plot_info.get('xlabel', x_col))
        ax.set_ylabel(plot_info.get('ylabel', y_col))

        # Set fixed axis limits
        ax.set_xlim(self.df[x_col].min(), self.df[x_col].max())
        ax.set_ylim(self.df[y_col].min(), self.df[y_col].max())

    def create_gif(self, output_path, duration=0.5):
        """
        Create a GIF from a set of images.

        :param output_path: The path where the GIF will be saved.
        :param duration: The duration (in seconds) between each frame in the GIF. Defaults to 0.5 seconds.
        :return: None
        """
        images = []
        total_rows = len(self.df)
        step = max(1, total_rows // 20)  # Create 20 frames or less

        for num_rows in range(1, total_rows + 1, step):
            for ax in self.axes.flat:
                ax.clear()
            self.arrange_plots(num_rows)
            self.fig.tight_layout(pad=3.0)  # Reapply tight_layout for each frame

            self.fig.canvas.draw()
            image = np.array(self.fig.canvas.renderer.buffer_rgba())
            images.append(image)

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        imageio.imwrite(output_path, images, duration=duration, loop=0, format='GIF')
        print(f"GIF saved to: {output_path}")

    def generate_figure(self):
        self.create_figure()
        self.arrange_plots(len(self.df))

        if self.payload.get('save_gif', False):
            gif_path = self.payload.get('gif_path', 'output.gif')
            gif_duration = self.payload.get('gif_duration', 0.5)
            self.create_gif(gif_path, gif_duration)

        return self.fig


# Example usage:
if __name__ == "__main__":
    # Create a sample DataFrame with 100 rows
    np.random.seed(42)
    df = pd.DataFrame({
        'A': range(100),
        'B': np.random.rand(100) * 100,
        'C': np.random.rand(100) * 100,
        'D': np.random.randn(100) * 20,
        'E': np.random.randn(100) * 15,
        'F': np.random.rand(100) * 50,
        'G': np.random.rand(100) * 30
    })

    # Define the payload
    payload = {
        'figure_size': (16, 12),
        'layout': [
            [1, 1, 1],  # Three plots in the top row
            [1, 1, 1, 1]  # Four plots in the bottom row
        ],
        'plots': [
            {
                'type': 'line',
                'x': 'A',
                'y': 'B',
                'title': 'Line Plot: A vs B',
                'xlabel': 'X-axis (A)',
                'ylabel': 'Y-axis (B)',
                'color': 'red'
            },
            {
                'type': 'scatter',
                'x': 'A',
                'y': 'C',
                'title': 'Scatter Plot: A vs C',
                'xlabel': 'X-axis (A)',
                'ylabel': 'Y-axis (C)',
                'color': 'blue'
            },
            {
                'type': 'bar',
                'x': 'A',
                'y': 'D',
                'title': 'Bar Plot: A vs D',
                'xlabel': 'X-axis (A)',
                'ylabel': 'Y-axis (D)',
                'color': 'green'
            },
            {
                'type': 'line',
                'x': 'A',
                'y': 'E',
                'title': 'Line Plot: A vs E',
                'xlabel': 'X-axis (A)',
                'ylabel': 'Y-axis (E)',
                'color': 'purple'
            },
            {
                'type': 'scatter',
                'x': 'A',
                'y': 'F',
                'title': 'Scatter Plot: A vs F',
                'xlabel': 'X-axis (A)',
                'ylabel': 'Y-axis (F)',
                'color': 'orange'
            },
            {
                'type': 'bar',
                'x': 'A',
                'y': 'G',
                'title': 'Bar Plot: A vs G',
                'xlabel': 'X-axis (A)',
                'ylabel': 'Y-axis (G)',
                'color': 'brown'
            },
            {
                'type': 'line',
                'x': 'B',
                'y': 'C',
                'title': 'Line Plot: B vs C',
                'xlabel': 'X-axis (B)',
                'ylabel': 'Y-axis (C)',
                'color': 'pink'
            }
        ],
        'save_gif': True,
        'gif_path': 'output/animation.gif',
        'gif_duration': 0.1
    }

    # Create the plotter and generate the figure
    plotter = FlexiPlotter(payload, df)
    fig = plotter.generate_figure()

    # Show the final figure
    plt.show()