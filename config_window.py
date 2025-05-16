# -*- coding: utf-8 -*-

import sys

from PySide6.QtCore import (Signal)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QLineEdit,
                               QPushButton, QDialog, QFormLayout, QSpinBox, QMessageBox)

from net_kit_config import NetKitConfig


class ConfigWindow(QDialog):
    close_event_signal = Signal()

    def __init__(self):
        super().__init__()
        self.config = NetKitConfig("netkit_config.json")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("NetKit Default Config")
        # self.setGeometry(100, 100, 400, 300)
        self.resize(400, 300)
        layout = QFormLayout()
        self.setLayout(layout)

        self.protocol_index_edit = QComboBox()
        self.protocol_index_edit.addItems(self.config.default_protocol_index_dict.keys())
        self.protocol_index_edit.setCurrentIndex(self.config.default_protocol_index)
        layout.addRow("默认显示协议:", self.protocol_index_edit)

        self.port_edit = QSpinBox()
        self.port_edit.setRange(1, 65535)
        self.port_edit.setValue(self.config.default_port)
        layout.addRow("默认本地端口:", self.port_edit)

        self.hex_rx_check = QCheckBox()
        self.hex_rx_check.setChecked(self.config.default_hex_rx_index)
        layout.addRow("默认hex接收:", self.hex_rx_check)

        self.hex_tx_check = QCheckBox()
        self.hex_tx_check.setChecked(self.config.default_hex_tx_index)
        layout.addRow("默认hex发送:", self.hex_tx_check)

        self.loop_interval_edit = QSpinBox()
        self.loop_interval_edit.setRange(10, 10000)
        self.loop_interval_edit.setValue(self.config.default_loop_interval)
        layout.addRow("默认循环发送间隔 (ms):", self.loop_interval_edit)

        self.udp_target_ip_edit = QLineEdit(self.config.default_udp_target_ip)
        layout.addRow("默认UDP目标IP:", self.udp_target_ip_edit)

        self.ber_update_interval_edit = QSpinBox()
        self.ber_update_interval_edit.setRange(10, 10000)
        self.ber_update_interval_edit.setValue(self.config.default_ber_update_interval)
        layout.addRow("默认BER窗口刷新间隔 (ms):", self.ber_update_interval_edit)

        self.cp_update_interval_edit = QSpinBox()
        self.cp_update_interval_edit.setRange(10, 10000)
        self.cp_update_interval_edit.setValue(self.config.default_cp_update_interval)
        layout.addRow("默认相关峰窗口刷新间隔 (ms):", self.cp_update_interval_edit)

        self.fresh_window_interval_edit = QSpinBox()
        self.fresh_window_interval_edit.setRange(10, 10000)
        self.fresh_window_interval_edit.setValue(self.config.default_fresh_window_interval)
        layout.addRow("默认主窗口刷新间隔 (ms):", self.fresh_window_interval_edit)

        self.default_ber_listen_port_edit = QSpinBox()
        self.default_ber_listen_port_edit.setRange(1, 65535)
        self.default_ber_listen_port_edit.setValue(self.config.default_ber_listen_port)
        layout.addRow("默认BER监听端口:", self.default_ber_listen_port_edit)

        self.default_cp_listen_port_edit = QSpinBox()
        self.default_cp_listen_port_edit.setRange(1, 65535)
        self.default_cp_listen_port_edit.setValue(self.config.default_cp_listen_port)
        layout.addRow("默认相关峰监听端口:", self.default_cp_listen_port_edit)

        self.default_unknown_listen_port_edit = QSpinBox()
        self.default_unknown_listen_port_edit.setRange(1, 65535)
        self.default_unknown_listen_port_edit.setValue(self.config.default_unknown_listen_port)
        layout.addRow("Default Unknown Listen Port:", self.default_unknown_listen_port_edit)

        save_button = QPushButton("保存")
        save_button.clicked.connect(self.save_config)
        layout.addRow(save_button)

    def save_config(self):
        self.config.default_port = self.port_edit.value()
        self.config.default_hex_rx_index = self.hex_rx_check.isChecked()
        self.config.default_hex_tx_index = self.hex_tx_check.isChecked()
        self.config.default_loop_interval = self.loop_interval_edit.value()
        self.config.default_protocol_index = self.protocol_index_edit.currentIndex()
        self.config.default_udp_target_ip = self.udp_target_ip_edit.text()
        self.config.default_ber_update_interval = self.ber_update_interval_edit.value()
        self.config.default_cp_update_interval = self.cp_update_interval_edit.value()
        self.config.default_fresh_window_interval = self.fresh_window_interval_edit.value()
        self.config.default_ber_listen_port = self.default_ber_listen_port_edit.value()
        self.config.default_cp_listen_port = self.default_cp_listen_port_edit.value()
        self.config.default_unknown_listen_port = self.default_unknown_listen_port_edit.value()
        self.config.save_to_json("netkit_config.json")
        # print("Config saved!")

    def closeEvent(self, arg__1):
        # 默认高亮按钮为Yes
        reply = QMessageBox.question(
            self,
            "确认关闭",
            "您确认要关闭并保存吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.config.save_to_json("netkit_config.json")
            self.config.load_from_json("netkit_config.json")
            self.close_event_signal.emit()
            arg__1.accept()  # 允许关闭
        else:
            self.config.load_from_json("netkit_config.json")
            self.close_event_signal.emit()
            arg__1.accept()


# class ConfigWindow(QDialog, NetKitConfig):
#
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("ConfigWindow")
#         self.resize(660, 210)
#         self.setModal(True)
#         # self.setMaximumSize(QSize(16777215, 480))
#
#         self.main_widget_layout = QHBoxLayout()
#         self.main_widget_layout.setObjectName("main_widget_layout")
#         self.main_widget_layout.setContentsMargins(0, 0, 0, 0)
#         self.main_widget_layout.setSpacing(0)
#
#         self.tab_list = QListWidget()
#         self.tab_list.setObjectName("tab_list")
#         self.tab_list.setMaximumSize(QSize(100, 16777215))
#         self.main_widget_layout.addWidget(self.tab_list)
#
#         self.common_item = QListWidgetItem("普通窗口配置")
#         self.common_item.setSizeHint(QSize(90, 50))
#         self.tab_list.addItem(self.common_item)
#
#         self.debug_item = QListWidgetItem("调试窗口配置")
#         self.debug_item.setSizeHint(QSize(90, 50))
#         self.tab_list.addItem(self.debug_item)
#
#         self.profession_item = QListWidgetItem("业务窗口配置")
#         self.profession_item.setSizeHint(QSize(90, 50))
#         self.tab_list.addItem(self.profession_item)
#
#         self.scroll_area = QScrollArea(self)
#         self.scroll_area.setObjectName("scroll_area")
#         self.scroll_area.setWidgetResizable(False)
#         # self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
#         self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
#         self.main_widget_layout.addWidget(self.scroll_area)
#
#         self.setLayout(self.main_widget_layout)
#
#         self.content_widget = QWidget()
#         self.content_widget.setObjectName("content_widget")
#         # self.content_widget.setMinimumSize(QSize(535, 1440))
#         self.content_widget.setGeometry(QRect(0, 0, 535, 600))
#         self.scroll_area.setWidget(self.content_widget)
#         self.content_layout = QVBoxLayout()
#         self.content_layout.setObjectName("content_layout")
#         self.content_widget.setLayout(self.content_layout)
#
#         self.default_common_tab_config_groupbox = QGroupBox(self.content_widget)
#         self.default_common_tab_config_groupbox.setObjectName("default_common_tab_config_groupbox")
#         self.default_common_tab_config_groupbox.setTitle("普通窗口配置")
#         # self.default_common_tab_config_groupbox.setMinimumSize(QSize(640, 480))
#         self.content_layout.addWidget(self.default_common_tab_config_groupbox)
#
#         self.default_common_tab_config_layout = QGridLayout(self.default_common_tab_config_groupbox)
#         self.default_common_tab_config_layout.setObjectName("default_common_tab_config_layout")
#
#         self.default_port_lb = QLabel("默认监听端口")
#         self.default_port_lb.setObjectName("default_port_lb")
#         self.default_common_tab_config_layout.addWidget(self.default_port_lb, 0, 0, 1, 1)
#
#         self.default_port_le = QLineEdit()
#         self.default_port_le.setObjectName("default_port_le")
#         self.default_common_tab_config_layout.addWidget(self.default_port_le, 0, 1, 1, 1)
#
#         self.default_loop_interval_lb = QLabel("默认循环发送间隔")
#         self.default_loop_interval_lb.setObjectName("default_loop_interval_lb")
#         self.default_common_tab_config_layout.addWidget(self.default_loop_interval_lb, 1, 0, 1, 1)
#
#
#
#         self.default_loop_interval_le = QLineEdit()
#         self.default_loop_interval_le.setObjectName("default_loop_interval_le")
#         self.default_common_tab_config_layout.addWidget(self.default_loop_interval_le, 1, 1, 1, 1)
#         self.default_debug_tab_config_groupbox = QGroupBox(self.content_widget)
#         self.default_debug_tab_config_groupbox.setObjectName("default_debug_tab_config_groupbox")
#         self.default_debug_tab_config_groupbox.setTitle("调试窗口配置")
#         # self.default_debug_tab_config_groupbox.setMinimumSize(QSize(640, 480))
#         self.content_layout.addWidget(self.default_debug_tab_config_groupbox)
#
#         self.default_profession_tab_config_groupbox = QGroupBox(self.content_widget)
#         self.default_profession_tab_config_groupbox.setObjectName("default_profession_tab_config_groupbox")
#         self.default_profession_tab_config_groupbox.setTitle("业务窗口配置")
#         # self.default_profession_tab_config_groupbox.setMinimumSize(QSize(640, 480))
#         self.content_layout.addWidget(self.default_profession_tab_config_groupbox)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    config_window = ConfigWindow()
    config_window.show()

    sys.exit(app.exec())
