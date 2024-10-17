import socket
import struct

# 创建 FINS 请求
def create_fins_request(command, data_area, address, size):
    request = bytearray()
    request.extend(b'\x46\x49\x4E\x53')  # FINS 协议标识
    request.extend(b'\x00\x00\x00\x00')  # 数据长度（后面填充）
    request.extend(struct.pack('>B', 0x01))  # 版本
    request.extend(b'\x00\x00')  # 服务类型（读取/写入）
    request.extend(struct.pack('>B', command))  # 指令
    request.extend(struct.pack('>B', data_area))  # 数据区
    request.extend(struct.pack('>H', address))  # 地址
    request.extend(struct.pack('>H', size))  # 数据大小
    length = len(request) - 4
    request[4:6] = struct.pack('>H', length)  # 更新数据长度
    return request

# 发送 FINS 请求
def send_fins_request(ip, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(request, (ip, port))
        response, _ = sock.recvfrom(1024)
        return response

# 读取数据
def read_data(ip, port, data_area, address, size):
    request = create_fins_request(0x01, data_area, address, size)  # 读取指令
    response = send_fins_request(ip, port, request)
    return response

# 写入数据
def write_data(ip, port, data_area, address, value):
    request = create_fins_request(0x00, data_area, address, 1)  # 写入指令
    request.extend(struct.pack('>H', value))  # 添加要写入的值
    response = send_fins_request(ip, port, request)
    return response

# 示例用法
ip = '127.0.0.1'  # 替换为你的PLC IP
port = 9600  # 替换为你的PLC端口

# 读取数据
data_area = 0x01  # 数据区（D区）
address = 100  # 地址
size = 1  # 读取大小
response = read_data(ip, port, data_area, address, size)
print(f'Read response: {response}')

# 写入数据
value = 123  # 要写入的值
response = write_data(ip, port, data_area, address, value)
print(f'Write response: {response}')
