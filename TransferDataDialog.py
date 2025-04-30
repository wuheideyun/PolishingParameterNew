import json
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QFrame, QGridLayout, QPushButton, QMessageBox, QSizePolicy
)
from PySide6.QtGui import QFont, QPainter, QColor, QBrush
from PySide6.QtCore import Qt, QSettings, QTimer
import FinsTcp
from ImageChangeButton import ImageChangeButton


class TransferDataDialog(QDialog):
    def __init__(self, selected_data):
        super().__init__()
        self.setWindowTitle(self.tr("数据传输"))
        self.setGeometry(450, 200, 100, 150)  # 调整窗口大小
        self.setStyleSheet("background-color: rgb(31, 55, 96); color: white;")  # 设置背景颜色和字体颜色

        # 创建主布局
        main_layout = QVBoxLayout()

        # 创建参数区域
        self.create_parameter_area(main_layout, selected_data)

        # 创建设备连接区域
        self.create_device_connection_area(main_layout)

        # 创建发送按钮
        self.create_send_button(main_layout)

        # 设置布局
        self.setLayout(main_layout)

        # 初始化 TCP 连接状态
        self.tcp = None
        self.connected = False

        # 创建定时器监控连接状态
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_connection_status)
        self.timer.start(1000)  # 每秒检查一次连接状态

    def create_parameter_area(self, main_layout, selected_data):
        # 创建一个 QFrame 作为参数区域容器，并设置样式
        parameter_frame = QFrame(self)
        parameter_frame.setStyleSheet("QFrame { border: 5px solid #1e5dab; border-radius: 15px; padding: 10px; }")
        parameter_layout = QGridLayout(parameter_frame)  # 使用网格布局

        # 添加参数区域标题
        parameter_title = QLabel(self.tr("确认发送参数"), self)
        parameter_title.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        parameter_title.setAlignment(Qt.AlignCenter)
        parameter_title.setStyleSheet("QLabel { border: none; }")  # 设置无边框
        main_layout.addWidget(parameter_title)

        # 创建标签和不可编辑的输入框
        labels = [
            self.tr("模式"), 
            self.tr("方案选择"),
            self.tr("设备"), 
            self.tr("主皮带速度(mm/s)"),
            self.tr("横梁摆动速度(mm/s)"), 
            self.tr("加速度大小(mm/s²)"),  
            self.tr("同粒度磨头数(个)"), 
            self.tr("摆幅(mm)"), 
            self.tr("延时时间(s)"), 
            self.tr("横梁边部停留时间(s)")
        ]
        self.line_edits = []

        # 设置字体
        font = QFont("Microsoft YaHei", 12)

        # 添加标签和输入框到网格布局
        for i, label_text in enumerate(labels):
            label = QLabel(label_text + ":", self)
            label.setFont(font)
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # 文字右对齐并垂直居中
            label.setStyleSheet("QLabel { border: none; }")  # 设置无边框
            line_edit = QLineEdit(self)
            line_edit.setFont(font)
            line_edit.setReadOnly(True)  # 设置为不可编辑
            line_edit.setStyleSheet("background-color: #444;color: white; border: 1px solid #666; border-radius: 3px; padding: 5px;")
            line_edit.setFixedWidth(100)  # 调整输入框宽度
            self.line_edits.append(line_edit)

            # 将组件添加到网格布局中，每行4个组件
            row = i // 3  # 每行4个组件，计算行号
            col = i % 3   # 计算列号
            parameter_layout.addWidget(label, row, col * 2)
            parameter_layout.addWidget(line_edit, row, col * 2 + 1)

        # 将参数区域 QFrame 添加到主布局
        main_layout.addWidget(parameter_frame)

        # 填充数据
        if selected_data:
            self.fill_data(selected_data)

    def create_device_connection_area(self, main_layout):
        # 创建一个 QFrame 作为设备连接区域容器，并设置样式
        connection_frame = QFrame(self)
        connection_frame.setStyleSheet("QFrame { border: 5px solid #1e5dab; border-radius: 15px; padding: 10px; }")
        connection_frame.setFixedSize(600,150)
        connection_layout = QGridLayout(connection_frame)  # 使用网格布局
        connection_layout.setAlignment(connection_frame, Qt.AlignmentFlag.AlignHCenter)

        # 添加设备连接区域标题
        connection_title = QLabel(self.tr("设备连接配置"), self)
        connection_title.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        connection_title.setAlignment(Qt.AlignCenter)
        connection_title.setStyleSheet("QLabel { border: none; }")  # 设置无边框
        main_layout.addWidget(connection_title)

        # 设置字体
        font = QFont("Microsoft YaHei", 12)

        # 创建标签和输入框
        self.plc_ip_label = QLabel(self.tr("PLC IP:"), self)
        self.plc_ip_label.setFont(font)
        self.plc_ip_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # 标签宽度仅包含文本
        self.plc_ip_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # 文字右对齐并垂直居中
        self.plc_ip_label.setStyleSheet("QLabel { border: none; }")  # 设置无边框

        self.plc_ip_edit = QLineEdit(self)
        self.plc_ip_edit.setFont(font)
        self.plc_ip_edit.setStyleSheet(
            "background-color: #444; border: 1px solid #666; border-radius: 3px; padding: 5px;")
        self.plc_ip_edit.setFixedWidth(150)  # 调整输入框宽度

        self.port_label = QLabel(self.tr("端口号:"), self)
        self.port_label.setFont(font)
        self.port_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # 标签宽度仅包含文本
        self.port_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # 文字右对齐并垂直居中
        self.port_label.setStyleSheet("QLabel { border: none; }")  # 设置无边框

        self.port_edit = QLineEdit(self)
        self.port_edit.setFont(font)
        self.port_edit.setStyleSheet(
            "background-color: #444; border: 1px solid #666; border-radius: 3px; padding: 5px;")
        self.port_edit.setFixedWidth(100)  # 调整输入框宽度

        # 从配置文件中读取初始值
        self.settings = QSettings("config.ini", QSettings.IniFormat)
        self.plc_ip_edit.setText(self.settings.value("PLCIP", ""))
        self.port_edit.setText(self.settings.value("Port", ""))

        # 添加到网格布局
        connection_layout.addWidget(self.plc_ip_label, 0, 0)
        connection_layout.addWidget(self.plc_ip_edit, 0, 1)
        connection_layout.addWidget(self.port_label, 0, 2)
        connection_layout.addWidget(self.port_edit, 0, 3)

        # 创建保存按钮
        self.save_button = ImageChangeButton(self.tr("保存配置"), ":SmallFrame", ":SmallFrameClicked", 114, 37, True)
        self.save_button.clicked.connect(self.save_settings)

        # 创建连接PLC按钮
        self.connect_button = ImageChangeButton(self.tr("连接PLC"), ":SmallFrame", ":SmallFrameClicked", 114, 37, True)
        self.connect_button.clicked.connect(self.toggle_connection)

        # 添加按钮到布局
        connection_layout.addWidget(self.save_button, 0, 4)
        connection_layout.addWidget(self.connect_button, 1, 1)

        # 创建状态标签和圆形图标
        self.status_label = QLabel(self.tr("连接状态:"), self)
        self.status_label.setFont(font)
        self.status_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # 标签宽度仅包含文本
        self.status_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # 文字右对齐并垂直居中
        self.status_label.setStyleSheet("QLabel { border: none; }")  # 设置无边框

        self.status_icon = QLabel(self)
        self.status_icon.setFixedSize(20, 20)  # 圆形图标大小
        self.status_icon.setStyleSheet("QLabel { border: none; }")  # 设置无边框
        self.update_status_icon(False)  # 初始状态为红色

        # 添加到布局
        connection_layout.addWidget(self.status_label, 1, 2)
        connection_layout.addWidget(self.status_icon, 1, 3)

        # 将设备连接区域 QFrame 添加到主布局并水平居中
        main_layout.addWidget(connection_frame)
        main_layout.setAlignment(connection_frame, Qt.AlignHCenter)  # 水平居中

    def create_send_button(self, main_layout):
        # 创建发送按钮
        self.send_button = ImageChangeButton(self.tr("发送参数"), ":SmallFrame", ":SmallFrameClicked", 114, 37, True)
        self.send_button.clicked.connect(self.send_data)

        # 添加到主布局
        main_layout.addWidget(self.send_button)
        main_layout.setAlignment(self.send_button, Qt.AlignmentFlag.AlignHCenter)

    def fill_data(self, data):
        full_motion_param_dict = json.loads(data[8])
        self.line_edits[0].setText(data[0])  # 模式
        self.line_edits[1].setText(data[1])  # 方案选择
        self.line_edits[2].setText(data[7])  # 设备
        self.line_edits[3].setText(data[2])  # 主皮带速度
        self.line_edits[4].setText(data[4])  # 横梁摆动速度
        self.line_edits[5].setText(str(full_motion_param_dict['lineEdit_accelerate']))  # 加速度大小
        self.line_edits[6].setText(str(full_motion_param_dict['lineEdit_num_output']))  # 同粒度磨头数
        self.line_edits[7].setText(str(full_motion_param_dict['lineEdit_swing']))  # 摆幅
        self.line_edits[8].setText(str(full_motion_param_dict['lineEdit_delay_time']))  # 延时时间
        self.line_edits[9].setText(str(full_motion_param_dict['lineEdit_stay_time']))  # 横梁边部停留时间

    def save_settings(self):
        # 将 PLC IP 和端口号保存到配置文件中
        self.settings.setValue("PLCIP", self.plc_ip_edit.text())
        self.settings.setValue("Port", self.port_edit.text())
        QMessageBox.information(self, "保存成功", "配置已保存！")

    def toggle_connection(self):
        # 切换连接状态
        if self.connect_button.text() == "连接PLC":
            # 获取 PLC IP 和端口号
            plc_ip = self.plc_ip_edit.text()
            port = self.port_edit.text()

            # 检查是否输入了值
            if not plc_ip or not port:
                QMessageBox.warning(self, "输入错误", "请输入 PLC IP 和端口号！")
                return

            try:
                # 创建 FinsTcp 对象
                self.tcp = FinsTcp.FinsTcp(plc_ip, int(port), 22)

                # 检查连接状态
                if self.tcp.connected:
                    self.connect_button.setText("断开PLC")
                    self.connected = True
                    QMessageBox.information(self, "连接成功", "已成功连接到 PLC！")
                else:
                    QMessageBox.warning(self, "连接失败", "无法连接到 PLC，请检查 IP 和端口号！")
            except Exception as e:
                QMessageBox.critical(self, "连接错误", f"连接过程中发生错误：{str(e)}")
        else:
            # 断开连接
            if self.tcp:
                self.tcp.disconnect()
                self.connect_button.setText("连接PLC")
                self.connected = False
                QMessageBox.information(self, "断开成功", "已成功断开连接！")

    def update_connection_status(self):
        # 更新连接状态图标
        if self.tcp and self.tcp.connected:
            self.update_status_icon(True)
        else:
            self.update_status_icon(False)

    def update_status_icon(self, connected):
        # 更新圆形图标颜色
        if connected:
            self.status_icon.setStyleSheet("border : none;background-color: green; border-radius: 10px;")
        else:
            self.status_icon.setStyleSheet("border : none;background-color: red; border-radius: 10px;")

    def send_data(self):
        # 判断连接状态
        if not self.tcp or not self.tcp.connected:
            QMessageBox.warning(self, "发送失败", "请先连接设备！")
            return

        # 发送数据逻辑
        QMessageBox.information(self, "发送成功", "数据已成功发送！")

    def closeEvent(self, event):
        # 关闭窗口时断开连接
        if self.tcp:
            self.tcp.disconnect()
        event.accept()