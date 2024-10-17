#!/usr/bin/python
# -*- coding:utf-8 -*-
from socket import *
import threading
import time
import re
import struct
import string
import platform

import os
# import fcntl
import struct
 

typeBool    =   'Bool'      #2个字节
typeShort   =   'Short'     #2个字节
typeUShort   =   'UShort'     #2个字节
typeInt     =   'Int'       #4个字节
typeFloat   =   'Float'     #4个字节
typeString  =   'String'    #字符串长度
typeBit     =   'Bit'       #


#cip客户端
class Fins():
    # exit = QtCore.pyqtSignal()  # 信号
    def __init__(self,aimIp,aimPort):
        # 数据部分
        print(aimIp)
        print(aimPort)

        self.sock = socket(AF_INET, SOCK_STREAM)      #用于保存socket套接字

        #网络状态由这两个共同决定，握手失败主动断开，数据发送不符合规格，主动断开
        self.connectState = False       # 网络是否连接成功
        self.handshakeState = False       # 握手成功标志

        self.serverIp = ''  # 这个用来保存服务器的IP节点--组帧需要使用
        self.clientIp = ''  # 这个用来保存客户端的IP节点--组帧需要使用

        #错误码
        self.finsErrorCode = {
            '\x00\x00\x00\x00': "Normal",
            '\x00\x00\x00\x01': "The header is not 'Fins'",
            '\x00\x00\x00\x02': "The data length is too long",
            '\x00\x00\x00\x03': "The command is not supported",
            '\x00\x00\x00\x20': "All connections are in use",
            '\x00\x00\x00\x21': "The specified node is already connected",
            '\x00\x00\x00\x22': "Attempt to access a protected node from an unspecified IP address",
            '\x00\x00\x00\x23': "The client FINS node address is out of range",
            '\x00\x00\x00\x24': "The same FINS node address is being used by the client and server",
            '\x00\x00\x00\x25': "All the node addresses available for allocation have been used",
        }

        self.lock = threading.Lock()    #它是一个基本的锁对象，每次只能锁定一次，其余的锁请求，需等待锁释放后才能获取
        #self.rlock = threading.RLock() #对于可重入锁，在同一个线程中可以对它进行多次锁定，也可以多次释放。如果使用 RLock，那么 acquire() 和 release() 方法必须成对出现。如果调用了 n 次 acquire() 加锁，则必须调用 n 次 release() 才能释放锁

        #获取当前系统的ip，目前支持Linux、Windows系统
        self.ipAddr = self.getSystemIp()
        print(self.ipAddr)
        if self.ipAddr == '':
            print('Check The Network')
            return
        
        self.initSys(aimIp,aimPort)

    # Fins协议,连接网络,发送握手帧
    def initSys(self,Ip,Port):
        try:
            self.connectState = self.connect(Ip, Port)
            if self.connectState == True:
                handshakeFrame = self.createHandshake(Ip)
                str = struct.pack(
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
                    # int('192.168.0.128'.split('.')[-1], 10))
                    0x00000000)
                self.sendFrame(str)
                self.recvMsg()
        except Exception as e:
            print(f"Database error: {e}")
            print('function initSys error')

    ##连接服务器
    def connect(self, Ip, Port):
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.settimeout(2)
            self.sock.connect((Ip, Port))
            return True
        except Exception:
            self.disConnect()
            print('function connect error')
            return False

    def disConnect(self):
        self.connectState = False
        self.handshakeState = False
        self.sock.close()
        print('网络连接失败')

    def getLinuxIp(self):
        try:
            ifname = 'eth0'
            s = socket(AF_INET, SOCK_DGRAM)
            ip = inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

        except Exception as e:
            print(f"Database error: {e}")
            ip = ''
        finally:
            s.close()
        return ip

    def getWindowsIp(self):
        try:
            ip = gethostbyname(gethostname())
            return ip
        except Exception as e:
            print(f"Database error: {e}")
            return ''
        return ip

    def getSystemIp(self):
        sysType = platform.system()
        if sysType == 'Windows':
            print('Windows System')
            return self.getWindowsIp()
        elif sysType == 'Linux':
            print('Linux System')
            return self.getLinuxIp()
        else:
            print('Other System')
            return ''

    def createHandshake(self, Ip):
        try:
            handshakeMsg = b'\x46\x49\x4e\x53\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            # handshakeMsg += (self.toHex(bytes(self.ipAddr.split('.')[3]), 'B'))
            handshakeFrame = handshakeMsg
            # handshakeFrame = ''.join(handshakeMsg)
            t = ['%02x' % byte for byte in handshakeFrame]
            print("发送数据:" + "".join(t))
            return handshakeFrame
        except Exception as e:
            print(f"Database error: {e}")
            print('function createHandshake error1')

    # 发送函数
    def sendFrame(self, data):
        try:
            self.sock.send(data)
        except Exception as e:
            print(f"Database error: {e}")
            self.disConnect()   #数据发送失败，则主动断开连接
            print('function sendFrame error')


    def recvMsg(self):
        try:
            # 网络连接的时候这里是阻塞的,除非是接收到数据才会执行下一步
            data = self.sock.recv(2024)
            if data == "":
                self.disConnect()
            else:
                return self.handleData(data)
        except Exception as e:
            print(f"Database error: {e}")
            print( 'function recvMsg error' ) #这里是由于超时引起的问题
            self.disConnect()

    def parseData(self,data,dataType):
        if data == "":
            pass
            #print('无数据')
        else:
            index = 0
            if dataType == typeInt:
                return struct.unpack('>i', (data[index + 2:index + 4] + data[index:index + 2]))[0]
            elif dataType == typeShort:
                return struct.unpack('>h', (data[index:index + 2]))[0]
            elif dataType == typeFloat:
                return struct.unpack('>f', (data[index + 2:index + 4] + data[index:index + 2]))[0]
            elif dataType == typeString:
                #printself.printData(data)
                pass
                #printstruct.unpack('>f', (data[index + 2:index + 4] + data[index:index + 2]))[0]


    # fins头
    def createFinsHeader(self, finsFrame):
        try:
            finsFrameLength = len(finsFrame)
            finsHeaderMsg = ['\x46\x49\x4e\x53']
            finsHeaderMsg.append(self.toHex(finsFrameLength + 8, 'i'))
            finsHeaderMsg.append('\x00\x00\x00\x02')  # 发送命令
            finsHeaderMsg.append('\x00\x00\x00\x00')  # 错误码(默认00 00 00 00)
            finsHeaderMsg.append(finsFrame)

            finsHeader = ''.join(finsHeaderMsg)

            #print'Send Frame is:' + self.printData(finsHeader)

            # print'length = ',len(finsHeader)

            return finsHeader
        except Exception as e:
            print(f"Database error: {e}")
            print('function createFinsHeader error')

    # fins帧
    def createReadFinsFrame(self, addr, length):
        try:
            finsFrameMsg = ['\x80\x00\x02\x00']  # FINS命令 固定
            finsFrameMsg.append(self.toHex(self.serverIp, 'B'))  # 服务器IP节点
            finsFrameMsg.append('\x00\x00')  #
            finsFrameMsg.append(self.toHex(self.clientIp, 'B'))  # 客户端IP节点
            finsFrameMsg.append('\x00\x00\x01\x01')  # 读命令
            finsFrameMsg.append('\x82')  # 读地址区域代码(82表示读取的是DM区)
            finsFrameMsg.append(self.toHex(addr, 'h'))  # 读数据起始地址
            finsFrameMsg.append('\x00')
            finsFrameMsg.append(self.toHex(length, 'h'))  # 读数据长度

            finsFrame = ''.join(finsFrameMsg)

            return finsFrame
        except Exception as e:
            print(f"Database error: {e}")
            print('function createReadFinsFrame error')

    # fins帧
    def createWriteFinsFrame(self, addr, dataType, value):
        try:
            #printisinstance(value, list)  #判断数据变量类型   变量value     类型list
            dataFrame = ''
            if type(value) == list:
                for i in range(len(value)):
                    dataFrame += self.dataFraming(dataType,value[i])
            else:
                dataFrame = self.dataFraming(dataType, value)

            finsFrameMsg = ['\x80\x00\x02\x00']  # FINS命令 固定
            finsFrameMsg.append(self.toHex(self.serverIp, 'B'))  # 服务器IP节点
            finsFrameMsg.append('\x00\x00')  #
            finsFrameMsg.append(self.toHex(self.clientIp, 'B'))  # 客户端IP节点
            finsFrameMsg.append('\x00\x00\x01\x02')  # 写命令
            finsFrameMsg.append('\x82')  # 写地址区域代码(82表示读取的是DM区)
            finsFrameMsg.append(self.toHex(addr, 'h'))  # 写数据起始地址
            finsFrameMsg.append('\x00')

            finsFrameMsg.append(self.toHex(len(dataFrame)/2, 'h'))  #数据帧长度
            finsFrameMsg.append(dataFrame)  #数据帧添加



            finsFrame = ''.join(finsFrameMsg)

            return finsFrame
        except Exception as e:
            print(f"Database error: {e}")
            print('function createWriteFinsFrame error')

    def dataFraming(self,dataType,value):
        dataFrameMsg = []

        if dataType == 'Bool':
            if value.lower() == 'true':
                dataFrameMsg.append('\x00\x01')  # 写数据内容
            elif value.lower() == 'false':
                dataFrameMsg.append('\x00\x00')  # 写数据内容
        
        elif dataType == 'UShort':
            dataFrameMsg.append(self.toHex(value, 'H')[0])  # 写数据起始地址
            dataFrameMsg.append(self.toHex(value, 'H')[1])  # 写数据起始地址
        
        elif dataType == 'Int':
            dataFrameMsg.append(self.toHex(value, 'i')[2])  # 写数据起始地址
            dataFrameMsg.append(self.toHex(value, 'i')[3])  # 写数据起始地址
            dataFrameMsg.append(self.toHex(value, 'i')[0])  # 写数据起始地址
            dataFrameMsg.append(self.toHex(value, 'i')[1])  # 写数据起始地址

        elif dataType == 'Float':
            dataFrameMsg.append(self.toHex(value, 'f')[2])  # 写数据起始地址
            dataFrameMsg.append(self.toHex(value, 'f')[3])  # 写数据起始地址
            dataFrameMsg.append(self.toHex(value, 'f')[0])  # 写数据起始地址
            dataFrameMsg.append(self.toHex(value, 'f')[1])  # 写数据起始地址
        elif dataType == 'String':
            print('value = ',value)  #'abcde'    'abcdef'
            
            for i in range(len(value)/2):
                dataFrameMsg.append(self.toHex(ord(value[2*i+1]), 'B'))  # 将字符转换成ASCII,然后在转成16进制
                dataFrameMsg.append(self.toHex(ord(value[2*i]), 'B'))  # 将字符转换成ASCII,然后在转成16进制

            if len(value) % 2 == 1:
                dataFrameMsg.append(self.toHex(0, 'B'))  # 将字符转换成ASCII,然后在转成16进制
                dataFrameMsg.append(self.toHex(ord(value[len(value) - 1]), 'B'))  # 将字符转换成ASCII,然后在转成16进制

        dataFrame = ''.join(dataFrameMsg)
        return dataFrame


    def reMatch(self,addr):
        try:
            return re.search(r'^D[0-9]*$', addr).group()
        except Exception as e:
            print(f"Database error: {e}")
            return

    # 读取指定地址数据
    # addr      起始地址
    # length    读取字数量
    # 返回值       数据帧部分
    def finsRead(self, addr, length):
        self.lock.acquire()
        try:
            if self.connectState == True and self.handshakeState == True:
                if self.reMatch(addr) != "":
                    finsReadFrame = self.createFinsHeader(self.createReadFinsFrame(int(self.reMatch(addr)[1:]), length))
                    self.sendFrame(finsReadFrame)
                    return self.recvMsg()
                    # self.parseData(self.recvMsg(),typeInt)
                else:
                    print('地址错误或不存在')
        except Exception as e:
            print(f"Database error: {e}")
            print('function finsRead error')
        finally:
            self.lock.release()

    # 写指定地址数据
    # addr      起始地址
    # dataType    写入类型
    # value     值
    def finsWrite(self, addr, dataType, value):
        self.lock.acquire()
        try:
            if self.connectState == True and self.handshakeState == True:
                if self.reMatch(addr) != "":
                    finsWriteFrame = self.createFinsHeader(
                        self.createWriteFinsFrame(int(self.reMatch(addr)[1:]), dataType, value))
                    self.sendFrame(finsWriteFrame)
                    self.parseData(self.recvMsg(), dataType)

                else:
                    print('地址错误或不存在')
        except Exception as e:
            print(f"Database error: {e}")
            print('function finsWrite error')
        finally:
            self.lock.release()

    #addr   地址(这里只读取1个字的长度,即16位)
    #site   读取当前字节的位置
    #返回值    Bool类型的值
    def finsReadBit(self,addr,site):
        data = self.parseData(self.finsRead(addr, 1), typeShort)
        if ((data & (1<<site))>>site) == 1:
            return True
        else:
            return False


    # 位操作，写1、0
    # addr      地址  'D100'
    # value     值   0/1		1
    # site     当前地址的第几位操作  [0,15]	3
    # 这里一次读取出来的数据为两个字，所以需要处理
    def finsWriteBit(self,addr,value,site):
        try:
            #这里必须取无符号数据方可，否则当出现
            #例如0xffff这样的数据时，第一位被当作符号位，造成数据值转换出错，造成数据处理错误
            currData = struct.unpack('>H', self.finsRead(addr, 1))[0]

            if site >= 0 and site <=15:
                #读回来原来的数据并做移位处理
                a = self.operateBit(currData,value,site)
                #写入当前的数据
                self.finsWrite(addr,typeUShort,a)
            else:
                print('out of range')
        except Exception as e:
            print(f"Database error: {e}")
            pass

    # 打印接收的16进制字节数据
    def printData(self, data):
        try:
            t = ['%02x' % ord(i) for i in data]
            return "".join(t)
        except Exception as e:
            print(f"Database error: {e}")
            pass
    def handleHandshake(self, data, index):
        try:
            # 判断错误码信息
            if data[index:index + 4] in self.finsErrorCode:  # 错误码
                if data[index:index + 4] == b'\x00\x00\x00\x00':
                    print('握手成功')
                    self.handshakeState = True
                else:
                    print('error code is : ', self.finsErrorCode[data[index:index + 4]])
                    self.disConnect()
                    return
            index += 4

            # 客户端节点地址
            # print'client ip is :',struct.unpack('>i',str(data[index:index+4]))[0]
            self.clientIp = struct.unpack('>i', (data[index:index + 4]))[0]
            index += 4

            # 服务器节点地址
            # print'server ip is',struct.unpack('>i',str(data[index:index+4]))[0]
            self.serverIp = struct.unpack('>i', (data[index:index + 4]))[0]
            index += 4
        except Exception as e:
            print(f"Database error: {e}")
            self.disConnect()
            print('function handleHandshake error')


    def handleDataFrame(self,data,index):
        try:
            # 判断错误码信息
            if data[index:index + 4] in self.finsErrorCode:  # 错误码
                if data[index:index + 4] != b'\x00\x00\x00\x00':
                    print('error code is : ', self.finsErrorCode[data[index:index + 4]])
                    self.disConnect()
                    return
            index += 4

            # FINS命令
            if data[index:index + 4] != b'\xc0\x00\x02\x00':
                print('FINS命令不正确')
                self.disConnect()
                return
            index += 4

            # IP地址
            # 这里先不管，好像IP地址和文档描述中存在差异，后期查阅资料补全，这里不检测
            index += 4

            # 读取数据命令
            if data[index:index + 4] == b'\x00\x00\x01\x01':
                pass
                # print('读数据命令返回帧')
            elif data[index:index + 4] == b'\x00\x00\x01\x02':
                pass
                # print('写数据命令返回帧')
            index += 4

            # 通讯状态
            if data[index:index + 2] != b'\x00\x00' and data[index:index + 2] != b'\x00\x40':
                pass
                print('通讯异常')
                print(self.printData(data))

                self.disConnect()
                return
            index += 2

            # 数据
            realDate = data[index:]

            return realDate
            # 解析完成
        except Exception as e:
            print(f"Database error: {e}")
            print('function handleDataFrame error')


    def handleData(self,data):

        try:
            index = 0
            #printself.printData(data)

            # 头部     4
            if data[0:4] != b'\x46\x49\x4e\x53':
                print(data)
                print('不是FINS协议命令')
                self.disConnect()
                return
            index += 4

            # 帧长度    4
            # print'=====',struct.unpack('>i',str(data[index:index+4]))[0]
            if (len(data) - 8) != struct.unpack('>i', (data[index:index + 4]))[0]:  # 大端模式
                print('接收长度错误')
                self.disConnect()
                return
            index += 4

            # 判断帧类型
            if data[index:index + 4] == b'\x00\x00\x00\x01':  # 握手帧返回
                index += 4
                self.handleHandshake(data, index)
            elif data[index:index + 4] == b'\x00\x00\x00\x02':  # 读写指令
                index += 4
                realDate = self.handleDataFrame(data, index)
                #printself.printData(realDate)
                return realDate
        except Exception as e:
            print(f"Database error: {e}")
            self.disConnect()
            print('function handleData error')

    #位操作函数
    #data   原数据
    #value  值
    #site	偏移位置
    def operateBit(self,data, value, site):
        if value == 1:  #置1
            return data | (1 << site)
        elif value == 0:    #置0
            return data & (~(1 << site))
        else:
            print('value is error')

    # --------  数字转进制  --------
    # num    转换的数字
    # fmt    转换的格式
    # fmt = 'b' => \x01
    # fmt = 'h' => \x00\x01
    # fmt = 'i' => \x00\x00\x00\x01
    def toHex(self, num, fmt):
        try:
            if fmt == 'b':  #signedchar
                return struct.pack('>b', num)
            elif fmt == 'B':  #unsignedchar
                return struct.pack('>B', num)
            elif fmt == 'h':  #short
                return struct.pack('>h', num)
            elif fmt == 'H':  #unsignedshort
                return struct.pack('>H', num)
            elif fmt == 'i':  #int
                return struct.pack('>i', num)
            elif fmt == 'I':  #unsignedint
                return struct.pack('>I', num)
            elif fmt == 'f':  #float
                return struct.pack('>f', num)
        except Exception as e:
            print(f"Database error: {e}")
            print('function toHex error')

if __name__ == '__main__':

    print('********enter FINS*************')
    aimIp = '127.0.0.1'
    #aimIp = '192.168.0.1'
    #aimIp = '192.167.4.119'
    aimPort = 9600

    f = Fins(aimIp,aimPort)


    '''
    while 1:
        j = 0
        if f.connectState == True:

            #读数据--最少读取一个字的长度数据
            #printf.printData(f.finsRead('D100', 1))

            #写数据Int--目前仅实现了写单独一个数据
            #f.finsWrite('D100',typeInt,12)
            #f.parseData(f.finsRead('D100', 2),typeInt)

            #写数据Float
            #f.finsWrite('D100',typeFloat,12.123)
            #f.parseData(f.finsRead('D100', 2),typeFloat)

            #位操作--地址、值、第几位	地址D100这个字的第3位写1
            f.finsWriteBit('D100',0,8)

        break
        time.sleep(1)
    '''















