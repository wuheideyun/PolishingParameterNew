import json
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QFrame,
    QGridLayout, QMessageBox, QPushButton, QApplication
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QSettings, QTimer
from omron_plc_gui import PLCCommunicator
from ImageChangeButton import ImageChangeButton
from datetime import datetime, time


class PLCInterface(QDialog):
    VARIABLES = [
        {"name": "传动给定速度", "type": "float"},
        {"name": "同步给定速度", "type": "float"},
        {"name": "横梁当前运行状态", "type": "bool"},
        {"name": "界面模式1选择", "type": "bool"},
        {"name": "界面模式3选择", "type": "bool"},
        {"name": "界面横梁同步确定按钮", "type": "bool"},
        {"name": "界面横梁1同步选择", "type": "bool"},
        {"name": "界面横梁2同步选择", "type": "bool"},
        {"name": "界面横梁3同步选择", "type": "bool"},
        {"name": "界面横梁4同步选择", "type": "bool"},
        {"name": "界面横梁5同步选择", "type": "bool"},
        {"name": "界面横梁6同步选择", "type": "bool"},
        {"name": "横梁1加速度", "type": "float"},
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
        self.setWindowTitle("单机PLC参数读写")
        self.setGeometry(300, 100, 800, 600)  # 增加高度以容纳所有变量
        self.setStyleSheet("background-color: rgb(31, 55, 96); color: white;")

        self.plc = plc
        self.line_edits = line_edits

        main_layout = QVBoxLayout()
        self.create_table_area(main_layout)
        self.create_action_area(main_layout)
        self.setLayout(main_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.query_variables)
        self.timer.setSingleShot(True)
        if self.plc and self.plc.is_connected():
            self.timer.start(100)

    def create_table_area(self, main_layout):
        table_frame = QFrame(self)
        table_frame.setStyleSheet("QFrame { border: 5px solid #1e5dab; border-radius: 15px; padding: 10px; }")
        table_layout = QGridLayout(table_frame)
        table_layout.setVerticalSpacing(2)
        font_bold = QFont("Microsoft YaHei", 10, QFont.Bold)
        font_normal = QFont("Microsoft YaHei", 10)

        header_labels = ["参数", "PLC变量名", "读取值", "写入值"]
        for col, text in enumerate(header_labels):
            label = QLabel(text, self)
            label.setFont(font_bold)
            label.setStyleSheet("border: none; padding: 2px;")
            label.setMaximumHeight(20)
            table_layout.addWidget(label, 0, col, alignment=Qt.AlignCenter)

        self.read_labels = []
        self.write_entries = []

        for i, var in enumerate(self.VARIABLES, start=1):
            param_name = self.PARAMETER_MAPPING.get(var["name"], "-")
            param_label = QLabel(param_name, self)
            param_label.setFont(font_normal)
            param_label.setStyleSheet("border: none; padding: 2px;")
            param_label.setFixedWidth(150)
            param_label.setMaximumHeight(20)
            table_layout.addWidget(param_label, i, 0, alignment=Qt.AlignLeft)

            var_label = QLabel(var["name"], self)
            var_label.setFont(font_normal)
            var_label.setStyleSheet("border: none; padding: 2px;")
            var_label.setFixedWidth(200)  # 增加变量名列宽
            var_label.setMaximumHeight(20)
            table_layout.addWidget(var_label, i, 1, alignment=Qt.AlignLeft)

            read_label = QLabel("", self)
            read_label.setFont(font_normal)
            read_label.setStyleSheet(
                "background-color: #444; border: 1px solid #666; border-radius: 3px; padding: 2px;")
            read_label.setFixedWidth(100)
            read_label.setMaximumHeight(20)
            table_layout.addWidget(read_label, i, 2)
            self.read_labels.append(read_label)

            write_entry = QLineEdit(self)
            write_entry.setFont(font_normal)
            write_entry.setStyleSheet(
                "background-color: white; color: black; border: 1px solid #666; border-radius: 3px; padding: 2px;")
            write_entry.setFixedWidth(100)
            write_entry.setMaximumHeight(20)
            table_layout.addWidget(write_entry, i, 3)
            self.write_entries.append(write_entry)

        main_layout.addWidget(table_frame)
        self.fill_line_edits()

    def create_action_area(self, main_layout):
        action_frame = QFrame(self)
        action_frame.setStyleSheet("QFrame { border: 5px solid #1e5dab; border-radius: 15px; padding: 10px; }")
        action_layout = QHBoxLayout(action_frame)
        font = QFont("Microsoft YaHei", 12)
        button_style = """
            QPushButton { 
                background-color: #30438c; color: white; border: none; 
                padding: 5px; font-size: 14px; border-radius: 5px; min-width: 80px;
            }
            QPushButton:hover { background-color: #40539c; }
            QPushButton:pressed { background-color: #7986b5; }
        """
        buttons = [
            ("交叉摆", self.set_cross_swing), ("顺序摆", self.set_sequence_swing),
            ("同步摆", self.set_sync_swing), ("查询", self.query_variables), ("写入", self.write_variables)
        ]
        action_layout.addStretch()
        for text, command in buttons:
            button = QPushButton(text, self)
            button.setFont(font)
            button.setStyleSheet(button_style)
            button.clicked.connect(command)
            action_layout.addWidget(button)
        action_layout.addStretch()
        main_layout.addWidget(action_frame)

    def fill_line_edits(self):
        if not self.line_edits: return
        try:
            if self.line_edits[3]: self.write_entries[0].setText(f"{float(self.line_edits[3]) * 0.06:.1f}")
            if self.line_edits[4]: self.write_entries[1].setText(f"{float(self.line_edits[4]):.1f}")
            if self.line_edits[5]: self.write_entries[12].setText(f"{float(self.line_edits[5]):.1f}")
            if self.line_edits[7]:
                swing = float(self.line_edits[7])
                self.write_entries[13].setText(f"{swing / 2:.1f}")
                self.write_entries[14].setText(f"{-swing / 2:.1f}")
            if self.line_edits[9]:
                stay_time = float(self.line_edits[9]) * 100
                self.write_entries[15].setText(str(int(stay_time)))
                self.write_entries[16].setText(str(int(stay_time)))
            if self.line_edits[8]: self.write_entries[17].setText(str(int(float(self.line_edits[8]) * 100)))

            scheme = self.line_edits[1]
            if "交叉" in scheme:
                self.write_entries[3].setText("True")
            elif "顺序" in scheme:
                self.write_entries[4].setText("True")
            elif "同步" in scheme:
                self.write_entries[5].setText("True")
        except Exception as e:
            print(f"填充 line_edits 失败: {str(e)}")

    def set_cross_swing(self):
        if not self.plc or not self.plc.is_connected():
            QMessageBox.critical(self, "错误", "未连接到PLC");
            return
        try:
            self.plc.write_bool("界面模式1选择", True)
            QMessageBox.information(self, "成功", "已设置交叉摆")
            time.sleep(0.5);
            self.query_variables()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"设置交叉摆失败: {str(e)}")

    def set_sequence_swing(self):
        if not self.plc or not self.plc.is_connected():
            QMessageBox.critical(self, "错误", "未连接到PLC");
            return
        try:
            self.plc.write_bool("界面模式3选择", True)
            QMessageBox.information(self, "成功", "已设置顺序摆")
            time.sleep(0.5);
            self.query_variables()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"设置顺序摆失败: {str(e)}")

    def set_sync_swing(self):
        if not self.plc or not self.plc.is_connected():
            QMessageBox.critical(self, "错误", "未连接到PLC");
            return
        try:
            for var_name in [f"界面横梁{i}同步选择" for i in range(1, 7)] + ["界面横梁同步确定按钮"]:
                self.plc.write_bool(var_name, True)
            QMessageBox.information(self, "成功", "已设置同步摆")
            time.sleep(0.5);
            self.query_variables()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"设置同步摆失败: {str(e)}")

    def query_variables(self):
        if not self.plc or not self.plc.is_connected():
            QMessageBox.critical(self, "错误", "未连接到PLC");
            return
        try:
            for i, var in enumerate(self.VARIABLES):
                var_name, var_type = var["name"], var["type"]
                try:
                    if var_type == "bool":
                        value = self.plc.read_bool(var_name)[0]
                    elif var_type == "float":
                        value = self.plc.read_float(var_name)[0]
                    else:
                        value = self.plc.read_int(var_name)[0]
                    self.read_labels[i].setText(str(value))
                except Exception:
                    self.read_labels[i].setText("读取失败")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"查询失败: {str(e)}")

    def write_variables(self):
        if not self.plc or not self.plc.is_connected():
            QMessageBox.critical(self, "错误", "未连接到PLC");
            return
        try:
            written_count = 0
            for i, var in enumerate(self.VARIABLES):
                var_name, var_type = var["name"], var["type"]
                write_value = self.write_entries[i].text().strip()
                if not write_value: continue
                try:
                    if var_type == "bool":
                        value = write_value.lower() in ["true", "1"]
                        self.plc.write_bool(var_name, value)
                    elif var_type == "float":
                        self.plc.write_float(var_name, float(write_value))
                    else:
                        self.plc.write_int(var_name, int(write_value))
                    written_count += 1
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"写入 {var_name} 失败: {str(e)}")
            if written_count > 0:
                QMessageBox.information(self, "成功", f"已成功写入 {written_count} 个变量")
            else:
                QMessageBox.information(self, "提示", "没有有效的写入值")
            time.sleep(0.5);
            self.query_variables()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"写入失败: {str(e)}")


