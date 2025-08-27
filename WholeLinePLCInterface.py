import sys
import re
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QMessageBox, QWidget
)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt, QThread, Signal

# 确保这些文件在您的项目中存在
from omron_plc_gui import PLCCommunicator


class PLCReadWriteWorker(QThread):
    # 信号: (行号, 列号, 文本, 是否成功)
    task_finished = Signal(int, int, str, bool)

    def __init__(self, row, col, plc_instance, variable, action='query', write_value=None, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.plc_instance = plc_instance
        self.variable = variable
        self.action = action
        self.write_value = write_value

    def run(self):
        try:
            var_name, var_type = self.variable["name"], self.variable["type"]
            if self.action == 'query':
                if var_type == "bool":
                    value = self.plc_instance.read_bool(var_name)[0]
                elif var_type == "float":
                    value = self.plc_instance.read_float(var_name)[0]
                else:
                    value = self.plc_instance.read_int(var_name)[0]
                self.task_finished.emit(self.row, self.col, str(value), True)

            elif self.action == 'write':
                if not self.write_value:
                    if var_type == "bool":
                        value = self.plc_instance.read_bool(var_name)[0]
                    elif var_type == "float":
                        value = self.plc_instance.read_float(var_name)[0]
                    else:
                        value = self.plc_instance.read_int(var_name)[0]
                    self.task_finished.emit(self.row, self.col, str(value), True)
                    return

                if var_type == "bool":
                    self.plc_instance.write_bool(var_name, [self.write_value.lower() in ["true", "1"]])
                elif var_type == "float":
                    self.plc_instance.write_float(var_name, float(self.write_value))
                else:
                    self.plc_instance.write_int(var_name, int(self.write_value))

                if var_type == "bool":
                    value = self.plc_instance.read_bool(var_name)[0]
                elif var_type == "float":
                    value = self.plc_instance.read_float(var_name)[0]
                else:
                    value = self.plc_instance.read_int(var_name)[0]
                self.task_finished.emit(self.row, self.col, str(value), True)
        except Exception as e:
            self.task_finished.emit(self.row, self.col, "操作失败", False)


class WholeLinePLCInterface(QDialog):
    VARIABLES = [
        {"name": "传动给定速度", "type": "float"}, {"name": "同步给定速度", "type": "float"},
        {"name": "横梁当前运行状态", "type": "bool"}, {"name": "界面模式1选择", "type": "bool"},
        {"name": "界面模式3选择", "type": "bool"}, {"name": "界面横梁同步确定按钮", "type": "bool"},
        {"name": "界面横梁1同步选择", "type": "bool"}, {"name": "界面横梁2同步选择", "type": "bool"},
        {"name": "界面横梁3同步选择", "type": "bool"}, {"name": "界面横梁4同步选择", "type": "bool"},
        {"name": "界面横梁5同步选择", "type": "bool"}, {"name": "界面横梁6同步选择", "type": "bool"},
        {"name": "横梁1加速度", "type": "float"}, {"name": "同步操作面设定值", "type": "float"},
        {"name": "同步非操作面设定值", "type": "float"}, {"name": "横梁同步操作面停留时间", "type": "int"},
        {"name": "横梁同步非操作面停留时间", "type": "int"}, {"name": "延时时间", "type": "int"}
    ]
    PARAMETER_MAPPING = {
        "传动给定速度": "主皮带速度",
        "同步给定速度": "摆动速度",
        "横梁1加速度": "加速度",
        "同步操作面设定值": "摆幅(+)",
        "同步非操作面设定值": "摆幅(-)",
        "横梁同步操作面停留时间": "边部停留时间(+)",
        "横梁同步非操作面停留时间": "边部停留时间(-)",
        "延时时间": "延时时间",
        # 以下为布尔值，没有直接的参数名映射，显示 "-"
        "横梁当前运行状态": "-", "界面模式1选择": "-", "界面模式3选择": "-",
        "界面横梁同步确定按钮": "-", "界面横梁1同步选择": "-", "界面横梁2同步选择": "-",
        "界面横梁3同步选择": "-", "界面横梁4同步选择": "-", "界面横梁5同步选择": "-",
        "界面横梁6同步选择": "-"
    }

    def __init__(self, plc_instances: dict, solution_params: dict, parent=None):
        super().__init__(parent)
        self.plc_instances = plc_instances
        self.solution_params = solution_params

        self.setWindowTitle("整线PLC参数批量读写")
        self.setFixedSize(1400, 800)
        self.setStyleSheet("background-color: rgb(31, 55, 96); color: white;")

        main_layout = QVBoxLayout(self)
        title = QLabel("整线PLC参数批量读写", self)
        title.setFont(QFont("Microsoft YaHei", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        self.param_table = QTableWidget()
        self.param_table.setStyleSheet("""
            QTableWidget { gridline-color: #555; background-color: rgb(31, 55, 96); }
            QHeaderView::section { background-color: #2c3e50; padding: 5px; }
            QTableWidgetItem { color: white; }
            QLineEdit { background-color: white; color: black; }
        """)
        main_layout.addWidget(self.param_table)

        button_layout = QHBoxLayout()
        self.query_all_button = QPushButton("全部查询")
        self.write_all_button = QPushButton("全部写入")
        self.close_button = QPushButton("关闭")
        button_layout.addStretch()
        button_layout.addWidget(self.query_all_button)
        button_layout.addWidget(self.write_all_button)
        button_layout.addWidget(self.close_button)
        main_layout.addLayout(button_layout)

        self.close_button.clicked.connect(self.accept)
        self.query_all_button.clicked.connect(self.query_all)
        self.write_all_button.clicked.connect(self.write_all)

        self.setup_table()
        # self.populate_write_values() # 暂时留空
        self.query_all()

    def setup_table(self):
        print("[DEBUG] 开始构建界面布局...")
        num_devices = len(self.plc_instances)

        self.param_table.setRowCount(len(self.VARIABLES))
        self.param_table.setColumnCount(3 + num_devices)  # 固定的3列 + 动态的设备列

        # 设置水平表头
        headers = ["参数名", "PLC变量名", "待写入值"]
        self.connected_plc_indices = sorted(self.plc_instances.keys())
        for idx in self.connected_plc_indices:
            headers.append(f"{idx + 1} 号机读取值")
        self.param_table.setHorizontalHeaderLabels(headers)
        self.param_table.verticalHeader().setVisible(True)  # 显示行号

        # 设置列宽
        self.param_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.param_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.param_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        # 填充固定的前两列
        for row, var in enumerate(self.VARIABLES):
            param_name = self.PARAMETER_MAPPING.get(var["name"], "-")

            param_name_item = QTableWidgetItem(param_name)
            param_name_item.setFlags(Qt.ItemIsEnabled)
            self.param_table.setItem(row, 0, param_name_item)

            var_name_item = QTableWidgetItem(var["name"])
            var_name_item.setFlags(Qt.ItemIsEnabled)
            self.param_table.setItem(row, 1, var_name_item)

            # 为“待写入值”和“读取值”创建空的、可编辑的单元格
            write_item = QTableWidgetItem("")
            self.param_table.setItem(row, 2, write_item)

            for col_offset in range(num_devices):
                read_col = 3 + col_offset
                read_item = QTableWidgetItem("---")
                read_item.setFlags(Qt.ItemIsEnabled)
                read_item.setTextAlignment(Qt.AlignCenter)
                self.param_table.setItem(row, read_col, read_item)

        print("[DEBUG] 界面布局构建完成。")

    def populate_write_values(self):
        pass  # 暂时留空

    def query_all(self):
        print("[DEBUG] 开始全部查询...")
        for col_offset, device_idx in enumerate(self.connected_plc_indices):
            plc = self.plc_instances[device_idx]
            read_col = 3 + col_offset
            for row_idx, var in enumerate(self.VARIABLES):
                worker = PLCReadWriteWorker(row_idx, read_col, plc, var, action='query')
                worker.task_finished.connect(self.update_cell)
                worker.start()

    def write_all(self):
        print("[DEBUG] 开始全部写入...")
        for col_offset, device_idx in enumerate(self.connected_plc_indices):
            plc = self.plc_instances[device_idx]
            read_col = 3 + col_offset
            for row_idx, var in enumerate(self.VARIABLES):
                write_item = self.param_table.item(row_idx, 2)
                if write_item:
                    write_value = write_item.text()
                    worker = PLCReadWriteWorker(row_idx, read_col, plc, var, action='write', write_value=write_value)
                    worker.task_finished.connect(self.update_cell)
                    worker.start()

    def update_cell(self, row, col, text, success):
        item = self.param_table.item(row, col)
        if item:
            item.setText(text)
            item.setBackground(QColor("lightgreen") if success else QColor("red"))