import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from collections import deque

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Real-time Plotting with PySide6")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a Figure
        self.figure = Figure()

        # Create a Canvas and add the Figure to it
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Initialize input fields
        self.rx_ber_current_frame_le = QLineEdit(self)
        self.rx_ber_num_le = QLineEdit(self)
        self.rx_ber_le = QLineEdit(self)
        layout.addWidget(self.rx_ber_current_frame_le)
        layout.addWidget(self.rx_ber_num_le)
        layout.addWidget(self.rx_ber_le)

        # Create a subplot
        self.ax = self.figure.add_subplot(111)

        # Initialize the data line and average line
        self.line, = self.ax.semilogy([], [], 'r', label='Data')
        self.avg_line, = self.ax.semilogy([], [], 'b--', label='Average')

        # Set the y-axis limits
        self.ax.set_ylim(1e-10, 1)

        # Add a button to clear the plot
        self.clear_button = QPushButton("Clear Plot")
        layout.addWidget(self.clear_button)
        self.clear_button.clicked.connect(self.clear_plot)

        # Draw the canvas
        self.canvas.draw()

        # Data storage
        self.window_size = 100  # Size of the rolling window
        self.counts = deque(maxlen=self.window_size)
        self.data = deque(maxlen=self.window_size)

        # Text annotation
        self.text_annotation = None

    def update_window_item(self, signal):
        frame, ber_num, ber_rate, count, data = signal
        try:
            self.rx_ber_current_frame_le.setText(str(frame))
            self.rx_ber_num_le.setText(str(ber_num))
            self.rx_ber_le.setText(str(ber_rate))

            # Ensure count and data are lists and have the same length
            if isinstance(count, list) and isinstance(data, list) and len(count) == len(data):
                # Append new data to deques
                self.counts.extend(count)
                self.data.extend(data)

                # Convert deques to lists
                count_list = list(self.counts)
                data_list = list(self.data)

                # Update the data line
                self.line.set_data(count_list, data_list)

                # Calculate the average and update the average line
                avg_data = [np.mean(data_list)] * len(data_list)
                self.avg_line.set_data(count_list, avg_data)

                # Update text annotation
                if self.text_annotation:
                    self.text_annotation.remove()
                avg_value = np.mean(data_list[-10:])  # Calculate average of last 10 points
                self.text_annotation = self.ax.text(count_list[-1], avg_data[-1], f"Current Avg: {avg_value:.4f}",
                                                    fontsize=10, ha='right', va='bottom')

                # Automatically scale the x-axis
                self.ax.relim()
                self.ax.autoscale_view()

                # Redraw the canvas
                self.canvas.draw()
            else:
                print("Count and data should be lists of the same length")
        except Exception as e:
            print(f"{e}")

    def clear_plot(self):
        # Clear the deques
        self.counts.clear()
        self.data.clear()

        # Remove the lines from the plot
        self.line.set_data([], [])
        self.avg_line.set_data([], [])

        # Remove the text annotation
        if self.text_annotation:
            self.text_annotation.remove()

        # Redraw the canvas to reflect the removal
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    # Simulate incoming data for testing
    import random
    from PySide6.QtCore import QTimer

    def generate_signal():
        frame = random.randint(0, 1000)
        ber_num = random.randint(0, 100)
        ber_rate = random.random()
        count = list(range(len(main_window.counts), len(main_window.counts) + 10))
        data = [ber_rate * (random.random() + 0.5) for _ in range(10)]
        signal = (frame, ber_num, ber_rate, count, data)
        main_window.update_window_item(signal)

    timer = QTimer()
    timer.timeout.connect(generate_signal)
    timer.start(20)  # Update every 2 seconds

    sys.exit(app.exec())
