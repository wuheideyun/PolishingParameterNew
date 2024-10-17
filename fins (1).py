import struct
import socket

BUFSIZE = 11024


class FinsUDP():
    '''
    OMRON UDP Transmission.
    '''

    def __init__(self, ip, debug=False):
        '''PC's IP'''
        self.__ip = ip
        self.__SID = 0
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__client.settimeout(0.5)
        self.__debug = debug

    def __packet(self, ip, command, pos, length, *datas):
        '''
        Packet Command. PC ->  PLC
        ip: PLC's IP
        command: read / write
        '''
        self.__SID = (self.__SID + 1) % 0xFF
        ICF = 0x80
        RSV = 0x00
        GCT = 0x02
        DNA = 0x00
        DA1 = int(ip.split(".")[-1], 10)
        DA2 = 0x00
        SNA = 0x00
        SA1 = int(self.__ip.split(".")[-1], 10)
        SA2 = 0x00
        SID = self.__SID
        CMD = 0x0101 if command == 'read' else 0x0102
        TYP = 0x82 if pos[0].lower() == 'd' else 0xB1
        POS = int(pos[1:], 10)
        spacer = 0x00
        LEN = length
        frame = struct.pack(
            '>BBBBBBBBBBHBHBH',
            ICF, RSV, GCT, DNA, DA1, DA2, SNA, SA1, SA2, SID,
            CMD, TYP, POS, spacer, LEN
        )
        if command == 'write':
            frame += struct.pack(
                '>' + 'H' * LEN,
                *datas
            )
        return frame

    def __unpacket(self, data):
        (ICF, RSV, GCT, DNA, DA1, DA2, SNA, SA1, SA2, SID, CMD, STA) = struct.unpack('>BBBBBBBBBBHH', data[:14])
        print(ICF, RSV, GCT, DNA, DA1, DA2, SNA, SA1, SA2, SID, CMD, STA, data[14:])

    def read(self, ip, pos, length):
        buffer = self.__packet(ip, 'read', pos, length)
        if self.__debug:
            print('PC->PLC:', ' '.join([hex(k)[2:] if len(hex(k)[2:]) == 2 else (
                '0' + hex(k)[2:]) for k in struct.unpack('B' * len(buffer), buffer)]))
        self.__client.sendto(buffer, (ip, 9600))
        try:
            data, server_addr = self.__client.recvfrom(BUFSIZE)
            if self.__debug:
                print('PLC->PC:', ' '.join([hex(k)[2:] if len(hex(k)[2:]) == 2 else (
                    '0' + hex(k)[2:]) for k in struct.unpack('B' * len(data), data)]))
            print(self.__unpacket(data))
        except:
            print('PLC->PC: TIMEOUT')

    def write(self, ip, pos, length, *datas):
        buffer = self.__packet(ip, 'write', pos, length, *datas)
        if self.__debug:
            print('PC->PLC:', ' '.join([hex(k)[2:] if len(hex(k)[2:]) == 2 else (
                '0' + hex(k)[2:]) for k in struct.unpack('B' * len(buffer), buffer)]))
        self.__client.sendto(buffer, (ip, 9600))
        
