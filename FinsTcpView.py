import sys

from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QRadioButton,
                               QVBoxLayout, QHBoxLayout, QGroupBox, QGridLayout, QCheckBox)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from FinsTcp import FinsTcp


class PLCCommunicationDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('欧姆龙PLC访问Demo')
        self.setGeometry(300, 100, 800, 500)
        self.tcp = ''



        # Title and Info
        main_layout = QVBoxLayout()
        # title_layout = QHBoxLayout()
        # title_label = QLabel("博客地址: http://www.hslcommunication.cn/")
        # title_label.setFont(QFont("Arial", 10))
        # protocol_label = QLabel("使用协议：Fins-Tcp")
        # protocol_label.setFont(QFont("Arial", 10))
        # version_label = QLabel("Version:")
        # version_label.setFont(QFont("Arial", 10))
        # title_layout.addWidget(title_label)
        # title_layout.addStretch(1)
        # title_layout.addWidget(protocol_label)
        # title_layout.addWidget(version_label)
        # main_layout.addLayout(title_layout)

        # Connection Section
        connection_layout = QHBoxLayout()
        self.ip_edit = QLineEdit("127.0.0.1")
        self.port_edit = QLineEdit("9600")
        self.plc_unit_edit = QLineEdit("0")
        self.sa1_edit = QLineEdit()
        self.da1_edit = QLineEdit()
        connect_btn = QPushButton("Connect")
        connect_btn.clicked.connect(self.connectplc)
        disconnect_btn = QPushButton("DisConnect")

        connection_layout.addWidget(QLabel("Ip:"))
        connection_layout.addWidget(self.ip_edit)
        connection_layout.addWidget(QLabel("Port:"))
        connection_layout.addWidget(self.port_edit)
        connection_layout.addWidget(QLabel("PLC单元号:"))
        connection_layout.addWidget(self.plc_unit_edit)
        connection_layout.addWidget(QLabel("SA1"))
        connection_layout.addWidget(self.sa1_edit)
        connection_layout.addWidget(QLabel("DA1"))
        connection_layout.addWidget(self.da1_edit)
        connection_layout.addWidget(connect_btn)
        connection_layout.addWidget(disconnect_btn)
        main_layout.addLayout(connection_layout)

        # Read/Write Data Group
        data_layout = QGridLayout()

        read_group = QGroupBox("Read Data Single")
        read_layout = QGridLayout()
        self.read_address_edit = QLineEdit()
        self.read_result_edit = QLineEdit()
        self.read_result_edit.setReadOnly(True)
        read_layout.addWidget(QLabel("Address:"), 0, 0)
        read_layout.addWidget(self.read_address_edit, 0, 1)
        read_layout.addWidget(QLabel("Result:"), 1, 0)
        read_layout.addWidget(self.read_result_edit, 1, 1)
        read_group.setLayout(read_layout)

        write_group = QGroupBox("Write Data Single")
        write_layout = QGridLayout()
        self.write_address_edit = QLineEdit()
        self.write_value_edit = QLineEdit("False")
        write_layout.addWidget(QLabel("Address:"), 0, 0)
        write_layout.addWidget(self.write_address_edit, 0, 1)
        write_layout.addWidget(QLabel("Value:"), 1, 0)
        write_layout.addWidget(self.write_value_edit, 1, 1)
        write_layout.addWidget(QLabel("Note: The value of the string needs to be converted"), 2, 1, 1, 2)
        write_group.setLayout(write_layout)

        data_layout.addWidget(read_group, 0, 0)
        data_layout.addWidget(write_group, 0, 1)
        main_layout.addLayout(data_layout)

        # Bulk Read Section
        bulk_read_group = QGroupBox("Bulk Read Test")
        bulk_read_layout = QHBoxLayout()
        self.bulk_address_edit = QLineEdit("D100")
        self.bulk_length_edit = QLineEdit("10")
        self.bulk_result_edit = QLineEdit()
        bulk_read_btn = QPushButton("Bulk Read")
        bulk_read_layout.addWidget(QLabel("Address:"))
        bulk_read_layout.addWidget(self.bulk_address_edit)
        bulk_read_layout.addWidget(QLabel("Length:"))
        bulk_read_layout.addWidget(self.bulk_length_edit)
        bulk_read_layout.addWidget(bulk_read_btn)
        bulk_read_layout.addWidget(QLabel("Result:"))
        bulk_read_layout.addWidget(self.bulk_result_edit)
        bulk_read_group.setLayout(bulk_read_layout)
        main_layout.addWidget(bulk_read_group)

        # Special Function Test Section
        special_function_group = QGroupBox("Message Reading Test, Hex String Needs to Be Filled In")
        special_function_layout = QHBoxLayout()
        self.message_edit = QLineEdit()
        self.message_result_edit = QLineEdit()
        special_read_btn = QPushButton("Read")
        special_function_layout.addWidget(QLabel("Message:"))
        special_function_layout.addWidget(self.message_edit)
        special_function_layout.addWidget(special_read_btn)
        special_function_layout.addWidget(QLabel("Result:"))
        special_function_layout.addWidget(self.message_result_edit)
        special_function_group.setLayout(special_function_layout)
        main_layout.addWidget(special_function_group)

        # Set main layout
        self.setLayout(main_layout)


    def connectplc(self):
        self.tcp = FinsTcp('127.0.0.1', 9600, 22)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PLCCommunicationDemo()
    window.show()
    app.exec()
