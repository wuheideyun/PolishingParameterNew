import os
import logging
from datetime import datetime
# 1. 创建每日文件夹
#def create_daily_log_folder(base_folder='logs'):
#    pass
    # # 获取当前日期
    # today = datetime.today().strftime('%Y-%m-%d')
    # # 构建文件夹路径
    # folder_path = os.path.join(base_folder, today)
    # # 如果文件夹不存在则创建
    # if not os.path.exists(folder_path):
    #     os.makedirs(folder_path)
    # return folder_path
def create_daily_log_folder(base_folder='D:/logs'):
    # 获取当前日期
    today = datetime.today().strftime('%Y-%m-%d')
    # 构建文件夹路径
    folder_path = os.path.join(base_folder, today)
    # 如果文件夹不存在则创建
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except Exception as e:
        print(f"创建日志文件夹时出错: {e}")
        return None  # 或者可以选择抛出异常

    return folder_path
# 2. 设置日志记录
def setup_logger(log_name, log_file, level=logging.INFO):
    """配置logger，输出到指定文件"""
    logger = logging.getLogger(log_name)
    logger.setLevel(level)
    # 创建文件处理器，写入到指定的日志文件
    fh = logging.FileHandler(log_file)
    fh.setLevel(level)
    # 定义日志格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # 如果 logger 没有 handler 则添加一个
    if not logger.handlers:
        logger.addHandler(fh)
    return logger
# 参数变更日志记录函数封装----同步摆计算系统----
def log_equal_cal_parm_change(button_name,between,grind_size,belt_speed,accelerate,radius,ceramic_width,beam_speed_up,overlap,
                           beam_swing_speed,beam_constant_time,stay_time,num,swing):
    # 获取每日文件夹路径
    folder_path = create_daily_log_folder()
    # 创建日志文件的路径
    param_change_log_path = os.path.join(folder_path, 'param_change.log')
    # 设置 logger，分别记录到不同的文件
    param_logger = setup_logger('param_logger', param_change_log_path)
    # 记录 按键操作 和 参数变更前后数值
    param_logger.info(f"---------------------Equal_Parameter_Calculate---------------------\n"
                      f"The user enters parameter information:\n"
                      f"{'between:':^20} {between:^6} {'geind_size:':^20} {grind_size:^6} {'belt_speed:':^20} {belt_speed:^6} {'accelerate:':^20} {accelerate:^6} \n"
                      f"{'radius:':^20} {radius:^6} {'ceramic_width:':^20} {ceramic_width:^6} {'beam_speed_up:':^20} {beam_speed_up:^6} {'overlap:':^20} {overlap:^6}\n"
                      f"User clicks button:{button_name},the output parameter:\n"
                      f"{'beam_swing_speed:':^20} {beam_swing_speed:^6} {'beam_constant_time:':^20} {beam_constant_time:^6} {'stay_time:':^20} {stay_time:^6} {'num:':^20} {num:^6} {'swing:':^20} {swing:^6}\n")

# 参数变更日志记录函数封装----同步摆仿真系统----
def log_equal_simulation(button_name,between,grind_size,belt_speed,accelerate,radius,
                           beam_swing_speed,beam_constant_time,stay_time,num):
    # 获取每日文件夹路径
    folder_path = create_daily_log_folder()
    # 创建日志文件的路径
    param_change_log_path = os.path.join(folder_path, 'param_change.log')
    # 设置 logger，分别记录到不同的文件
    param_logger = setup_logger('param_logger', param_change_log_path)
    # 记录 按键操作 和 参数变更前后数值
    param_logger.info(f"---------------------Equal_Parameter_Simulation---------------------\n"
                      f"The user enters parameter information:\n"
                      f"{'belt_speed:':^20} {belt_speed:^6} {'beam_swing_speed:':^20} {beam_swing_speed:^6} {'beam_constant_time:':^20} {beam_constant_time:^6} {'stay_time:':^20} {stay_time:^6}"
                      f"{'accelerate:':^20} {accelerate:^6} {'num:':^20} {num:^6}\n"
                      f"{'between:':^20} {between:^6} {'radius:':^20} {radius:^6} {'geind_size:':^20} {grind_size:^6} \n"
                      f"User clicks button:{button_name}\n")

# 参数变更日志记录函数封装----双头摆计算系统----
def log_double_cal_parm_change(button_name,between,grind_size,belt_speed,accelerate,radius,ceramic_width,beam_speed_up,overlap,beam_between,num_set,group_count,
                           beam_swing_speed,beam_constant_time,stay_time,num,swing,delay_time):
    # 获取每日文件夹路径
    folder_path = create_daily_log_folder()
    # 创建日志文件的路径
    param_change_log_path = os.path.join(folder_path, 'param_change.log')
    # 设置 logger，分别记录到不同的文件
    param_logger = setup_logger('param_logger', param_change_log_path)
    # 记录 按键操作 和 参数变更前后数值
    param_logger.info(f"---------------------Double_Parameter_Calculate---------------------\n"
                      f"The user enters parameter information:\n"
                      f"{'between:':^20} {between:^6} {'geind_size:':^20} {grind_size:^6} {'belt_speed:':^20} {belt_speed:^6} {'accelerate:':^20} {accelerate:^6} \n"
                      f"{'radius:':^20} {radius:^6} {'ceramic_width:':^20} {ceramic_width:^6} {'beam_speed_up:':^20} {beam_speed_up:^6} {'overlap:':^20} {overlap:^6} {'beam_between:':^20} {beam_between:^6}\n"
                      f"{'num_set:':^20} {num_set:^6} {'group_count:':^20} {group_count:^6}\n"
                      f"User clicks button:{button_name},the output parameter:\n"
                      f"{'beam_swing_speed:':^20} {beam_swing_speed:^6} {'beam_constant_time:':^20} {beam_constant_time:^6} {'stay_time:':^20} {stay_time:^6} {'num:':^20} {num:^6}\n"
                      f"{'swing:':^20} {swing:^6} {'delay_time:':^20} {delay_time:^6}\n")

