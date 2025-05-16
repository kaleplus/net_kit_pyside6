# -*- coding: utf-8 -*-

import binascii
import queue
import threading
import time
import numpy as np
import pyqtgraph as pg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtCore import (Signal, QObject, Slot)
from PySide6.QtWidgets import (QGridLayout,
                               QMainWindow, QWidget, QLineEdit, QSizePolicy, QPushButton, QVBoxLayout,
                               QFormLayout, QMessageBox)

from udp_logic import UdpServer


# 可以用=None消除已经创建的实例
class BerPlotWindow(QMainWindow):
    ber_update_signal = Signal(tuple)

    def __init__(self, setting):
        super().__init__()

        self.ber_data_process = None
        self.ber_server = None
        self.ber_setting = setting
        self.ber_listen_flag = False
        self.ber_list = []
        self.data_list = []

        self.setWindowTitle("ber_plot_window")
        self.resize(640, 480)
        self.main_widget = QWidget(self)
        self.main_widget.setObjectName("main_widget")
        self.setCentralWidget(self.main_widget)
        self.main_widget_layout = QVBoxLayout(self.main_widget)
        self.main_widget_layout.setObjectName("main_widget_layout")
        self.main_widget_layout.setSpacing(0)
        self.main_widget_layout.setContentsMargins(0, 0, 0, 0)

        # 添加pyqtgraph
        # 对于pyqtgraph的设置要放在创建widget之前
        # 设置不可左键拖动，背景为白，前景为黑
        pg.setConfigOptions(leftButtonPan=False, background='w', foreground='k')

        self.graphics_layout_widget = pg.GraphicsLayoutWidget(show=True)
        container_widget = QWidget()
        container_layout = QVBoxLayout()
        container_layout.addWidget(self.graphics_layout_widget)
        container_widget.setLayout(container_layout)
        # self.main_widget_layout.addWidget(container_widget)

        self.p1 = self.graphics_layout_widget.addPlot(title="误比特率")
        # self.p2 = self.graphics_layout_widget.addPlot(title="Max Correlation Peak")

        self.p1.setLabel('left', '误比特率', units='')
        # self.p1.setLabel('bottom', 'Time', units='s')
        self.p1.showGrid(x=False, y=True)
        self.p1.setLogMode(y=True)
        # self.p1.setYRange(0, 1)

        # self.p2.setLabel('left', 'Max Correlation Peak', units='')
        # # self.p2.setLabel('bottom', 'Time', units='s')
        # self.p2.showGrid(x=False, y=True)

        # Initialize data
        self.data1 = np.zeros(300)
        self.curve1 = self.p1.plot(self.data1)
        # self.curve2 = self.p2.plot(self.data1)
        self.ptr1 = 0

        # # 添加pyqtgraph
        # self.plt_gridlayout_widget = QWidget(self.main_widget)
        # self.plt_gridlayout_widget.setObjectName("plt_gridlayout_widget")
        # self.plt_gridlayout_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # # self.plt_gridlayout_widget.setMaximumSize(16777215, 16777215)
        # self.plt_gridlayout = QGridLayout(self.plt_gridlayout_widget)
        # self.plt_gridlayout.setObjectName("plt_gridlayout")
        #
        # # 对于pyqtgraph的设置要放在创建widget之前
        # # 设置不可左键拖动，背景为白，前景为黑
        # pg.setConfigOptions(leftButtonPan=False, background='w', foreground='k')
        # plot_item = pg.PlotItem()
        # plot_item.setLabel('left', '误比特率')
        # plot_item.setLogMode(y=True)
        # # plot_item.getAxis('bottom').setStyle(showValue=False)
        # self.plot_plt = pg.PlotWidget(plotItem=plot_item)
        # self.plot_plt.showGrid(x=False, y=True)
        # self.plot_plt.getPlotItem().enableAutoRange()
        # # self.plot_plt.setYRange({1, 1e-6})
        #
        # self.plt_gridlayout.addWidget(self.plot_plt)
        # self.main_widget_layout.addWidget(self.plt_gridlayout_widget)

        # # 添加matplotlib
        # # Create a Figure
        # self.figure = Figure()
        # # Create a Canvas and add the Figure to it
        # self.canvas = FigureCanvas(self.figure)
        # # Get the axis from the Figure
        # self.ax = self.figure.add_subplot(111)
        # # Initialize the data line
        # self.line, = self.ax.semilogy([], [], 'r', label='BER')
        # # self.avg_line, = self.ax.semilogy([], [], 'b--', label='Average')
        # self.ax.set_xlabel('X-axis')
        # self.ax.set_ylabel('Y-axis (BER)')
        # # ax.set_title('')
        # self.ax.legend()
        # # Set the y-axis limits
        # self.ax.set_ylim(1e-7, 1)  # Set bottom limit to a small value close to 0, and top limit to 1
        # # Draw the canvas
        # self.canvas.draw()

        self.rx_ber_display_layout_widget = QWidget(self.main_widget)
        self.rx_ber_display_layout_widget.setObjectName("rx_ber_display_layout_widget")
        self.rx_ber_display_layout_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.rx_ber_display_layout = QGridLayout(self.rx_ber_display_layout_widget)
        self.rx_ber_display_layout.setObjectName("rx_ber_display_layout")
        self.main_widget_layout.addWidget(self.rx_ber_display_layout_widget)
        self.main_widget_layout.addWidget(container_widget)
        # self.main_widget_layout.addWidget(self.plt_gridlayout_widget)
        # self.main_widget_layout.addWidget(self.canvas)
        self.rx_ber_display_layout.setVerticalSpacing(0)
        self.rx_ber_display_layout.setContentsMargins(0, 0, 0, 0)
        # self.rx_ber_tablewidget = QTableWidget(self.rx_ber_display_layoutwidget)
        # self.rx_ber_tablewidget.setObjectName("rx_ber_tableview")
        # # self.rx_ber_tablewidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # # 设置不可编辑
        # self.rx_ber_tablewidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # self.rx_ber_tablewidget.setRowCount(1)
        # self.rx_ber_tablewidget.setColumnCount(6)
        # self.rx_ber_tablewidget.setItem(0, 0, QTableWidgetItem("当前帧数"))
        # self.rx_ber_tablewidget.setItem(0, 2, QTableWidgetItem("误比特数"))
        # self.rx_ber_tablewidget.setItem(0, 4, QTableWidgetItem("误比特率"))
        # # self.rx_ber_tablewidget.setMaximumSize(16777215, 33)
        # # self.rx_ber_tablewidget.setMinimumSize(420, 0)
        # # 设置表头不可见
        # self.rx_ber_tablewidget.horizontalHeader().setVisible(False)
        # self.rx_ber_tablewidget.verticalHeader().setVisible(False)
        # # 设置列拉伸
        # self.rx_ber_tablewidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # self.rx_ber_tablewidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        # self.rx_ber_tablewidget.setMaximumSize(16777215, 33)

        self.rx_ber_view_layout = QFormLayout()
        self.rx_ber_view_layout.setObjectName("rx_ber_view_layout")
        self.rx_ber_display_layout.addLayout(self.rx_ber_view_layout, 0, 0, 3, 1)
        self.rx_ber_current_frame_le = QLineEdit()
        # self.rx_ber_current_frame_le.setEnabled(False)
        self.rx_ber_view_layout.addRow("当前帧数:", self.rx_ber_current_frame_le)
        self.rx_ber_num_le = QLineEdit()
        # self.rx_ber_num_le.setEnabled(False)
        self.rx_ber_view_layout.addRow("误比特数:", self.rx_ber_num_le)
        self.rx_ber_le = QLineEdit()
        # self.rx_ber_le.setEnabled(False)
        self.rx_ber_view_layout.addRow("误比特率:", self.rx_ber_le)

        # self.rx_ber_interval_le = QLineEdit()
        # self.rx_ber_view_layout.addRow("刷新间隔(ms):", self.rx_ber_interval_le)

        # self.rx_ber_interval_layout = QHBoxLayout()
        # self.rx_ber_interval_layout.setObjectName("rx_ber_interval_layout")
        # self.rx_ber_interval_layout.setSpacing(0)
        # self.rx_ber_interval_layout.setContentsMargins(0, 0, 0, 0)
        # self.rx_ber_interval_lb2 = QLabel(self.rx_ber_display_layoutwidget)
        # self.rx_ber_interval_lb2.setObjectName("rx_ber_interval_lb2")
        # self.rx_ber_interval_layout.addWidget(self.rx_ber_interval_lb2)
        # self.rx_ber_interval_le = QLineEdit(self.rx_ber_display_layoutwidget)
        # self.rx_ber_interval_le.setObjectName("rx_ber_interval_le")
        # self.rx_ber_interval_le.setMaximumSize(100, 30)
        # self.rx_ber_interval_le.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # self.rx_ber_interval_layout.addWidget(self.rx_ber_interval_le)
        # self.rx_ber_interval_lb = QLabel(self.rx_ber_display_layoutwidget)
        # self.rx_ber_interval_lb.setObjectName("rx_ber_interval_lb")
        # self.rx_ber_interval_layout.addWidget(self.rx_ber_interval_lb)
        # self.rx_ber_display_layout.addLayout(self.rx_ber_interval_layout, 3, 0, 1, 1)

        self.rx_ber_start_btn = QPushButton(self.rx_ber_display_layout_widget)
        self.rx_ber_start_btn.setObjectName("rx_ber_start_btn")
        self.rx_ber_start_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.rx_ber_display_layout.addWidget(self.rx_ber_start_btn, 0, 1, 1, 1)

        self.rx_ber_clear_btn = QPushButton(self.rx_ber_display_layout_widget)
        self.rx_ber_clear_btn.setObjectName("rx_ber_clear_btn")
        self.rx_ber_display_layout.addWidget(self.rx_ber_clear_btn, 1, 1, 1, 1)

        self.rx_ber_save_btn = QPushButton(self.rx_ber_display_layout_widget)
        self.rx_ber_save_btn.setObjectName("rx_ber_save_btn")
        self.rx_ber_display_layout.addWidget(self.rx_ber_save_btn, 2, 1, 1, 1)

        self.rx_ber_start_btn.setText("开始")
        self.rx_ber_clear_btn.setText("清除计数")
        self.rx_ber_save_btn.setText("保存")

        self.rx_ber_start_btn.setStyleSheet("QPushButton:enabled { background-color: #87CEEB; }")
        self.rx_ber_clear_btn.setStyleSheet("QPushButton:enabled { background-color: #87CEEB; }")
        self.rx_ber_save_btn.setStyleSheet("QPushButton:enabled { background-color: #87CEEB; }")
        self.rx_ber_clear_btn.setDisabled(True)
        self.rx_ber_save_btn.setDisabled(True)

        # 槽
        self.rx_ber_start_btn.clicked.connect(self.ber_start_btn_event)
        self.rx_ber_clear_btn.clicked.connect(self.ber_clear_btn_event)
        self.rx_ber_save_btn.clicked.connect(self.ber_save_btn_event)

    @Slot()
    def ber_save_btn_event(self):
        try:
            with open('ber_data.txt', 'w') as file:
                for item1, item2 in zip(self.data_list, self.ber_list):
                    file.write(f"{item1}\t{item2}\n")  # 使用制表符作为分隔符
        except Exception as e:
            print(f"{e}")
        else:
            print("ber_data save!")
            reply = QMessageBox.information(
                self,
                "提示",
                "保存成功",
                QMessageBox.StandardButton.Yes
            )

    @Slot()
    def ber_clear_btn_event(self):
        # 默认高亮按钮为No
        reply = QMessageBox.question(
            self,
            "确认清除",
            "您确认要清除吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.ber_list = []
            self.data_list = []
            self.rx_ber_clear_btn.setDisabled(True)
            self.rx_ber_save_btn.setDisabled(True)
            self.rx_ber_current_frame_le.clear()
            self.rx_ber_num_le.clear()
            self.rx_ber_le.clear()
            self.curve1.clear()
            # # Remove the line from the plot
            # self.line.remove()
            # # self.avg_line.remove()
            # # Redraw the canvas to reflect the removal
            # self.canvas.draw()
            # # Re-initialize the data line (optional, want to keep the plot object for future use)
            # self.line, = self.ax.semilogy([], [], 'r', label='BER')
            # # self.avg_line, = self.ax.semilogy([], [], 'b--', label='Average')
        else:
            pass

    def update_window_item(self, signal):
        data, frame, ber_num, ber_rate, plot_data, avg_ber = signal
        try:
            self.ber_list = plot_data
            self.data_list = data
            self.rx_ber_current_frame_le.setText(str(frame))
            self.rx_ber_num_le.setText(str(ber_num))
            self.rx_ber_le.setText(str(ber_rate))
            plot_data = np.array(plot_data).flatten()  # 转换为一维数组
            self.curve1.setData(plot_data, pen='r')
            # if len(count) == len(plot_data) and len(count) == len(avg_ber):
            #     self.line.set_data(count, plot_data)
            #     # self.avg_line.set_data(count, avg_ber)
            #     # # Adjust the x-axis limits to fit the new data
            #     # self.ax.set_xlim(min(count), max(count))
            #     # Automatically scale the x-axis
            #     self.ax.relim()
            #     self.ax.autoscale_view()
            #     self.canvas.draw()
        except Exception as e:
            print(f"{e}")

    @Slot()
    def ber_start_btn_event(self):
        if not self.ber_listen_flag:
            ber_queue = queue.Queue()
            self.ber_server = UdpServer('', self.ber_setting.default_ber_listen_port, ber_queue)
            self.ber_data_process = BerDataProcess(ber_queue, self.ber_setting.default_ber_update_interval)
            self.ber_server.udp_server_error_info_signal.connect(self.ber_error_message_info)
            self.ber_server.start()
            self.ber_data_process.start()
            self.ber_data_process.ber_info_signal.connect(self.update_window_item)
            # 成功bind
            try:
                self.ber_server.udp_server_socket.getsockname()
            except OSError as e:
                print(f"{e}")
            else:
                self.ber_listen_flag = True
                self.rx_ber_start_btn.setText("停止")
                self.rx_ber_clear_btn.setDisabled(True)
                self.rx_ber_save_btn.setDisabled(True)
            pass
        # ber listen stop
        else:
            self.ber_server.stop()
            self.ber_server.join()
            self.ber_data_process.stop()
            self.ber_data_process.join()
            self.ber_listen_flag = False
            self.rx_ber_start_btn.setText("开始")
            self.rx_ber_clear_btn.setDisabled(False)
            self.rx_ber_save_btn.setDisabled(False)

    @Slot()
    def ber_error_message_info(self, msg):
        QMessageBox.warning(self, 'ber_plot_window', str(msg), QMessageBox.StandardButton.Yes)

    def closeEvent(self, event):
        if self.ber_server:
            self.ber_server.stop()
            self.ber_server.join()
            self.ber_data_process.stop()
            self.ber_data_process.join()
            self.ber_listen_flag = False
            self.rx_ber_start_btn.setText("开始")
            event.accept()  # 允许关闭
        else:
            event.accept()


class BerDataProcess(QObject, threading.Thread):
    ber_info_signal = Signal(tuple)

    def __init__(self, recv_queue, ber_update_interval):
        QObject.__init__(self)
        threading.Thread.__init__(self)

        self.daemon = True

        self.recv_queue = recv_queue
        self.ber_update_interval = ber_update_interval

        self.data_process_running = True

        self.data_list = []
        self.ber = 0
        self.ber_count = 0
        self.ber_count_list = []
        self.ber_rate = 0
        self.ber_list = []
        self.avg_ber = 0
        self.current_ber_num = 0
        self.current_frame = 0

    def run(self):
        next_time = time.perf_counter() + self.ber_update_interval / 1000.0
        while self.data_process_running:
            try:
                item = self.recv_queue.get(timeout=self.ber_update_interval / 1000.0)
                self.process_item(item)
            except queue.Empty:
                pass

            next_time += self.ber_update_interval / 1000.0
            sleep_time = next_time - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)

    def process_item(self, item):
        """
        判断接收到的信息符合ber接收格式
        :return:
        """
        # print(f"Processing item: {item}")
        recv_data, recv_addr = item
        # hex接收
        data = binascii.b2a_hex(recv_data).decode('utf-8').upper()
        # 在这里发送给ber
        if len(data) == 10:
            self.data_list.append(data)
            self.current_frame = int(f'{data[:4]}', 16)
            self.current_ber_num = int(f'{data[4:]}', 16)
            self.ber = self.current_ber_num/self.current_frame/(255*8)
            # 简化值
            self.ber_rate = format(self.ber, '.5e')
            # 传给画图窗口
            self.ber_list.append(float(self.ber))
            # self.ber_count_list.append(len(self.ber_list))
            self.avg_ber = np.full(len(self.ber_list), np.mean(self.ber_list), dtype=float).tolist()
            self.ber_info_signal.emit((self.data_list, self.current_frame, self.current_ber_num, self.ber_rate,
                                       self.ber_list, self.avg_ber))
            # print(self.ber_rate)
            # print(len(self.ber_list))
            # print(len(self.ber_count_list))
            # print(len(self.avg_ber))
        else:
            pass

    def stop(self):
        self.data_process_running = False
        print("Stopping data processing...")



