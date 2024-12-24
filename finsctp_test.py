import struct
import time

import FinsTcp

def short_to_bytes(value):
    low = value & 0xffff  # 获取低16位
    result = struct.pack('>H', low)  # 按大端序打包低16位
    return result
def int_to_bytes(value):
    high = (value >> 16) & 0xffff  # 高16位
    low = value & 0xffff  # 低16位
    result = struct.pack('>HH', low, high)# 按大端序打包低16位和高16位
    return result
def swap_bytes(data,dig):
    if dig == 4:
        if len(data) != 4:
            raise ValueError("Input data must be 4 bytes long.")
        return data[2:4] + data[0:2]
    elif dig == 2:
        if len(data) != 2:
            raise ValueError("Input data must be 2 bytes long.")
        return data[1:2] + data[0:1]

if __name__ == "__main__":
    tcp = FinsTcp.FinsTcp('192.168.4.1',9600,22)
    # value = tcp.read_short('DM.000',2)
    # print('DM.000:'+str(value.result_value[0]))
    # value = tcp.read_short('DM.300',2)
    # print('DM.300:'+str(value.result_value[0]))
    # value = tcp.read_short('DM.320',2)
    # print('DM.320:'+str(value.result_value[0]))
    # value = tcp.read_short('DM.100', 2)
    # print('DM.100:'+str(value.result_value[0]))
    # value = tcp.read_short('DM.120', 2)
    # print('DM.120:'+str(value.result_value[0]))
    # value = tcp.read_int('DM.140', 4)
    # print('DM.140:'+str(value.result_value[0]))
    # value = tcp.read_int('DM.160', 4)
    # print('DM.160:'+str(value.result_value[0]))
    # value = tcp.read_int('DM.180', 4)
    # print('DM.180:'+str(value.result_value[0]))
    # value = tcp.read_long('DM.220', 4)
    # print('DM.220:'+str(value.result_value[0]))

    # value = tcp.read_float('DM.260', 4)
    # print('DM.260:'+str(value.result_value[0]))
    # value = tcp.read_float('DM.280', 4)
    # print('DM.280:'+str(value.result_value[0]))





    # 写入测试

    # value = tcp.read_short('DM.000',2)
    # print('电机运行信号DM.000:'+str(value.result_value[0]))
    # value = tcp.read_short('DM.300',2)
    # print('启动信号DM.300:'+str(value.result_value[0]))
    # value = tcp.read_short('DM.320',2)
    # print('停止信号DM.320:'+str(value.result_value[0]))
    # value = tcp.read_short('DM.100', 2)

    # tcp.write_short('DM.300',[1])
    # value = tcp.read_short('DM.300',2)
    # print('信号DM.300:'+str(value.result_value[0]))
    values = -1234789
    value = tcp.read_float('DM.260',2)
    print(value.result_value[0])
    tcp.write_float('DM.2260',values)
    tcp.disconnect()
    time.sleep(1)
    tcp = FinsTcp.FinsTcp('192.168.4.1',9600,22)
    value = tcp.read_float('DM.260', 2)
    print(value.result_value[0])



    tcp.disconnect()


