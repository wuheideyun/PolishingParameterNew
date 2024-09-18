import hashlib
import platform
import uuid

def get_device_fingerprint() -> str:
    # 获取设备的硬件信息，可以选择使用CPU、硬盘或主板信息
    device_info = platform.node() + platform.system() + platform.processor() + str(uuid.getnode())
    # 生成一个唯一的指纹（哈希值）
    fingerprint = hashlib.sha256(device_info.encode()).hexdigest()
    return fingerprint
