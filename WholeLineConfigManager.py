import configparser
import os
from PySide6.QtCore import QSettings


class WholeLineConfigManager:
    """
    负责整线配置文件的读取和写入，将复杂的配置文件操作封装成对象。
    """

    def __init__(self, config_filename="whole_line_config.ini"):
        self.config_path = os.path.join(os.getcwd(), config_filename)
        self.settings = QSettings(self.config_path, QSettings.IniFormat)

    def save_config(self, config_data: dict):
        """
        将一个结构化的字典保存到 .ini 文件中。
        :param config_data: 包含所有配置的大字典。
        """
        # --- 保存全局配置 ---
        if 'global' in config_data:
            self.settings.beginGroup('Global')
            for key, value in config_data['global'].items():
                self.settings.setValue(key, value)
            self.settings.endGroup()

        # --- 保存设备间距 ---
        if 'spacings' in config_data:
            self.settings.beginGroup('Spacing')
            # 清除旧的间距数据，防止数量减少时留下脏数据
            self.settings.remove("")
            for i, value in enumerate(config_data['spacings']):
                self.settings.setValue(f'spacing_{i + 1}_{i + 2}', value)
            self.settings.endGroup()

        # --- 保存通讯配置 ---
        if 'communication' in config_data:
            self.settings.beginGroup('Communication')
            self.settings.remove("")
            for i, comm in enumerate(config_data['communication']):
                self.settings.setValue(f'ip_{i + 1}', comm.get('ip', ''))
                self.settings.setValue(f'port_{i + 1}', comm.get('port', ''))
            self.settings.endGroup()

        # --- 保存每台设备的详细配置 ---
        if 'devices' in config_data:
            # 先清除所有旧的 [Device_X] 节
            for group in self.settings.childGroups():
                if group.startswith('Device_'):
                    self.settings.remove(group)

            for i, device_data in enumerate(config_data['devices']):
                group_name = f'Device_{i + 1}'
                self.settings.beginGroup(group_name)
                for key, value in device_data.items():
                    # 对列表（磨块配置）特殊处理，转为字符串
                    if isinstance(value, list):
                        self.settings.setValue(key, ",".join(map(str, value)))
                    else:
                        self.settings.setValue(key, value)
                self.settings.endGroup()

        # 确保所有写入都已同步到文件
        self.settings.sync()
        print(f"配置已成功保存到 {self.config_path}")

    def load_config(self) -> dict:
        """
        从 .ini 文件中读取配置，并组装成一个结构化的字典返回。
        """
        config_data = {
            'global': {},
            'spacings': [],
            'devices': [],
            'communication': []
        }

        # --- 读取全局配置 ---
        self.settings.beginGroup('Global')
        config_data['global']['machine_count'] = self.settings.value('machine_count', 1, type=int)
        self.settings.endGroup()

        machine_count = config_data['global']['machine_count']

        # --- 读取设备间距 ---
        self.settings.beginGroup('Spacing')
        spacings = []
        for i in range(machine_count - 1):
            spacings.append(self.settings.value(f'spacing_{i + 1}_{i + 2}', ''))
        config_data['spacings'] = spacings
        self.settings.endGroup()

        # --- 读取通讯配置 ---
        self.settings.beginGroup('Communication')
        comms = []
        for i in range(machine_count):
            comm = {
                'ip': self.settings.value(f'ip_{i + 1}', ''),
                'port': self.settings.value(f'port_{i + 1}', '')
            }
            comms.append(comm)
        config_data['communication'] = comms
        self.settings.endGroup()

        # --- 读取每台设备的详细配置 ---
        devices = []
        for i in range(machine_count):
            device_data = {}
            group_name = f'Device_{i + 1}'
            self.settings.beginGroup(group_name)

            keys = self.settings.childKeys()
            for key in keys:
                value = self.settings.value(key)
                # 对磨块配置特殊处理，转回列表
                if key == 'grinding_config' and value:
                    device_data[key] = value.split(',')
                else:
                    device_data[key] = value

            devices.append(device_data)
            self.settings.endGroup()
        config_data['devices'] = devices

        return config_data


# --- 用于独立测试 ---
if __name__ == '__main__':
    # 这是一个测试用的示例数据
    sample_data = {
        'global': {'machine_count': 2},
        'spacings': ['100.5'],
        'devices': [
            {'type': '单头摆', 'head_count': '8', 'head_spacing': '650', 'beam_spacing': '1900',
             'grinding_config': ['140', '180', '240']},
            {'type': '双头摆', 'head_count': '10', 'head_spacing': '660', 'beam_spacing': '2000',
             'grinding_config': ['320', '400', '600']}
        ],
        'communication': [
            {'ip': '192.168.1.10', 'port': '9600'},
            {'ip': '192.168.1.11', 'port': '9600'}
        ]
    }

    # 创建管理器实例
    manager = WholeLineConfigManager()

    # 测试保存
    print("--- 正在测试保存 ---")
    manager.save_config(sample_data)

    # 测试加载
    print("\n--- 正在测试加载 ---")
    loaded_data = manager.load_config()
    import json

    print(json.dumps(loaded_data, indent=4, ensure_ascii=False))