class TransferDataDialog(QDialog):
    def __init__(self, selected_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("数据传输")
        self.setGeometry(450, 200, 800, 500)
        self.setStyleSheet("background-color: rgb(31, 55, 96); color: white;")
        self.setModal(True)

        main_layout = QVBoxLayout(self)
        self.create_parameter_area(main_layout, selected_data)
        self.create_device_connection_area(main_layout)
        self.create_send_button(main_layout)
        self.setLayout(main_layout)

        self.plc = PLCCommunicator()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_connection_status)
        self.timer.start(1000)

    def create_parameter_area(self, main_layout, selected_data):
        parameter_frame = QFrame(self)
        parameter_frame.setStyleSheet("QFrame { border: 5px solid #1e5dab; border-radius: 15px; padding: 10px; }")
        parameter_layout = QGridLayout(parameter_frame)
        parameter_title = QLabel("确认发送参数", self)
        parameter_title.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        parameter_title.setAlignment(Qt.AlignCenter)
        parameter_title.setStyleSheet("QLabel { border: none; }")
        main_layout.addWidget(parameter_title)

        labels = ["模式:", "方案选择:", "设备:", "主皮带速度(mm/s):", "横梁摆动速度(mm/s):",
                  "加速度大小(mm/s²):", "同粒度磨头数(个):", "摆幅(mm):", "延时时间(s):",
                  "横梁边部停留时间(s):"]
        self.line_edits = []
        font = QFont("Microsoft YaHei", 12)

        for i, label_text in enumerate(labels):
            label = QLabel(label_text, self)
            label.setFont(font)
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            line_edit = QLineEdit(self)
            line_edit.setFont(font)
            line_edit.setReadOnly(True)
            line_edit.setStyleSheet(
                "background-color: #444;color: white; border: 1px solid #666; border-radius: 3px; padding: 5px;")
            self.line_edits.append(line_edit)
            row, col = i // 3, (i % 3) * 2
            parameter_layout.addWidget(label, row, col)
            parameter_layout.addWidget(line_edit, row, col + 1)

        main_layout.addWidget(parameter_frame)
        if selected_data: self.fill_data(selected_data)

    def create_device_connection_area(self, main_layout):
        connection_frame = QFrame(self)
        connection_frame.setStyleSheet("QFrame { border: 5px solid #1e5dab; border-radius: 15px; padding: 10px; }")
        connection_layout = QGridLayout(connection_frame)
        connection_title = QLabel("设备连接配置", self)
        connection_title.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        connection_title.setAlignment(Qt.AlignCenter)
        connection_title.setStyleSheet("QLabel { border: none; }")
        main_layout.addWidget(connection_title)

        font = QFont("Microsoft YaHei", 12)
        self.plc_ip_label = QLabel("PLC IP:", self);
        self.plc_ip_label.setFont(font)
        self.plc_ip_edit = QLineEdit(self);
        self.plc_ip_edit.setFont(font)
        self.plc_ip_edit.setStyleSheet(
            "background-color: #444; border: 1px solid #666; border-radius: 3px; padding: 5px;")
        self.port_label = QLabel("端口号:", self);
        self.port_label.setFont(font)
        self.port_edit = QLineEdit(self);
        self.port_edit.setFont(font)
        self.port_edit.setStyleSheet(
            "background-color: #444; border: 1px solid #666; border-radius: 3px; padding: 5px;")

        self.settings = QSettings("config.ini", QSettings.IniFormat)
        self.plc_ip_edit.setText(self.settings.value("PLCIP", "192.168.2.10"))
        self.port_edit.setText(self.settings.value("Port", "9600"))

        self.save_button = ImageChangeButton("保存配置", ":SmallFrame", ":SmallFrameClicked", 114, 37, True)
        self.save_button.clicked.connect(self.save_settings)
        self.connect_button = ImageChangeButton("连接PLC", ":SmallFrame", ":SmallFrameClicked", 114, 37, True)
        self.connect_button.clicked.connect(self.toggle_connection)

        self.status_label = QLabel("连接状态:", self);
        self.status_label.setFont(font)
        self.status_icon = QLabel(self)
        self.status_icon.setFixedSize(20, 20)
        self.update_status_icon(False)

        connection_layout.addWidget(self.plc_ip_label, 0, 0)
        connection_layout.addWidget(self.plc_ip_edit, 0, 1)
        connection_layout.addWidget(self.port_label, 0, 2)
        connection_layout.addWidget(self.port_edit, 0, 3)
        connection_layout.addWidget(self.save_button, 1, 0)
        connection_layout.addWidget(self.connect_button, 1, 1)
        connection_layout.addWidget(self.status_label, 1, 2)
        connection_layout.addWidget(self.status_icon, 1, 3)
        main_layout.addWidget(connection_frame, alignment=Qt.AlignHCenter)

    def create_send_button(self, main_layout):
        self.send_button = ImageChangeButton("发送参数", ":SmallFrame", ":SmallFrameClicked", 114, 37, True)
        self.send_button.clicked.connect(self.send_data)
        main_layout.addWidget(self.send_button, alignment=Qt.AlignHCenter)

    def fill_data(self, data):
        try:
            if len(data) >= 10:
                for i in range(10):
                    self.line_edits[i].setText(str(data[i]))
        except Exception as e:
            print(f"填充数据失败: {e}")

    def save_settings(self):
        self.settings.setValue("PLCIP", self.plc_ip_edit.text())
        self.settings.setValue("Port", self.port_edit.text())
        QMessageBox.information(self, "保存成功", "配置已保存！")

    def toggle_connection(self):
        btn_text = self.connect_button.text
        if btn_text == "连接PLC" or not hasattr(self.connect_button, 'text_label'):
            try:
                self.plc.connect(self.plc_ip_edit.text())
                self.connect_button.set_name("断开PLC")
                QMessageBox.information(self, "连接成功", "已成功连接到PLC！")
            except Exception as e:
                QMessageBox.critical(self, "连接错误", str(e))
        else:
            try:
                self.plc.disconnect()
                self.connect_button.set_name("连接PLC")
                QMessageBox.information(self, "断开成功", "已成功断开连接！")
            except Exception as e:
                QMessageBox.critical(self, "断开错误", str(e))

    def update_connection_status(self):
        self.update_status_icon(self.plc.is_connected())

    def update_status_icon(self, connected):
        color = "green" if connected else "red"
        self.status_icon.setStyleSheet(f"border: none; background-color: {color}; border-radius: 10px;")

    def send_data(self):
        # if not self.plc.is_connected():
        #     QMessageBox.warning(self, "发送失败", "请先连接设备！")
        #     return
        try:
            line_edits_text = [le.text() for le in self.line_edits]
            dialog = PLCInterface(self.plc, line_edits_text, self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法启动 PLC 通讯界面: {str(e)}")

    def closeEvent(self, event):
        if self.plc.is_connected():
            try:
                self.plc.disconnect()
            except:
                pass
        event.accept()