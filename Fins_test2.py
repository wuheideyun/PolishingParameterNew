import socket


def recognition_frame(req_bytes_frame, Trigger):
    get_frame = req_bytes_frame.hex().upper()
    print("设备请求:", get_frame)
    # 判断是否为握手命令
    if get_frame == "46494E530000000C000000000000000000000000":
        response = "46494E530000001000000000000000000000000100000001"
        return bytes().fromhex(response)
    # 　判断是否为其他ＦＩＮＳ命令的请求头，只要是请求头都只反应空
    elif "46494E53" in get_frame:  # 收到FINS的请求头 == "46494E530000001A0000000200000000" 或 其他请求头
        print("只收到请求头，响应将为空！")
        response = ""
        return bytes().fromhex(response)
    else:
        SRC_value = get_frame[22:24]  # 判断读写，01为读，02为写
        Area_value = get_frame[24:26]  # 判断寄存器区域，82为保持寄存器
        # print(SRC_value)
        # print(Area_value)
        if SRC_value == "01":
            if Area_value == "82":
                response_1 = "46494E5300000018000000000000000000000000000000000000010100000001"  # Trigger位为True
                response_0 = "46494E5300000018000000000000000000000000000000000000010100000000"  # Trigger位为False
                if Trigger == True:
                    return bytes().fromhex(response_1)
                else:
                    return bytes().fromhex(response_0)
            else:
                raise ValueError("Area_value is error!")
        elif SRC_value == "02":
            if Area_value == "82":
                print("***************************************")
                # 写保持寄存器的响应
                print("扫码器写入的结果数据：", bytes().fromhex(get_frame))
                response = "46494E530000001600000000000000000000000000000000000001020000"
                return bytes().fromhex(response)
            else:
                raise ValueError("Area_value is error!")
        else:
            raise ValueError("SRC_value is error!")


if __name__ == "__main__":
    DM_start = 1000

    # 创建FINS服务端
    # 创建一个TCP/IP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定套接字到特定地址和端口
    server_address = ('127.0.0.1', 9600)  # 服务器地址和端口
    server_socket.bind(server_address)
    # 监听连接
    server_socket.listen(1)
    print('等待客户端连接...')
    connection, client_address = server_socket.accept()
    print('客户端已连接:', client_address)

    try:
        num = 0  # 触发标志
        Trigger_rec = 0  # Trigger置为True时，对应变为1，表示触发一次
        response = ""  # 响应
        while True:
            # 接收客户端请求
            request = connection.recv(1024)
            if request:
                # 如果收到的不是请求头
                if "8000020001000001" in request.hex():
                    # print(request.hex()[22:24])
                    # 实现扫码触发
                    if request.hex()[22:24] == "01":  # 判断读写，01为读触发指令，02为写触发结果
                        if Trigger_rec != 2:
                            Trigger_rec += 1
                        if Trigger_rec == 1:
                            response = recognition_frame(request, Trigger=False)  # 先清空触发信号
                            connection.sendall(response)
                        elif Trigger_rec == 2:  # 复位Trigger信号
                            response = recognition_frame(request, Trigger=True)  # 再置位触发信号
                            connection.sendall(response)
                    # 实现结果接收
                    elif request.hex()[22:24] == "02":
                        print(request.hex())
                        # print("---------------", int(request.hex()[26:30], 16))
                        if int(request.hex()[26:30], 16) == DM_start + 4:
                            if any(c != '0' for c in request.hex()[36:]):  # 不全为0
                                print("扫码结果：", request.hex()[36:])
                                num += 1
                                Trigger_rec = 0
                            else:
                                response = recognition_frame(request, Trigger=True)
                                connection.sendall(response)
                                print("还没有收到结果，继续等待扫码结果！")
                        else:
                            response = recognition_frame(request, Trigger=True)
                            connection.sendall(response)
                # 处理其他请求
                else:
                    response = recognition_frame(request, Trigger=True)
                    connection.sendall(response)
                print("服务响应：", response.hex())
                if num == 1:
                    assert bytes().fromhex(request.hex()[36:]).decode() == "NG", "实际扫码结果为：{}，不符合预期".format(
                        bytes().fromhex(request.hex()[36:]).decode())
                    break
                request = False
    finally:
        # 清理连接
        connection.close()