from pycomm3 import LogixDriver

# 建立一个连接PLC的函数
def connect_plc(ip_address):
    try:
        plc = LogixDriver(ip_address)
        plc.open()
        return plc
    except:
        print('连接PLC失败！')

# 读取PLC地址的函数
def read_plc_address(plc, address):
    return plc.read(address)

# 建立一个连接PLC的对象
plc = connect_plc('127.0.0.1')

# 读取PLC地址D500的值
value = read_plc_address(plc, 'D100')

# 输出读取到的值
print('PLC地址D100的值为：', value)
