import os
from collections import Counter
from PySide6.QtCore import QSettings


class WholeLineConfigManager:
    """
    负责整线配置文件的读取和写入，并将配置数据处理成算法需要的格式。
    """

    def __init__(self, config_filename="whole_line_config.ini"):
        self.config_path = os.path.join(os.getcwd(), config_filename)
        self.settings = QSettings(self.config_path, QSettings.IniFormat)

        # 定义标准的磨块目数顺序，用于排序
        self.GRIT_ORDER = ["140", "180", "240", "320", "400", "600", "800", "1000", "1200", "2000", "3000", "5000"]

    def save_config(self, config_data: dict):
        """
        将一个结构化的字典保存到 .ini 文件中。
        """
        if 'global' in config_data:
            self.settings.beginGroup('Global')
            for key, value in config_data['global'].items():
                self.settings.setValue(key, value)
            self.settings.endGroup()
        if 'spacings' in config_data:
            self.settings.beginGroup('Spacing')
            self.settings.remove("")
            for i, value in enumerate(config_data['spacings']):
                self.settings.setValue(f'spacing_{i + 1}_{i + 2}', value)
            self.settings.endGroup()
        if 'communication' in config_data:
            self.settings.beginGroup('Communication')
            self.settings.remove("")
            for i, comm in enumerate(config_data['communication']):
                self.settings.setValue(f'ip_{i + 1}', comm.get('ip', ''))
                self.settings.setValue(f'port_{i + 1}', comm.get('port', ''))
            self.settings.endGroup()
        if 'devices' in config_data:
            for group in self.settings.childGroups():
                if group.startswith('Device_'):
                    self.settings.remove(group)
            for i, device_data in enumerate(config_data['devices']):
                group_name = f'Device_{i + 1}'
                self.settings.beginGroup(group_name)
                for key, value in device_data.items():
                    if isinstance(value, list):
                        self.settings.setValue(key, ",".join(map(str, value)))
                    else:
                        self.settings.setValue(key, value)
                self.settings.endGroup()
        self.settings.sync()
        print(f"配置已成功保存到 {self.config_path}")

    def load_config(self) -> dict:
        """
        从 .ini 文件中读取配置，并组装成一个结构化的字典返回。
        """
        config_data = {'global': {}, 'spacings': [], 'devices': [], 'communication': []}
        self.settings.beginGroup('Global')
        config_data['global']['machine_count'] = self.settings.value('machine_count', 1, type=int)
        self.settings.endGroup()
        machine_count = config_data['global']['machine_count']
        self.settings.beginGroup('Spacing')
        spacings = []
        for i in range(machine_count - 1):
            spacings.append(self.settings.value(f'spacing_{i + 1}_{i + 2}', ''))
        config_data['spacings'] = spacings
        self.settings.endGroup()
        self.settings.beginGroup('Communication')
        comms = []
        for i in range(machine_count):
            comm = {'ip': self.settings.value(f'ip_{i + 1}', ''), 'port': self.settings.value(f'port_{i + 1}', '')}
            comms.append(comm)
        config_data['communication'] = comms
        self.settings.endGroup()
        devices = []
        for i in range(machine_count):
            device_data = {}
            group_name = f'Device_{i + 1}'
            self.settings.beginGroup(group_name)
            keys = self.settings.childKeys()
            for key in keys:
                value = self.settings.value(key)
                if key == 'grinding_config' and value:
                    device_data[key] = value.split(',')
                else:
                    device_data[key] = value
            devices.append(device_data)
            self.settings.endGroup()
        config_data['devices'] = devices
        return config_data


    def get_grinding_counts(self) -> list:
        """
        1. 返回一个嵌套列表，每个子列表代表一台抛光机的磨块目数汇总 (从小到大排序)。
        例如：[[4, 6, 4], [6, 6, 4]]
        """
        config = self.load_config()
        result_list = []

        # 遍历每一台设备
        for device in config.get('devices', []):
            device_grits = device.get('grinding_config', [])

            if not device_grits:
                result_list.append([])  # 如果该设备没有配置磨块，则添加一个空列表
                continue

            # 使用 Counter 统计当前设备的每种目数数量
            grit_counts = Counter(device_grits)

            # 按照预定义的 GRIT_ORDER 顺序来生成当前设备的结果列表
            current_device_result = []
            for grit in self.GRIT_ORDER:
                if grit in grit_counts:
                    current_device_result.append(grit_counts[grit])

            result_list.append(current_device_result)

        return result_list

    def get_all_head_counts(self) -> list:
        """
        2. 返回所有抛光机的磨头数列表。
        例如：[10, 20, 30]
        """
        config = self.load_config()
        head_counts = []
        for device in config.get('devices', []):
            try:
                count = int(device.get('head_count', 0))
                head_counts.append(count)
            except (ValueError, TypeError):
                head_counts.append(0)
        return head_counts

    def get_all_betweens(self) -> list:
        """
        3. 返回所有抛光机的磨头间距(between)列表。
        例如：[500.0, 500.0, 600.5, 700.0]
        """
        config = self.load_config()
        betweens = []
        for device in config.get('devices', []):
            try:
                value = float(device.get('between', 0.0))
                betweens.append(value)
            except (ValueError, TypeError):
                betweens.append(0.0)
        return betweens

    def get_all_beam_betweens(self) -> list:
        """
        4. 返回所有抛光机的横梁间距(beam_between)列表。
        例如：[1900.0, 1900.0, 2000.0, 2100.0]
        """
        config = self.load_config()
        beam_betweens = []
        for device in config.get('devices', []):
            try:
                value = float(device.get('beam_between', 0.0))
                beam_betweens.append(value)
            except (ValueError, TypeError):
                beam_betweens.append(0.0)
        return beam_betweens


