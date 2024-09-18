# 模拟存储激活码绑定设备的字典
# 实际应用中可以存储在文件或数据库中
import hashlib
import time

from test import generate_activation_code
from test3 import get_device_fingerprint

activation_code_bindings = {}


def validate_activation_code_with_device(code: str) -> bool:
    try:
        duration_type, timestamp, unique_id, checksum = code.split('-')
        raw_string = f"{duration_type}-{timestamp}-{unique_id}"
        # 重新生成校验位
        expected_checksum = hashlib.sha256(raw_string.encode()).hexdigest()[:6].upper()
        if expected_checksum != checksum:
            return False  # 校验位不匹配

        # 获取当前设备指纹
        current_device_fingerprint = get_device_fingerprint()

        # 检查激活码是否已绑定设备
        if code in activation_code_bindings:
            if activation_code_bindings[code] != current_device_fingerprint:
                return False  # 该激活码已绑定到其他设备，校验失败
        else:
            # 第一次使用该激活码，绑定当前设备
            activation_code_bindings[code] = current_device_fingerprint

        # 校验时间是否过期（与之前的逻辑相同）
        timestamp = int(timestamp)
        current_time = int(time.time())
        duration_map = {
            'TEMP': 60,  # 临时码，1分钟
            '1M': 60,  # 1分钟码
            '1H': 3600,  # 1小时码
            '1D': 86400,  # 1天码
            '1W': 604800,  # 1周码
            '1MO': 2592000,  # 1个月码
            '6MO': 15552000,  # 6个月码
            'PERM': float('inf'),  # 永久码
        }

        if current_time > timestamp + duration_map.get(duration_type, 0):
            return False  # 已过期
        return True
    except Exception as e:
        return False  # 解析失败或错误
def get_device_fingerprint() -> str:
    # 获取设备的硬件信息，可以选择使用CPU、硬盘或主板信息
    device_info = platform.node() + platform.system() + platform.processor() + str(uuid.getnode())
    # 生成一个唯一的指纹（哈希值）
    fingerprint = hashlib.sha256(device_info.encode()).hexdigest()
    return fingerprint


# # 示例调用
# activation_code = generate_activation_code('1M')
# is_valid = validate_activation_code_with_device(activation_code)
# print("激活码是否有效:", is_valid)
