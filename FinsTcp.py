import socket
import struct

class TResult:
    def __init__(self):
        self.is_success = False
        self.result_value = None

class FinsTcp:
    def __init__(self, ip, port, local_node):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(1)
        self.server_node = 10
        self.local = local_node
        self.connected = False
        self.timeout_flag = False

        try:
            self.client_socket.connect((ip, port))
            self.client_socket.send(self.get_hand_byte(local_node))
            response = self.get_receive_byte(24)
            if not response:
                print("握手失败")
                return
            self.server_node = self.get_server_node(response)
            self.connected = True
        except Exception as ex:
            print(ex)

    def disconnect(self):
        self.client_socket.close()
        self.connected = False

    def get_hand_byte(self, local_node):
        return struct.pack('>BBBBBBBBBBBBBBBBBBBB',
                           0x46, 0x49, 0x4E, 0x53,  # ASICC fins
                           0x00, 0x00, 0x00, 0x0C,      # 字节数量
                           0x00, 0x00, 0x00, 0x00,      # 命令码
                           0x00, 0x00, 0x00, 0x00,      # 错误码
                           0x00, 0x00, 0x00, local_node)  # 本地节点号

    def get_receive_byte(self, byte_length):
        buffer = bytearray()
        while len(buffer) < byte_length and not self.timeout_flag:
            try:
                data = self.client_socket.recv(1024)
                buffer.extend(data)
                if len(buffer) >= 16:
                    if any(buffer[i] != 0x00 for i in range(12, 16)):
                        return None
                if len(buffer) >= byte_length:
                    break
            except socket.timeout:
                self.timeout_flag = True
        return bytes(buffer)

    def get_server_node(self, hand_response_byte):
        if len(hand_response_byte) >= 24:
            return hand_response_byte[23]
        return 255

    def analyze_receive_msg(self, msg, mode, length):
        result = TResult()
        if msg is None or len(msg) < 30:
            return result
        temp = bytearray(length * 2)
        if mode == OperatorMode.Read:
            temp[:] = msg[30:30 + length * 2]
        result.is_success = True
        result.result_value = temp
        return result

    def read_short(self, address, length):
        str_parts = address.split('.')
        area = OperatorArea.DMWord if str_parts[0].upper() == "DM" else OperatorArea.CIOWord
        content = TResult()
        content.result_value = [0] * length
        temp = self.get_data_change_msg_byte_read(OperatorMode.Read, area, int(str_parts[1]), 0, length)
        self.client_socket.send(temp)
        buffer = self.get_receive_byte(30 + (length * 2))
        if buffer == None:
            return content
        result = self.analyze_receive_msg(buffer, OperatorMode.Read, length)
        if not result.is_success:
            return content
        print(result.result_value)

        values = []
        for i in range(0, len(result.result_value), 2):
            value = struct.unpack('>h', result.result_value[i:i + 2])[0]
            values.append(value)
            # content.result_value[i // 2] = (result.result_value[i] * 256) + result.result_value[i + 1]
        content.result_value = values
        return content

    def read_int(self, address, length):
        str_parts = address.split('.')
        area = OperatorArea.DMWord if str_parts[0].upper() == "DM" else OperatorArea.CIOWord
        content = TResult()
        content.result_value = [0] * length
        temp = self.get_data_change_msg_byte_read(OperatorMode.Read, area, int(str_parts[1]), 0, length)
        self.client_socket.send(temp)
        buffer = self.get_receive_byte(30 + (length * 2))  # 注意：32 位整数需要 4 个字节
        if buffer is None:
            return content
        result = self.analyze_receive_msg(buffer, OperatorMode.Read, length)
        if not result.is_success:
            return content
        print(result.result_value)  # 打印原始数据

        # 调换前两位和后两位的顺序
        if len(result.result_value) >= 4:
            result.result_value[0], result.result_value[2] = result.result_value[2], result.result_value[0]
            result.result_value[1], result.result_value[3] = result.result_value[3], result.result_value[1]
        print(result.result_value)  # 打印调换顺序后的数据
        values = []
        for i in range(0, len(result.result_value), 4):  # 解析 32 位整数
            value = struct.unpack('>i', result.result_value[i:i + 4])[0]
            values.append(value)
        content.result_value = values
        return content

    def read_long(self, address, length):
        str_parts = address.split('.')
        area = OperatorArea.DMWord if str_parts[0].upper() == "DM" else OperatorArea.CIOWord
        content = TResult()
        content.result_value = [0] * length
        temp = self.get_data_change_msg_byte_read(OperatorMode.Read, area, int(str_parts[1]), 0, length)
        self.client_socket.send(temp)
        buffer = self.get_receive_byte(30 + (length * 4))  # 注意：64 位整数需要 8 个字节
        if buffer is None:
            return content
        result = self.analyze_receive_msg(buffer, OperatorMode.Read, length)
        if not result.is_success:
            return content
        print(result.result_value)  # 打印原始数据

        # 调换前两位和后两位的顺序
        if len(result.result_value) >= 4:
            result.result_value[0], result.result_value[2] = result.result_value[2], result.result_value[0]
            result.result_value[1], result.result_value[3] = result.result_value[3], result.result_value[1]
        print(result.result_value)  # 打印调换顺序后的数据

        values = []
        for i in range(0, len(result.result_value), 4):
            # 使用大端序解析 4 个字节为 uint32
            value = struct.unpack('>I', result.result_value[i:i + 4])[0]
            values.append(value)
        content.result_value = values
        return content

    def read_float(self, address, length):
        str_parts = address.split('.')
        area = OperatorArea.DMWord if str_parts[0].upper() == "DM" else OperatorArea.CIOWord
        content = TResult()
        content.result_value = [0] * length
        temp = self.get_data_change_msg_byte_read(OperatorMode.Read, area, int(str_parts[1]), 0, length)
        self.client_socket.send(temp)
        buffer = self.get_receive_byte(30 + (length * 4))  # 注意：32 位浮点数需要 4 个字节
        if buffer is None:
            return content
        result = self.analyze_receive_msg(buffer, OperatorMode.Read, length)
        if not result.is_success:
            return content
        print(result.result_value)  # 打印原始数据

        # 调换前两位和后两位的顺序
        if len(result.result_value) >= 4:
            result.result_value[0], result.result_value[2] = result.result_value[2], result.result_value[0]
            result.result_value[1], result.result_value[3] = result.result_value[3], result.result_value[1]
        print(result.result_value)  # 打印调换顺序后的数据

        values = []
        for i in range(0, len(result.result_value), 4):  # 解析 32 位浮点数
            # 使用大端序解析 4 个字节为 float
            value = struct.unpack('>f', result.result_value[i:i + 4])[0]
            values.append(value)
        content.result_value = values
        return content
    def read_bool(self, address, length):
        if address is None:
            raise ValueError("Address cannot be None")
        str_parts = address.split('.')
        area = {
            "DM": OperatorArea.DMBit,
            "CIO": OperatorArea.CIOBit,
            "WR": OperatorArea.WRBit
        }.get(str_parts[0].upper(), OperatorArea.DMBit)

        content = TResult()
        content.result_value = [False] * length
        temp = self.get_data_change_msg_byte_read(OperatorMode.Read, area, int(str_parts[1]), int(str_parts[2]), length)
        self.client_socket.send(temp)
        buffer = self.get_receive_byte(30 + length)
        if not buffer.is_success:
            return content
        result = self.analyze_receive_msg(buffer.result_value, OperatorMode.Read, length)
        for i in range(len(result)):
            content.result_value[i] = result[i] == 0x01
        return content

    def write_short(self, address, value):
        values = self.short_to_bytes(value)
        str_parts = address.split('.')
        area = {
            "DM": OperatorArea.DMWord,
            "CIO": OperatorArea.CIOWord
        }.get(str_parts[0].upper(), OperatorArea.DMWord)

        obj = list(values)
        temp = self.get_data_change_msg_byte_write(OperatorMode.Write, area, int(str_parts[1]), 0, len(values), obj, False)
        self.client_socket.send(temp)

        buffer = self.get_receive_byte(30)
        if buffer is None:
            return False
        else:
            return True

    def write_long(self, address, value):
        values = self.int_to_bytes(value)
        str_parts = address.split('.')
        area_id = str_parts[0].upper()
        address_number = int(str_parts[1])

        # Map area identifier to the correct OperatorArea for longs
        area = {
            "DM": OperatorArea.DMWord,
            "CIO": OperatorArea.CIOWord
        }.get(str_parts[0].upper(), OperatorArea.DMWord)

        # Prepare the data to be written
        obj = list(values)

        # Generate the message to send
        temp = self.get_data_change_msg_byte_write(
            OperatorMode.Write,
            area,
            address_number,
            0,
            len(values),
            obj,
            False
        )

        # Send the message
        self.client_socket.send(temp)

        # Receive the response
        buffer = self.get_receive_byte(30)

        # Check the response and return the result
        if buffer is None:
            return False
        else:
            return True

    def write_int(self, address, value):
        values = self.int_to_bytes(value)
        # 解析地址，分成区域标识和地址号
        str_parts = address.split('.')
        area_id = str_parts[0].upper()
        address_number = int(str_parts[1])

        # 确定操作区域，使用字典映射
        area = {
            "DM": OperatorArea.DMWord,
            "CIO": OperatorArea.CIOWord
        }.get(str_parts[0].upper(), OperatorArea.DMWord)

        # 将values转换为列表
        obj = list(values)

        # 生成数据更改消息字节写入
        temp = self.get_data_change_msg_byte_write(
            OperatorMode.Write,
            area,
            address_number,
            0,  # 偏移
            len(values),
            obj,
            False
        )

        # 发送数据
        self.client_socket.send(temp)

        # 接收响应
        buffer = self.get_receive_byte(30)

        # 判断响应是否成功
        if buffer is None:
            return False
        else:
            return True
    def write_float(self, address, value):
        values = self.float_to_bytes(value)
        str_parts = address.split('.')
        area = {
            "DM": OperatorArea.DMWord,
            "CIO": OperatorArea.CIOWord
        }.get(str_parts[0].upper(), OperatorArea.DMWord)
        obj = []
        obj = list(values)
        obj = obj[2:4] + obj[0:2]
        length = len(obj)
        # Get the message bytes to write
        temp = self.get_data_change_msg_byte_write(
            OperatorMode.Write, area, int(str_parts[1]), 0, length, obj, False
        )
        self.client_socket.send(temp)

        # Receive the response
        buffer = self.get_receive_byte(30)
        if buffer is None:
            return False
        else:
            return True
    def write_bool(self, address, values):
        str_parts = address.split('.')
        area = {
            "DM": OperatorArea.DMBit,
            "CIO": OperatorArea.CIOBit,
            "WR": OperatorArea.WRBit
        }.get(str_parts[0].upper(), OperatorArea.DMBit)

        obj = [(0x01 if value else 0x00) for value in values]
        temp = self.get_data_change_msg_byte_write(OperatorMode.Write, area, int(str_parts[1]), int(str_parts[2]), len(values), obj, True)
        self.client_socket.send(temp)

        buffer = self.get_receive_byte(30)
        return buffer.is_success

    def get_data_change_msg_byte_read(self, mode, area, start_word, start_bit, length):
        send_byte = bytearray(34)
        send_byte[0:4] = bytes([0x46, 0x49, 0x4E, 0x53])  # ASICC FINS
        send_byte[4:8] = bytes([0x00, 0x00, 0x00, 0x1A])  # Length
        send_byte[8:12] = bytes([0x00, 0x00, 0x00, 0x02])  # Command code
        send_byte[12:16] = bytes([0x00, 0x00, 0x00, 0x00])  # Error code
        send_byte[16:20] = bytes([0x80, 0x00, 0x02, 0x00])  # FINS header
        send_byte[20] = self.server_node  # DA1
        send_byte[23] = self.local  # SA1

        send_byte[26:28] = bytes([0x01, 0x01])  # Read
        send_byte[28] = area  # Memory area
        send_byte[29] = (start_word >> 8) & 0xFF  # Start word high
        send_byte[30] = start_word & 0xFF  # Start word low
        send_byte[31] = start_bit  # Start bit
        send_byte[32] = (length >> 8) & 0xFF  # Length high
        send_byte[33] = length & 0xFF  # Length low

        return send_byte

    def get_data_change_msg_byte_write(self, mode, area, start_word, start_bit, length, values, bit_flag):
        value_length = len(values) if bit_flag else len(values) * 2
        send_byte = bytearray(34 + value_length)
        send_byte[0:4] = bytes([0x46, 0x49, 0x4E, 0x53])  # ASICC FINS
        send_byte[4:8] = bytes([0x00, 0x00, 0x00, (34 + value_length - 8) & 0xFF])  # Length
        send_byte[8:12] = bytes([0x00, 0x00, 0x00, 0x02])  # Command code
        send_byte[12:16] = bytes([0x00, 0x00, 0x00, 0x00])  # Error code
        send_byte[16:20] = bytes([0x80, 0x00, 0x02, 0x00])  # FINS header
        send_byte[20] = self.server_node  # DA1
        send_byte[23] = self.local  # SA1

        if mode == OperatorMode.Read:
            send_byte[26:28] = bytes([0x01, 0x01])
        elif mode == OperatorMode.Write:
            send_byte[26:28] = bytes([0x01, 0x02])

        send_byte[28] = area  # Memory area
        send_byte[29] = (start_word >> 8) & 0xFF  # Start word high
        send_byte[30] = start_word & 0xFF  # Start word low
        send_byte[31] = start_bit  # Start bit
        send_byte[32] = (length >> 8) & 0xFF  # Length high
        send_byte[33] = length & 0xFF  # Length low

        if bit_flag:
            send_byte[34:] = bytes(values)
        else:
            for i in range(len(values)):
                # send_byte[34 + i * 2] = (values[i] >> 8) & 0xFF
                send_byte[34 + i * 1] = values[i] & 0xFF

        return send_byte
    def get_data_change_msg_byte_write2(self, mode, area, start_word, start_bit, length, values, bit_flag):
        value_length = len(values) if bit_flag else len(values) * 2
        send_byte = bytearray(34 + value_length)
        send_byte[0:4] = bytes([0x46, 0x49, 0x4E, 0x53])  # ASICC FINS
        send_byte[4:8] = bytes([0x00, 0x00, 0x00, (34 + value_length - 8) & 0xFF])  # Length
        send_byte[8:12] = bytes([0x00, 0x00, 0x00, 0x02])  # Command code
        send_byte[12:16] = bytes([0x00, 0x00, 0x00, 0x00])  # Error code
        send_byte[16:20] = bytes([0x80, 0x00, 0x02, 0x00])  # FINS header
        send_byte[20] = self.server_node  # DA1
        send_byte[23] = self.local  # SA1

        if mode == OperatorMode.Read:
            send_byte[26:28] = bytes([0x01, 0x01])
        elif mode == OperatorMode.Write:
            send_byte[26:28] = bytes([0x01, 0x02])

        send_byte[28] = area  # Memory area
        send_byte[29] = (start_word >> 8) & 0xFF  # Start word high
        send_byte[30] = start_word & 0xFF  # Start word low
        send_byte[31] = start_bit  # Start bit
        send_byte[32] = (length >> 8) & 0xFF  # Length high
        send_byte[33] = length & 0xFF  # Length low

        if bit_flag:
            send_byte[34:] = bytes(values)
        else:
            for i in range(len(values)):
                # send_byte[34 + i * 2] = (values[i] >> 8) & 0xFF
                send_byte[34 + i * 1+1] = values[i]

        return send_byte

    def short_to_bytes(self,value):
        low = value & 0xffff  # 获取低16位
        result = struct.pack('>H', low)  # 按大端序打包低16位
        # return self.swap_bytes(result, 2)
        return result

    def float_to_bytes(self, value):
        # 使用 struct.pack 将浮点数按大端序打包为 4 字节的字节数组
        result = struct.pack('>f', value)
        return result
    def int_to_bytes(self,value):
        high = (value >> 16) & 0xffff  # 高16位
        low = value & 0xffff  # 低16位
        result = struct.pack('>HH', low, high)  # 按大端序打包低16位和高16位
        # return self.swap_bytes(result, 4)
        return result
    def swap_bytes(self,data, dig):
        if dig == 4:
            if len(data) != 4:
                raise ValueError("Input data must be 4 bytes long.")
            return data[2:4] + data[0:2]
        elif dig == 2:
            if len(data) != 2:
                raise ValueError("Input data must be 2 bytes long.")
            return data[1:2] + data[0:1]

class OperatorMode:
    Read = 0x0101
    Write = 0x0102

class OperatorArea:
    DMWord = 0x82
    DMBit = 0x02
    CIOWord = 0xB0
    CIOBit = 0x30
    WRBit = 0x31
