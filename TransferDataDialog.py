import json
import time
from aphyt import omron
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QFrame, QGridLayout, QMessageBox, QSizePolicy, QPushButton, QApplication
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QSettings, QTimer
from omron_plc_gui import PLCCommunicator
from ImageChangeButton import ImageChangeButton
from datetime import datetime

class PLCInterface(QDialog):
    VARIABLES = [
        {"name": "传动给定速度", "type": "float"},  # 对应主皮带速度
        {"name": "同步给定速度", "type": "float"},  # 对应横梁摆动速度
        {"name": "横梁当前运行状态", "type": "bool"},
        {"name": "界面模式1选择", "type": "bool"},  # 交叉摆
        {"name": "界面模式3选择", "type": "bool"},  # 顺序摆
        {"name": "界面横梁同步确定按钮", "type": "bool"},  # 同步摆
        {"name": "界面横梁1同步选择", "type": "bool"},
        {"name": "界面横梁2同步选择", "type": "bool"},
        {"name": "界面横梁3同步选择", "type": "bool"},
        {"name": "界面横梁4同步选择", "type": "bool"},
        {"name": "界面横梁5同步选择", "type": "bool"},
        {"name": "界面横梁6同步选择", "type": "bool"},
        {"name": "横梁1加速度", "type": "float"},  # 对应加速度大小
        {"name": "同步操作面设定值", "type": "float"},
        {"name": "同步非操作面设定值", "type": "float"},
        {"name": "横梁同步操作面停留时间", "type": "int"},
        {"name": "横梁同步非操作面停留时间", "type": "int"},
        {"name": "延时时间", "type": "int"}
    ]

    PARAMETER_MAPPING = {
        "传动给定速度": "主皮带速度",
        "同步给定速度": "横梁摆动速度",
        "界面模式1选择": "方案选择 (交叉摆)",
        "界面模式3选择": "方案选择 (顺序摆)",
        "界面横梁同步确定按钮": "方案选择 (同步摆)",
        "横梁1加速度": "加速度大小",
        "同步操作面设定值": "摆幅",
        "横梁同步操作面停留时间": "横梁边部停留时间",
        "延时时间": "延时时间",
    }

    def __init__(self, plc, line_edits, parent=None):
        super().__init__(parent)
        print("初始化 PLCInterface")
        self.setWindowTitle("欧姆龙PLC通讯")
        self.setGeometry(300, 100, 800, 400)
        try:
            self.setStyleSheet("background-color: rgb(31, 55, 96); color: white;")
            print("设置窗口样式成功")
        except Exception as e:
            print(f"设置窗口样式失败: {str(e)}")
            raise

        self.plc = plc
        self.line_edits = line_edits

        main_layout = QVBoxLayout()
        self.create_table_area(main_layout)
        self.create_action_area(main_layout)
        self.setLayout(main_layout)

        # 自动查询
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.query_variables)
        self.timer.setSingleShot(True)
        if self.plc and self.plc.is_connected():
            self.timer.start(100)
            print("启动自动查询定时器")

    def create_table_area(self, main_layout):
        print("创建表格区域")
        table_frame = QFrame(self)
        if not table_frame:
            print("table_frame 创建失败")
            raise RuntimeError("无法创建 table_frame")
        try:
            table_frame.setStyleSheet("QFrame { border: 5px solid #1e5dab; border-radius: 15px; padding: 10px; }")
            print("设置 table_frame 样式成功")
        except Exception as e:
            print(f"设置 table_frame 样式失败: {str(e)}")
            raise

        table_layout = QGridLayout(table_frame)
        table_layout.setVerticalSpacing(2)  # 减少行间距
        font = QFont("Microsoft YaHei", 10, QFont.Bold)  # 表头字体大小减小

        # 表头
        header_labels = ["参数", "PLC变量名", "读取值", "写入值"]
        for col, text in enumerate(header_labels):
            label = QLabel(text, self)
            if not label:
                print(f"表头标签 {text} 创建失败")
                raise RuntimeError(f"无法创建表头标签 {text}")
            label.setFont(font)
            label.setStyleSheet("border: none; padding: 2px;")  # 减少padding
            label.setMaximumHeight(20)  # 设置最大高度
            table_layout.addWidget(label, 0, col, alignment=Qt.AlignCenter)
            print(f"添加表头 {text}")

        self.read_labels = []
        self.write_entries = []
        font = QFont("Microsoft YaHei", 10)  # 内容字体大小减小

        for i, var in enumerate(self.VARIABLES, start=1):
            # 参数
            param_name = self.PARAMETER_MAPPING.get(var["name"], "-")
            param_label = QLabel(param_name, self)
            if not param_label:
                print(f"参数标签 {param_name} 创建失败")
                raise RuntimeError(f"无法创建参数标签 {param_name}")
            param_label.setFont(font)
            param_label.setStyleSheet("border: none; padding: 2px;")  # 减少padding
            param_label.setFixedWidth(150)
            param_label.setMaximumHeight(20)  # 设置最大高度
            table_layout.addWidget(param_label, i, 0, alignment=Qt.AlignLeft)
            print(f"添加参数 {param_name}")

            # PLC变量名
            var_label = QLabel(var["name"], self)
            if not var_label:
                print(f"PLC变量名标签 {var['name']} 创建失败")
                raise RuntimeError(f"无法创建 PLC变量名标签 {var['name']}")
            var_label.setFont(font)
            var_label.setStyleSheet("border: none; padding: 2px;")  # 减少padding
            var_label.setFixedWidth(150)
            var_label.setMaximumHeight(20)  # 设置最大高度
            table_layout.addWidget(var_label, i, 1, alignment=Qt.AlignLeft)
            print(f"添加 PLC变量名 {var['name']}")

            # 读取值
            read_label = QLabel("", self)
            if not read_label:
                print(f"读取值标签 {i} 创建失败")
                raise RuntimeError(f"无法创建读取值标签 {i}")
            read_label.setFont(font)
            read_label.setStyleSheet("background-color: #444; border: 1px solid #666; border-radius: 3px; padding: 2px;")  # 减少padding
            read_label.setFixedWidth(100)
            read_label.setMaximumHeight(20)  # 设置最大高度
            table_layout.addWidget(read_label, i, 2)
            self.read_labels.append(read_label)
            print(f"添加读取值标签 {i}")

            # 写入值
            write_entry = QLineEdit(self)
            if not write_entry:
                print(f"写入值输入框 {i} 创建失败")
                raise RuntimeError(f"无法创建写入值输入框 {i}")
            write_entry.setFont(font)
            write_entry.setStyleSheet("background-color: #444; border: 1px solid #666; border-radius: 3px; padding: 2px;")  # 减少padding
            write_entry.setFixedWidth(100)
            write_entry.setMaximumHeight(20)  # 设置最大高度
            table_layout.addWidget(write_entry, i, 3)
            self.write_entries.append(write_entry)
            print(f"添加写入值输入框 {i}")

        main_layout.addWidget(table_frame)
        print("表格区域创建完成")
        self.fill_line_edits()

    def create_action_area(self, main_layout):
        print("创建按钮区域")
        action_frame = QFrame(self)
        if not action_frame:
            print("action_frame 创建失败")
            raise RuntimeError("无法创建 action_frame")
        try:
            action_frame.setStyleSheet("QFrame { border: 5px solid #1e5dab; border-radius: 15px; padding: 10px; }")
            print("设置 action_frame 样式成功")
        except Exception as e:
            print(f"设置 action_frame 样式失败: {str(e)}")
            raise

        action_layout = QHBoxLayout(action_frame)
        font = QFont("Microsoft YaHei", 12)
        button_style = """
            QPushButton { background-color: #444; color: white; border: 1px solid #666; border-radius: 3px; padding: 5px; }
            QPushButton:hover { background-color: #666; }
        """

        buttons = [
            ("交叉摆", self.set_cross_swing),
            ("顺序摆", self.set_sequence_swing),
            ("同步摆", self.set_sync_swing),
            ("查询", self.query_variables),
            ("写入", self.write_variables)
        ]

        for text, command in buttons:
            button = QPushButton(text, self)
            if not button:
                print(f"按钮 {text} 创建失败")
                raise RuntimeError(f"无法创建按钮 {text}")
            button.setFont(font)
            button.setStyleSheet(button_style)
            button.clicked.connect(command)
            action_layout.addWidget(button)
            print(f"添加按钮 {text}")

        main_layout.addWidget(action_frame)
        main_layout.setAlignment(action_frame, Qt.AlignHCenter)
        print("按钮区域创建完成")

    def fill_line_edits(self):
        print("填充 line_edits 数据")
        if not self.line_edits:
            print("line_edits 为空，跳过填充")
            return
        try:
            if self.line_edits[3].text():
                #毫米每秒转换成米每分钟
                value_mm_per_sec = float(self.line_edits[3].text())  # Value in mm/s
                value_m_per_min = value_mm_per_sec * 0.06  # Convert to m/min
                # value = float(self.line_edits[3].text())
                self.write_entries[0].setText(f"{value_m_per_min:.1f}")
            if self.line_edits[4].text():
                value = float(self.line_edits[4].text())
                self.write_entries[1].setText(f"{value:.1f}")
            if self.line_edits[5].text():
                value = float(self.line_edits[5].text())
                self.write_entries[12].setText(f"{value:.1f}")
            if self.line_edits[7].text():#摆幅
                value = float(str(float(self.line_edits[7].text())/2))
                self.write_entries[13].setText(f"{value:.1f}")
                value = float('-'+str(float(self.line_edits[7].text())/2))
                self.write_entries[14].setText(f"{value:.1f}")
            if self.line_edits[9].text():#横梁边部停留时间
                self.write_entries[15].setText(str(float(self.line_edits[9].text())*100))
                self.write_entries[16].setText(str(float(self.line_edits[9].text())*100))
            if self.line_edits[8].text():#延时时间
                value = str(float(self.line_edits[8].text())*100)
                self.write_entries[17].setText(str(value))
            scheme = self.line_edits[1].text()
            if scheme == "交叉摆":
                self.write_entries[3].setText("True")
            elif scheme == "顺序摆":
                self.write_entries[4].setText("True")
            elif scheme == "同步摆":
                self.write_entries[5].setText("True")
            print("已填充 line_edits 数据到写入值")
        except Exception as e:
            print(f"填充 line_edits 失败: {str(e)}")

    def set_cross_swing(self):
        if not self.plc or not self.plc.is_connected():
            QMessageBox.critical(self, "错误", "未连接到PLC")
            return
        try:
            self.plc.write_bool("界面模式1选择", True)
            QMessageBox.information(self, "成功", "已设置交叉摆（界面模式1选择 = True）")
            time.sleep(0.5)
            self.query_variables()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"设置交叉摆失败: {str(e)}")

    def set_sequence_swing(self):
        if not self.plc or not self.plc.is_connected():
            QMessageBox.critical(self, "错误", "未连接到PLC")
            return
        try:
            self.plc.write_bool("界面模式3选择", True)
            QMessageBox.information(self, "成功", "已设置顺序摆（界面模式3选择 = True）")
            time.sleep(0.5)
            self.query_variables()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"设置顺序摆失败: {str(e)}")

    def set_sync_swing(self):
        if not self.plc or not self.plc.is_connected():
            QMessageBox.critical(self, "错误", "未连接到PLC")
            return
        try:
            sync_variables = [
                "界面横梁同步确定按钮",
                "界面横梁1同步选择",
                "界面横梁2同步选择",
                "界面横梁3同步选择",
                "界面横梁4同步选择",
                "界面横梁5同步选择",
                "界面横梁6同步选择"
            ]
            for var_name in sync_variables:
                self.plc.write_bool(var_name, True)
            QMessageBox.information(self, "成功", "已设置同步摆（7 个同步变量 = True）")
            time.sleep(0.5)
            self.query_variables()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"设置同步摆失败: {str(e)}")

    def query_variables(self):
        if not self.plc or not self.plc.is_connected():
            QMessageBox.critical(self, "错误", "未连接到PLC")
            return
        try:
            for i, var in enumerate(self.VARIABLES):
                retries = 3  # Number of retry attempts
                while retries > 0:
                    var_name = var["name"]
                    var_type = var["type"]
                    try:
                        if var_type == "bool":
                            value = self.plc.read_bool(var_name)[0]
                        elif var_type == "float":
                            value = self.plc.read_float(var_name)[0]
                        else:  # int
                            value = self.plc.read_int(var_name)[0]
                        self.read_labels[i].setText(str(value))
                        break  # Exit retry loop on success
                    except Exception as e:
                        retries -= 1
                        if retries == 0:
                            self.read_labels[i].setText("读取失败")
                            print(f"读取 {var_name} 失败: {str(e)}")
                        else:
                            time.sleep(0.5)  # Wait before retrying
            print("查询变量完成")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"查询失败: {str(e)}")


    def write_variables(self):
        if not self.plc or not self.plc.is_connected():
            QMessageBox.critical(self, "错误", "未连接到PLC")
            return
        try:
            written_count = 0
            for i, var in enumerate(self.VARIABLES):
                var_name = var["name"]
                var_type = var["type"]
                write_value = self.write_entries[i].text().strip()
                if not write_value:
                    continue
                try:
                    if var_type == "bool":
                        if write_value.lower() in ["true", "1"]:
                            self.plc.write_bool(var_name, True)
                        elif write_value.lower() in ["false", "0"]:
                            self.plc.write_bool(var_name, False)
                        else:
                            QMessageBox.critical(self, "错误", f"{var_name} 的写入值必须为 True、False、1 或 0")
                            continue
                    elif var_type == "float":
                        try:
                            value = float(write_value)
                            self.plc.write_float(var_name, value)
                        except ValueError:
                            QMessageBox.critical(self, "错误", f"{var_name} 的写入值必须为数字")
                            continue
                    else:  # int
                        try:
                            value = int(write_value)
                            self.plc.write_int(var_name, value)
                        except ValueError:
                            QMessageBox.critical(self, "错误", f"{var_name} 的写入值必须为整数")
                            continue
                    written_count += 1
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"写入 {var_name} 失败: {str(e)}")
                    continue
            if written_count > 0:
                QMessageBox.information(self, "成功", f"已成功写入 {written_count} 个变量到PLC")
            else:
                QMessageBox.information(self, "提示", "没有有效的写入值，跳过写入操作")
            time.sleep(0.5)
            self.query_variables()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"写入失败: {str(e)}")

