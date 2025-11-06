import sys
from collections import deque

from PyQt5 import QtWidgets
import pyqtgraph as pg


class RealtimeGraph:

    def __init__(self, channels, window_title="Realtime Data", buffer_size=500):
        self.channels = channels
        self.buffer_size = buffer_size
        self.window_title = window_title

        # Initialize Qt application if needed
        if not QtWidgets.QApplication.instance():
            self.app = QtWidgets.QApplication(sys.argv)
        else:
            self.app = QtWidgets.QApplication.instance()

        # Create main window with layout
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setWindowTitle(window_title)
        self.layout = QtWidgets.QVBoxLayout(self.main_widget)

        # Create graph widget with multiple plots
        self.graph_widget = pg.GraphicsLayoutWidget()

        # Create individual plots for each channel
        self.plots = {}
        self.visible_channels = [ch_id for ch_id, config in self.channels.items() if config['show']]

        for i, (channel_id, config) in enumerate(self.channels.items()):
            if config['show']:
                if i > 0:
                    self.graph_widget.nextRow()
                plot = self.graph_widget.addPlot(
                    labels={'left': config['name'], 'bottom': 'Samples' if i == len(self.visible_channels)-1 else ''}
                )
                plot.showGrid(x=True, y=True, alpha=0.3)
                plot.enableAutoRange('x', True)  # Only auto-range X, we'll handle Y manually
                self.plots[channel_id] = plot

        # Create info label (generic display for computed values)
        self.info_label = QtWidgets.QLabel("--")
        self.info_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")

        # Add widgets to layout
        self.layout.addWidget(self.graph_widget)
        self.layout.addWidget(self.info_label)

        # Track if window is closed
        self.window_closed = [False]

        def on_window_close():
            self.window_closed[0] = True

        self.main_widget.closeEvent = lambda event: on_window_close()

        # Create curves and buffers for each channel
        self.channel_data = {}

        for channel_id, config in self.channels.items():
            if config['show']:
                self.channel_data[channel_id] = {
                    'curve': self.plots[channel_id].plot(pen=pg.mkPen(color=config['color'], width=2)),
                    'buffer': deque(maxlen=self.buffer_size),
                    'plot': self.plots[channel_id]
                }

    def show(self):
        self.main_widget.show()

    def is_closed(self):
        return self.window_closed[0]

    def update_data(self, channel_readings):
        # Process each channel's data for buffering
        for channel_id, data_config in self.channel_data.items():
            if channel_id in channel_readings:
                channel_value = channel_readings[channel_id]
                data_config['buffer'].append(channel_value)

        # Update curves for all channels
        for channel_id, data_config in self.channel_data.items():
            # Create x-axis that starts from 0 and matches the actual buffer length
            buffer_length = len(data_config['buffer'])
            x = list(range(buffer_length))
            buffer_data = list(data_config['buffer'])

            # Update curve
            data_config['curve'].setData(x, buffer_data)

            # Auto-scale Y axis with 10% extra space
            if buffer_data:
                y_min = min(buffer_data)
                y_max = max(buffer_data)
                y_range = y_max - y_min
                if y_range > 0:
                    y_margin = y_range * 0.1
                    data_config['plot'].setYRange(y_min - y_margin, y_max + y_margin, padding=0)
                else:
                    # Handle case where all values are the same
                    data_config['plot'].setYRange(y_min - abs(y_min) * 0.1 - 1, y_max + abs(y_max) * 0.1 + 1, padding=0)

        # Process Qt events to update the GUI
        self.app.processEvents()


    def hide_info_label(self):
        self.info_label.hide()

    def set_info_text(self, text):
        self.info_label.setText(text)
