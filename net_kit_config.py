# -*- coding: utf-8 -*-

import json
import os


class NetKitConfig:
    """
    储存默认配置的类
    """
    def __init__(self, config_file=None):
        """
        初始化设置
        """
        # 普通
        # default端口
        self.default_port = 9000
        self.default_hex_rx_index = 1
        self.default_hex_tx_index = 1

        # default循环发送间隔
        self.default_loop_interval = 1000   # ms
        # default协议dict
        self.default_protocol_index_dict = {
            "TCP服务端": 0,
            "TCP客户端": 1,
            "UDP": 2
        }
        # 默认显示UDP界面
        self.default_protocol_index = 2
        # default udp目标IP
        self.default_udp_target_ip = "192.168.1.255"

        # default ber_update_interval
        self.default_ber_update_interval = 100  # ms

        # default ber_update_interval
        self.default_cp_update_interval = 100  # ms

        # default fresh window interval
        self.default_fresh_window_interval = 20     # ms

        self.default_ber_listen_port = 9001
        self.default_cp_listen_port = 9002
        self.default_unknown_listen_port = 9003

        # 如果提供了配置文件，则读取配置文件中的数据
        if config_file:
            self.load_from_json(config_file)

    def to_dict(self):
        """
        将类属性转换为字典
        """
        return self.__dict__

    def save_to_json(self, file_path):
        """
        将类数据保存到JSON文件中
        """
        data = self.to_dict()
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        print("save success!")

    def load_from_json(self, file_path):
        """
        从JSON文件加载数据并更新类的属性
        """
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                self.__dict__.update(data)
                # print(f"Loaded data from JSON: {data}")  # 添加调试输出
                print("Config updated from JSON")
        else:
            print(f"File {file_path} does not exist")


# 使用示例1,写入类中的默认值到json
# config = NetKitConfig()
# config.save_to_json('netkit_config.json')
# print(config.default_ber_update_interval)

# 使用示例2，从json写入,改变的是实例的值
# config = NetKitConfig("netkit_config.json")
# print(config.default_ber_update_interval)

# 使用示例3,改变值，写入json
# config = NetKitConfig()
#
# print(config.default_ber_update_interval)
#
# config.default_ber_update_interval = 400
# config.save_to_json("netkit_config.json")

