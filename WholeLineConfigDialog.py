import sys
import re
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QGroupBox, QSpinBox, QScrollArea, QWidget, QTabWidget, QGridLayout, QLineEdit, QMessageBox,
    QCheckBox, QComboBox
)
from PySide6.QtGui import QFont, QPainter, QColor, QDoubleValidator
from PySide6.QtCore import Qt

from WholeLineDeviceWidget import WholeLineDeviceWidget
from WholeLineGrindingHeadWidget import WholeLineGrindingHeadWidget
from WholeLineConfigManager import WholeLineConfigManager


class DarkBackgroundWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(31, 55, 96))


class WholeLineConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.config_manager = WholeLineConfigManager()
        self.device_widgets = []

        self.setWindowTitle("整线参数配置")
        self.setFixedSize(1000, 720)
        self.setStyleSheet("""
            QDialog { background-color: rgb(31, 55, 96); color: white; }
            QLabel { color: white; font-family: "Microsoft YaHei"; }
            QGroupBox {
                font-family: "Microsoft YaHei"; font-size: 14px; color: white;
                border: 1px solid #1e5dab; border-radius: 8px; margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin; subcontrol-position: top center; padding: 0 10px;
            }
            QTabWidget::pane {
                border: 2px solid #1e5dab; border-radius: 10px; background-color: rgb(31, 55, 96);
            }
            QTabBar::tab {
                background: #2c3e50; color: white; padding: 10px 25px;
                border-top-left-radius: 8px; border-top-right-radius: 8px;
                font-size: 16px; font-family: "Microsoft YaHei";
            }
            QTabBar::tab:selected { background: #1e5dab; }
            QScrollArea { border: none; background-color: transparent; }
            QLineEdit { color: black; padding: 3px; border-radius: 3px; border: 1px solid #777; }
            QComboBox { color: black; padding: 3px; }
            QComboBox QLineEdit { color: black; padding: 3px; }
            QComboBox QAbstractItemView {
                color: black; background-color: white;
                selection-background-color: #3d7ccb;
            }
            QSpinBox { color: black; }
            QCheckBox {
                spacing: 5px; font-family: "Microsoft YaHei"; 
                font-size: 14px; color: #FFFFFF;
            }
            QCheckBox::indicator {
                width: 18px; height: 18px;
                border: 2px solid #1e5dab; border-radius: 5px;
                background-color: #2c3e50;
            }
            QCheckBox::indicator:hover { border-color: #3d7ccb; }
            QCheckBox::indicator:checked { background-color: #0078d7; }
        """)
        self.setModal(True)

        main_layout = QVBoxLayout(self)

        title_label = QLabel("整线参数配置", self)
        title_label.setFont(QFont("Microsoft YaHei", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # --- 步骤 1: 创建所有UI控件 ---
        self.tab_widget = QTabWidget(self)
        main_layout.addWidget(self.tab_widget)

        self.create_device_and_com_tab()
        self.create_grinding_block_tab()

        button_layout = QHBoxLayout()
        self.whole_line_calc_checkbox = QCheckBox("整线计算", self)
        self.save_button = QPushButton("保存配置", self)
        self.save_button.setFixedSize(120, 40)
        self.cancel_button = QPushButton("取消", self)
        self.cancel_button.setFixedSize(120, 40)

        button_style = """
            QPushButton { 
                background-color: #30438c; color: white; border: none; 
                padding: 10px; font-size: 16px; border-radius: 5px;
            }
            QPushButton:hover { background-color: #40539c; }
            QPushButton:pressed { background-color: #7986b5; }
        """
        self.save_button.setStyleSheet(button_style)
        self.cancel_button.setStyleSheet(button_style)

        button_layout.addWidget(self.whole_line_calc_checkbox)
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        # --- 步骤 2: 连接所有信号 ---
        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.on_save_button_clicked)
        self.machine_count_spinbox.valueChanged.connect(self.on_machine_count_changed)
        self.save_conv_button.clicked.connect(self.on_save_speed_conversion)
        self.speed_conv_combo.currentTextChanged.connect(self.on_speed_conv_changed)
        self.delete_conv_button.clicked.connect(self.on_delete_speed_conversion)

        # --- 步骤 3: 加载数据到UI ---
        self.load_configuration_to_ui()

    def create_device_and_com_tab(self):
        tab1_widget = QWidget()
        tab1_layout = QVBoxLayout(tab1_widget)
        self.tab_widget.addTab(tab1_widget, "设备与通讯")
        self.create_global_config_group(tab1_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = DarkBackgroundWidget()
        scroll_content.setObjectName("scrollContentWidget")
        scroll_area.setWidget(scroll_content)
        content_layout = QHBoxLayout(scroll_content)
        self.machines_layout = QVBoxLayout()
        self.machines_layout.setAlignment(Qt.AlignTop)
        self.com_layout = QVBoxLayout()
        self.com_layout.setAlignment(Qt.AlignTop)
        content_layout.addLayout(self.machines_layout, 3)
        content_layout.addLayout(self.com_layout, 1)
        tab1_layout.addWidget(scroll_area)

    def create_global_config_group(self, parent_layout):
        count_group = QGroupBox("整线全局配置")
        global_layout = QHBoxLayout()
        global_layout.setContentsMargins(15, 15, 15, 15)
        machine_count_label = QLabel("抛光机数量：", self)
        machine_count_label.setFont(QFont("Microsoft YaHei", 12))
        self.machine_count_spinbox = QSpinBox(self)
        self.machine_count_spinbox.setMinimum(1)
        self.machine_count_spinbox.setMaximum(10)
        self.machine_count_spinbox.setFont(QFont("Microsoft YaHei", 12))
        global_layout.addWidget(machine_count_label)
        global_layout.addWidget(self.machine_count_spinbox)

        global_layout.addSpacing(40)
        font_12 = QFont("Microsoft YaHei", 12)
        speed_conv_label = QLabel("速度换算：", self)
        speed_conv_label.setFont(font_12)
        self.speed_conv_combo = QComboBox(self)
        self.speed_conv_combo.setFont(font_12)
        self.speed_conv_combo.addItems(["主皮带", "横梁", "其他"]) # 添加示例选项
        self.speed_conv_combo.setFixedWidth(120)
        self.speed_conv_combo.setEditable(True)
        self.speed_conv_combo.lineEdit().setPlaceholderText("选择或输入")
        self.speed_conv_combo.setStyleSheet("""
                    QComboBox { 
                        color: black; 
                        padding: 3px; 
                    }
                    QComboBox QAbstractItemView {
                        color: black; /* 将下拉项的文字颜色设置为黑色 */
                        background-color: white; /* 将下拉列表的背景设置为白色 */
                        selection-background-color: #3d7ccb; /* 设置选中项的背景色 */
                    }
                """)
        hz_label = QLabel("1HZ=", self)
        hz_label.setFont(font_12)

        # 第一个输入框 (皮带速度)
        self.hz_value_edit_belt = QLineEdit(self)
        self.hz_value_edit_belt.setFont(font_12)
        self.hz_value_edit_belt.setFixedWidth(120)  # 调整宽度
        self.hz_value_edit_belt.setValidator(QDoubleValidator(0.0, 9999.99, 4, self))
        self.hz_value_edit_belt.setPlaceholderText("皮带速度")  # 添加提示信息

        # 第二个输入框 (横梁摆动速度)
        self.hz_value_edit_beam = QLineEdit(self)
        self.hz_value_edit_beam.setFont(font_12)
        self.hz_value_edit_beam.setFixedWidth(120)  # 调整宽度
        self.hz_value_edit_beam.setValidator(QDoubleValidator(0.0, 9999.99, 4, self))
        self.hz_value_edit_beam.setPlaceholderText("横梁摆动速度")  # 添加提示信息


        unit_label = QLabel("mm/s", self)
        unit_label.setFont(font_12)
        self.save_conv_button = QPushButton("保存", self)
        self.save_conv_button.setFont(QFont("Microsoft YaHei", 10))
        button_style = """
                    QPushButton { 
                        background-color: #30438c; color: white; border: none; 
                        padding: 5px 15px; font-size: 14px; border-radius: 5px;
                    }
                    QPushButton:hover { background-color: #40539c; }
                    QPushButton:pressed { background-color: #7986b5; }
                """

        self.save_conv_button.setStyleSheet(button_style)
        # 创建删除按钮
        self.delete_conv_button = QPushButton("删除", self)
        self.delete_conv_button.setFont(QFont("Microsoft YaHei", 10))
        self.delete_conv_button.setStyleSheet(button_style)  # 复用样式
        # 将新控件添加到布局中
        global_layout.addWidget(speed_conv_label)
        global_layout.addWidget(self.speed_conv_combo)
        global_layout.addWidget(hz_label)
        global_layout.addWidget(self.hz_value_edit_belt) # 添加第一个输入框
        global_layout.addWidget(self.hz_value_edit_beam) # 添加第二个输入框
        global_layout.addWidget(unit_label)
        global_layout.addSpacing(10)
        global_layout.addWidget(self.save_conv_button)
        global_layout.addWidget(self.delete_conv_button) # 添加删除按钮到布局


        global_layout.addStretch()
        count_group.setLayout(global_layout)
        count_group.setFixedHeight(80)
        parent_layout.addWidget(count_group)
        self.spacing_group = QGroupBox("设备间距配置")
        self.spacing_layout = QGridLayout()
        self.spacing_group.setLayout(self.spacing_layout)
        self.spacing_group.setVisible(False)
        parent_layout.addWidget(self.spacing_group)

    def create_grinding_block_tab(self):
        tab2_widget = QWidget()
        tab2_layout = QVBoxLayout(tab2_widget)
        main_scroll_area = QScrollArea()
        main_scroll_area.setWidgetResizable(True)
        scroll_content_widget = DarkBackgroundWidget()
        main_scroll_area.setWidget(scroll_content_widget)
        self.grinding_config_layout = QVBoxLayout(scroll_content_widget)
        self.grinding_config_layout.setAlignment(Qt.AlignTop)
        tab2_layout.addWidget(main_scroll_area)
        self.tab_widget.addTab(tab2_widget, "磨块配比")

    def gather_ui_data(self):
        all_configs = {'global': {}, 'spacings': [], 'devices': [], 'communication': [], 'speed_conversions': {}}

        # 1. 收集全局配置
        global_config = {
            'machine_count': self.machine_count_spinbox.value(),
            'whole_line_calc_enabled': self.whole_line_calc_checkbox.isChecked()
        }
        all_configs['global'] = global_config

        # 2. 收集速度换算方案列表
        all_configs['speed_conversions'] = self.speed_conv_data

        # 3. 收集设备间距
        machine_count = self.machine_count_spinbox.value()
        spacings = []
        if machine_count > 1:
            for i in range(self.spacing_layout.count()):
                widget = self.spacing_layout.itemAt(i).widget()
                if isinstance(widget, QLineEdit):
                    spacings.append(widget.text())
        all_configs['spacings'] = spacings

        # 4. 收集每个设备的详细配置
        devices = []
        for i in range(self.machines_layout.count()):
            device_config = {}
            device_widget = self.machines_layout.itemAt(i).widget()
            if isinstance(device_widget, WholeLineDeviceWidget):
                device_config['type'] = device_widget.type_combo.currentText()
                device_config['head_count'] = device_widget.head_count_edit.text()
                device_config['between'] = device_widget.between_edit.text()
                device_config['beam_between'] = device_widget.beam_between_edit.text()
                # 收集当前设备选择的换算方案
                device_config['conversion_profile'] = device_widget.conversion_combo.currentText()

            if i < self.grinding_config_layout.count():
                grinding_widget = self.grinding_config_layout.itemAt(i).widget()
                if isinstance(grinding_widget, WholeLineGrindingHeadWidget):
                    grinding_selections = [combo.currentText() for combo in grinding_widget.grit_combos]
                    device_config['grinding_config'] = grinding_selections
            devices.append(device_config)
        all_configs['devices'] = devices

        # 5. 收集通讯配置
        comms = []
        for i in range(self.com_layout.count()):
            com_group = self.com_layout.itemAt(i).widget()
            if isinstance(com_group, QGroupBox):
                edits = com_group.findChildren(QLineEdit)
                com_config = {'ip': edits[0].text() if len(edits) > 0 else '',
                              'port': edits[1].text() if len(edits) > 1 else ''}
                comms.append(com_config)
        all_configs['communication'] = comms

        return all_configs

    def on_machine_count_changed(self, count):
        current_data = self.gather_ui_data()
        for layout in [self.machines_layout, self.com_layout, self.spacing_layout]:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        self.populate_ui_with_data(current_data, target_count=count)
        self.update_grinding_tab(current_data)

    def load_configuration_to_ui(self):
        self.machine_count_spinbox.blockSignals(True)
        config_data = self.config_manager.load_config()

        #1：将加载速度方案的逻辑提前
        # 必须先将 speed_conv_data 加载到内存中，后续的 populate 方法才能使用它
        self.speed_conv_data = config_data.get('speed_conversions', {})

        # 现在可以安全地填充UI了
        self.populate_ui_with_data(config_data)

        self.machine_count_spinbox.blockSignals(False)
        self.update_grinding_tab(config_data)

        #填充全局速度换算UI
        self.speed_conv_combo.blockSignals(True)
        self.speed_conv_combo.clear()
        if self.speed_conv_data:
            self.speed_conv_combo.addItems(self.speed_conv_data.keys())
        self.speed_conv_combo.blockSignals(False)

        if self.speed_conv_combo.count() > 0:
            self.on_speed_conv_changed(self.speed_conv_combo.currentText())
        else:
            self.hz_value_edit_belt.clear()
            self.hz_value_edit_beam.clear()


    def populate_ui_with_data(self, data: dict, target_count=None):
        global_config = data.get('global', {})
        machine_count = target_count if target_count is not None else global_config.get('machine_count', 1)
        self.machine_count_spinbox.blockSignals(True)
        self.machine_count_spinbox.setValue(machine_count)
        self.machine_count_spinbox.blockSignals(False)
        is_checked = global_config.get('whole_line_calc_enabled', False)
        self.whole_line_calc_checkbox.setChecked(is_checked)
        spacings_data = data.get('spacings', [])
        devices_data = data.get('devices', [])
        comms_data = data.get('communication', [])

        if machine_count > 1:
            self.spacing_group.setVisible(True)
            items_per_row = 4
            for i in range(machine_count - 1):
                row, col = i // items_per_row, (i % items_per_row) * 2
                spacing_label = QLabel(f"{i + 1}-{i + 2}号机间距(mm):")
                spacing_edit = QLineEdit(spacings_data[i] if i < len(spacings_data) else "")
                spacing_edit.setValidator(QDoubleValidator(0, 99999, 2, self))
                spacing_edit.setFixedWidth(100)
                self.spacing_layout.addWidget(spacing_label, row, col)
                self.spacing_layout.addWidget(spacing_edit, row, col + 1)
            self.spacing_layout.setColumnStretch(items_per_row * 2, 1)
        else:
            self.spacing_group.setVisible(False)

        conversion_options = list(self.speed_conv_data.keys())
        self.device_widgets.clear()
        for i in range(machine_count):
            device_widget = WholeLineDeviceWidget(i + 1, self)
            device_widget.conversion_combo.addItems(conversion_options)
            if i < len(devices_data):
                device_info = devices_data[i]
                device_widget.type_combo.setCurrentText(device_info.get('type', '单头摆'))
                device_widget.head_count_edit.setText(device_info.get('head_count', ''))
                device_widget.between_edit.setText(device_info.get('between', ''))
                device_widget.beam_between_edit.setText(device_info.get('beam_between', ''))
                #新增：加载并设置当前设备选择的换算方案
                # 使用 .get() 提供一个默认空字符串，以兼容没有此配置的旧文件
                saved_profile = device_info.get('conversion_profile', '')
                device_widget.conversion_combo.setCurrentText(saved_profile)

            self.machines_layout.addWidget(device_widget)
            self.device_widgets.append(device_widget)

            com_group = QGroupBox(f"{i + 1} 号机通讯")
            com_group.setFixedHeight(75)
            com_layout = QHBoxLayout()
            ip_edit = QLineEdit(comms_data[i].get('ip', '') if i < len(comms_data) else "")
            ip_edit.setPlaceholderText("IP 地址")
            ip_edit.setFixedWidth(140)
            port_edit = QLineEdit(comms_data[i].get('port', '') if i < len(comms_data) else "")
            port_edit.setPlaceholderText("端口号")
            port_edit.setFixedWidth(70)
            com_layout.addWidget(ip_edit)
            com_layout.addWidget(port_edit)
            com_layout.addStretch()
            com_group.setLayout(com_layout)
            self.com_layout.addWidget(com_group)

    def on_save_button_clicked(self):
        is_valid, error_message = self.validate_all_inputs()
        if not is_valid:
            QMessageBox.warning(self, "输入错误", error_message)
            return

        # 1. 从UI收集基础数据
        config_data = self.gather_ui_data()

        # 2. 将内存中的 speed_conv_data 添加到要保存的数据的顶层
        config_data['speed_conversions'] = self.speed_conv_data

        # 3. 保存
        self.config_manager.save_config(config_data)
        QMessageBox.information(self, "成功", "整线配置已成功保存！")
        self.accept()

    def validate_all_inputs(self):
        ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        for i in range(self.com_layout.count()):
            com_group = self.com_layout.itemAt(i).widget()
            ip_edit = com_group.findChild(QLineEdit)
            if ip_edit and ip_edit.text() and not ip_pattern.match(ip_edit.text()):
                return False, f"{i + 1}号机通讯的IP地址格式不正确！"
        return True, ""

    def update_grinding_tab(self, source_data=None):
        if source_data is None:
            source_data = self.gather_ui_data()
        while self.grinding_config_layout.count():
            child = self.grinding_config_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        devices_data = source_data.get('devices', [])
        for i in range(self.machines_layout.count()):
            device_widget = self.machines_layout.itemAt(i).widget()
            if isinstance(device_widget, WholeLineDeviceWidget):
                device_number = i + 1
                try:
                    head_count = int(device_widget.head_count_edit.text())
                except (ValueError, TypeError):
                    head_count = 0
                if head_count > 0:
                    grinding_widget = WholeLineGrindingHeadWidget(device_number, head_count)
                    if i < len(devices_data):
                        grinding_data = devices_data[i].get('grinding_config', [])
                        for combo_idx, combo in enumerate(grinding_widget.grit_combos):
                            if combo_idx < len(grinding_data):
                                combo.setCurrentText(grinding_data[combo_idx])
                    self.grinding_config_layout.addWidget(grinding_widget)


    def on_save_speed_conversion(self):
        """
        修正后的方法：“保存”按钮逻辑，用于处理两个输入框。
        """
        key = self.speed_conv_combo.currentText().strip()
        belt_value = self.hz_value_edit_belt.text().strip()
        beam_value = self.hz_value_edit_beam.text().strip()

        if not key:
            QMessageBox.warning(self, "输入错误", "换算名称不能为空！")
            return

        # 将两个值存为一个列表
        self.speed_conv_data[key] = [belt_value, beam_value]

        config = self.config_manager.load_config()
        config['speed_conversions'] = self.speed_conv_data
        self.config_manager.save_config(config)

        if self.speed_conv_combo.findText(key) == -1:
            self.speed_conv_combo.addItem(key)

        QMessageBox.information(self, "成功", f"速度换算配置 '{key}' 已保存！")

        self.update_all_conversion_combos()

    def on_speed_conv_changed(self, text):
        """
        当速度换算下拉框的内容改变时触发。
        现在会加载两个速度值到对应的输入框。
        """
        # 从内存中查找对应的值，现在应该是一个列表
        values = self.speed_conv_data.get(text, ["", ""])  # 默认值是一个包含两个空字符串的列表

        # 安全性检查：确保values是一个有两个元素的列表
        if not isinstance(values, list) or len(values) < 2:
            values = ["", ""]  # 如果格式不對，提供安全的默认值

        self.hz_value_edit_belt.setText(values[0])
        self.hz_value_edit_beam.setText(values[1])

    def on_speed_conv_changed(self, text):
        """
        修正后的方法：下拉框切换逻辑，用于更新两个输入框。
        """
        # 从内存数据中获取值列表，默认值为包含两个空字符串的列表
        values = self.speed_conv_data.get(text, ["", ""])

        # 安全性检查，确保获取到的是一个至少有两个元素的列表
        if not isinstance(values, list) or len(values) < 2:
            values = ["", ""] # 如果数据格式损坏，则提供安全默认值

        # 将列表中的值分别设置到两个输入框中
        self.hz_value_edit_belt.setText(values[0])
        self.hz_value_edit_beam.setText(values[1])

    def on_delete_speed_conversion(self):
        """
        “速度换算”旁边的“删除”按钮被点击时触发。
        """
        # 1. 获取当前选中的项
        key_to_delete = self.speed_conv_combo.currentText()
        current_index = self.speed_conv_combo.currentIndex()

        # 2. 检查是否有可删除的项
        if not key_to_delete or current_index == -1:
            QMessageBox.warning(self, "操作无效", "没有可删除的配置项。")
            return

        # 3. 弹窗确认，防止误删
        reply = QMessageBox.question(self, '确认删除',
                                     f"您确定要删除速度换算配置 '{key_to_delete}' 吗？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.No:
            return

        # 4. 从内存数据中删除
        if key_to_delete in self.speed_conv_data:
            del self.speed_conv_data[key_to_delete]

        # 5. 更新并保存配置文件
        config = self.config_manager.load_config()
        config['speed_conversions'] = self.speed_conv_data
        self.config_manager.save_config(config)

        # 6. 从UI的下拉框中移除该项
        self.speed_conv_combo.removeItem(current_index)

        QMessageBox.information(self, "成功", f"配置 '{key_to_delete}' 已被删除。")
        self.update_all_conversion_combos()

    def update_all_conversion_combos(self):
        """
        更新所有设备控件的“换算”下拉框选项。
        """
        options = list(self.speed_conv_data.keys())  # 获取所有全局换算选项的名称
        for widget in self.device_widgets:
            widget.update_conversion_options(options)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = WholeLineConfigDialog()
    dialog.show()
    sys.exit(app.exec())