import sys
import sqlite3
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QHBoxLayout,
    QCheckBox, QLabel, QMessageBox, QSizePolicy
)
from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtCore import Qt, QTimer
from matplotlib import pyplot as plt

from Comparison_project import ComparisonWorkerThread, dict_value_to_float
from ImageChangeButton import ImageChangeButton
# 导入两个不同的对话框类
from TransferDataDialog import TransferDataDialog
from WholeLineTransferDialog import WholeLineTransferDialog


class OutputReportWidget(QWidget):
    def __init__(self, data_model, config_manager):
        super().__init__()
        self.setWindowTitle("输出报告")
        self.setGeometry(400, 100, 1280, 800)
        self.setFixedSize(1280, 800)

        self.data_model = data_model
        self.config_manager = config_manager  # 保存config_manager的引用

        self.filter_condition = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.current_text_index = 0

        self.setStyleSheet("background-color: rgb(31, 55, 96);")
        self.data_model.dataChanged.connect(self.load_data_from_database)

        layout = QVBoxLayout(self)
        self.checkbox_style = """
            QCheckBox { spacing: 0px; color: white; font-size: 14px; }
            QCheckBox::indicator { width: 20px; height: 20px; border-radius: 5px; background-color: #a0a0a0; }
            QCheckBox::indicator:checked { background-color: #0078d7; image: url(:/icons/checkmark.png); }
            """

        self.title_label = QLabel("抛光参数选择", self)
        self.title_label.setFont(QFont("Microsoft YaHei", 25))
        self.title_label.setStyleSheet("color: white;")
        layout.addWidget(self.title_label)

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(10)
        self.table_widget.setHorizontalHeaderLabels(
            ["序号", "模式","方案选择","主皮带速度", "进砖宽度", "摆动速度", "边部停留时间","边部停留时间", "操作",  "操作"]
        )
        self.table_widget.setColumnHidden(0, True)
        self.table_widget.setColumnHidden(6, True)
        self.table_widget.setColumnHidden(9, True)

        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        header_font = QFont("Microsoft YaHei", 18, QFont.Bold)
        self.table_widget.horizontalHeader().setFont(header_font)
        self.table_widget.setFont(QFont("Microsoft YaHei", 13))
        self.table_widget.setStyleSheet("""
            QTableWidget { color: white; gridline-color: #ddd; border: 1px solid #ddd; }
            QHeaderView::section { 
                background-color: rgb(31, 55, 96); color: white; border: 1px solid #ddd; 
                font-family: "Microsoft YaHei"; font-size: 18px; font-weight: bold; 
            }
        """)

        # 设置列宽
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)

        self.load_data_from_database()

        layout.addWidget(self.table_widget)

        button1_layout = QHBoxLayout()
        delete_button = ImageChangeButton("删除", ":SmallFrame", ":SmallFrameClicked", 114, 37, True)
        delete_button.clicked.connect(self.delete_selected_rows)
        button1_layout.addStretch()
        button1_layout.addWidget(delete_button)
        layout.addLayout(button1_layout)

        button2_layout = QHBoxLayout()
        self.compare_button = ImageChangeButton("方案对比", ":MiddleFrame", ":MiddleFrameClicked", 236, 56, True)
        self.compare_button.clicked.connect(self.on_compare_btn)
        transfer_button = ImageChangeButton("数据传输", ":MiddleFrame", ":MiddleFrameClicked", 236, 56, True)
        transfer_button.clicked.connect(self.transfer_parameter)
        button2_layout.addStretch()
        button2_layout.addWidget(self.compare_button)
        button2_layout.addSpacing(30)
        button2_layout.addWidget(transfer_button)
        layout.addLayout(button2_layout)

        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Microsoft YaHei", 16))
        layout.addWidget(self.status_label)
        self.status_label.setStyleSheet("color: white;")
        self.setLayout(layout)
        self.setContentsMargins(40, 40, 40, 20)

        self.worker_thread = ComparisonWorkerThread()
        self.worker_thread.result_signal.connect(self.update_progress)

    def set_filter_condition(self, filter_condition):
        self.load_data_from_database()

    def load_data_from_database(self):
        # DataModel.fetch_data() 返回的列顺序:
        # rowid(0), mode(1), swing_mode(2), belt_speed(3), ceramic_width(4),
        # beam_swing_speed(5), stay_time(6), device_name(7), full_motion_param(8)
        rows = self.data_model.fetch_data()
        self.table_widget.setRowCount(len(rows))

        for row_idx, row_data in enumerate(rows):
            # 表格列与数据源列的对应关系
            self.table_widget.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))  # 序号(rowid)
            self.table_widget.setItem(row_idx, 1, QTableWidgetItem(str(row_data[1])))  # 模式
            self.table_widget.setItem(row_idx, 2, QTableWidgetItem(str(row_data[2])))  # 方案选择
            self.table_widget.setItem(row_idx, 3, QTableWidgetItem(str(row_data[3])))  # 主皮带速度
            self.table_widget.setItem(row_idx, 4, QTableWidgetItem(str(row_data[4])))  # 进砖宽度
            self.table_widget.setItem(row_idx, 5, QTableWidgetItem(str(row_data[5])))  # 摆动速度
            self.table_widget.setItem(row_idx, 6, QTableWidgetItem(str(row_data[6])))  # 边部停留时间(旧)
            self.table_widget.setItem(row_idx, 7, QTableWidgetItem(str(row_data[7])))  # 设备
            self.table_widget.setItem(row_idx, 9, QTableWidgetItem(str(row_data[8])))  # 完整参数 (隐藏列)

            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row_idx, col)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)

            container = QWidget()
            layout = QHBoxLayout(container)
            checkbox = QCheckBox()
            checkbox.setStyleSheet(self.checkbox_style)
            layout.addWidget(checkbox, alignment=Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            self.table_widget.setCellWidget(row_idx, 8, container)  # 操作列

    def on_compare_btn(self):
        rows = self.table_widget.rowCount()
        selected_rowids = []
        for row in range(rows):
            checkbox = self.table_widget.cellWidget(row, 8).findChild(QCheckBox)
            if checkbox and checkbox.isChecked():
                selected_rowids.append(self.table_widget.item(row, 0).text())

        if not selected_rowids:
            QMessageBox.warning(self, "警告", "请先选择要对比的方案！")
            return

        if len(selected_rowids) > 3:
            QMessageBox.warning(self, "警告", "最多只能选择3个方案进行对比！")
            return

        fullparams = self.data_model.query_full(selected_rowids)
        self.compare_button.setEnabled(False)
        self.timer.start(500)
        plt.close('comparision_fig')
        self.comparision_fig = plt.figure('comparision_fig', figsize=(16, 8), dpi=100)
        self.comparision_fig.suptitle("方案对比")
        self.worker_thread.fig = self.comparision_fig
        self.worker_thread.args = tuple(fullparams)
        self.worker_thread.start()

    def update_progress(self, value):
        self.compare_button.setEnabled(True)
        self.timer.stop()
        self.status_label.setText('方案对比图表生成完毕，请查看结果！')
        plt.show()

    def transfer_parameter(self):
        rows = self.table_widget.rowCount()
        selected_row_indexes = []
        for row in range(rows):
            checkbox = self.table_widget.cellWidget(row, 8).findChild(QCheckBox)
            if checkbox and checkbox.isChecked():
                selected_row_indexes.append(row)

        if len(selected_row_indexes) != 1:
            QMessageBox.warning(self, "警告", "请只勾选一条方案记录进行数据传输！")
            return

        selected_row = selected_row_indexes[0]
        row_id = self.table_widget.item(selected_row, 0).text()

        full_params = self.data_model.query_full_by_id(row_id)
        if not full_params:
            QMessageBox.critical(self, "错误", "无法从数据库获取方案详情。")
            return

        line_config = self.config_manager.load_config()
        machine_count = line_config.get('global', {}).get('machine_count', 1)

        if machine_count > 1:
            print(f"检测到整线配置中有 {machine_count} 台设备，强制打开整线通讯中心...")
            try:
                dialog = WholeLineTransferDialog(full_params, self.config_manager)
                dialog.exec()
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法加载整线传输模块: {e}")
        else:
            print("检测到整线配置为1台设备，打开单机数据传输界面...")

            selected_data_for_old_dialog = [
                full_params.get('mode', ''),
                full_params.get('swing_mode', ''),
                full_params.get('device_name', ''),
                str(full_params.get('lineEdit_belt_speed', '')),
                str(full_params.get('lineEdit_beam_swing_speed', '')),
                str(full_params.get('lineEdit_accelerate', '')),
                str(full_params.get('lineEdit_num_output', '')),
                str(full_params.get('lineEdit_swing', '')),
                str(full_params.get('lineEdit_delay_time', '')),
                str(full_params.get('lineEdit_stay_time', ''))
            ]

            dialog = TransferDataDialog(selected_data_for_old_dialog, self)
            dialog.exec()

    def update_status(self):
        self.status_texts = ["正在生成方案对比图表，请稍后", "正在生成方案对比图表，请稍后。",
                             "正在生成方案对比图表，请稍后。。", "正在生成方案对比图表，请稍后。。。"]
        self.status_label.setText(self.status_texts[self.current_text_index])
        self.current_text_index = (self.current_text_index + 1) % len(self.status_texts)

    def delete_selected_rows(self):
        rows = self.table_widget.rowCount()
        selected_rowids = []
        for row in range(rows):
            checkbox = self.table_widget.cellWidget(row, 8).findChild(QCheckBox)
            if checkbox and checkbox.isChecked():
                selected_rowids.append(self.table_widget.item(row, 0).text())

        if not selected_rowids:
            QMessageBox.warning(self, "警告", "请先选择要删除的行！")
            return

        reply = QMessageBox.question(self, '确认删除', f"您确定要删除选中的 {len(selected_rowids)} 行数据吗？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.data_model.delete_multiple_data(selected_rowids)
            QMessageBox.information(self, "成功", "选中的行已成功删除！")