# 参数变更日志记录函数封装----双头摆仿真系统----
def log_double_simulation(button_name,belt_speed,beam_swing_speed,beam_constant_time,stay_time,accelerate,num,
                         between,beam_between,grind_size,radius,delay_time):
    # 获取每日文件夹路径
    folder_path = create_daily_log_folder()
    # 创建日志文件的路径
    param_change_log_path = os.path.join(folder_path, 'param_change.log')
    # 设置 logger，分别记录到不同的文件
    param_logger = setup_logger('param_logger', param_change_log_path)
    # 记录 按键操作 和 参数变更前后数值
    param_logger.info(f"---------------------Double_Parameter_Simulation---------------------\n"
                      f"The user enters parameter information:\n"
                      f"{'belt_speed:':^20} {belt_speed:^6} {'beam_swing_speed:':^20} {beam_swing_speed:^6} {'beam_constant_time:':^20} {beam_constant_time:^6} {'stay_time:':^20} {stay_time:^6}"
                      f"{'accelerate:':^20} {accelerate:^6} {'delay_time:':^20} {delay_time:^6} {'num:':^20} {num:^6}\n"
                      f"{'between:':^20} {between:^6} {'beam_between:':^20} {beam_between:^6} {'radius:':^20} {radius:^6} {'geind_size:':^20} {grind_size:^6} \n"
                      f"User clicks button:{button_name}\n")

# 参数变更日志记录函数封装----单头摆计算系统----
def log_single_cal_parm_change(button_name,between,grind_size,belt_speed,accelerate,radius,ceramic_width,beam_speed_up,overlap,beam_between,num_set,group_count,
                           beam_swing_speed,beam_constant_time,stay_time,num,swing,delay_time):
    # 获取每日文件夹路径
    folder_path = create_daily_log_folder()
    # 创建日志文件的路径
    param_change_log_path = os.path.join(folder_path, 'param_change.log')
    # 设置 logger，分别记录到不同的文件
    param_logger = setup_logger('param_logger', param_change_log_path)
    # 记录 按键操作 和 参数变更前后数值
    param_logger.info(f"---------------------Single_Parameter_Calculate---------------------\n"
                      f"The user enters parameter information:\n"
                      f"{'beam_between:':^20} {beam_between:^6} {'geind_size:':^20} {grind_size:^6} {'belt_speed:':^20} {belt_speed:^6} {'accelerate:':^20} {accelerate:^6} \n"
                      f"{'radius:':^20} {radius:^6} {'ceramic_width:':^20} {ceramic_width:^6} {'beam_speed_up:':^20} {beam_speed_up:^6} {'overlap:':^20} {overlap:^6}\n"
                      f"{'num_set:':^20} {num_set:^6} {'group_count:':^20} {group_count:^6}\n"
                      f"User clicks button:{button_name},the output parameter:\n"
                      f"{'beam_swing_speed:':^20} {beam_swing_speed:^6} {'beam_constant_time:':^20} {beam_constant_time:^6} {'stay_time:':^20} {stay_time:^6} {'num:':^20} {num:^6}\n"
                      f"{'swing:':^20} {swing:^6} {'delay_time:':^20} {delay_time:^6} {'between:':^20} {between:^6}\n")

# 参数变更日志记录函数封装----单头摆仿真系统----
def log_single_simulation(button_name,belt_speed,beam_swing_speed,beam_constant_time,stay_time,accelerate,num,
                         beam_between,grind_size,radius,delay_time):
    # 获取每日文件夹路径
    folder_path = create_daily_log_folder()
    # 创建日志文件的路径
    param_change_log_path = os.path.join(folder_path, 'param_change.log')
    # 设置 logger，分别记录到不同的文件
    param_logger = setup_logger('param_logger', param_change_log_path)
    # 记录 按键操作 和 参数变更前后数值
    param_logger.info(f"---------------------Single_Parameter_Simulation---------------------\n"
                      f"The user enters parameter information:\n"
                      f"{'belt_speed:':^20} {belt_speed:^6} {'beam_swing_speed:':^20} {beam_swing_speed:^6} {'beam_constant_time:':^20} {beam_constant_time:^6} {'stay_time:':^20} {stay_time:^6}"
                      f"{'accelerate:':^20} {accelerate:^6} {'delay_time:':^20} {delay_time:^6} {'num:':^20} {num:^6}\n"
                      f"{'beam_between:':^20} {beam_between:^6} {'radius:':^20} {radius:^6} {'geind_size:':^20} {grind_size:^6} \n"
                      f"User clicks button:{button_name}\n")
# 按钮  点击事件  日志记录函数封装
def log_button_click(button_name):
    # 获取每日文件夹路径
    folder_path = create_daily_log_folder()
    # 创建两个日志文件的路径
    button_click_log_path = os.path.join(folder_path, 'button_click.log')
    # 设置两个 logger，分别记录到不同的文件
    button_logger = setup_logger('button_logger', button_click_log_path)
    # 记录 按键操作 和 参数变更前后数值
    button_logger.info("User clicked %s button" %button_name)