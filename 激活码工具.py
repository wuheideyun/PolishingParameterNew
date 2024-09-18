# 生成激活码
import hashlib
import random

from cryptography.fernet import Fernet


def generate_activation_code(duration_type: str) -> str:
    unique_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=8))  # 8位唯一标识
    raw_string = f"{duration_type}-{unique_id}"

    # 生成校验位 (使用SHA-256哈希生成前6位)
    checksum = hashlib.sha256(raw_string.encode()).hexdigest()[:6].upper()

    fernet = Fernet('lvpWRiS8TmjvizHmWLha18gr75tmQwUMzrB4g1PW3i0 =')
    oldcode = f"{duration_type}-{unique_id}-{checksum}"
    newcode = fernet.encrypt(oldcode.encode()).decode()
    return newcode


# # 示例调用
activation_code = generate_activation_code('1H')
print("激活码:", activation_code)
