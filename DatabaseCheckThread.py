from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import QThread, Signal, QSettings
import time
import sqlite3  # 假设使用sqlite数据库


# 模拟数据库查询的线程
class DatabaseCheckThread(QThread):
    # 定义一个信号，当校验完成时发送结果
    result_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.interval = 1

        self.settings = QSettings("config.ini", QSettings.IniFormat)  # 使用配置文件
        self.is_running = True  # 控制线程的执行状态

    def run(self):
        while self.is_running:
            activation_code = self.settings.value("activation_code", "")  # 获取激活码
            if activation_code != "":  # 若数据库查询功能被启用
                result = self.check_database(activation_code)
                self.result_signal.emit(result)  # 发送查询结果到主线程
                time.sleep(self.interval)  # 模拟每5秒查询一次

    def check_database(self,activation_code):
        # 模拟查询数据库，这里是使用 sqlite3 示例
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT key,created_at FROM keys WHERE content = '{activation_code}' order by created_at DESC LIMIT 1;")
            result = cursor.fetchone()
            conn.close()
            if result:
                duration_type, unique_id, checksum = result[0].split('-')
                current_time = int(time.time())  # 当前时间戳
                # 检查激活码是否已过期
                duration_map = {
                    'TEMP': 60,  # 临时码，1分钟
                    '1M': 60,  # 1分钟码
                    '2M': 120,  # 2分钟码
                    '1H': 3600,  # 1小时码
                    '1D': 86400,  # 1天码
                    '1W': 604800,  # 1周码
                    '1MO': 2592000,  # 1个月码
                    '6MO': 15552000,  # 6个月码
                    'PERM': float('inf'),  # 永久码
                }

                if duration_type == 'PERM':
                    # self.is_running = False
                    return "永久!"

                valid_duration = duration_map.get(duration_type, 0)
                timeStamp = int(time.mktime(time.strptime(result[1], "%Y-%m-%d %H:%M:%S")))
                if current_time > timeStamp + valid_duration:
                    return "未激活！"
                else:

                    return str(self.time_shift(timeStamp + valid_duration - current_time))
            else:
                return "未激活！"
        except Exception as e:
            return f"Database error: {e}"

    def stop(self):
        self.is_running = False  # 停止线程

    def time_shift(self,seconds):
        if seconds < 60:
            self.interval = 1
            return f"{seconds}秒"

        if seconds < 120:
            self.interval = 1
        else:
            self.interval = 30
        # 计算一天的秒数
        day_seconds = 24 * 3600
        # 如果秒数超过24小时，计算天数和剩余时间
        if seconds >= day_seconds:
            days = seconds // day_seconds
            seconds %= day_seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{days}天{hours:02}:{minutes:02}分"

        # 如果秒数在24小时内，直接转换为小时和分钟
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours:02}:{minutes:02}分"