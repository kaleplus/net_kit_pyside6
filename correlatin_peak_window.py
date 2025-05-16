# -*- coding: utf-8 -*-

import binascii
import heapq
import queue
import threading
import time
import numpy as np
import pyqtgraph as pg
from PySide6.QtGui import QAction
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtCore import (Signal, QObject, Slot)
from PySide6.QtWidgets import (QGridLayout,
                               QMainWindow, QWidget, QLineEdit, QSizePolicy, QPushButton, QVBoxLayout,
                               QFormLayout, QMessageBox, QMenuBar, QHBoxLayout)

from udp_logic import UdpServer


class CorrelationPeakWindow(QMainWindow):
    correlation_peak_update_signal = Signal(tuple)

    def __init__(self, setting):
        super().__init__()

        self.cp_data_process = None
        self.cp_server = None
        self.cp_setting = setting
        self.cp_listen_flag = False
        self.cp_max_list = []
        self.data_list = []

        self.setWindowTitle("CorrelationPeakWindow")
        self.resize(640, 480)
        self.main_widget = QWidget(self)
        self.main_widget.setObjectName("main_widget")
        self.setCentralWidget(self.main_widget)
        self.main_widget_layout = QGridLayout(self.main_widget)
        self.main_widget_layout.setObjectName("main_widget_layout")
        self.main_widget_layout.setSpacing(0)
        self.main_widget_layout.setContentsMargins(0, 0, 0, 0)

        # 添加pyqtgraph
        # 对于pyqtgraph的设置要放在创建widget之前
        # 设置不可左键拖动，背景为白，前景为黑
        pg.setConfigOptions(leftButtonPan=False, background='w', foreground='k')

        self.graphics_layout_widget = pg.GraphicsLayoutWidget()
        pg.setConfigOptions(antialias=True)
        container_widget = QWidget()
        container_layout = QHBoxLayout()
        container_layout.addWidget(self.graphics_layout_widget)
        container_widget.setLayout(container_layout)
        self.main_widget_layout.addWidget(container_widget, 0, 0, 1, 1)

        self.p1 = self.graphics_layout_widget.addPlot(title="Correlation Peak")
        self.p2 = self.graphics_layout_widget.addPlot(title="Max Correlation Peak")

        self.p1.setLabel('left', 'Correlation Peak', units='')
        # self.p1.setLabel('bottom', 'Time', units='s')
        self.p1.showGrid(x=False, y=True)

        self.p2.setLabel('left', 'Max Correlation Peak', units='')
        # self.p2.setLabel('bottom', 'Time', units='s')
        self.p2.showGrid(x=False, y=True)

        # Initialize data
        self.data1 = np.zeros(300)
        self.curve1 = self.p1.plot(self.data1)
        self.curve2 = self.p2.plot(self.data1)
        self.ptr1 = -298

        # # 添加pyqtgraph
        # self.plt_gridlayout_widget2 = QWidget(self.main_widget)
        # self.plt_gridlayout_widget2.setObjectName("plt_gridlayout_widget2")
        # self.plt_gridlayout2 = QGridLayout(self.plt_gridlayout_widget2)
        # self.plt_gridlayout2.setObjectName("plt_gridlayout2")
        #
        # # 对于pyqtgraph的设置要放在创建widget之前
        # # 设置不可左键拖动，背景为白，前景为黑
        # pg.setConfigOptions(leftButtonPan=False, background='w', foreground='k')
        # plot_item2 = pg.PlotItem()
        # # view_box = pg.ViewBox()
        # # plot_item2.scatterPlot([], [])
        # plot_item2.setLabel('left', '相关峰最大值')
        # # plot_item2.setLogMode(y=True)
        # # plot_item.getAxis('bottom').setStyle(showValue=False)
        # self.plot_plt2 = pg.PlotWidget(plotItem=plot_item2)
        # self.plot_plt2.showGrid(x=False, y=True)
        # # self.plot_plt2.getPlotItem().enableAutoRange()
        # # self.plot_plt2.getPlotItem().autoRange()
        #
        # self.plt_gridlayout2.addWidget(self.plot_plt2)
        #
        # self.main_widget_layout.addWidget(self.plt_gridlayout_widget2, 0, 1, 1, 1)

        # # 添加matplotlib
        # # Create a Figure
        # self.figure = Figure()
        # # Create a Canvas and add the Figure to it
        # self.canvas = FigureCanvas(self.figure)
        # # Get the axis from the Figure
        # self.ax = self.figure.add_subplot(111)
        # # Initialize the data line
        # self.line, = self.ax.plot([], [], 'r', label='Max_CorrelationPeak')
        # # self.avg_line, = self.ax.plot([], [], 'b--', label='Average')
        # self.ax.set_xlabel('X-axis')
        # self.ax.set_ylabel('Y-axis (Max_CorrelationPeak)')
        # # ax.set_title('')
        # self.ax.legend()
        # # Set the y-axis limits
        # # self.ax.set_ylim(1e-7, 1)  # Set bottom limit to a small value close to 0, and top limit to 1
        # # Draw the canvas
        # self.canvas.draw()
        # self.main_widget_layout.addWidget(self.canvas, 0, 1, 1, 1)

        self.menubar = QMenuBar()
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.rx_cp_start_btn = QAction("开始")
        self.menubar.addAction(self.rx_cp_start_btn)
        self.rx_cp_clear_btn = QAction("清除")
        self.menubar.addAction(self.rx_cp_clear_btn)
        self.rx_cp_save_btn = QAction("保存")
        self.menubar.addAction(self.rx_cp_save_btn)

        self.rx_cp_clear_btn.setDisabled(True)
        self.rx_cp_save_btn.setDisabled(True)

        # 槽
        self.rx_cp_start_btn.triggered.connect(self.cp_start_btn_event)
        self.rx_cp_clear_btn.triggered.connect(self.cp_clear_btn_event)
        self.rx_cp_save_btn.triggered.connect(self.cp_save_btn_event)

    @Slot()
    def cp_save_btn_event(self):
        try:
            with open('cp_data.txt', 'w') as file:
                for item1, item2 in zip(self.data_list, self.cp_max_list):
                    file.write(f"{item1}\t{item2}\n")  # 使用制表符作为分隔符
        except Exception as e:
            print(f"{e}")
        else:
            print("cp_data save!")
            reply = QMessageBox.information(
                self,
                "提示",
                "保存成功",
                QMessageBox.StandardButton.Yes
            )

    @Slot()
    def cp_clear_btn_event(self):
        # 默认高亮按钮为No
        reply = QMessageBox.question(
            self,
            "确认清除",
            "您确认要清除吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.cp_max_list = []
            self.data_list = []
            self.data1 = np.zeros(300)
            self.ptr1 = -298
            self.rx_cp_clear_btn.setDisabled(True)
            self.rx_cp_save_btn.setDisabled(True)
            self.curve1.clear()
            self.curve2.clear()

            # # Remove the line from the plot
            # self.line.remove()
            # # self.avg_line.remove()
            # # Redraw the canvas to reflect the removal
            # self.canvas.draw()
            # # Re-initialize the data line (optional, want to keep the plot object for future use)
            # self.line, = self.ax.plot([], [], 'r', label='Max_CorrelationPeak')
            # # self.avg_line, = self.ax.plot([], [], 'b--', label='Average')
        else:
            pass

    def update_window_item(self, signal):
        data_list, max_list, avg_max_list, cp_data_list = signal
        try:
            self.cp_max_list = max_list
            self.data_list = data_list
            cp_data_list = np.array(cp_data_list).flatten()  # 转换为一维数组
            self.curve1.setData(cp_data_list, pen='r')
            # count = np.array(count).flatten()  # 转换为一维数组
            max_list = np.array(max_list).flatten()  # 转换为一维数组
            self.data1[:-1] = self.data1[1:]  # Shift data in the array one sample left
            self.data1[-1] = max_list[-1]
            self.ptr1 += 1
            self.curve2.setData(self.data1, pen='r')
            self.curve2.setPos(self.ptr1, 0)

            # # self.line.set_data(count, max_list)
            # self.line.set_xdata(count)
            # self.line.set_ydata(max_list[-1])
            # # self.avg_line.set_data(count, avg_max_list)
            #
            # # Automatically scale the x-axis
            # self.ax.relim()
            # self.ax.autoscale_view()
            # self.canvas.draw()
        except Exception as e:
            print(f"{e}")

    @Slot()
    def cp_start_btn_event(self):
        if not self.cp_listen_flag:
            cp_queue = queue.Queue()
            self.cp_server = UdpServer('', self.cp_setting.default_cp_listen_port, cp_queue)
            self.cp_data_process = CorrelationPeakDataProcess(cp_queue, self.cp_setting.default_cp_update_interval)
            self.cp_server.udp_server_error_info_signal.connect(self.cp_error_message_info)
            self.cp_server.start()
            self.cp_data_process.start()
            self.cp_data_process.cp_info_signal.connect(self.update_window_item)
            # 成功bind
            try:
                self.cp_server.udp_server_socket.getsockname()
            except OSError as e:
                print(f"{e}")
            else:
                self.cp_listen_flag = True
                self.rx_cp_start_btn.setText("停止")
                self.rx_cp_clear_btn.setDisabled(True)
                self.rx_cp_save_btn.setDisabled(True)
            pass
        # ber listen stop
        else:
            self.cp_server.stop()
            self.cp_server.join()
            self.cp_data_process.stop()
            self.cp_data_process.join()
            self.cp_listen_flag = False
            self.rx_cp_start_btn.setText("开始")
            self.rx_cp_clear_btn.setDisabled(False)
            self.rx_cp_save_btn.setDisabled(False)

    @Slot()
    def cp_error_message_info(self, msg):
        QMessageBox.warning(self, 'cp_plot_window', str(msg), QMessageBox.StandardButton.Yes)

    def closeEvent(self, event):
        if self.cp_server:
            self.cp_server.stop()
            self.cp_server.join()
            self.cp_data_process.stop()
            self.cp_data_process.join()
            self.cp_listen_flag = False
            self.rx_cp_start_btn.setText("开始")
            event.accept()  # 允许关闭
        else:
            event.accept()


class CorrelationPeakDataProcess(QObject, threading.Thread):
    cp_info_signal = Signal(tuple)

    def __init__(self, recv_queue, cp_update_interval):
        QObject.__init__(self)
        threading.Thread.__init__(self)

        self.daemon = True

        self.recv_queue = recv_queue
        self.cp_update_interval = cp_update_interval

        self.data_process_running = True

        self.data_list = []
        self.max_cp_list = []
        self.avg_max_cp = 0
        self.cp_count = 0
        self.cp_count_list = []

    def run(self):
        next_time = time.perf_counter() + self.cp_update_interval / 1000.0
        while self.data_process_running:
            try:
                item = self.recv_queue.get(timeout=self.cp_update_interval / 1000.0)
                self.process_item(item)
            except queue.Empty:
                pass

            next_time += self.cp_update_interval / 1000.0
            sleep_time = next_time - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)

    def process_item(self, item):
        """
        判断接收到的信息符合cp接收格式
        :return:
        """
        # print(f"Processing item: {item}")
        recv_data, recv_addr = item
        # hex接收
        data = binascii.b2a_hex(recv_data).decode('utf-8').upper()
        correlation_peak_data_list = []
        for i in range(0, len(data), 8):
            temp = data[i:i + 8]
            temp = int(f"{temp}", 16)
            correlation_peak_data_list.append(temp)

        self.data_list.append(data)
        self.max_cp_list.append(heapq.nlargest(1, correlation_peak_data_list))
        # print(self.max_cp_list)
        self.avg_max_cp = [np.mean(self.max_cp_list)] * len(self.max_cp_list)
        # print(self.cp_count_list)

        self.cp_info_signal.emit((self.data_list, self.max_cp_list, self.avg_max_cp, correlation_peak_data_list))

    def stop(self):
        self.data_process_running = False
        print("Stopping data processing...")
