import os
from collections import Counter
from PySide6.QtCore import QSettings
import json

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
        :param config_data: 包含所有配置的大字典。
        """
        # --- 保存全局配置 ---
        if 'global' in config_data:
            self.settings.beginGroup('Global')
            for key, value in config_data['global'].items():
                self.settings.setValue(key, value)
            self.settings.endGroup()
        if 'speed_conversions' in config_data:
            self.settings.beginGroup('SpeedConversions')
            # 将字典转换为 JSON 字符串
            # ensure_ascii=False 确保中文字符不会被转义
            json_string = json.dumps(config_data['speed_conversions'], ensure_ascii=False)
            self.settings.setValue('data', json_string)
            self.settings.endGroup()
        # --- 保存设备间距 ---
        if 'spacings' in config_data:
            self.settings.beginGroup('Spacing')
            self.settings.remove("")  # 清除旧的间距数据
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
            all_groups = self.settings.childGroups()
            for group in all_groups:
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

        config_data['global']['whole_line_calc_enabled'] = self.settings.value(
            'whole_line_calc_enabled', False, type=bool
        )
        self.settings.endGroup()

        self.settings.beginGroup('SpeedConversions')
        json_string = self.settings.value('data', '{}')
        try:
            # 将 JSON 字符串解析回 Python 字典
            config_data['speed_conversions'] = json.loads(json_string)
        except json.JSONDecodeError:
            # 如果解析失败（例如文件内容损坏），则返回一个安全的空字典
            config_data['speed_conversions'] = {}
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

    def get_grit_counts(self) -> list:
        """
        1. 返回一个嵌套列表，每个子列表代表一台抛光机的磨块目数汇总 (从小到大排序)。
        """
        config = self.load_config()
        result_list = []

        for device in config.get('devices', []):
            device_grits = device.get('grinding_config', [])

            if not device_grits:
                result_list.append([])
                continue

            grit_counts = Counter(device_grits)

            current_device_result = []
            for grit in self.GRIT_ORDER:
                if grit in grit_counts:
                    current_device_result.append(grit_counts[grit])

            result_list.append(current_device_result)

        return result_list

    def get_all_head_counts(self) -> list:
        """
        2. 返回所有抛光机的磨头数列表。
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
    def get_all_ceramic_widths(self) -> list:
        """
        5. 返回所有抛光机的进砖宽度(ceramic_width)列表。
        """
        config = self.load_config()
        ceramic_width = []
        for device in config.get('devices', []):
            try:
                value = float(device.get('ceramic_width', 0.0))
                ceramic_width.append(value)
            except (ValueError, TypeError):
                ceramic_width.append(0.0)
        return ceramic_width

    def get_all_belt_speeds(self) -> list:
        """
        6. 返回所有抛光机的主皮带速度(belt_speed)列表。
        """
        config = self.load_config()
        belt_speed = []
        for device in config.get('devices', []):
            try:
                value = float(device.get('belt_speed', 0.0))
                belt_speed.append(value)
            except (ValueError, TypeError):
                belt_speed.append(0.0)
        return belt_speed
    def get_all_beam_swing_tempos(self) -> list:
        """
        7. 返回所有抛光机的横梁摆动快慢(beam_swing_tempo)列表。
        """
        config = self.load_config()
        beam_swing_tempo = []
        for device in config.get('devices', []):
            try:
                value = int(device.get('beam_swing_tempo', 0))
                beam_swing_tempo.append(value)
            except (ValueError, TypeError):
                beam_swing_tempo.append(0)
        return beam_swing_tempo
if __name__ == '__main__':
    # 这是一个测试用的示例数据
    sample_data_for_test = {
        'global': {'machine_count': 3, 'whole_line_calc_enabled': True},
        'spacings': ['1000.50', '1200.25'],
        'devices': [
            {'type': '单头摆', 'head_count': '14', 'between': '650.5', 'beam_between': '1900.0',
             'grinding_config': ['180', '180', '180', '180', '240', '240', '240', '240', '240', '240', '400', '400',
                                 '400', '400']},
            {'type': '双头摆', 'head_count': '16', 'between': '660', 'beam_between': '2000.75',
             'grinding_config': ['180', '180', '180', '180', '180', '180', '320', '320', '320', '320', '800', '800',
                                 '800', '800', '3000', '3000']},
            {'type': '同步摆', 'head_count': '6', 'between': '550.0', 'beam_between': '', 'grinding_config': []}
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

    print("\n--- 正在加载并验证保存的数据 ---")
    loaded_data = manager.load_config()
    import json

    print(json.dumps(loaded_data, indent=4, ensure_ascii=False))

    # 验证布尔值是否正确加载
    is_calc_enabled = loaded_data.get('global', {}).get('whole_line_calc_enabled')
    print(f"\n整线计算是否启用: {is_calc_enabled} (类型: {type(is_calc_enabled)})")
    assert isinstance(is_calc_enabled, bool)

    print('测试------------------')
    print(manager.get_grit_counts())