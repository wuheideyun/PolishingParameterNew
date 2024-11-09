import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QGroupBox, QHBoxLayout, QStackedWidget, QFrame
from PySide6.QtGui import QPixmap, QPalette, QBrush
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("运动输出参数和产品质量参数设置")
        self.setGeometry(100, 100, 400, 300)

        # 创建主布局
        main_layout = QVBoxLayout()

        # 创建 QStackedWidget
        self.stacked_widget = QStackedWidget()

        # 创建运动输出参数的页面
        self.motion_page_frame = QFrame()
        # self.motion_page.setFrameShape(QFrame.StyledPanel)
        motion_layout = QFormLayout()

        # 添加主皮带速度输入框
        self.main_belt_speed_input = QLineEdit()
        motion_layout.addRow(QLabel("主皮带速度："), self.main_belt_speed_input)

        # 添加摆动速度输入框
        self.swing_speed_input = QLineEdit()
        motion_layout.addRow(QLabel("摆动速度："), self.swing_speed_input)

        # 添加匀速摆动时间输入框
        self.constant_swing_time_input = QLineEdit()
        motion_layout.addRow(QLabel("匀速摆动时间："), self.constant_swing_time_input)

        # 添加边部停留时间输入框
        self.edge_stay_time_input = QLineEdit()
        motion_layout.addRow(QLabel("边部停留时间："), self.edge_stay_time_input)

        # 添加摆幅输入框
        self.swing_amplitude_input = QLineEdit()
        motion_layout.addRow(QLabel("摆幅："), self.swing_amplitude_input)

        # 添加同粒度磨头数输入框
        self.same_grain_moto_count_input = QLineEdit()
        motion_layout.addRow(QLabel("同粒度磨头数："), self.same_grain_moto_count_input)

        # 将运动输出参数的布局添加到页面中
        self.motion_page_frame.setLayout(motion_layout)

        # 设置背景图片
        self.main_param_frame_image_path = "path_to_your_image.png"  # 替换为你的图片路径
        self.main_param_frame_image = QPixmap(self.main_param_frame_image_path)
        main_param_frame_size = self.motion_page_frame.size()
        scaled_image = self.main_param_frame_image.scaled(main_param_frame_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette3 = QPalette()
        palette3.setBrush(QPalette.Window, QBrush(scaled_image))
        self.motion_page_frame.setPalette(palette3)
        self.motion_page_frame.setAutoFillBackground(True)

        # 将页面添加到 QStackedWidget
        self.stacked_widget.addWidget(self.motion_page_frame)

        # 创建产品质量参数的页面
        self.quality_page = QWidget()
        quality_layout = QFormLayout()

        # 添加均匀系数输入框
        self.uniformity_coefficient_input = QLineEdit()
        quality_layout.addRow(QLabel("均匀系数："), self.uniformity_coefficient_input)

        # 将产品质量参数的布局添加到页面中
        self.quality_page.setLayout(quality_layout)

        # 将页面添加到 QStackedWidget
        self.stacked_widget.addWidget(self.quality_page)

        # 将 QStackedWidget 添加到主布局中
        main_layout.addWidget(self.stacked_widget)

        # 添加显示/隐藏按钮
        self.toggle_button = QPushButton("隐藏/显示产品质量参数")
        self.toggle_button.clicked.connect(self.toggle_quality_page)
        main_layout.addWidget(self.toggle_button)

        # 添加保存按钮
        self.save_button = QPushButton("参数保存")
        self.save_button.clicked.connect(self.save_parameters)
        main_layout.addWidget(self.save_button)

        # 设置主布局
        self.setLayout(main_layout)

    def toggle_quality_page(self):
        # 切换产品质量参数页面的可见性
        if self.stacked_widget.currentWidget() == self.motion_page_frame:
            self.stacked_widget.setCurrentWidget(self.quality_page)
        else:
            self.stacked_widget.setCurrentWidget(self.motion_page_frame)

    def save_parameters(self):
        # 获取输入的参数
        main_belt_speed = self.main_belt_speed_input.text()
        swing_speed = self.swing_speed_input.text()
        constant_swing_time = self.constant_swing_time_input.text()
        edge_stay_time = self.edge_stay_time_input.text()
        swing_amplitude = self.swing_amplitude_input.text()
        same_grain_moto_count = self.same_grain_moto_count_input.text()
        uniformity_coefficient = self.uniformity_coefficient_input.text()

        # 打印参数（实际应用中可以保存到文件或数据库）
        print("主皮带速度:", main_belt_speed)
        print("摆动速度:", swing_speed)
        print("匀速摆动时间:", constant_swing_time)
        print("边部停留时间:", edge_stay_time)
        print("摆幅:", swing_amplitude)
        print("同粒度磨头数:", same_grain_moto_count)
        print("均匀系数:", uniformity_coefficient)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())