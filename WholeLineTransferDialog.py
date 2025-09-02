import sys
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QGridLayout,
    QMessageBox, QPushButton, QApplication, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt, QTimer

from WholeLineConfigManager import WholeLineConfigManager
from ConnectionWorker import ConnectionWorker
from omron_plc_gui import PLCCommunicator
from WholeLinePLCInterface import WholeLinePLCInterface


class WholeLineTransferDialog(QDialog):
    def __init__(self, whole_line_param_json: str, config_manager, parent=None):
        super().__init__(parent)

        # 将传入的JSON字符串暂存起来
        self.params_to_send_json = whole_line_param_json
        self.config_manager = config_manager

        self.connection_threads = {}
        self.plc_instances = {}

        self.setWindowTitle("整线数据传输")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: rgb(31, 55, 96); color: white;")
        self.setModal(True)

        main_layout = QVBoxLayout(self)

        title_label = QLabel("整线通讯中心", self)
        title_label.setFont(QFont("Microsoft YaHei", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 创建表格来显示每台设备
        self.device_table = QTableWidget()
        self.device_table.setColumnCount(5)
        self.device_table.setHorizontalHeaderLabels(["设备编号", "目标IP地址", "端口", "连接状态", "操作"])
        self.device_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.device_table.horizontalHeader().setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.device_table.setFont(QFont("Microsoft YaHei", 11))
        self.device_table.setStyleSheet("""
            QTableWidget { gridline-color: #555; }
            QHeaderView::section { background-color: #2c3e50; }
        """)
        main_layout.addWidget(self.device_table)

        # 创建底部总控按钮
        bottom_button_layout = QHBoxLayout()
        self.connect_all_button = QPushButton("全部连接")
        self.disconnect_all_button = QPushButton("全部断开")
        self.send_params_button = QPushButton("进入参数发送")
        self.close_button = QPushButton("关闭")

        button_style = """
            QPushButton { 
                background-color: #30438c; color: white; border: none; 
                padding: 10px; font-size: 16px; border-radius: 5px; min-width: 120px;
            }
            QPushButton:hover { background-color: #40539c; }
            QPushButton:pressed { background-color: #7986b5; }
        """
        for btn in [self.connect_all_button, self.disconnect_all_button, self.send_params_button, self.close_button]:
            btn.setStyleSheet(button_style)

        bottom_button_layout.addStretch()
        bottom_button_layout.addWidget(self.connect_all_button)
        bottom_button_layout.addWidget(self.disconnect_all_button)
        bottom_button_layout.addWidget(self.send_params_button)
        bottom_button_layout.addWidget(self.close_button)
        main_layout.addLayout(bottom_button_layout)

        # 连接信号
        self.close_button.clicked.connect(self.accept)
        self.connect_all_button.clicked.connect(self.connect_all_devices)
        self.disconnect_all_button.clicked.connect(self.disconnect_all_devices)
        self.send_params_button.clicked.connect(self.open_plc_interface)

        self.populate_device_table()

    def populate_device_table(self):
        line_config = self.config_manager.load_config()
        comm_configs = line_config.get('communication', [])
        self.device_table.setRowCount(len(comm_configs))

        for i, comm_config in enumerate(comm_configs):
            setattr(self, f'connect_btn_{i}', QPushButton("连接"))
            connect_button = getattr(self, f'connect_btn_{i}')
            connect_button.clicked.connect(lambda _, r=i: self.toggle_connection(r))

            device_num_item = QTableWidgetItem(f"{i + 1} 号机")
            ip_item = QTableWidgetItem(comm_config.get('ip', 'N/A'))
            port_item = QTableWidgetItem(comm_config.get('port', 'N/A'))
            status_item = QTableWidgetItem("未连接")
            status_item.setBackground(QColor("gray"))
            status_item.setTextAlignment(Qt.AlignCenter)

            self.device_table.setItem(i, 0, device_num_item)
            self.device_table.setItem(i, 1, ip_item)
            self.device_table.setItem(i, 2, port_item)
            self.device_table.setItem(i, 3, status_item)
            self.device_table.setCellWidget(i, 4, connect_button)

    def toggle_connection(self, row):
        if row in self.plc_instances:
            plc_instance = self.plc_instances.get(row)
            thread = ConnectionWorker(row, None, None, plc_instance, action='disconnect')
            thread.disconnection_finished.connect(self.on_disconnection_finished)
            self.connection_threads[row] = thread
            thread.start()
        else:
            ip = self.device_table.item(row, 1).text()
            port_text = self.device_table.item(row, 2).text()
            try:
                port = int(port_text)
            except (ValueError, TypeError):
                QMessageBox.warning(self, "错误", f"{row + 1}号机端口号无效！")
                return

            status_item = self.device_table.item(row, 3)
            status_item.setText("连接中...")
            status_item.setBackground(QColor("orange"))

            thread = ConnectionWorker(row, ip, port, action='connect')
            thread.connection_finished.connect(self.on_connection_finished)
            self.connection_threads[row] = thread
            thread.start()

    def connect_all_devices(self):
        for row in range(self.device_table.rowCount()):
            if row not in self.plc_instances:
                self.toggle_connection(row)

    def disconnect_all_devices(self):
        for row in range(self.device_table.rowCount()):
            if row in self.plc_instances:
                self.toggle_connection(row)

    def on_connection_finished(self, row, success, result):
        status_item = self.device_table.item(row, 3)
        connect_button = self.device_table.cellWidget(row, 4)
        if success:
            status_item.setText("已连接")
            status_item.setBackground(QColor("green"))
            if connect_button: connect_button.setText("断开")
            self.plc_instances[row] = result
        else:
            status_item.setText("失败")
            status_item.setBackground(QColor("red"))
            QMessageBox.warning(self, f"{row + 1}号机连接失败", str(result))

    def on_disconnection_finished(self, row, success, message):
        status_item = self.device_table.item(row, 3)
        connect_button = self.device_table.cellWidget(row, 4)
        status_item.setText("未连接")
        status_item.setBackground(QColor("gray"))
        if connect_button: connect_button.setText("连接")
        if row in self.plc_instances:
            del self.plc_instances[row]

    def open_plc_interface(self):
        # if not self.plc_instances:
        #     QMessageBox.warning(self, "提示", "没有已连接的PLC设备！")
        #     return

        dialog = WholeLinePLCInterface(self.plc_instances, self.params_to_send_json, self)
        dialog.exec()

    def closeEvent(self, event):
        self.disconnect_all_devices()
        for thread in self.connection_threads.values():
            thread.wait()
        event.accept()