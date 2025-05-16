# -*- coding: utf-8 -*-

from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize)
from PySide6.QtGui import (QAction)
from PySide6.QtWidgets import (QCheckBox, QComboBox, QGridLayout,
                               QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                               QMenuBar, QPushButton, QSizePolicy,
                               QStatusBar, QTextBrowser, QWidget, QTabWidget, QTextEdit, QVBoxLayout, QMenu)


class Ui_NetKit(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 480)
        self.centralwidget = QWidget(MainWindow)
        # 设置光标类型，不知道作用
        # self.centralwidget.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.centralwidget.setObjectName("centralwidget")
        # 设置主窗口布局为水平布局
        self.main_layout = QHBoxLayout(self.centralwidget)
        self.main_layout.setObjectName("main_layout")
        # self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_tabwidget = QTabWidget(self.centralwidget)
        self.main_tabwidget.setObjectName("main_tabwidget")
        self.common_tab = QWidget()
        self.common_tab.setObjectName("common_tab")
        self.debug_tab = QWidget()
        self.debug_tab.setObjectName("debug_tab")
        self.profession_tab = QWidget()
        self.profession_tab.setObjectName("profession_tab")
        self.main_tabwidget.addTab(self.common_tab, "普通")
        self.main_tabwidget.addTab(self.debug_tab, "调试")
        self.main_tabwidget.addTab(self.profession_tab, "业务")
        self.main_layout.addWidget(self.main_tabwidget)

        self.common_tab_layout = QHBoxLayout(self.common_tab)
        self.common_tab_layout.setObjectName("common_tab_layout")

        # 添加左侧的配置布局
        self.left_config_layout = QGridLayout()
        self.left_config_layout.setObjectName("left_config_layout")
        # 在左侧的配置布局添加net_config_groupbox，属于中心部件
        self.net_config_groupbox = QGroupBox(self.centralwidget)
        self.net_config_groupbox.setMaximumSize(QSize(221, 16777215))
        # self.net_config_groupbox.setMinimumSize(QtCore.QSize(221, 200))
        self.net_config_groupbox.setObjectName("net_config_groupbox")
        # 在net_config_groupbox中添加网格布局
        self.net_config_gridlayout = QGridLayout(self.net_config_groupbox)
        self.net_config_gridlayout.setObjectName("net_config_gridlayout")
        # 添加协议选择
        self.protocol_lb = QLabel(self.net_config_groupbox)
        self.protocol_lb.setObjectName("protocol_lb")
        self.net_config_gridlayout.addWidget(self.protocol_lb, 0, 0, 1, 1)
        self.protocol_comboBox = QComboBox(self.net_config_groupbox)
        self.protocol_comboBox.setObjectName("protocol_comboBox")
        self.protocol_comboBox.addItem("")
        self.protocol_comboBox.addItem("")
        self.protocol_comboBox.addItem("")
        # self.protocol_comboBox.setCurrentIndex(2)
        self.protocol_comboBox.setEditable(False)
        self.net_config_gridlayout.addWidget(self.protocol_comboBox, 1, 0, 1, 1)
        self.ip_lb = QLabel(self.net_config_groupbox)
        self.ip_lb.setObjectName("ip_lb")
        self.net_config_gridlayout.addWidget(self.ip_lb, 2, 0, 1, 1)
        self.ip_cb = QComboBox(self.net_config_groupbox)
        self.ip_cb.setObjectName("ip_cb")
        self.ip_cb.setEditable(True)
        self.net_config_gridlayout.addWidget(self.ip_cb, 3, 0, 1, 1)
        self.port_lb = QLabel(self.net_config_groupbox)
        self.port_lb.setObjectName("port_lb")
        self.net_config_gridlayout.addWidget(self.port_lb, 4, 0, 1, 1)
        self.port_le = QLineEdit(self.net_config_groupbox)
        self.port_le.setObjectName("port_le")
        self.net_config_gridlayout.addWidget(self.port_le, 5, 0, 1, 1)
        self.link_bt = QPushButton(self.net_config_groupbox)
        self.link_bt.setObjectName("link_bt")
        self.net_config_gridlayout.addWidget(self.link_bt, 6, 0, 1, 1)
        self.multi_port_monitor_bt = QPushButton(self.net_config_groupbox)
        self.multi_port_monitor_bt.setObjectName("multi_port_monitor_bt")
        self.net_config_gridlayout.addWidget(self.multi_port_monitor_bt, 7, 0, 1, 1)
        self.multi_port_monitor_bt.hide()
        # self.multi_port_monitor_bt.hide()

        self.left_config_layout.addWidget(self.net_config_groupbox, 0, 0, 1, 1)

        # 在左侧的配置布局添加rx_config_groupbox，接收设置，属于中心部件
        self.rx_config_groupbox = QGroupBox(self.centralwidget)
        self.rx_config_groupbox.setObjectName("rx_config_groupbox")
        self.rx_config_groupbox.setMaximumSize(QSize(221, 16777215))
        # 在rx_config_groupbox中添加网格布局
        self.rx_config_gridlayout = QGridLayout(self.rx_config_groupbox)
        self.rx_config_gridlayout.setObjectName("rx_config_gridlayout")
        self.hex_rx_cb = QCheckBox(self.rx_config_groupbox)
        self.hex_rx_cb.setObjectName("hex_rx_cb")
        self.rx_config_gridlayout.addWidget(self.hex_rx_cb, 0, 0, 1, 1)
        self.rx_display_clear_btn = QPushButton(self.rx_config_groupbox)
        self.rx_display_clear_btn.setObjectName("rx_display_clear_btn")
        self.rx_config_gridlayout.addWidget(self.rx_display_clear_btn, 3, 1, 1, 1)

        self.left_config_layout.addWidget(self.rx_config_groupbox, 1, 0, 1, 1)

        # 在左侧的配置布局添加tx_config_groupbox，发送设置，属于中心部件
        self.tx_config_groupbox = QGroupBox(self.centralwidget)
        self.tx_config_groupbox.setObjectName("tx_config_groupbox")
        self.tx_config_groupbox.setMaximumSize(QSize(221, 16777215))
        # 在tx_config_groupbox中添加网格布局
        self.tx_config_gridlayout = QGridLayout(self.tx_config_groupbox)
        self.tx_config_gridlayout.setObjectName("tx_config_gridlayout")
        self.hex_tx_cb = QCheckBox(self.tx_config_groupbox)
        self.hex_tx_cb.setObjectName("hex_tx_cb")
        self.tx_config_gridlayout.addWidget(self.hex_tx_cb, 0, 0, 1, 1)
        self.tx_loop_layout = QHBoxLayout()
        self.tx_loop_layout.setObjectName("tx_loop_layout")
        self.tx_loop_checkbox = QCheckBox(self.tx_config_groupbox)
        self.tx_loop_checkbox.setObjectName("tx_loop_checkbox")
        self.tx_loop_layout.addWidget(self.tx_loop_checkbox)
        self.tx_loop_le = QLineEdit(self.tx_config_groupbox)
        self.tx_loop_le.setObjectName("tx_loop_le")
        self.tx_loop_layout.addWidget(self.tx_loop_le)
        self.tx_loop_ms_lb = QLabel(self.tx_config_groupbox)
        self.tx_loop_ms_lb.setObjectName("tx_loop_ms_lb")
        self.tx_loop_layout.addWidget(self.tx_loop_ms_lb)
        self.tx_config_gridlayout.addLayout(self.tx_loop_layout, 1, 0, 1, 2)

        self.tx_display_clear_btn = QPushButton(self.tx_config_groupbox)
        self.tx_display_clear_btn.setObjectName("tx_display_clear_btn")
        self.tx_config_gridlayout.addWidget(self.tx_display_clear_btn, 3, 1, 1, 1)

        self.left_config_layout.addWidget(self.tx_config_groupbox, 2, 0, 1, 1)

        # 添加右侧的显示布局
        self.right_display_layout = QGridLayout()
        self.right_display_layout.setObjectName("right_display_layout")

        # 在右侧布局中添加接收显示窗口组rx_display_group
        self.rx_display_groupbox = QGroupBox(self.centralwidget)
        self.rx_display_groupbox.setObjectName("rx_display_groupbox")
        self.rx_display_gridlayout = QGridLayout(self.rx_display_groupbox)
        self.rx_display_gridlayout.setObjectName("rx_display_gridlayout")

        self.rx_tb = QTextBrowser(self.rx_display_groupbox)
        self.rx_tb.setObjectName("rx_tb")
        self.rx_tb.setMinimumSize(420, 150)
        self.rx_display_gridlayout.addWidget(self.rx_tb, 0, 0, 1, 1)
        # self.rx_display_gridlayout.setVerticalSpacing(0)

        self.right_display_layout.addWidget(self.rx_display_groupbox, 0, 0, 1, 1)

        # 在右侧布局中添加发送显示窗口组tx_display_group
        self.tx_display_groupbox = QGroupBox(self.centralwidget)
        self.tx_display_groupbox.setObjectName("tx_display_groupbox")
        self.tx_display_gridlayout = QGridLayout(self.tx_display_groupbox)
        self.tx_display_gridlayout.setObjectName("tx_display_gridlayout")
        self.tx_tb = QTextBrowser(self.tx_display_groupbox)
        self.tx_tb.setObjectName("tx_tb")
        self.tx_display_gridlayout.addWidget(self.tx_tb, 0, 0, 1, 1)

        self.right_display_layout.addWidget(self.tx_display_groupbox, 1, 0, 1, 1)

        # 在右侧布局中添加发送输入控制窗口组tx_input_control_group
        self.tx_input_control_groupbox = QGroupBox(self.centralwidget)
        self.tx_input_control_groupbox.setObjectName("tx_input_control_groupbox")
        self.tx_input_control_gridlayout = QGridLayout(self.tx_input_control_groupbox)
        self.tx_input_control_gridlayout.setObjectName("tx_input_control_gridlayout")
        # 通过widget中加入layout，可以实现组件的布局，又可以利用widget的hide()方法，十分牛
        self.tx_udp_config_layoutwidget = QWidget(self.tx_input_control_groupbox)
        self.tx_udp_config_layoutwidget.setObjectName("tx_udp_config_layoutwidget")
        # 在widget中加入layout时需要在创建layout的同时指定父组件为widget
        self.tx_udp_config_layout = QHBoxLayout(self.tx_udp_config_layoutwidget)
        self.tx_udp_config_layout.setObjectName("tx_udp_config_layout")
        self.udp_target_ip_lb = QLabel(self.tx_udp_config_layoutwidget)
        self.udp_target_ip_lb.setObjectName("udp_target_ip_lb")
        self.tx_udp_config_layout.addWidget(self.udp_target_ip_lb)
        self.udp_target_ip_le = QLineEdit(self.tx_udp_config_layoutwidget)
        self.udp_target_ip_le.setObjectName("udp_target_ip_le")
        self.tx_udp_config_layout.addWidget(self.udp_target_ip_le)
        self.udp_target_port_lb = QLabel(self.tx_udp_config_layoutwidget)
        self.udp_target_port_lb.setObjectName("udp_target_port_lb")
        self.tx_udp_config_layout.addWidget(self.udp_target_port_lb)
        self.udp_target_port_le = QLineEdit(self.tx_udp_config_layoutwidget)
        self.udp_target_port_le.setObjectName("udp_target_port_le")
        self.tx_udp_config_layout.addWidget(self.udp_target_port_le)
        self.tx_input_control_gridlayout.addWidget(self.tx_udp_config_layoutwidget, 0, 0, 1, 2)
        self.tx_input_te = QTextEdit(self.tx_input_control_groupbox)
        self.tx_input_te.setObjectName("tx_input_te")
        self.tx_input_control_gridlayout.addWidget(self.tx_input_te, 1, 0, 1, 1)
        self.tx_btn_layout = QVBoxLayout()
        self.tx_btn_layout.setObjectName("tx_btn_layout")
        self.tx_clear_btn = QPushButton(self.tx_input_control_groupbox)
        self.tx_clear_btn.setObjectName("tx_clear_btn")
        self.tx_btn_layout.addWidget(self.tx_clear_btn)
        self.tx_btn = QPushButton(self.tx_input_control_groupbox)
        self.tx_btn.setObjectName("tx_btn")
        self.tx_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.tx_btn_layout.addWidget(self.tx_btn)
        self.tx_input_control_gridlayout.addLayout(self.tx_btn_layout, 1, 1, 1, 1)

        self.right_display_layout.addWidget(self.tx_input_control_groupbox, 2, 0, 1, 1)

        self.common_tab_layout.addLayout(self.left_config_layout)
        self.common_tab_layout.addLayout(self.right_display_layout)
        # self.main_layout.addLayout(self.left_config_layout)
        # self.main_layout.addLayout(self.right_display_layout)

        self.debug_layout = QVBoxLayout()
        self.debug_layout.setObjectName("debug_layout")
        self.debug_tab.setLayout(self.debug_layout)
        self.ber_window_btn = QPushButton(self.debug_tab)
        self.ber_window_btn.setObjectName("ber_window_btn")
        self.ber_window_btn.setText("打开误比特率图窗")
        self.debug_layout.addWidget(self.ber_window_btn)

        self.cp_window_btn = QPushButton(self.debug_tab)
        self.cp_window_btn.setObjectName("cp_window_btn")
        self.cp_window_btn.setText("打开相关峰图窗")
        self.debug_layout.addWidget(self.cp_window_btn)

        # 十分重要的代码，不加会出问题
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.menu = QMenu("新建")
        self.menubar.addMenu(self.menu)
        self.new_window_action = QAction("新窗口")
        # self.new_window_action.connect()
        self.menu.addAction(self.new_window_action)
        self.config_menu = QAction("设置")
        self.menubar.addAction(self.config_menu)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Net_Kit"))
        self.net_config_groupbox.setTitle(_translate("MainWindow", "网络配置"))
        self.protocol_lb.setText(_translate("MainWindow", "协议类型"))
        self.protocol_comboBox.setItemText(0, _translate("MainWindow", "TCP服务端"))
        self.protocol_comboBox.setItemText(1, _translate("MainWindow", "TCP客户端"))
        self.protocol_comboBox.setItemText(2, _translate("MainWindow", "UDP"))
        self.ip_lb.setText(_translate("MainWindow", "IP"))
        self.port_lb.setText(_translate("MainWindow", "Port"))
        self.link_bt.setText(_translate("MainWindow", "连接"))
        self.multi_port_monitor_bt.setText(_translate("MainWindow", "多端口监听"))
        self.rx_config_groupbox.setTitle(_translate("MainWindow", "接收设置"))
        self.hex_rx_cb.setText(_translate("MainWindow", "hex接收"))
        self.rx_display_clear_btn.setText(_translate("MainWindow", "清空显示"))
        self.tx_config_groupbox.setTitle(_translate("MainWindow", "发送设置"))
        self.hex_tx_cb.setText(_translate("MainWindow", "hex发送"))
        self.tx_loop_checkbox.setText(_translate("MainWindow", "循环发送"))
        self.tx_loop_ms_lb.setText(_translate("MainWindow", "ms"))
        self.tx_display_clear_btn.setText(_translate("MainWindow", "清空显示"))
        self.rx_display_groupbox.setTitle(_translate("MainWindow", "接收区"))
        self.tx_display_groupbox.setTitle(_translate("MainWindow", "已发送的消息"))
        self.tx_input_control_groupbox.setTitle(_translate("MainWindow", "发送区"))
        self.udp_target_ip_lb.setText(_translate("MainWindow", "目标IP"))
        self.udp_target_port_lb.setText(_translate("MainWindow", "目标端口"))
        self.tx_input_te.setPlaceholderText(_translate("MainWindow", "请输入发送内容"))
        self.tx_clear_btn.setText(_translate("MainWindow", "清空"))
        self.tx_btn.setText(_translate("MainWindow", "发送"))


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    from PySide6.QtWidgets import QMainWindow
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    gui = Ui_NetKit()
    gui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

