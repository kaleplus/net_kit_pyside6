import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


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

        # Initialize the data line
        self.line, = self.ax.semilogy([], [], 'r')

        # Set the y-axis limits
        self.ax.set_ylim(1e-10, 1)

        # Add a button to clear the plot
        self.clear_button = QPushButton("Clear Plot")
        layout.addWidget(self.clear_button)
        self.clear_button.clicked.connect(self.clear_plot)

        # Draw the canvas
        self.canvas.draw()

    def update_window_item(self, signal):
        frame, ber_num, ber_rate, count, data = signal
        try:
            self.rx_ber_current_frame_le.setText(str(frame))
            self.rx_ber_num_le.setText(str(ber_num))
            self.rx_ber_le.setText(str(ber_rate))

            # Ensure count and data are lists
            if isinstance(count, list) and isinstance(data, list):
                # Update the data of the plot
                self.line.set_data(count, data)

                # Adjust the x-axis limits to fit the new data
                self.ax.set_xlim(min(count), max(count))

                # Redraw the canvas
                self.canvas.draw()
            else:
                print("count and data should be lists")
        except Exception as e:
            print(f"{e}")

    def clear_plot(self):
        # Remove the line from the plot
        self.line.remove()

        # Redraw the canvas to reflect the removal
        self.canvas.draw()

        # Re-initialize the data line (optional, if you want to keep the plot object for future use)
        self.line, = self.ax.semilogy([], [], 'r')


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
        count = [i for i in range(1, 101)]  # Use a list instead of numpy array
        data = [ber_rate / (i + 1) for i in range(1, 101)]  # Use a list instead of numpy array
        signal = (frame, ber_num, ber_rate, count, data)
        main_window.update_window_item(signal)


    timer = QTimer()
    timer.timeout.connect(generate_signal)
    timer.start(2000)  # Update every 2 seconds

    sys.exit(app.exec())
