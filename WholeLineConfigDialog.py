import sys
import re
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QGroupBox, QSpinBox, QScrollArea, QWidget, QTabWidget, QGridLayout, QLineEdit, QMessageBox
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
            QSpinBox { color: black; }
        """)
        self.setModal(True)

        main_layout = QVBoxLayout(self)

        title_label = QLabel("整线参数配置", self)
        title_label.setFont(QFont("Microsoft YaHei", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        self.tab_widget = QTabWidget(self)
        main_layout.addWidget(self.tab_widget)

        self.create_device_and_com_tab()
        self.create_grinding_block_tab()

        button_layout = QHBoxLayout()
        button_layout.addStretch()
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
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.on_save_button_clicked)
        self.machine_count_spinbox.valueChanged.connect(self.on_machine_count_changed)

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
        all_configs = {'global': {}, 'spacings': [], 'devices': [], 'communication': []}
        machine_count = self.machine_count_spinbox.value()
        all_configs['global']['machine_count'] = machine_count
        spacings = []
        if machine_count > 1:
            for i in range(self.spacing_layout.count()):
                widget = self.spacing_layout.itemAt(i).widget()
                if isinstance(widget, QLineEdit):
                    spacings.append(widget.text())
        all_configs['spacings'] = spacings
        devices = []
        for i in range(self.machines_layout.count()):
            device_config = {}
            device_widget = self.machines_layout.itemAt(i).widget()
            if isinstance(device_widget, WholeLineDeviceWidget):
                device_config['type'] = device_widget.type_combo.currentText()
                device_config['head_count'] = device_widget.head_count_edit.text()
                device_config['between'] = device_widget.between_edit.text()
                device_config['beam_between'] = device_widget.beam_between_edit.text()

            if i < self.grinding_config_layout.count():
                grinding_widget = self.grinding_config_layout.itemAt(i).widget()
                if isinstance(grinding_widget, WholeLineGrindingHeadWidget):
                    grinding_selections = [combo.currentText() for combo in grinding_widget.grit_combos]
                    device_config['grinding_config'] = grinding_selections

            devices.append(device_config)
        all_configs['devices'] = devices

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
        self.update_grinding_tab()

    def load_configuration_to_ui(self):
        self.machine_count_spinbox.blockSignals(True)
        config_data = self.config_manager.load_config()
        self.populate_ui_with_data(config_data)
        self.machine_count_spinbox.blockSignals(False)
        self.update_grinding_tab()

    def populate_ui_with_data(self, data: dict, target_count=None):
        machine_count = target_count if target_count is not None else data.get('global', {}).get('machine_count', 1)
        self.machine_count_spinbox.blockSignals(True)
        self.machine_count_spinbox.setValue(machine_count)
        self.machine_count_spinbox.blockSignals(False)

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

        for i in range(machine_count):
            device_widget = WholeLineDeviceWidget(i + 1, self)
            if i < len(devices_data):
                device_info = devices_data[i]
                device_widget.type_combo.setCurrentText(device_info.get('type', '单头摆'))
                device_widget.head_count_edit.setText(device_info.get('head_count', ''))
                device_widget.between_edit.setText(device_info.get('between', ''))
                device_widget.beam_between_edit.setText(device_info.get('beam_between', ''))
            self.machines_layout.addWidget(device_widget)

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
        config_data = self.gather_ui_data()
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

    def update_grinding_tab(self):
        while self.grinding_config_layout.count():
            child = self.grinding_config_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        all_data = self.gather_ui_data()
        devices_data = all_data.get('devices', [])

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = WholeLineConfigDialog()
    dialog.show()
    sys.exit(app.exec())