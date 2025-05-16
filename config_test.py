import sys
import os
import json
from PySide6.QtWidgets import (
    QApplication, QWidget, QFormLayout, QLineEdit, QSpinBox, QComboBox, QPushButton, QVBoxLayout, QDialog
)

from net_kit_config import NetKitConfig


class ConfigWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.config = NetKitConfig()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("NetKit Default Config")
        self.setGeometry(100, 100, 400, 300)

        layout = QFormLayout()
        self.setLayout(layout)

        self.port_edit = QSpinBox()
        self.port_edit.setRange(1, 65535)
        self.port_edit.setValue(self.config.default_port)
        layout.addRow("Default Port:", self.port_edit)

        self.loop_interval_edit = QSpinBox()
        self.loop_interval_edit.setRange(10, 10000)
        self.loop_interval_edit.setValue(self.config.default_loop_interval)
        layout.addRow("Default Loop Interval (ms):", self.loop_interval_edit)

        self.protocol_index_edit = QComboBox()
        self.protocol_index_edit.addItems(self.config.default_protocol_index_dict.keys())
        self.protocol_index_edit.setCurrentIndex(self.config.default_protocol_index)
        layout.addRow("Default Protocol:", self.protocol_index_edit)

        self.udp_target_ip_edit = QLineEdit(self.config.default_udp_target_ip)
        layout.addRow("Default UDP Target IP:", self.udp_target_ip_edit)

        self.ber_update_interval_edit = QSpinBox()
        self.ber_update_interval_edit.setRange(10, 10000)
        self.ber_update_interval_edit.setValue(self.config.default_ber_update_interval)
        layout.addRow("BER Update Interval (ms):", self.ber_update_interval_edit)

        self.fresh_window_interval_edit = QSpinBox()
        self.fresh_window_interval_edit.setRange(10, 10000)
        self.fresh_window_interval_edit.setValue(self.config.default_fresh_window_interval)
        layout.addRow("Fresh Window Interval (ms):", self.fresh_window_interval_edit)

        self.default_ber_listen_port_edit = QSpinBox()
        self.default_ber_listen_port_edit.setRange(1, 65535)
        self.default_ber_listen_port_edit.setValue(self.config.default_ber_listen_port)
        layout.addRow("Default BER Listen Port:", self.default_ber_listen_port_edit)

        self.default_cp_listen_port_edit = QSpinBox()
        self.default_cp_listen_port_edit.setRange(1, 65535)
        self.default_cp_listen_port_edit.setValue(self.config.default_cp_listen_port)
        layout.addRow("Default Correlation Peak Listen Port:", self.default_cp_listen_port_edit)

        self.default_unknown_listen_port_edit = QSpinBox()
        self.default_unknown_listen_port_edit.setRange(1, 65535)
        self.default_unknown_listen_port_edit.setValue(self.config.default_unknown_listen_port)
        layout.addRow("Default BER Listen Port:", self.default_unknown_listen_port_edit)

        save_button = QPushButton("Save Config")
        save_button.clicked.connect(self.save_config)
        layout.addRow(save_button)

    def save_config(self):
        self.config.default_port = self.port_edit.value()
        self.config.default_loop_interval = self.loop_interval_edit.value()
        self.config.default_protocol_index = self.protocol_index_edit.currentIndex()
        self.config.default_udp_target_ip = self.udp_target_ip_edit.text()
        self.config.default_ber_update_interval = self.ber_update_interval_edit.value()
        self.config.default_fresh_window_interval = self.fresh_window_interval_edit.value()
        self.config.save_to_json("netkit_config.json")
        print("Config saved!")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    config_window = ConfigWindow()
    config_window.show()

    sys.exit(app.exec())
