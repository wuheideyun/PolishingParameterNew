from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget


class FormOmron(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 111, 111)  # 设置窗体的位置和大小情况
        self.setWindowTitle('欧姆龙PLC访问Demo')  # 设置窗体的标题
        self.userControlHead = UserControlHead(self)
        self.userControlHead.setGeometry(QtCore.QRect(0, 0, 1004, 32))
        self.userControlHead.setProtocol('Fins-Tcp')

        self.omron = None
        self.Address = 'D100'

        self.settings = QtWidgets.QWidget(self)
        self.settings.setGeometry(QtCore.QRect(14, 34, 978, 64))
        self.settings.setObjectName('settings')
        self.settings.setStyleSheet('QWidget#settings{border:1px solid gray;}')
        self.setStyleSheet('FormOmron{background:#F0F8FF;font:微软雅黑;}')

        self.label1 = QtWidgets.QLabel('Ip：', self.settings)
        self.label1.move(8, 17)
        self.textboxIp = QtWidgets.QLineEdit("", self.settings)
        self.textboxIp.setGeometry(62, 14, 114, 23)
        self.textboxIp.setText('127.0.0.1')

        self.label2 = QtWidgets.QLabel('Port：', self.settings)
        self.label2.move(182, 17)
        self.textboxPort = QtWidgets.QLineEdit("", self.settings)
        self.textboxPort.setGeometry(236, 14, 69, 23)
        self.textboxPort.setText('9600')

        self.label24 = QtWidgets.QLabel('PLC单元号：', self.settings)
        self.label24.move(311, 8)
        self.textbox16 = QtWidgets.QLineEdit("", self.settings)
        self.textbox16.setGeometry(387, 5, 56, 23)
        self.textbox16.setText('0')

        self.label25 = QtWidgets.QLabel('SA1', self.settings)
        self.label25.move(311, 35)
        self.textbox15 = QtWidgets.QLineEdit("", self.settings)
        self.textbox15.setGeometry(385, 32, 45, 23)
        self.textbox15.setText('')
        self.textbox15.setReadOnly(True)

        self.label26 = QtWidgets.QLabel('DA1', self.settings)
        self.label26.move(434, 35)
        self.textbox17 = QtWidgets.QLineEdit("", self.settings)
        self.textbox17.setGeometry(481, 32, 45, 23)
        self.textbox17.setText('')
        self.textbox17.setReadOnly(True)

        self.buttonConnect = QtWidgets.QPushButton('Connect', self.settings)
        self.buttonConnect.setGeometry(690, 11, 100, 28)
        self.buttonConnect.clicked.connect(self.button_connect_click)
        self.buttonDisConnect = QtWidgets.QPushButton('DisConnect', self.settings)
        self.buttonDisConnect.setGeometry(831, 11, 100, 28)
        self.buttonDisConnect.clicked.connect(self.button_disconnect_click)
        self.buttonDisConnect.setEnabled(False)
        # panel2
        self.panel2 = QtWidgets.QWidget(self)
        self.panel2.setGeometry(14, 100, 978, 537)
        self.panel2.setObjectName('panel2')
        self.panel2.setStyleSheet('QWidget#panel2{border:1px solid gray;}')
        self.userControlReadWriteOp1 = UserControlReadWriteOp(self.panel2)
        self.userControlReadWriteOp1.move(11, 2)
        # groupBox3
        self.groupBox3 = QtWidgets.QGroupBox(self.panel2)
        self.groupBox3.setTitle('Bulk Read test')
        self.groupBox3.setGeometry(11, 243, 518, 154)
        self.label11 = QtWidgets.QLabel('Address：', self.groupBox3)
        self.label11.move(9, 30)
        self.textbox6 = QtWidgets.QLineEdit('', self.groupBox3)
        self.textbox6.setGeometry(63, 27, 102, 23)
        self.textbox6.setText(self.Address)
        self.label12 = QtWidgets.QLabel('Length：', self.groupBox3)
        self.label12.move(180, 30)
        self.textbox9 = QtWidgets.QLineEdit('', self.groupBox3)
        self.textbox9.setGeometry(234, 27, 102, 23)
        self.textbox9.setText('10')
        self.button25 = QtWidgets.QPushButton('bulk read', self.groupBox3)
        self.button25.setGeometry(426, 24, 82, 28)
        self.button25.clicked.connect(self.button25_click)
        self.label13 = QtWidgets.QLabel("Result:", self.groupBox3)
        self.label13.move(9, 62)
        self.textbox10 = QtWidgets.QTextEdit("", self.groupBox3)
        self.textbox10.setGeometry(63, 60, 445, 78)
        # groupBox4
        self.groupBox4 = QtWidgets.QGroupBox(self.panel2)
        self.groupBox4.setTitle('Message reading test, hex string needs to be filled in')
        self.groupBox4.setGeometry(11, 403, 518, 118)
        self.label16 = QtWidgets.QLabel('Message：', self.groupBox4)
        self.label16.move(9, 30)
        self.textbox13 = QtWidgets.QLineEdit('', self.groupBox4)
        self.textbox13.setGeometry(63, 27, 357, 23)
        self.button26 = QtWidgets.QPushButton('Read', self.groupBox4)
        self.button26.setGeometry(426, 24, 82, 28)
        self.button26.clicked.connect(self.button26_click)
        self.label14 = QtWidgets.QLabel("Result:", self.groupBox4)
        self.label14.move(9, 62)
        self.textbox11 = QtWidgets.QTextEdit('', self.groupBox4)
        self.textbox11.setGeometry(63, 60, 445, 52)
        # groupBox5
        self.groupBox5 = QtWidgets.QGroupBox(self.panel2)
        self.groupBox5.setTitle('Special function test')
        self.groupBox5.setGeometry(546, 243, 419, 278)

        self.textbox3 = QtWidgets.QTextEdit('', self.groupBox5)
        self.textbox3.setGeometry(16, 93, 388, 145)

        self.panel2.setEnabled(False)
        self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()),
                  (screen.height() - size.height()))

    def button_connect_click(self):
        self.omron = OmronFinsNet(self.textboxIp.text(), int(self.textboxPort.text()))
        self.omron.DA2 = int(self.textbox16.text())
        connect = self.omron.ConnectServer()
        if connect.IsSuccess == False:
            QMessageBox.information(self, 'Info', 'Connect Failed: ' + connect.ToMessageShowString())
        else:
            QMessageBox.information(self, 'Info', 'Connect Success!')
            self.buttonConnect.setEnabled(False)
            self.buttonDisConnect.setEnabled(True)
            self.textbox15.setText(str(self.omron.SA1))
            self.textbox17.setText(str(self.omron.DA1))
            self.panel2.setEnabled(True)
            self.userControlReadWriteOp1.SetReadWriteNet(self.omron, self.Address)

    def button_disconnect_click(self):
        disconnect = self.omron.ConnectClose()
        if disconnect.IsSuccess == True:
            self.panel2.setEnabled(False)
            self.buttonConnect.setEnabled(True)
            self.buttonDisConnect.setEnabled(False)
        else:
            QMessageBox.information(self, 'Info', 'DisConnect Failed: ' + disconnect.ToMessageShowString())

    def button25_click(self):
        read = self.omron.Read(self.textbox6.text(), int(self.textbox9.text()))
        if read.IsSuccess == True:
            self.textbox10.setText(datetime.datetime.now().strftime(
                '%H:%M:%S') + " [" + self.textbox6.text() + "] " + SoftBasic.ByteToHexString(read.Content))
        else:
            QMessageBox.information(self, 'Info', 'Read Failed: ' + read.ToMessageShowString())

    def button26_click(self):
        read = self.omron.ReadFromCoreServer(SoftBasic.HexStringToBytes(self.textbox13.text()))
        if read.IsSuccess == True:
            self.textbox11.setText(
                datetime.datetime.now().strftime('%H:%M:%S') + " " + SoftBasic.ByteToHexString(read.Content))
        else:
            QMessageBox.information(self, 'Info', 'Read Failed: ' + read.ToMessageShowString())
