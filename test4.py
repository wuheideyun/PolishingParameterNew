from cryptography.fernet import Fernet

# 生成并存储密钥
def generate_key() -> bytes:
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key

# 从文件中加载密钥
def load_key() -> bytes:
    with open("secret.key", "rb") as key_file:
        return key_file.read()

# 加密字符串
def encrypt_string(plain_text: str, key: bytes) -> bytes:
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(plain_text.decode())  # 将字符串加密
    return encrypted_message

# 解密字符串
def decrypt_string(encrypted_message: bytes, key: bytes) -> str:
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message).decode()  # 解密并解码为字符串
    return decrypted_message

# 示例调用
if __name__ == "__main__":
    # 第一次运行时生成密钥并存储在文件中
    # generate_key()

    # 从文件中加载密钥
    key = load_key()

    # 要加密的长字符串
    original_string = "这是一个需要加密的长字符串，包含大量内容......"

    # 加密
    encrypted = encrypt_string(original_string, key)
    print("加密后的字符串:", encrypted)

    # 解密
    decrypted = decrypt_string(encrypted, key)
    print("解密后的字符串:", decrypted)
