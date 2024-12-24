from pycomm3 import LogixDriver

class OmronPLC:
    def __init__(self, ip_address, slot=0):
        """
        初始化与欧姆龙PLC的连接
        :param ip_address: PLC的IP地址
        :param slot: PLC的槽号（默认0）
        """
        self.ip_address = ip_address
        self.slot = slot
        self.driver = LogixDriver(ip_address)

    def connect(self):
        """
        连接到PLC
        """
        try:
            self.driver.open()
            print(f"成功连接到PLC：{self.ip_address}")
        except Exception as e:
            print(f"连接PLC失败：{e}")

    def disconnect(self):
        """
        断开与PLC的连接
        """
        try:
            self.driver.close()
            print("已断开与PLC的连接")
        except Exception as e:
            print(f"断开连接失败：{e}")

    def read_d_area(self, address):
        """
        读取D区数据
        :param address: D区地址（例如：D100）
        :return: 读取到的数据
        """
        try:
            result = self.driver.read(address)
            if result:
                print(f"读取D区地址 {address} 的数据：{result.value}")
                return result.value
            else:
                print(f"读取D区地址 {address} 失败")
                return None
        except Exception as e:
            print(f"读取D区地址 {address} 失败：{e}")
            return None

    def write_d_area(self, address, value):
        """
        写入D区数据
        :param address: D区地址（例如：D100）
        :param value: 要写入的数据
        """
        try:
            self.driver.write((address, value))
            print(f"成功写入D区地址 {address} 的数据：{value}")
        except Exception as e:
            print(f"写入D区地址 {address} 失败：{e}")

# 示例使用
if __name__ == "__main__":
    # PLC的IP地址
    plc_ip = "192.168.4.1"

    # 创建PLC对象
    plc = OmronPLC(plc_ip)

    # 连接到PLC
    plc.connect()

    # 读取D区数据
    d_address = "D100"  # 替换为实际的D区地址
    data = plc.read_d_area(d_address)

    # 写入D区数据
    # new_value = 123  # 替换为要写入的数据
    # plc.write_d_area(d_address, new_value)

    # 断开连接
    plc.disconnect()