class FinsTCP():
    '''
    OMRON PLC Transmission.
    '''

    def __init__(self, ip, debug=False):
        '''PC's IP'''
        self.__ip = ip
        self.__SID = 0
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__client.settimeout(10)
        self.__debug = debug
    
    def connect(self, ip):
        self.__plc_ip = ip
        self.__client.connect((self.__plc_ip, 9600))
        self.__client.send(struct.pack(
            ">IIIII",
            # FINS
            0x46494e53,
            # 12
            0x0000000c,
            # CMD
            0x00000000,
            # ERR_CODE
            0x00000000,
            # PC IP
            int(self.__ip.split('.')[-1], 10)
        ))
        data = self.__client.recv(BUFSIZE)
        (LAB, LEN, CMD, ERR, PL, PLC) = struct.unpack(">IIIIII", data)
        self.__check_ERR(ERR)
    
    def __check_ERR(self, ERR):
        if ERR == 0x01:
            print("CONNECT ERROR: header is not 'FINS'")
        elif ERR == 0x02:
            print("CONNECT ERROR: data too long")
        elif ERR == 0x03:
            print("CONNECT ERROR: CMD ERROR")
        elif ERR == 0x20:
            print("CONNECT ERROR: BUSY")
        elif ERR == 0x21:
            print("CONNECT ERROR: HAS another connection")
        elif ERR == 0x22:
            print("CONNECT ERROR: no access")
        elif ERR == 0x23:
            print("CONNECT ERROR: address out of range")
        elif ERR == 0x24:
            print("CONNECT ERROR: address is being used")
        elif ERR == 0x25:
            print("CONNECT ERROR: no address")

    def __packet(self, ip, command, pos, length, *datas):
        '''
        Packet Command. PC ->  PLC
        ip: PLC's IP
        command: read / write
        '''
        self.__SID = (self.__SID + 1) % 0xFF
        ICF = 0x80
        RSV = 0x00
        GCT = 0x02
        DNA = 0x00
        DA1 = int(ip.split(".")[-1], 10)
        DA2 = 0x00
        SNA = 0x00
        SA1 = int(self.__ip.split(".")[-1], 10)
        SA2 = 0x00
        SID = self.__SID
        CMD = 0x0101 if command == 'read' else 0x0102
        TYP = 0x82 if pos[0].lower() == 'd' else 0xB1
        POS = int(pos[1:], 10)
        spacer = 0x00
        LEN = length
        frame = struct.pack(
            '>BBBBBBBBBBHBHBH',
            ICF, RSV, GCT, DNA, DA1, DA2, SNA, SA1, SA2, SID,
            CMD, TYP, POS, spacer, LEN
        )
        if command == 'write':
            frame += struct.pack(
                '>' + 'H' * LEN,
                *datas
            )
        # 0x46, 0x49, 0x4E, 0x53,0x00, 0x00, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01
        buffer = struct.pack(
            ">IIII",
            # FINS
            0x46494e53,
            # LENGTH - 8
            len(frame) + 8,
            # CMD
            0x00000002,
            # ERR_CODE
            0x00000000,
        ) + frame
        return buffer

    def __unpacket(self, data):
        (LAB, LEN, CMD, ERR) = struct.unpack(">IIII", data)
        self.__check_ERR(ERR)
        frame = data[16:]
        (ICF, RSV, GCT, DNA, DA1, DA2, SNA, SA1, SA2, SID, CMD, STA) = struct.unpack('>BBBBBBBBBBHH', frame[:14])
        print(ICF, RSV, GCT, DNA, DA1, DA2, SNA, SA1, SA2, SID, CMD, STA, frame[14:])

    def read(self, pos, length):
        buffer = self.__packet(self.__plc_ip, 'read', pos, length)
        if self.__debug:
            print('PC->PLC:', ' '.join([hex(k)[2:] if len(hex(k)[2:]) == 2 else (
                '0' + hex(k)[2:]) for k in struct.unpack('B' * len(buffer), buffer)]))
        self.__client.send(buffer)
        try:
            data = self.__client.recv(BUFSIZE)
            if self.__debug:
                print('PLC->PC:', ' '.join([hex(k)[2:] if len(hex(k)[2:]) == 2 else (
                    '0' + hex(k)[2:]) for k in struct.unpack('B' * len(data), data)]))
            print(self.__unpacket(data))
        except:
            print('PLC->PC: TIMEOUT')

    def write(self, pos, length, *datas):
        buffer = self.__packet(self.__plc_ip, 'write', pos, length, *datas)
        if self.__debug:
            print('PC->PLC:', ' '.join([hex(k)[2:] if len(hex(k)[2:]) == 2 else (
                '0' + hex(k)[2:]) for k in struct.unpack('B' * len(buffer), buffer)]))
        self.__client.send(buffer)
        try:
            data = self.__client.recv(BUFSIZE)
            if self.__debug:
                print('PLC->PC:', ' '.join([hex(k)[2:] if len(hex(k)[2:]) == 2 else (
                    '0' + hex(k)[2:]) for k in struct.unpack('B' * len(data), data)]))
            print(self.__unpacket(data))
        except:
            print('PLC->PC: TIMEOUT')

def main():
    # finsTCP = FinsTcp('192.168.13.10', debug=True)
    # finsTCP.read('192.168.13.61', 0, 8)
    # finsTCP.write('192.168.13.61', 0, 1, 1)
    # finsTCP.write('192.168.13.61', 10, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    finsTCP = FinsTCP('127.0.0.1', debug=True)
    finsTCP.connect('127.0.0.1')
    finsTCP.read('D100', 1)


if __name__ == '__main__':
    main()