# --- 用于独立测试 ---
if __name__ == '__main__':
    # 创建一个内容更丰富的示例数据用于测试
    sample_data_for_test = {
        'global': {'machine_count': 3},
        'spacings': ['1000.50', '1200.25'],
        'devices': [
            {'type': '单头摆', 'head_count': '14', 'between': '650.5', 'beam_between': '1900.0',
             'grinding_config': ['180', '180', '180', '180', '240', '240', '240', '240', '240', '240', '400', '400',
                                 '400', '400']},
            {'type': '双头摆', 'head_count': '16', 'between': '660', 'beam_between': '2000.75',
             'grinding_config': ['180', '180', '180', '180', '180', '180', '320', '320', '320', '320', '800', '800',
                                 '800', '800', '3000', '3000']},
            {'type': '同步摆', 'head_count': '6', 'between': '550.0', 'beam_between': '', 'grinding_config': []}
            # 测试没有配置磨块的情况
        ],
        'communication': [
            {'ip': '192.168.1.10', 'port': '9600'},
            {'ip': '192.168.1.11', 'port': '9600'},
            {'ip': '192.168.1.12', 'port': '9600'}
        ]
    }

    manager = WholeLineConfigManager()
    print("--- 正在保存测试数据 ---")
    manager.save_config(sample_data_for_test)

    print("\n--- 测试新增的四个方法 ---")

    # 1. 磨块目数汇总 (分组)
    # 预期结果:
    # Device 1: 180目有4个, 240目有6个, 400目有4个 -> [4, 6, 4]
    # Device 2: 180目有6个, 320目有4个, 800目有4个, 3000目有2个 -> [6, 4, 4, 2]
    # Device 3: 没有配置 -> []
    # 最终返回: [[4, 6, 4], [6, 4, 4, 2], []]
    grit_counts = manager.get_grinding_counts()
    print(f"1. 磨块目数汇总 (分组): {grit_counts}")

    # 2. 所有抛光机磨头数
    # 预期结果: [14, 16, 6]
    head_counts = manager.get_all_head_counts()
    print(f"2. 所有抛光机磨头数: {head_counts}")

    # 3. 所有抛光机磨头间距
    # 预期结果: [650.5, 660.0, 550.0]
    betweens = manager.get_all_betweens()
    print(f"3. 所有抛光机磨头间距 (between): {betweens}")

    # 4. 所有抛光机横梁间距
    # 预期结果: [1900.0, 2000.75, 0.0]
    beam_betweens = manager.get_all_beam_betweens()
    print(f"4. 所有抛光机横梁间距 (beam_between): {beam_betweens}")