class TransferDataDialog(QDialog):
    VARIABLE_MAPPING = {
        "模式": "D100",
        "方案选择": {
            "交叉摆": "Mode1Select",
            "顺序摆": "Mode3Select",
            "同步摆": "BeamSyncConfirm"
        },
        "设备": "D102",
        "主皮带速度": "DriveSetSpeed",
        "横梁摆动速度": "SyncSetSpeed",
        "加速度大小": "Beam1Acceleration",
        "同粒度磨头数": "D106",
        "摆幅": {
            "同步操作面设定值": "D107",
            "同步非操作面设定值": "D108"
        },
        "延时时间": "D109",
        "横梁边部停留时间": {
            "横梁同步操作面停留时间": "D110",
            "横梁同步非操作面停留时间": "D111"
        }
    }

    def __init__(self, selected_data, parent=None):
        super().__init__(parent)
        print("初始化 TransferDataDialog")
        self.setWindowTitle(self.tr("数据传输"))
        self.setGeometry(450, 200, 600, 400)
        try:
            self.setStyleSheet("background-color: rgb(31, 55, 96); color: white;")
            print("设置 TransferDataDialog 样式成功")
        except Exception as e:
            print(f"设置 TransferDataDialog 样式失败: {str(e)}")
            raise

        main_layout = QVBoxLayout()
        self.create_parameter_area(main_layout, selected_data)
        self.create_device_connection_area(main_layout)
        self.create_send_button(main_layout)
        self.setLayout(main_layout)

        self.plc = PLCCommunicator()
        self.connected = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_connection_status)
        self.timer.start(1000)
        print("TransferDataDialog 初始化完成")

    def create_parameter_area(self, main_layout, selected_data):
        print("创建参数区域")
        parameter_frame = QFrame(self)
        if not parameter_frame:
            print("parameter_frame 创建失败")
            raise RuntimeError("无法创建 parameter_frame")
        parameter_frame.setStyleSheet("QFrame { border: 5px solid #1e5dab; border-radius: 15px; padding: 10px; }")
        parameter_layout = QGridLayout(parameter_frame)

        parameter_title = QLabel(self.tr("确认发送参数"), self)
        parameter_title.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        parameter_title.setAlignment(Qt.AlignCenter)
        parameter_title.setStyleSheet("QLabel { border: none; }")
        main_layout.addWidget(parameter_title)

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

        font = QFont("Microsoft YaHei", 12)

        for i, label_text in enumerate(labels):
            label = QLabel(label_text + ":", self)
            label.setFont(font)
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            label.setStyleSheet("QLabel { border: none; }")
            line_edit = QLineEdit(self)
            line_edit.setFont(font)
            line_edit.setReadOnly(True)
            line_edit.setStyleSheet("background-color: #444;color: white; border: 1px solid #666; border-radius: 3px; padding: 5px;")
            line_edit.setFixedWidth(100)
            self.line_edits.append(line_edit)

            row = i // 3
            col = i % 3
            parameter_layout.addWidget(label, row, col * 2)
            parameter_layout.addWidget(line_edit, row, col * 2 + 1)

        main_layout.addWidget(parameter_frame)
        print("参数区域创建完成")
        if selected_data:
            self.fill_data(selected_data)

    def create_device_connection_area(self, main_layout):
        print("创建设备连接区域")
        connection_frame = QFrame(self)
        if not connection_frame:
            print("connection_frame 创建失败")
            raise RuntimeError("无法创建 connection_frame")
        connection_frame.setStyleSheet("QFrame { border: 5px solid #1e5dab; border-radius: 15px; padding: 10px; }")
        connection_frame.setFixedSize(600, 150)
        connection_layout = QGridLayout(connection_frame)

        connection_title = QLabel(self.tr("设备连接配置"), self)
        connection_title.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        connection_title.setAlignment(Qt.AlignCenter)
        connection_title.setStyleSheet("QLabel { border: none; }")
        main_layout.addWidget(connection_title)

        font = QFont("Microsoft YaHei", 12)

        self.plc_ip_label = QLabel(self.tr("PLC IP:"), self)
        self.plc_ip_label.setFont(font)
        self.plc_ip_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.plc_ip_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.plc_ip_label.setStyleSheet("QLabel { border: none; }")

        self.plc_ip_edit = QLineEdit(self)
        self.plc_ip_edit.setFont(font)
        self.plc_ip_edit.setStyleSheet(
            "background-color: #444; border: 1px solid #666; border-radius: 3px; padding: 5px;")
        self.plc_ip_edit.setFixedWidth(150)

        self.port_label = QLabel(self.tr("端口号:"), self)
        self.port_label.setFont(font)
        self.port_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.port_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.plc_ip_label.setStyleSheet("QLabel { border: none; }")

        self.port_edit = QLineEdit(self)
        self.port_edit.setFont(font)
        self.port_edit.setStyleSheet(
            "background-color: #444; border: 1px solid #666; border-radius: 3px; padding: 5px;")
        self.port_edit.setFixedWidth(100)

        self.settings = QSettings("config.ini", QSettings.IniFormat)
        self.plc_ip_edit.setText(self.settings.value("PLCIP", "192.168.2.1"))
        self.port_edit.setText(self.settings.value("Port", "9600"))

        connection_layout.addWidget(self.plc_ip_label, 0, 0)
        connection_layout.addWidget(self.plc_ip_edit, 0, 1)
        connection_layout.addWidget(self.port_label, 0, 2)
        connection_layout.addWidget(self.port_edit, 0, 3)

        self.save_button = ImageChangeButton(self.tr("保存配置"), ":SmallFrame", ":SmallFrameClicked", 114, 37, True)
        self.save_button.clicked.connect(self.save_settings)

        self.connect_button = ImageChangeButton(self.tr("连接PLC"), ":SmallFrame", ":SmallFrameClicked", 114, 37, True)
        self.connect_button.clicked.connect(self.toggle_connection)

        connection_layout.addWidget(self.save_button, 0, 4)
        connection_layout.addWidget(self.connect_button, 1, 1)

        self.status_label = QLabel(self.tr("连接状态:"), self)
        self.status_label.setFont(font)
        self.status_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.status_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.status_label.setStyleSheet("QLabel { border: none; }")

        self.status_icon = QLabel(self)
        self.status_icon.setFixedSize(20, 20)
        self.status_icon.setStyleSheet("QLabel { border: none; }")
        self.update_status_icon(False)

        connection_layout.addWidget(self.status_label, 1, 2)
        connection_layout.addWidget(self.status_icon, 1, 3)

        main_layout.addWidget(connection_frame)
        main_layout.setAlignment(connection_frame, Qt.AlignHCenter)
        print("设备连接区域创建完成")

    def create_send_button(self, main_layout):
        print("创建发送按钮")
        self.send_button = ImageChangeButton(self.tr("发送参数"), ":SmallFrame", ":SmallFrameClicked", 114, 37, True)
        self.send_button.clicked.connect(self.send_data)
        main_layout.addWidget(self.send_button)
        main_layout.setAlignment(self.send_button, Qt.AlignHCenter)
        print("发送按钮创建完成")

    def fill_data(self, data):
        print("填充 selected_data")
        try:
            full_motion_param_dict = json.loads(data[8])
            self.line_edits[0].setText(data[0])
            self.line_edits[1].setText(data[1])
            self.line_edits[2].setText(data[7])
            self.line_edits[3].setText(data[2])
            self.line_edits[4].setText(data[4])
            self.line_edits[5].setText(str(full_motion_param_dict['lineEdit_accelerate']))
            self.line_edits[6].setText(str(full_motion_param_dict['lineEdit_num_output']))
            self.line_edits[7].setText(str(full_motion_param_dict['lineEdit_swing']))
            self.line_edits[8].setText(str(full_motion_param_dict['lineEdit_delay_time']))
            self.line_edits[9].setText(str(full_motion_param_dict['lineEdit_stay_time']))
            print("selected_data 填充完成")
        except Exception as e:
            print(f"填充 selected_data 失败: {str(e)}")

    def save_settings(self):
        print("保存配置")
        self.settings.setValue("PLCIP", self.plc_ip_edit.text())
        self.settings.setValue("Port", self.port_edit.text())
        QMessageBox.information(self, "保存成功", "配置已保存！")
        print("配置保存成功")

    def toggle_connection(self):
        print("切换 PLC 连接状态")
        if self.connect_button.text == "连接PLC":
            plc_ip = self.plc_ip_edit.text()
            if not plc_ip:
                QMessageBox.warning(self, "输入错误", "请输入PLC IP！")
                print("PLC IP 为空")
                return
            try:
                self.plc.connect(plc_ip)
                self.connect_button.text = "断开PLC"
                self.connected = True
                QMessageBox.information(self, "连接成功", "已成功连接到PLC！")
                print("PLC 连接成功")
            except Exception as e:
                self.connected = False
                QMessageBox.critical(self, "连接错误", str(e))
                print(f"PLC 连接失败: {str(e)}")
        else:
            try:
                self.plc.disconnect()
                self.connect_button.text = "连接PLC"
                self.connected = False
                QMessageBox.information(self, "断开成功", "已成功断开连接！")
                print("PLC 断开成功")
            except Exception as e:
                QMessageBox.critical(self, "断开错误", str(e))
                print(f"PLC 断开失败: {str(e)}")

    def update_connection_status(self):
        self.update_status_icon(self.plc.is_connected())

    def update_status_icon(self, connected):
        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"更新连接状态图标: {connected}，当前时间: {current_time}")
        if connected:
            self.status_icon.setStyleSheet("border: none; background-color: green; border-radius: 10px;")
        else:
            self.status_icon.setStyleSheet("border: none; background-color: red; border-radius: 10px;")

    def send_data(self):
        print("执行 send_data")
        if not self.plc.is_connected():
            QMessageBox.warning(self, "发送失败", "请先连接设备！")
            print("PLC 未连接，发送失败")
            return
        try:
            QApplication.processEvents()
            print("启动 PLCInterface 界面")
            dialog = PLCInterface(self.plc, self.line_edits, self)
            dialog.exec()
            print("PLCInterface 界面关闭")
        except Exception as e:
            print(f"PLCInterface 初始化失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"无法启动 PLC 通讯界面: {str(e)}")

    def closeEvent(self, event):
        print("关闭 TransferDataDialog")
        if self.plc.is_connected():
            try:
                self.plc.disconnect()
                print("PLC 断开连接")
            except:
                pass
        event.accept()