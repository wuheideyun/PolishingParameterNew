import sys
import re
import json
import ast
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QMessageBox, QWidget
)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt, QThread, Signal, QTimer

# 确保这些文件在您的项目中存在
from omron_plc_gui import PLCCommunicator


class PLCReadWriteWorker(QThread):
    task_finished = Signal(int, int, str, bool)

    def __init__(self, row, col, plc_instance, variable, action='query', write_value=None, parent=None):
        super().__init__(parent)
        self.row, self.col, self.plc_instance, self.variable, self.action, self.write_value = \
            row, col, plc_instance, variable, action, write_value

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
    def __init__(self, plc_instances: dict, solution_params: dict, parent=None):
        super().__init__(parent)
        self.plc_instances = plc_instances
        self.whole_line_param_json = solution_params
        self.solution_params = solution_params
        self.static_variables = []
        self.dynamic_templates = []
        self.query_task_queue = []
        self.query_workers = []
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
            QPushButton { color: black; }
        """)
        main_layout.addWidget(self.param_table)
        button_layout = QHBoxLayout()
        self.load_temp_button = QPushButton("加载临时数据")
        self.query_all_button = QPushButton("全部查询")
        self.write_all_button = QPushButton("全部写入")
        self.close_button = QPushButton("关闭")
        button_style = """
            QPushButton { 
                background-color: #30438c; color: white; border: none; 
                padding: 10px; font-size: 16px; border-radius: 5px; min-width: 120px;
            }
            QPushButton:hover { background-color: #40539c; }
            QPushButton:pressed { background-color: #7986b5; }
        """
        for btn in [self.load_temp_button, self.query_all_button, self.write_all_button, self.close_button]:
            btn.setStyleSheet(button_style)
        button_layout.addStretch()
        button_layout.addWidget(self.load_temp_button)
        button_layout.addWidget(self.query_all_button)
        button_layout.addWidget(self.write_all_button)
        button_layout.addWidget(self.close_button)
        main_layout.addLayout(button_layout)

        self.close_button.clicked.connect(self.accept)
        self.query_all_button.clicked.connect(self.query_all)
        self.write_all_button.clicked.connect(self.write_all)
        self.load_temp_button.clicked.connect(self.load_from_temp_file)

        self.load_vars_from_excel_and_setup_table()
        self.auto_load_from_database()

    def load_vars_from_excel_and_setup_table(self):
        print("[DEBUG] 开始从Excel加载变量定义...")
        try:
            df = pd.read_excel("whole_line_param_batch.xls", header=0)
            self.static_variables = []
            self.dynamic_templates = []
            group_map = {}
            # 假设“类型”是第5列 (索引为4)
            col_plc, col_ui, col_key, col_repeat, col_type = (
                df.columns[0], df.columns[1], df.columns[2], df.columns[3], df.columns[4]
            )
            for index, row in df.iterrows():
                plc_name = str(row[col_plc]) if pd.notna(row[col_plc]) else ""
                repeat_flag = str(row[col_repeat]).upper()

                # 读取类型并转换为小写，例如 "FLOAT" -> "float"
                var_type = str(row[col_type]).lower().strip()

                param_info = {
                    "plc_name": plc_name,
                    "ui_name": str(row[col_ui]),
                    "param_key": str(row[col_key]),
                    "repeat_flag": repeat_flag,
                    "type": var_type
                }

                if repeat_flag == 'FALSE':
                    self.static_variables.append(param_info)
                else:
                    # 智能创建模板：根据原始名称是否带括号来决定模板格式
                    if '[' in plc_name and ']' in plc_name:
                        # 原始名称带括号，例如 "横梁启动顺序时间设定[1]"
                        # 模板也带括号 -> "横梁启动顺序时间设定[{}]"
                        template_name = re.sub(r'\[\d+\]', '[{}]', plc_name)
                    else:
                        # 原始名称不带括号，例如 "横梁1给定速度"
                        # 模板也不带括号 -> "横梁{}给定速度"
                        template_name = re.sub(r'\d+', '{}', plc_name)

                    param_info["plc_name_template"] = template_name
                    if repeat_flag == 'TRUE':
                        self.dynamic_templates.append([param_info])
                    else:
                        if repeat_flag in group_map:
                            group_map[repeat_flag].append(param_info)
                        else:
                            new_group = [param_info];
                            group_map[repeat_flag] = new_group;
                            self.dynamic_templates.append(new_group)
            print(
                f"[DEBUG] 成功加载 {len(self.static_variables)} 个静态变量和 {len(self.dynamic_templates)} 个动态模板组。")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"读取Excel文件时出错: {e}")
            self.static_variables, self.dynamic_templates = [], []
        self.setup_table()

    def setup_table(self):
        print("[DEBUG] setup_table: 开始构建基础表格...")
        line_config = self.parent().config_manager.load_config()
        num_devices = line_config.get('global',{}).get('machine_count',1)
        # num_devices = len(self.plc_instances)
        if num_devices == 0: num_devices = 1

        self.param_table.clear()
        self.param_table.setRowCount(len(self.static_variables))
        self.param_table.setColumnCount(2 + num_devices * 2)

        headers = ["PLC变量名", "软件参数"]
        for i in range(num_devices):
            headers.append(f"({i + 1}号抛光机)当前值")
            headers.append(f"({i + 1}号抛光机)待写入值")
        self.param_table.setHorizontalHeaderLabels(headers)
        self.param_table.verticalHeader().setVisible(True)

        self.param_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.param_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.param_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        for row, var_info in enumerate(self.static_variables):
            # 创建第一列的 item
            item = QTableWidgetItem(var_info["plc_name"])
            # 将类型信息存储在 item 的 UserRole 中
            item.setData(Qt.UserRole, var_info.get("type", "float"))
            self.param_table.setItem(row, 0, item)

            self.param_table.setItem(row, 1, QTableWidgetItem(var_info["ui_name"]))
            for i in range(num_devices):
                read_col = 2 + i * 2
                write_col = 3 + i * 2
                self.param_table.setItem(row, read_col, QTableWidgetItem("---"))
                self.param_table.setItem(row, write_col, QTableWidgetItem(""))

        print("[DEBUG] 基础表格构建完成。")

    def load_from_temp_file(self):
        try:
            with open("temp.txt", "r", encoding="utf-8") as f:
                content = f.read()
            params_data = ast.literal_eval(content)
            if isinstance(params_data, list):
                self.populate_all_devices_write_values(params_data);
                QMessageBox.information(self, "成功","所有设备的临时数据已成功加载。")
            else:
                raise ValueError("temp.txt 数据结构不符合预期的列表结构！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载临时文件时出错: {e}")

    def auto_load_from_database(self):
        print("[DEBUG] 尝试从数据库数据自动加载...")
        if not self.whole_line_param_json:
            print("[DEBUG] 没有从数据库传递参数，跳过自动加载。")
            return
        try:
            # 这里使用 json.loads()，因为数据库存的是标准JSON字符串
            params_data = json.loads(self.whole_line_param_json)

            if isinstance(params_data, list):
                self.populate_all_devices_write_values(params_data)
                print("[DEBUG] 从数据库传递的参数已自动加载。")
            else:
                raise ValueError("数据库中的整线参数不是列表结构！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"自动加载数据库参数时出错: {e}")

    def populate_all_devices_write_values(self, all_devices_params: list):
        print(f"[DEBUG] 开始为所有设备填充数据: {all_devices_params}")

        # 1. 确定动态迭代的总次数
        num_dynamic_iterations = 0
        if all_devices_params:
            max_iterations = 0
            for device_param_groups in all_devices_params:
                current_device_iterations = 0
                if isinstance(device_param_groups, list):
                    for group in device_param_groups:
                        if 'lineEdit_delay_time_list' in group and isinstance(group['lineEdit_delay_time_list'], list):
                            current_device_iterations += len(group['lineEdit_delay_time_list'])
                max_iterations = max(max_iterations, current_device_iterations)
            num_dynamic_iterations = max_iterations

        # 2. 计算并设置总行数
        total_dynamic_rows = sum(len(group) * num_dynamic_iterations for group in self.dynamic_templates)
        total_rows = len(self.static_variables) + total_dynamic_rows
        self.param_table.setRowCount(total_rows)

        # 3. 填充静态行
        for row, var_info in enumerate(self.static_variables):
            self.param_table.setItem(row, 0, QTableWidgetItem(var_info["plc_name"]))
            self.param_table.setItem(row, 1, QTableWidgetItem(var_info["ui_name"]))

        # 4. 智能混合排序逻辑
        self.dynamic_row_map = {}
        current_row_offset = 0
        for template_group in self.dynamic_templates:
            flag = template_group[0]["repeat_flag"]
            if flag == 'TRUE':
                for template in template_group:
                    for i in range(num_dynamic_iterations):
                        current_row = len(self.static_variables) + current_row_offset
                        plc_name = template["plc_name_template"].format(i + 1)
                        item = QTableWidgetItem(plc_name)
                        item.setData(Qt.UserRole, template.get("type", "float"))
                        self.param_table.setItem(current_row, 0, item)
                        self.param_table.setItem(current_row, 1, QTableWidgetItem(template["ui_name"]))
                        self.dynamic_row_map[plc_name] = current_row
                        current_row_offset += 1
            else:
                for i in range(num_dynamic_iterations):
                    for template in template_group:
                        current_row = len(self.static_variables) + current_row_offset
                        plc_name = template["plc_name_template"].format(i + 1)
                        item = QTableWidgetItem(plc_name)
                        item.setData(Qt.UserRole, template.get("type", "float"))
                        self.param_table.setItem(current_row, 0, item)
                        self.param_table.setItem(current_row, 1, QTableWidgetItem(template["ui_name"]))
                        self.dynamic_row_map[plc_name] = current_row
                        current_row_offset += 1

        # 5. 填充数据的逻辑
        for device_idx, param_groups in enumerate(all_devices_params):
            if not isinstance(param_groups, list) or not param_groups: continue
            write_col = 3 + device_idx * 2
            if write_col >= self.param_table.columnCount(): continue

            # 5.1 填充静态行的值
            base_params = param_groups[0]
            for row, var_info in enumerate(self.static_variables):
                param_key = var_info["param_key"]
                if not param_key: continue
                value_to_write = str(base_params.get(param_key, ""))
                self.param_table.setItem(row, write_col, QTableWidgetItem(value_to_write))

            # 5.2 填充动态行的值
            total_iterations_for_this_device = 0
            if isinstance(param_groups, list):
                for pg in param_groups:
                    total_iterations_for_this_device += len(pg.get('lineEdit_delay_time_list', []))

            for i in range(num_dynamic_iterations):
                if i < total_iterations_for_this_device:
                    source_group_index = 0;
                    temp_count = 0
                    for group_idx, pg in enumerate(param_groups):
                        delay_list = pg.get('lineEdit_delay_time_list', [])
                        if i < temp_count + len(delay_list): source_group_index = group_idx; break
                        temp_count += len(delay_list)
                    source_params = param_groups[source_group_index]

                    for template_group in self.dynamic_templates:
                        for template in template_group:
                            plc_name_to_find = template["plc_name_template"].format(i + 1)
                            if plc_name_to_find in self.dynamic_row_map:
                                target_row = self.dynamic_row_map[plc_name_to_find]
                                param_key = template["param_key"]
                                ui_name = template["ui_name"]
                                value_to_write = ""
                                # 1. 特殊结构处理 (摆幅)
                                if param_key == 'lineEdit_swing':
                                    swing = float(source_params.get(param_key, 0.0))
                                    if "操作面" in template["plc_name_template"] and "非" not in template[
                                        "plc_name_template"]:
                                        value_to_write = str(swing / 2)
                                    elif "非操作面" in template["plc_name_template"]:
                                        value_to_write = str(-swing / 2)
                                else:
                                    # 2. 通用值获取
                                    original_value = None
                                    if param_key == 'lineEdit_delay_time_list':
                                        original_value = source_params.get(param_key, [])[i - temp_count]
                                    else:
                                        original_value = source_params.get(param_key, "")

                                    # 3. 特殊值处理 (乘以100)
                                    if "延时启动时间" in ui_name or "边部停留时间" in ui_name:
                                        try:
                                            processed_value = int(float(original_value) * 100)
                                            value_to_write = str(processed_value)
                                        except (ValueError, TypeError):
                                            value_to_write = str(original_value)
                                    else:
                                        # 4. 默认处理
                                        value_to_write = str(original_value)

                                self.param_table.setItem(target_row, write_col, QTableWidgetItem(value_to_write))

        # 6. 为所有单元格设置对齐等属性
        for r in range(self.param_table.rowCount()):
            for c in range(2, self.param_table.columnCount()):
                item = self.param_table.item(r, c)
                if not item:
                    item = QTableWidgetItem("---")
                    self.param_table.setItem(r, c, item)
                item.setTextAlignment(Qt.AlignCenter)
                if c % 2 == 0:
                    item.setFlags(Qt.ItemIsEnabled)
        print("[DEBUG] 所有设备数据填充完成。")

    def query_all(self):
        """
        修改后的方法：在构建查询队列时，增加一个判断。
        仅当一个设备的“待写入值”不为“---”时，才为该设备添加该参数的查询任务。
        """
        if not self.plc_instances:
            QMessageBox.warning(self, "提示", "没有已连接的PLC设备，无法查询！")
            return

        self.query_task_queue.clear()
        self.query_workers.clear()

        # 步骤 1: 构建所有查询任务的队列
        for device_idx, plc_instance in self.plc_instances.items():
            # 计算此设备对应的“待写入值”列的索引
            # 这个列的内容决定了该参数是否适用于此设备
            write_col = 3 + device_idx * 2
            if write_col >= self.param_table.columnCount():
                continue

            for row in range(self.param_table.rowCount()):
                # 获取“待写入值”单元格的项
                write_item = self.param_table.item(row, write_col)

                # 如果待写入值的单元格为空，或者其内容为"---"，则跳过此查询
                if not write_item or write_item.text().strip() == "---":
                    continue

                # 只有在检查通过后，才继续获取变量信息并创建任务
                item = self.param_table.item(row, 0)
                if not item:
                    continue

                var_name = item.text()
                var_type = item.data(Qt.UserRole)
                if not var_type:
                    var_type = "float"

                # 将任务信息打包成字典，添加到队列中
                task = {
                    "device_idx": device_idx,
                    "plc_instance": plc_instance,
                    "row": row,
                    "var_name": var_name,
                    "var_type": var_type,
                }
                self.query_task_queue.append(task)

        # 步骤 2: 启动队列处理
        if self.query_task_queue:
            self.process_next_query()
        else:
            QMessageBox.information(self, "提示", "没有需要查询的变量。")

    def process_next_query(self):
        """
        新增方法：处理队列中的下一个查询任务，并设置定时器以在200ms后调用自身。
        """
        # 如果队列为空，则所有任务已派发完毕
        if not self.query_task_queue:
            return

        # 从队列头部取出一个任务
        task = self.query_task_queue.pop(0)

        device_idx = task["device_idx"]
        plc_instance = task["plc_instance"]
        row = task["row"]
        var_name = task["var_name"]
        var_type = task["var_type"]
        read_col = 2 + device_idx * 2

        variable_info = {"name": var_name, "type": var_type}

        # 为这个任务创建并启动工作线程
        worker = PLCReadWriteWorker(
            row=row,
            col=read_col,
            plc_instance=plc_instance,
            variable=variable_info,
            action='query'
        )
        worker.task_finished.connect(self.update_cell_value)
        worker.start()
        self.query_workers.append(worker)

        # 启动一个200毫秒的一次性定时器，到期后再次调用本方法
        QTimer.singleShot(20, self.process_next_query)

    def update_cell_value(self, row, col, value, success):
        """
        修改后的槽函数：增加了对浮点数查询结果的格式化处理。
        """
        item = self.param_table.item(row, col)
        if not item:
            item = QTableWidgetItem()
            self.param_table.setItem(row, col, item)

        if success:
            try:
                # 尝试将值转为浮点数并格式化为两位小数
                formatted_value = f"{float(value):.2f}"
                item.setText(formatted_value)
            except (ValueError, TypeError):
                # 如果转换失败 (例如，值是 "True", "False")，则直接显示原始值
                item.setText(str(value))
            item.setBackground(QColor("transparent"))
        else:
            item.setText("读取失败")
            item.setBackground(QColor("red"))

        item.setTextAlignment(Qt.AlignCenter)

    def write_all(self):
        pass