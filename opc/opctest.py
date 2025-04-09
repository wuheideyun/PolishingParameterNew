from datetime import datetime

from opcua import Client, ua
import time


def main():
    # OPC UA 服务器的 URL
    url = "opc.tcp://192.168.2.1:4840"

    # 创建 OPC UA 客户端
    client = Client(url)

    try:
        # 连接到 OPC UA 服务器
        print("Connecting to OPC UA server...")
        client.connect()
        print("Connected to OPC UA server.")

        # 读取 ns=4;s=实数数据1 的值
        node_real_data = client.get_node("ns=4;s=单字数据1")
        real_data_value = node_real_data.get_value()
        print(f"实数数据1 的当前值: {real_data_value}")

        # 写入新的值到 ns=4;s=输入_实数数据1
        node_input_data = client.get_node("ns=4;s=输入_单字数据1")
        print("设置 输入_实数数据1 为 100...")
        # 创建一个 Variant 类型的对象
        value = ua.Variant(5, ua.VariantType.Int32)
        print(1)
        # 设置节点的值
        node_input_data.set_value(value)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # 断开与服务器的连接
        client.disconnect()
        print("Disconnected from the OPC UA server.")


if __name__ == "__main__":
    main()
