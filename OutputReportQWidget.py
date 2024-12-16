import sys
import sqlite3
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout,
    QCheckBox, QLabel, QMessageBox
)
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt
from matplotlib import pyplot as plt

from Comparison_project import ComparisonWorkerThread, dict_value_to_float
from ImageChangeButton import ImageChangeButton


class OutputReportWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("输出报告")
        self.setGeometry(400, 100, 1280, 800)  # 设置窗口尺寸为 1280x800
        self.setFixedSize(1280, 800)

        # 设置背景颜色
        self.setStyleSheet("background-color: rgb(31, 55, 96);")

        # 创建布局
        layout = QVBoxLayout()
        self.checkbox_style = """
            QCheckBox {
                spacing: 0px; /* 文本与复选框之间的间距 */
                color: white; /* 文本颜色 */
                font-size: 14px; /* 字体大小 */
            }
            
            QCheckBox::indicator {
                width: 20px; /* 复选框宽度 */
                height: 20px; /* 复选框高度 */
                border: 0px solid #555; /* 复选框边框 */
                border-radius: 5px; /* 复选框圆角 */
                background-color: #a0a0a0; /* 复选框背景颜色 */
                transition: all 0.2s ease; /* 添加过渡效果 */
            }
            
            QCheckBox::indicator:checked {
                background-color: #0078d7; /* 选中时的背景颜色 */
                border: 1px solid #0078d7; /* 选中时的边框颜色 */
                image: url(:/icons/checkmark.png); /* 选中时的图标 */
                transition: all 0.2s ease; /* 添加过渡效果 */
            }
            
            QCheckBox::indicator:checked:hover {
                background-color: #005a9e; /* 选中且悬停时的背景颜色 */
                border: 1px solid #005a9e; /* 选中且悬停时的边框颜色 */
            }
            
            QCheckBox::indicator:unchecked:hover {
                border: 1px solid #0078d7; /* 未选中但悬停时的边框颜色 */
            }
            
            QCheckBox:disabled {
                color: #888; /* 禁用时的文本颜色 */
            }
            
            QCheckBox:disabled::indicator {
                background-color: #444; /* 禁用时的复选框背景颜色 */
                border: 1px solid #666; /* 禁用时的复选框边框颜色 */
            }
            """
        self.container_style = """
                    QWidget {
                        border-radius: 5px; /* 复选框圆角 */
                        width: 1px; /* 复选框宽度 */
                        height: 10px; /* 复选框高度 */
                        border: 1px solid #666; /* 禁用时的复选框边框颜色 */                    
                        }

                    """
        # 添加标题
        title_label = QLabel("数据库--双头摆抛光参数", self)
        title_label.setFont(QFont("Microsoft YaHei", 25))
        title_label.setStyleSheet("color: white;")
        layout.addWidget(title_label)

        # 创建一个表格控件
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(8)  # 增加一列用于显示序号
        self.table_widget.setHorizontalHeaderLabels(
            ["序号", "产量", "同粒度磨头数", "模式", "运动参数", "方案选择", "操作", "操作"]
        )
        # 隐藏序号列
        self.table_widget.setColumnHidden(0, True)
        self.table_widget.setColumnHidden(6, True)

        # 设置表格为可滚动
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)  # 禁止编辑
        self.table_widget.setColumnWidth(1, 130)  # 固定第一列宽度为150
        self.table_widget.setColumnWidth(2, 150)  # 固定第一列宽度为150
        self.table_widget.setColumnWidth(3, 100)  # 固定第一列宽度为150
        self.table_widget.setColumnWidth(4, 582)  # 固定第一列宽度为150
        self.table_widget.setColumnWidth(7, 80)  # 固定第一列宽度为150

        # 设置表格单元格内容居中
        self.table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.table_widget.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        # 设置表格字体为 20pt
        font = QFont("Microsoft YaHei", 13)
        self.table_widget.setFont(font)
        # 设置表头字体加粗
        header_font = QFont("Microsoft YaHei", 18, QFont.Bold)
        self.table_widget.horizontalHeader().setFont(header_font)
        self.table_widget.setStyleSheet("color: white; gridline-color: rgb(221, 221, 221);border: 1px solid rgb(221, 221, 221);")

        # 从数据库加载数据
        self.load_data_from_database()
        header = self.table_widget.horizontalHeader()
        for col in range(self.table_widget.columnCount()):
            header.setSectionResizeMode(col, QHeaderView.Fixed)  # 禁止手动调整列宽
        # 设置行高不可调整
        for row in range(self.table_widget.rowCount()):
            self.table_widget.setRowHeight(row, 30)  # 设置每行高度为 30 像素

        # 设置表格的边距
        layout.addSpacing(20)  # 上边距
        layout.addWidget(self.table_widget)

        # 添加删除按钮
        # delete_button = QPushButton("删除", self)
        delete_button = ImageChangeButton("删除", ":SmallFrame", ":SmallFrameClicked", 114, 37,True)

        delete_button.setStyleSheet("background-color: red; color: white;")
        delete_button.clicked.connect(self.delete_selected_rows)

        button1_layout = QHBoxLayout()
        button1_layout.addStretch()
        button1_layout.addWidget(delete_button)
        layout.addLayout(button1_layout)

        layout.addSpacing(20)  # 上边距
        # 添加“方案对比”和“数据传输”按钮
        button2_layout = QHBoxLayout()
        # compare_button = QPushButton("方案对比", self)
        # compare_button = ImageChangeButton("方案对比", ":SmallFrame", ":SmallFrameClicked", 114, 37,True)
        self.compare_button = ImageChangeButton("方案对比",":MiddleFrame",":MiddleFrameClicked",236,56,True)
        self.compare_button.clicked.connect(self.on_compare_btn)
        self.compare_button.setStyleSheet("background-color: blue; color: white;")
        # transfer_button = QPushButton("数据传输", self)
        # transfer_button = ImageChangeButton("数据传输", ":SmallFrame", ":SmallFrameClicked", 114, 37,True)
        transfer_button = ImageChangeButton("数据传输",":MiddleFrame",":MiddleFrameClicked",236,56,True)

        transfer_button.setStyleSheet("background-color: green; color: white;")
        button2_layout.addStretch()
        button2_layout.addWidget(self.compare_button)
        button2_layout.addSpacing(30)
        button2_layout.addWidget(transfer_button)
        button2_layout.addSpacing(30)
        layout.addLayout(button2_layout)

        # 设置布局
        self.setLayout(layout)
        self.setContentsMargins(40, 40, 40, 40)

        # 输入量（字典类型）
        a = {'lineEdit_beam_between': '650.0', 'lineEdit_diameter': '540.0', 'lineEdit_grind_length': '160.0',
             'lineEdit_work_time': '22.0', 'lineEdit_production_volume': '30000.0', 'lineEdit_ceramic_width': '900.0',
             'lineEdit_accelerate': '650.0', 'lineEdit_overlap': '10.0', 'lineEdit_num_input': '4.0',
             'lineEdit_group_count': '1.0', 'lineEdit_stay_time_input': '0.8',              'lineEdit_belt_speed': '420.88',
             'lineEdit_beam_swing_speed': '289.2', 'lineEdit_beam_constant_time': '1.21',
             'lineEdit_stay_time_output': '1.4',
             'lineEdit_swing': '478.6', 'lineEdit_num_output': '5', 'lineEdit_coefficient': '0.3864',
             'lineEdit_delay_time': '0.14', 'lineEdit_delay_time_list': [0.0, 0.14, 0.28, 0.42, 0.56],
             'lineEdit_between': '590.5492918897945', 'R': '270.0'}
        b = {'lineEdit_beam_between': '600.0', 'lineEdit_diameter': '540.0', 'lineEdit_grind_length': '160.0',
             'lineEdit_work_time': '22.0', 'lineEdit_production_volume': '25000.0', 'lineEdit_ceramic_width': '900.0',
             'lineEdit_accelerate': '650.0', 'lineEdit_overlap': '10.0', 'lineEdit_num_input': '4',
             'lineEdit_group_count': '1', 'lineEdit_stay_time_input': '0.8', 'lineEdit_belt_speed': '350.73',
             'lineEdit_beam_swing_speed': '559.0', 'lineEdit_beam_constant_time': '0',
             'lineEdit_stay_time_output': '0.8',
             'lineEdit_swing': '480.74', 'lineEdit_num_output': '4', 'lineEdit_coefficient': '0.3874',
             'lineEdit_delay_time': '0.45',
             'lineEdit_delay_time_list': [1.26, 0.45, 0.9, 1.35], 'lineEdit_between': '441.92', 'R': '270.0',
             'self_delay_time': '1.26'}
        c = {'lineEdit_between': '600.0', 'lineEdit_beam_between': '1906.0', 'lineEdit_diameter': '540.0',
             'lineEdit_grind_length': '150.0', 'lineEdit_work_time': '22.0', 'lineEdit_production_volume': '25000.0',
             'lineEdit_ceramic_width': '900.0', 'lineEdit_accelerate': '650.0', 'lineEdit_overlap': '10.0',
             'lineEdit_num_input': '4.0', 'lineEdit_group_count': '1.0', 'lineEdit_stay_time_input': '0.8',
             'lineEdit_belt_speed': '350.73', 'lineEdit_beam_swing_speed': '250.62',
             'lineEdit_beam_constant_time': '1.85',
             'lineEdit_stay_time_output': '0.8', 'lineEdit_swing': '560.28', 'lineEdit_num_output': '4.0',
             'lineEdit_coefficient': '', 'lineEdit_delay_time': '2.01', 'lineEdit_delay_time_list': [0.0, 2.01],
             'R': '270.0', 'self_delay_time': '1.71'}
        a = dict_value_to_float(a)
        b = dict_value_to_float(b)
        c = dict_value_to_float(c)
        a['device'] = 'single'
        a['mode'] = 'order'
        b['device'] = 'single'
        b['mode'] = 'self_order'
        c['device'] = 'double'
        c['mode'] = 'self_order'
        fig = plt.figure(figsize=(16, 8), dpi=100)
        fig.suptitle("方案对比")

        self.worker_thread = ComparisonWorkerThread(fig, a, b, c)
        self.worker_thread.result_signal.connect(self.update_progress)

    def on_compare_btn(self):
        self.compare_button.setEnabled(False)  # 禁用按钮，防止重复点击
        self.worker_thread.start()
    def update_progress(self, value):
        self.compare_button.setEnabled(True)  # 禁用按钮，防止重复点击
        print(value)
        plt.show()

    def load_data_from_database(self):
        # 连接数据库
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # 查询数据，包括rowid字段
        cursor.execute("SELECT rowid, production, num, mode, motion_param, swing_mode FROM param")
        rows = cursor.fetchall()

        # 关闭数据库连接
        conn.close()

        # 设置表格行数
        self.table_widget.setRowCount(len(rows))

        # 填充数据到表格
        for row_idx, row_data in enumerate(rows):
            for col_idx, item in enumerate(row_data):
                cell_item = QTableWidgetItem(str(item))
                cell_item.setTextAlignment(Qt.AlignCenter)  # 单元格内容居中
                self.table_widget.setItem(row_idx, col_idx, cell_item)

            # 添加 QCheckBox 到最后一列
            checkbox = QCheckBox()

            # 创建一个 QWidget 作为容器
            container = QWidget()
            # container.setFixedWidth(10)

            # 创建一个水平布局，并将 QCheckBox 添加到布局中
            layout = QHBoxLayout(container)
            checkbox.setStyleSheet(self.checkbox_style)
            container.setStyleSheet(self.container_style)
            layout.addWidget(checkbox)
            # 设置布局的对齐方式为居中
            layout.setAlignment(checkbox, Qt.AlignCenter)

            # 设置布局的边距为 0，避免多余的空白
            layout.setContentsMargins(8, 0, 0, 0)
            self.table_widget.setCellWidget(row_idx, 7, container)

        # 调整操作列的列宽，使其刚好跟复选框差不多大
        self.table_widget.horizontalHeader().resizeSection(6, 50)  # 设置操作列宽度为50像素

    def delete_selected_rows(self):
        # 获取所有行
        rows = self.table_widget.rowCount()
        selected_rows = []

        # 遍历每一行，检查最后一列的 QCheckBox 是否被选中
        for row in range(rows):
            checkbox = self.table_widget.cellWidget(row, 7).findChild(QCheckBox)
            if checkbox and checkbox.isChecked():
                selected_rows.append(row)

        if not selected_rows:
            nodata_box = QMessageBox()
            nodata_box.setWindowTitle("警告")
            nodata_box.setText("请先选择要删除的行！")
            nodata_box.setStandardButtons(QMessageBox.Ok)

            # 设置背景颜色为蓝色，文字颜色为白色
            nodata_box.setStyleSheet("""
                            QMessageBox {
                                background-color: rgb(31, 55, 96);
                            }
                            QMessageBox QLabel {
                                color: white;
                                font-family: "Microsoft YaHei"; /* 字体样式 */
                                font-size: 18px; /* 字体大小 */
                            }
                            QMessageBox QWidget#qt_msgbox_label {
                                font-family: "Microsoft YaHei"; /* 标题字体样式 */
                                font-size: 18px; /* 标题字体大小 */
                                color: white; /* 标题颜色 */
                            }
                            QMessageBox QPushButton {
                                background-color: #444;
                                color: white;
                                border: 1px solid #555;
                                padding: 5px 10px;
                            }
                            QMessageBox QPushButton:hover {
                                background-color: #555;
                            }
                        """)

            # 将删除成功对话框显示在列表界面的水平和垂直居中位置
            nodata_box.setWindowModality(Qt.ApplicationModal)
            nodata_box.move(self.mapToGlobal(self.rect().center()))

            nodata_box.exec()
            # QMessageBox.warning(self, "警告", "请先选择要删除的行！")
            return

        # 提示用户确认删除
        confirm_box = QMessageBox()
        confirm_box.setWindowTitle("确认删除")
        confirm_box.setText(f"您确定要删除选中的 {len(selected_rows)} 行数据吗？")
        confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_box.setDefaultButton(QMessageBox.No)

        # 设置背景颜色为蓝色，文字颜色为白色
        confirm_box.setStyleSheet("""
                            QMessageBox {
                                background-color: rgb(31, 55, 96);
                            }
                            QMessageBox QLabel {
                                color: white;
                                font-family: "Microsoft YaHei"; /* 字体样式 */
                                font-size: 18px; /* 字体大小 */
                            }
                            QMessageBox QWidget#qt_msgbox_label {
                                font-family: "Microsoft YaHei"; /* 标题字体样式 */
                                font-size: 18px; /* 标题字体大小 */
                                color: white; /* 标题颜色 */
                            }
                            QMessageBox QPushButton {
                                background-color: #444;
                                color: white;
                                border: 1px solid #555;
                                padding: 5px 10px;
                            }
                            QMessageBox QPushButton:hover {
                                background-color: #555;
                            }
                        """)

        # 将确认对话框显示在列表界面的水平和垂直居中位置
        confirm_box.setWindowModality(Qt.ApplicationModal)
        confirm_box.move(self.mapToGlobal(self.rect().center()))

        # 显示确认对话框并获取用户选择
        confirm_result = confirm_box.exec()

        if confirm_result == QMessageBox.Yes:
            # 连接数据库
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            # 删除数据库中的记录，根据rowid字段删除
            for row in selected_rows:
                # 获取选中行的rowid
                row_id = self.table_widget.item(row, 0).text()

                # 删除数据库中的记录
                cursor.execute("DELETE FROM param WHERE rowid=?", (row_id,))

            # 提交更改并关闭数据库连接
            conn.commit()
            conn.close()

            # 删除表格中的行
            for row in reversed(selected_rows):
                self.table_widget.removeRow(row)

            # 删除成功提示
            success_box = QMessageBox()
            success_box.setWindowTitle("删除成功")
            success_box.setText("选中的行已成功删除！")
            success_box.setStandardButtons(QMessageBox.Ok)

            # 设置背景颜色为蓝色，文字颜色为白色
            success_box.setStyleSheet("""
                            QMessageBox {
                                background-color: rgb(31, 55, 96);
                            }
                            QMessageBox QLabel {
                                color: white;
                                font-family: "Microsoft YaHei"; /* 字体样式 */
                                font-size: 18px; /* 字体大小 */
                            }
                            QMessageBox QWidget#qt_msgbox_label {
                                font-family: "Microsoft YaHei"; /* 标题字体样式 */
                                font-size: 18px; /* 标题字体大小 */
                                color: white; /* 标题颜色 */
                            }
                            QMessageBox QPushButton {
                                background-color: #444;
                                color: white;
                                border: 1px solid #555;
                                padding: 5px 10px;
                            }
                            QMessageBox QPushButton:hover {
                                background-color: #555;
                            }
                        """)

            # 将删除成功对话框显示在列表界面的水平和垂直居中位置
            success_box.setWindowModality(Qt.ApplicationModal)
            success_box.move(self.mapToGlobal(self.rect().center()))

            success_box.exec()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("主窗口")
        self.setGeometry(100, 100, 300, 200)

        # 创建按钮
        self.button = QPushButton("显示窗口", self)
        self.button.clicked.connect(self.show_second_window)

        # 设置按钮布局
        layout = QHBoxLayout()
        layout.addWidget(self.button)

        # 创建主窗口的中心部件
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 初始化第二个窗口
        self.second_window = OutputReportWidget()

    def show_second_window(self):
        # 显示第二个窗口
        self.second_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())