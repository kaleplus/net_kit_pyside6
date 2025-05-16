# -*- coding: utf-8 -*-

import binascii
import datetime
import re
import ipaddress
import socket

import psutil
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QTextCursor

from net_kit_config import NetKitConfig
from net_kit_ui import Ui_NetKit
from config_window import ConfigWindow


class NetkitUiLogic(Ui_NetKit, QMainWindow):
    # 主线程继承自Ui_NetKit
    # 初始化信号-槽中的signal
    link_btn_signal = Signal(tuple)     # protocol_flag,ip,port
    tx_btn_signal = Signal(tuple)

    def __init__(self):
        super(NetkitUiLogic, self).__init__()
        self.setupUi(self)
        self.ui_signal_slots_connect()
        # 加载默认配置
        self.settings = NetKitConfig("netkit_config.json")
        self.init_settings()

    def ui_signal_slots_connect(self):
        """
        UI的信号-槽设置
        :return:None
        """
        self.rx_display_clear_btn.clicked.connect(lambda: self.rx_tb.clear())
        self.tx_display_clear_btn.clicked.connect(lambda: self.tx_tb.clear())
        self.tx_clear_btn.clicked.connect(lambda: self.tx_input_te.clear())
        self.protocol_comboBox.currentIndexChanged.connect(self.index_change_protocol_combobox)
        self.link_bt.clicked.connect(self.click_link_btn)
        self.tx_btn.clicked.connect(self.click_tx_btn)
        self.config_menu.triggered.connect(self.click_config_menu)

    @Slot()
    def click_config_menu(self):
        """
        开启配置窗口
        :return:
        """
        self.config_window = ConfigWindow()
        self.config_window.close_event_signal.connect(self.config_window_save_close)
        # self.config_window.setWindowModality(Qt.WindowModality.WindowModal)
        current_window_position = self.pos()
        # print(current_window_position)
        offset_x = 120
        offset_y = 30
        self.config_window.move(current_window_position.x() + offset_x, current_window_position.y() + offset_y)
        self.config_window.show()

    def config_window_save_close(self):
        self.settings.load_from_json("netkit_config.json")
        # print(self.settings.default_port)
        self.init_settings()
        # print("???")

    def init_settings(self):
        if self.settings.default_protocol_index == 0:
            self.protocol_comboBox.setCurrentIndex(2)
            self.protocol_comboBox.setCurrentIndex(0)
        else:
            self.protocol_comboBox.setCurrentIndex(self.settings.default_protocol_index)

        self.hex_rx_cb.setChecked(self.settings.default_hex_rx_index)
        self.hex_tx_cb.setChecked(self.settings.default_hex_tx_index)

        # self.rx_ber_start_btn.setEnabled(False)
        self.port_le.setText(str(self.settings.default_port))
        self.tx_loop_le.setText(str(self.settings.default_loop_interval))
        self.udp_target_ip_le.setText(self.settings.default_udp_target_ip)
        # self.rx_ber_interval_le.setText(str(self.settings.default_ber_update_interval))

    @Slot()
    def click_link_btn(self):
        """
        link_bt被点击后激活link_btn_signal传递protocol_index, ip, port
        :return:
        """
        protocol_index = self.protocol_comboBox.currentIndex()
        ip = self.ip_cb.currentText()
        port = int(self.port_le.text())
        self.link_btn_signal.emit((protocol_index, ip, port))

    @Slot()
    def click_tx_btn(self):
        """
        tx_btn被点击后激活，判断业务模式，并传递相关参数
        :return:
        """
        tx_msg = self.tx_input_te.toPlainText()
        # 因为UDP发送需要IP和Port，这和TCP模式不同
        if self.protocol_comboBox.currentIndex() == 2:
            ip = self.udp_target_ip_le.text()
            port = self.udp_target_port_le.text()
            if not self.is_valid_ip(ip):
                self.error_message_info("目标IP格式非法！")
            elif not self.is_valid_port(port):
                self.error_message_info("目标端口格式非法！")
            elif not tx_msg:
                self.error_message_info("输入为空")
            else:
                self.tx_btn_signal.emit((ip, int(port), tx_msg))
        else:
            if not tx_msg:
                self.error_message_info("输入为空")
            else:
                self.tx_btn_signal.emit(tx_msg)

    @Slot()
    def index_change_protocol_combobox(self):
        """
        根据所选择的协议变化ip和port标题
        :return:
        """
        if self.protocol_comboBox.currentIndex() in [0, 2]:
            self.ip_cb.clear()
            self.port_le.clear()
            self.ip_lb.setText("本地IP地址")
            self.port_lb.setText("本地监听端口")
            self.get_filtered_local_ip_addresses()
        elif self.protocol_comboBox.currentIndex() == 1:
            self.ip_cb.clear()
            self.port_le.clear()
            self.ip_lb.setText("目标IP地址")
            self.port_lb.setText("目标监听端口")

    def hex_to_byte_str(self, input_msg) -> bytes:
        """
        hex转byte_str，编码
        :param input_msg:
        :return:
        """
        # 删除空格
        input_msg = input_msg.replace(' ', '').replace('\n', '')
        try:
            byte_str_msg = binascii.a2b_hex(input_msg)
            return byte_str_msg
        except binascii.Error as e:
            self.error_message_info(f"输入包含非法字符: {e}")

    def str_to_byte_str(self, input_msg) -> bytes:
        """
        str转byte_str，编码
        :param input_msg:
        :return:
        """
        byte_str_msg = input_msg.encode('utf-8')
        return byte_str_msg

    def is_valid_ip(self, ip):
        pattern = re.compile(
            r'^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'  # 第一段
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'  # 第二段
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'  # 第三段
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'  # 第四段
        )
        return pattern.match(ip) is not None

    def is_valid_port(self, port):
        if port.isdigit():
            port_num = int(port)
            return 0 < port_num < 65536
        return False

    def get_filtered_local_ip_addresses(self):
        ip_addresses = []
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    ip_address = addr.address
                    # Filter out loopback, link-local, and non-private addresses
                    if not ip_address.startswith('127.') and not ip_address.startswith('169.254.'):
                        if ipaddress.ip_address(ip_address).is_private:
                            ip_addresses.append(ip_address)
        self.ip_cb.addItems(ip_addresses)
        # self.port_le.setText(str(self.settings.default_port))

    @Slot()
    def error_message_info(self, msg):
        QMessageBox.warning(self, 'Net_kit', str(msg), QMessageBox.StandardButton.Yes)

    @Slot()
    def rx_write_msg_to_tb(self, msg):
        """
        功能函数，向接收区写入数据的方法
        信号-槽触发
        tip：Pyside6程序的子线程中，直接向主线程的界面传输字符是不符合安全原则的?
        :return: None
        """
        show_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        self.rx_tb.append(f"<span style='color: gray;'>[{show_time}]</span>" + msg)
        self.rx_tb.moveCursor(QTextCursor.MoveOperation.End)

    @Slot()
    def tx_write_msg_to_tb(self, msg):
        """
        功能函数，向已发送消息区写入数据的方法
        信号-槽触发
        tip：Pyside6程序的子线程中，直接向主线程的界面传输字符是不符合安全原则的?
        :return: None
        """
        show_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.tx_tb.append(f"<span style='color: gray;'>[{show_time}]</span>" + msg)
        self.tx_tb.moveCursor(QTextCursor.MoveOperation.End)


# if __name__ == '__main__':
#     import sys
#     from PySide6.QtWidgets import QApplication
#     app = QApplication(sys.argv)
#     gui = NetkitUiLogic()
#     gui.show()
#     sys.exit(app.exec())
