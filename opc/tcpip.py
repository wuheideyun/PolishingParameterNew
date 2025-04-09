from pymodbus.client import ModbusTcpClient

# PLC的IP地址和端口
PLC_IP = '192.168.4.1'
PLC_PORT = 9600

# 单元ID（通常是1，可能需要根据实际情况调整）
UNIT_ID = 1

# 要读取的保持寄存器的起始地址和数量
START_ADDRESS = 0
QUANTITY = 1

try:
    # 创建Modbus TCP客户端
    client = ModbusTcpClient(PLC_IP, port=PLC_PORT)

    # 连接到PLC
    if client.connect():
        print('连接成功')

        # 读取保持寄存器
        response = client.read_holding_registers(address=START_ADDRESS, count=QUANTITY, unit=UNIT_ID)

        if response.is_error():
            print(f'读取错误: {response}')
        else:
            # 获取读取的数据
            registers = response.registers
            print(f'读取到的数据: {registers}')

    else:
        print('连接失败')

finally:
    # 关闭连接
    client.close()
    print('连接已关闭')