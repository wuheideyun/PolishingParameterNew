import FinsTcp


if __name__ == "__main__":
    tcp = FinsTcp.FinsTcp('192.168.4.1',9600,22)
    # value = tcp.read_short('DM.320',2)
    # print(value.result_value[0])
    # value = tcp.read_short('DM.100', 2)
    # print(value.result_value[0])
    # value = tcp.read_short('DM.120', 2)
    # print(value.result_value[0])
    # value = tcp.read_int('DM.140', 4)
    # print(value.result_value[0])
    # value = tcp.read_int('DM.160', 4)
    # print(value.result_value[0])
    value = tcp.read_int('DM.220', 4)
    print(value.result_value[0])
    tcp.disconnect()