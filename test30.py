import struct

# 将 4294967290 转换为大端序字节数组
value = 4294967290
byte_array = struct.pack('>I', value)  # '>I' 表示大端序的 uint32
print(byte_array)  # 输出: b'\xff\xff\xff\xfa'



# 将 4294967290 转换为小端序字节数组
value = 4294967290
byte_array = struct.pack('<I', value)  # '<I' 表示小端序的 uint32
print(byte_array)  # 输出: b'\xfa\xff\xff\xff'



def bytes_to_uint32_big_endian(byte_array):
    """
    将字节数组转换为大端序的 uint32 整数。

    :param byte_array: 字节数组，例如 b'\xff\xff\xff\xfa\x00\x00\x00\x00'
    :return: 解析后的整数，例如 4294967290
    """
    # 检查字节数组的长度是否为 4 的倍数
    if len(byte_array) % 4 != 0:
        raise ValueError("字节数组长度必须是 4 的倍数")

    # 初始化结果列表
    values = []

    # 每次解析 4 个字节
    for i in range(0, len(byte_array), 4):
        # 使用大端序解析 4 个字节为 uint32
        value = struct.unpack('>I', byte_array[i:i + 4])[0]
        values.append(value)

    return values

# 示例调用
byte_array = b'\xff\xff\xff\xfa\x00\x00\x00\x00'
result = bytes_to_uint32_big_endian(byte_array)
print(result)  # 输出: [4294967290, 0]


def bytes_to_float(byte_array, byte_order='big'):
    """
    将字节数组转换为浮点数。

    :param byte_array: 字节数组，例如 b'y\xa3L\xeb\x00\x00\x00\x00'
    :param byte_order: 字节序，'big' 表示大端序，'little' 表示小端序
    :return: 解析后的浮点数
    """
    if byte_order == 'big':
        # 使用大端序（Big-Endian）解析
        value = struct.unpack('>f', byte_array[:4])[0]
    elif byte_order == 'little':
        # 使用小端序（Little-Endian）解析
        value = struct.unpack('<f', byte_array[:4])[0]
    else:
        raise ValueError("不支持的字节序，请使用 'big' 或 'little'")

    return value

# 示例调用
byte_array = b'y\xa3L\xeb\x00\x00\x00\x00'
value_big = bytes_to_float(byte_array, 'big')  # 大端序解析
value_little = bytes_to_float(byte_array, 'little')  # 小端序解析

print("大端序解析结果:", value_big)
print("小端序解析结果:", value_little)

byte_array = b'L\xeby\xa3\x00\x00\x00\x00'
value_big = bytes_to_float(byte_array, 'big')  # 大端序解析
value_little = bytes_to_float(byte_array, 'little')  # 小端序解析

print("大端序解析结果:", value_big)
print("小端序解析结果:", value_little)