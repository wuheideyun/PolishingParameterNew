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
        buffer = self.get_receive_byte(30 + (length * 4))  # 注意：32 位整数需要 4 个字节
        if buffer == None:
            return content
        result = self.analyze_receive_msg(buffer, OperatorMode.Read, length)
        if not result.is_success:
            return content
        print(result.result_value)

        values = []
        for i in range(0, len(result.result_value), 4):  # 解析 32 位整数
            # value = struct.unpack('<i', result.result_value[i:i + 4])[0]  # 使用小端序解析
            # value = struct.unpack('l', result.result_value[0:4])[0]
            value = struct.unpack('>i', result.result_value[0:4])[0]
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

    def write_short(self, address, values):
        str_parts = address.split('.')
        area = {
            "DM": OperatorArea.DMWord,
            "CIO": OperatorArea.CIOWord
        }.get(str_parts[0].upper(), OperatorArea.DMWord)

        obj = list(values)
        temp = self.get_data_change_msg_byte_write(OperatorMode.Write, area, int(str_parts[1]), 0, len(values), obj, False)
        self.client_socket.send(temp)

        buffer = self.get_receive_byte(30)
        return buffer.is_success

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
                send_byte[34 + i * 2] = (values[i] >> 8) & 0xFF
                send_byte[34 + i * 2 + 1] = values[i] & 0xFF

        return send_byte

class OperatorMode:
    Read = 0x0101
    Write = 0x0102

class OperatorArea:
    DMWord = 0x82
    DMBit = 0x02
    CIOWord = 0xB0
    CIOBit = 0x30
    WRBit = 0x31
