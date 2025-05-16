#!/usr/bin/env python
# -*- coding: utf-8 -*-

import binascii
import queue
import sys
import threading
import time

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Signal, Slot, QTimer, Qt, QObject

from ui_Logic import NetkitUiLogic
from udp_logic import UdpServer, UdpClient
from ber_window import BerPlotWindow
from correlatin_peak_window import CorrelationPeakWindow


class MainWindow(NetkitUiLogic):

    def __init__(self):
        super(MainWindow, self).__init__()

        # flag
        self.tx_loop_flag = False
        self.link_flag = False

        self.correlation_peak_window = None
        self.correlation_peak_count_list = []
        self.correlation_peak_data_list = []

        # init槽
        self.init_signal_slot()

    def init_signal_slot(self):
        self.new_window_action.triggered.connect(self.new_window)
        self.link_btn_signal.connect(self.link_btn_handle)
        self.tx_btn_signal.connect(self.tx_btn_handle)
        self.ber_window_btn.clicked.connect(self.ber_window_btn_handle)
        self.cp_window_btn.clicked.connect(self.cp_window_btn_handle)

    @Slot()
    def cp_window_btn_handle(self):
        """
        开启相关峰图窗
        :return:
        """
        self.cp_window = CorrelationPeakWindow(self.settings)
        # 槽

        # 位置

        self.cp_window.show()
        pass

    @Slot()
    def ber_window_btn_handle(self):
        """
        开启BER图窗
        :return:
        """
        self.ber_window = BerPlotWindow(self.settings)
        # 槽

        # 位置

        self.ber_window.show()
        pass

    @Slot()
    def tx_btn_handle(self, signal):
        """
        处理tx_btn事件
        :param signal:
        :return:
        """
        if self.protocol_comboBox.currentIndex() == 2:
            self.udp_client_event(signal)
        else:
            # tcp
            pass

    def udp_client_event(self, signal):
        ip, port, tx_msg = signal
        try:
            self.udp_client = UdpClient(ip, port)
            self.udp_client.udp_client_error_info_signal.connect(self.rx_write_msg_to_tb)
        except OSError as e:
            print(f"udp client {e.errno}:{e.strerror}")
        else:
            if self.hex_tx_cb.isChecked():
                pre_msg = self.hex_to_byte_str(tx_msg)
            else:
                pre_msg = self.str_to_byte_str(tx_msg)
            if pre_msg:
                if self.tx_loop_checkbox.isChecked():
                    if not self.tx_loop_flag:
                        try:
                            self.tx_loop_timer = QTimer()
                            self.tx_loop_timer.setTimerType(Qt.TimerType.PreciseTimer)
                        except Exception as e:
                            print(f"{e}")
                        else:
                            self.tx_loop_flag = True
                            self.loop_interval = int(self.tx_loop_le.text())
                            # 多端口发送判断？

                            # tcp\udp tx判断
                            if self.protocol_comboBox.currentIndex() == 2:
                                if self.loop_interval <= 100:
                                    # 传递参数可以用lambda
                                    self.tx_loop_timer.timeout.connect(lambda: self.udp_client.send(pre_msg))
                                    msg = (f"<span style='color: gray;'># TX to {ip}:{port}</span>"
                                           f"<br><span style='color: red;'>时间间隔不大于100ms，不显示在窗口，正在循环发送...</span><br>")
                                    self.tx_write_msg_to_tb(msg)
                                else:
                                    self.tx_loop_timer.timeout.connect(lambda: self.udp_client.send(pre_msg))
                                    msg = (f"<span style='color: gray;'># TX from {ip}:{port}</span>"
                                           f"<br><span style='color: blue;'>{tx_msg}</span><br>")
                                    self.tx_loop_timer.timeout.connect(lambda: self.tx_write_msg_to_tb(msg))
                            else:
                                pass

                            self.tx_loop_timer.start(self.loop_interval)
                            self.tx_loop_checkbox.setEnabled(False)
                            self.tx_loop_le.setEnabled(False)
                            self.tx_btn.setText("停止发送")

                    else:
                        self.tx_loop_timer.stop()
                        self.tx_loop_flag = False
                        self.tx_loop_checkbox.setEnabled(True)
                        self.tx_loop_le.setEnabled(True)
                        self.tx_btn.setText("发送")
                        msg = (f"<span style='color: gray;'># TX to {ip}:{port}</span>"
                               f"<br><span style='color: red;'>停止循环发送</span><br>")
                        self.tx_write_msg_to_tb(msg)
                else:
                    self.udp_client.send(pre_msg)
                    msg = (f"<span style='color: gray;'># TX to {ip}:{port}</span>"
                           f"<br><span style='color: blue;'>{tx_msg}</span><br>")
                    self.tx_write_msg_to_tb(msg)

    @Slot()
    def link_btn_handle(self, signal):
        """
        处理link_btn事件
        :param signal:
        :return:
        """
        protocol_index, ip, port = signal
        if protocol_index == 0:
            pass
        elif protocol_index == 1:
            pass
        elif protocol_index == 2:
            # udp server start
            self.udp_server_event(ip, port)

    def udp_server_event(self, ip, port):
        if not self.link_flag:
            udp_recv_queue = queue.Queue()
            self.udp_server = UdpServer(ip, port, udp_recv_queue)
            self.udp_recv_data_process = NetKitUiDataProcess(self.hex_rx_cb, udp_recv_queue,
                                                             self.settings.default_fresh_window_interval)
            self.udp_server.udp_server_error_info_signal.connect(self.error_message_info)
            self.udp_server.udp_server_listen_info_signal.connect(self.rx_write_msg_to_tb)
            self.udp_server.start()
            self.udp_recv_data_process.start()
            self.udp_recv_data_process.recv_msg_signal.connect(self.rx_write_msg_to_tb)
            # self.udp_recv_data_process.process_handle()
            # 成功bind
            try:
                self.udp_server.udp_server_socket.getsockname()
            except OSError as e:
                print(f"{e}")
            else:
                self.link_flag = True
                self.change_enable_net_config(False)
        # udp server stop
        else:
            self.udp_server.stop()
            self.udp_server.join()
            self.udp_recv_data_process.stop()
            self.udp_recv_data_process.join()
            self.link_flag = False
            self.change_enable_net_config(True)
            # self.udp_server.udp_server_error_info_signal.disconnect(self.error_message_info)
            # self.udp_server.udp_server_listen_info_signal.disconnect(self.rx_write_msg_to_tb)

    def change_enable_net_config(self, boolean):
        """
        改变net_config_group内组件的可用性，以及按钮变化
        :param boolean:
        :return:
        """
        self.protocol_comboBox.setEnabled(boolean)
        self.ip_cb.setEnabled(boolean)
        self.port_le.setEnabled(boolean)
        if boolean:
            self.link_bt.setText("连接")
        else:
            self.link_bt.setText("断开连接")

        # ber区设置
        # self.rx_ber_start_btn.setEnabled(not boolean)

    @Slot()
    def new_window(self):
        """
        开启一个新的窗口的方法
        :return:
        """
        # 弹出一个消息框，提示开启了一个新的窗口
        response = QMessageBox.warning(self, 'Net_kit', "是否开启新的Net_Kit窗口？",
                                       QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
        if response == QMessageBox.StandardButton.Yes:

            # 开启新的窗口
            self.new = MainWindow()
            current_window_position = self.pos()
            # print(current_window_position)
            offset_x = 150
            offset_y = 10
            self.new.move(current_window_position.x() + offset_x, current_window_position.y() + offset_y)
            self.new.show()
        else:
            pass

    def closeEvent(self, event):
        # 默认高亮按钮为No
        reply = QMessageBox.question(
            self,
            "确认退出",
            "您确认要退出吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()  # 允许关闭
        else:
            event.ignore()


class NetKitUiDataProcess(QObject, threading.Thread):
    recv_msg_signal = Signal(tuple)

    def __init__(self, hex_rx, recv_queue, fresh_window_interval):
        QObject.__init__(self)
        threading.Thread.__init__(self)
        self.daemon = True

        self.hex_rx = hex_rx
        self.recv_queue = recv_queue
        self.fresh_window_interval = fresh_window_interval

        self.data_process_running = True

    def run(self):
        next_time = time.perf_counter() + self.fresh_window_interval / 1000.0
        while self.data_process_running:
            try:
                item = self.recv_queue.get(timeout=self.fresh_window_interval / 1000.0)
                self.process_item(item)
            except queue.Empty:
                pass

            next_time += self.fresh_window_interval / 1000.0
            sleep_time = next_time - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)

    def process_item(self, item):
        # print(f"Processing item: {item}")
        recv_data, recv_addr = item
        if self.hex_rx.isChecked():
            # hex接收
            msg = self.byte_str_to_hex(recv_addr, recv_data)
            self.recv_msg_signal.emit(msg)
        else:
            msg = self.byte_str_to_str(recv_addr, recv_data)
            self.recv_msg_signal.emit(msg)

    def byte_str_to_str(self, recv_addr, recv_msg):
        """
        字节字符串转换为字符串，解码
        :param recv_addr:
        :param recv_msg:
        :return:
        """
        try:
            rcv_msg = recv_msg.decode('utf-8')
            msg = (f"<span style='color: gray;'># RX from {recv_addr[0]}:{recv_addr[1]}</span>"
                   f"<br><span style='color: green;'>{rcv_msg}</span><br>")
            return msg
        except Exception as ret:
            msg = (f"<span style='color: gray;'># RX from {recv_addr[0]}:{recv_addr[1]}</span>"
                   f"<br><span style='color: red;'>解码错误，请尝试hex接收</span><br>")
            print(f"{ret}")
            return msg

    def byte_str_to_hex(self, recv_addr, recv_msg):
        """
        字节字符串转换为hex字符串，解码
        :param recv_addr:
        :param recv_msg:
        :return:
        """
        try:
            rcv_msg = binascii.b2a_hex(recv_msg).decode('utf-8').upper()
            # print(rcv_msg)
            format_rcv_msg = ' '.join([rcv_msg[2 * i:2 * (i + 1)] for i in range(len(rcv_msg) // 2)])
            msg = (f"<span style='color: gray;'># RX from {recv_addr[0]}:{recv_addr[1]}</span>"
                   f"<br><span style='color: green;'>{format_rcv_msg}</span><br>")
            return msg
        except Exception as ret:
            msg = (f"<span style='color: gray;'># RX from {recv_addr[0]}:{recv_addr[1]}</span>"
                   f"<br><span style='color: red;'>解码错误，请尝试非hex接收</span><br>")
            print(f"{ret}")
            return msg

    def stop(self):
        self.data_process_running = False
        print("Stopping data processing...")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec())
