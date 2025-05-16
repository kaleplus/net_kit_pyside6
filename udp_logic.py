#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading
from PySide6.QtCore import Signal, QObject


class UdpServer(QObject, threading.Thread):
    # 类变量，实例将会共享这个变量
    # 非高频发生事件，高频事件通过线程安全的queue传输
    udp_server_error_info_signal = Signal(str)
    udp_server_listen_info_signal = Signal(str)

    def __init__(self, host, port, udp_recv_queue):
        QObject.__init__(self)
        threading.Thread.__init__(self)
        self.daemon = True
        # 实例变量
        self.host = host
        self.port = port
        self.udp_server_running = True
        self.udp_server_socket = None
        self.udp_server_bind = True
        self.udp_recv_queue = udp_recv_queue

        self.udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        try:
            self.udp_server_socket.bind((self.host, self.port))
            msg = f"<br><span style='color: red;'>正在监听 {self.host}:{self.port}</span>"
            print(f"Socket successfully created and bound to {self.host}:{self.port}")
            self.udp_server_listen_info_signal.emit(msg)

        except OSError as e:
            msg = f"Failed to create or bind socket({e.errno}:{e.strerror})"
            print(msg)
            self.udp_server_error_info_signal.emit(msg)
        else:
            while self.udp_server_running:
                try:
                    recv_data, recv_addr = self.udp_server_socket.recvfrom(2048)
                    self.udp_recv_queue.put((recv_data, recv_addr))
                    # print((recv_data, recv_addr))

                except OSError as e:
                    print(f"udp server running error({e.errno}:{e.strerror})")
                    break

    def stop(self):
        if self.udp_server_socket:
            self.udp_server_running = False
            self.udp_server_socket.close()
            print("udp server socket closed")
            msg = f"<br><span style='color: red;'>停止监听 {self.host}:{self.port}</span>"
            self.udp_server_listen_info_signal.emit(msg)


class UdpClient(QObject):
    udp_client_error_info_signal = Signal(str)

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

        self.udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, byte_msg):
        try:
            self.udp_client_socket.sendto(byte_msg, (self.host, self.port))
            # print(f"Sent: {byte_msg} to {self.host}:{self.port}")
        except OSError as e:
            msg = f"Failed to send message {e.errno}:{e.strerror}"
            # print(msg)
            self.udp_client_error_info_signal.emit(msg)