class UserControlHead(QWidget):
	def __init__(self, parent = None):
		super().__init__()
		self.setParent(parent)
		self.initUI()
	def initUI(self):
		self.setMinimumSize(800, 32)
		self.HelpLink = 'http://www.hslcommunication.cn/'

		self.helpLinkLabel1 = QtWidgets.QLabel('博客地址：', self)
		self.helpLinkLabel1.move(13, 10)

		self.helpLinkLabel = QtWidgets.QLabel(self.HelpLink, self)
		self.helpLinkLabel.move(80, 10)
		self.helpLinkLabel.mousePressEvent = self.pushButtonClick

		self.protocol1 = QtWidgets.QLabel('使用协议：', self)
		self.protocol1.move(544, 10)

		self.protocol = QtWidgets.QLabel('HSL', self)
		self.protocol.move(618, 10)

		self.version = QtWidgets.QLabel('Version: ', self)
		self.version.move(886, 10)

		self.setStyleSheet('QWidget{color:#eeeeee;}')
	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		self.drawWidget(qp)
		qp.end()
	def drawWidget(self, qp):
		qp.setBrush(QColor(0x40, 0x40, 0x40))
		qp.drawRect(0, 0, self.size().width(), self.size().height())
	def pushButtonClick(self, e):
		QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.helpLinkLabel.text()))
	def setHelpLink( self, value : str ):
		'''设置显示的帮助链接'''
		self.HelpLink = value
		self.helpLinkLabel.setText(value)
	def setProtocol( self, value : str ):
		'''设置协议名称'''
		self.protocol.setText(value)


