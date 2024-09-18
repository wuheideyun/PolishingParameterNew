import time
import random
import hashlib


def generate_activation_code(duration_type: str) -> str:
    timestamp = int(time.time())  # 当前时间戳
    unique_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=8))  # 8位唯一标识
    raw_string = f"{duration_type}-{timestamp}-{unique_id}"

    # 生成校验位 (使用SHA-256哈希生成前6位)
    checksum = hashlib.sha256(raw_string.encode()).hexdigest()[:6].upper()

    return f"{duration_type}-{timestamp}-{unique_id}-{checksum}"


# 示例调用：生成一分钟激活码
# activation_code = generate_activation_code('1M')
# print(activation_code)
