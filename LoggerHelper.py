import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

class LoggerHelper:
    def __init__(self, logger_name, log_dir='D:/logs'):
        self.logger_name = logger_name
        self.log_dir = log_dir
        self.logger = self._setup_logger()

    def _setup_logger(self):
        # 获取当前日期
        current_date = datetime.now().strftime('%Y-%m-%d')
        # 创建日志目录
        daily_log_dir = os.path.join(self.log_dir, current_date)
        if not os.path.exists(daily_log_dir):
            os.makedirs(daily_log_dir)

        # 创建日志文件路径
        log_file = os.path.join(daily_log_dir, f'{self.logger_name}.log')

        # 创建 logger
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(logging.DEBUG)

        # 创建 TimedRotatingFileHandler，按天分割日志
        handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7, encoding='utf-8')
        handler.suffix = "%Y-%m-%d"  # 设置日志文件名后缀为日期
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # 添加 handler 到 logger
        logger.addHandler(handler)

        return logger

    def log(self, level, message):
        """对外提供的日志记录接口"""
        if level == 'debug':
            self.logger.debug(message)
        elif level == 'info':
            self.logger.info(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'critical':
            self.logger.critical(message)
        else:
            raise ValueError(f"Invalid log level: {level}")

    def log_multiple_params(self, level, *args):
        """接收不定数量的多个参数，并在同一行显示"""
        # 格式化参数
        formatted_params = ', '.join([f'{key}[ {value} ]' for key, value in args])
        # 获取当前时间
        current_time = datetime.now().strftime('%y-%m-%d %H:%M:%S')
        # 构建日志消息
        log_message = f'[{current_time}]>>{formatted_params}'
        # 记录日志
        self.log(level, formatted_params)

# 示例使用
if __name__ == "__main__":
    logger = LoggerHelper('my_app')
    logger.log('info', 'This is an info message.')
    logger.log('error', 'This is an error message.')
    logger.log_multiple_params('info', ('轨道', '3012_储砖轨道'), ('倒库', 'True -> False'), ('等级', '3 -> 0'), ('备注', '已生成一次倒库任务'))