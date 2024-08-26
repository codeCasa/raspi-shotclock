import matplotlib.pyplot as plt
import json
import matplotlib.dates as mdates
from datetime import datetime

class LineGraphPlotter:
    def __init__(self, data_json, config_json):
        """
        Initialize the plotter with the provided data and configuration JSON.
        
        :param data_json: JSON object containing the data to plot along with optional colors.
        :param config_json: JSON object containing axis labels, chart title, and other configurations.
        """
        self.data = data_json
        self.config = config_json

    def plot(self, output_file):
        """
        Plot the data and save it as an SVG file.

        :param output_file: The path where the SVG file will be saved.
        """
        # Calculate the width based on the number of data points
        max_points = max(len(content['points']) for content in self.data.values())
        width_per_point = 0.2  # Adjust this to set how wide each point should be
        width = max_points * width_per_point
        height = 5  # You can adjust the height as needed

        plt.figure(figsize=(width, height))

        # Handle datetime formatting
        is_datetime = False
        if self.config.get('x_label_format') == 'datetime':
            is_datetime = True
            date_format = self.config.get('datetime_format', '%m/%d/%Y %H:%M')
        
        # Iterate over each key in the data JSON object (e.g., "Fastest", "Slowest", etc.)
        for label, content in self.data.items():
            # Extract x and y values for the current line
            x_values = [datetime.strptime(point['x'], date_format) if is_datetime else point['x'] for point in content['points']]
            y_values = [point['y'] for point in content['points']]
            
            # Use specified color or default to None
            color = content.get('color', None)

            # Plot the line with the label and optional color
            plt.plot(x_values, y_values, label=label, color=color)

        # Set axis labels and title from config JSON
        plt.xlabel(self.config.get('x_label', 'X Axis'), rotation=self.config.get('x_label_orientation', 0))
        plt.ylabel(self.config.get('y_label', 'Y Axis'), rotation=self.config.get('y_label_orientation', 0))

        # Set title location (above or below chart)
        title = self.config.get('title', 'Line Graph')
        title_loc = self.config.get('title_location', 'above')
        if title_loc == 'above':
            plt.title(title, pad=20)
        elif title_loc == 'below':
            plt.gcf().text(0.5, -0.1, title, ha='center')

        # Set custom axis limits if provided
        if 'x_min' in self.config or 'x_max' in self.config:
            plt.xlim(self.config.get('x_min'), self.config.get('x_max'))
        if 'y_min' in self.config or 'y_max' in self.config:
            plt.ylim(self.config.get('y_min'), self.config.get('y_max'))

        # Configure grid lines
        x_grid = self.config.get('x_grid', True)
        y_grid = self.config.get('y_grid', True)
        grid_color = self.config.get('grid_color', '#eaeaea')
        grid_line_style = self.config.get('grid_line_style', '--')
        grid_line_width = self.config.get('grid_line_width', 0.5)

        plt.grid(which='major', axis='both', color=grid_color, linestyle=grid_line_style, linewidth=grid_line_width)
        plt.minorticks_on()
        plt.grid(which='minor', axis='both', color=grid_color, linestyle=':', linewidth=0.2)

        # Handle X-axis date formatting and label spacing
        if is_datetime:
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(date_format))
            max_labels = self.config.get('max_x_labels', 10)
            plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
            
            # Adjust the number of labels
            if max_points > max_labels:
                interval = max(1, max_points // max_labels)
                plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=interval))

        # Show the legend
        plt.legend()

        # Save the plot as an SVG file
        plt.savefig(output_file, format='svg', bbox_inches='tight')
        plt.close()
