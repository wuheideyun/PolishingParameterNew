'''

验证码窗口

'''
import hashlib
import platform
import random
import sqlite3
import time
import uuid
from tkinter.tix import Form
import datetime
from PySide6.QtCore import Qt, Signal, QSettings
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox, QGridLayout, \
    QSpacerItem, QSizePolicy, QMessageBox, QComboBox
from cryptography.fernet import Fernet


from DatabaseHelper import DatabaseHelper
from FrameLessDialog import FrameLessDialog
from ImageButton import ImageButton
from LoginEdit import LoginEdit
from PopupMessageBox import PopupMessageBox


class CheckCodeDialog(FrameLessDialog):
    def __init__(self):
        super().__init__()
        self.db = DatabaseHelper('database.db')
        self.setWindowTitle("验证码")
        self.setFixedSize(1200, 300)

        self.settings = QSettings("config.ini", QSettings.IniFormat)  # 使用配置文件



        self.setWindowFlag(Qt.FramelessWindowHint)
        self.saved_username = ""
        outHLay = QHBoxLayout()
        outHLay.setContentsMargins(0, 0, 20, 0)

        mainVLay = QVBoxLayout()

        hlay1 = QHBoxLayout()

        self.btnClose = ImageButton(":close16", 16, 16)
        self.btnClose.clicked.connect(self.btn_close)

        hlay1.addStretch()
        hlay1.addWidget(self.btnClose)
        hlay1.setContentsMargins(0, 0, 0, 0)
        mainVLay.addLayout(hlay1)
        # self.btnClose.move(500, 10)

        mainVLay.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed))

        logoLabel = QLabel("")
        logoLabel.setFixedSize(302, 48)

        pixmap = QPixmap(":login_logo2")  # 替换为实际图片路径
        logoLabel.setPixmap(pixmap)

        # 如果需要，可以让图片自适应 QLabel 的大小
        logoLabel.setScaledContents(True)

        hlay2 = QHBoxLayout()
        hlay2.addWidget(logoLabel)
        hlay2.setContentsMargins(0, 0, 0, 0)
        mainVLay.addLayout(hlay2)

        hlay3 = QHBoxLayout()
        mainVLay.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed))
        mainVLay.addLayout(hlay3)
        mainVLay.setContentsMargins(0, 0, 0, 0)
        mainVLay.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed))
        gridLayout = QGridLayout()

        self.activationCodeEdit = LoginEdit(":activation_code")
        self.activationCodeEdit.setPlaceholderText("激活码")
        self.activationCodeEdit.setFixedWidth(1000)
        gridLayout.addWidget(self.activationCodeEdit, 0, 0, 1, 2)  # 第0行，第0列，占1行，占2列

        self.btnCheckCode = QPushButton("验证激活码")
        self.btnCheckCode.setFixedSize(128, 48)

        self.btnCheckCode.clicked.connect(self.OnCheckCode)

        self.btnCheckCode.setStyleSheet("""
                           QPushButton {
                               background-color: #30438c; /* 按钮的默认背景色为绿色 */
                               color: white; /* 设置按钮文字颜色为白色 */
                               border: none; /* 移除边框 */
                               padding: 10px; /* 内边距 */
                               font-size: 18px; /* 文字大小 */
                           }
                           QPushButton:hover {
                               background-color: #40539c; /* 鼠标悬停时按钮的背景色变深 */
                           }
                           QPushButton:pressed {
                               background-color: #7986b5; /* 鼠标按下时按钮的背景色更深 */
                           }
                       """)
        gridLayout.addWidget(self.btnCheckCode, 0, 2, 1, 2)  # 第0行，第0列，占1行，占2列



        self.activation_code_gainEdit = LoginEdit(":activation_code")
        self.activation_code_gainEdit.setPlaceholderText("获取激活码")
        self.activation_code_gainEdit.setFixedWidth(1000)
        gridLayout.addWidget(self.activation_code_gainEdit, 1, 0, 1, 2)  # 第1行，第0列，占1行，占2列
        self.activation_code_gainEdit.setVisible(False)
        self.lang_dic = {
            'TEMP': 60,  # 临时码，1分钟
            '1M': 60,  # 1分钟码
            '1H': 3600,  # 1小时码
            '1D': 86400,  # 1天码
            '1W': 604800,  # 1周码
            '1MO': 2592000,  # 1个月码
            '6MO': 15552000,  # 6个月码
            'PERM': float('inf'),  # 永久码
        }

        lang_keys = list(self.lang_dic.keys())
        self.lang_count = len(lang_keys)
        self.comboBox_src = QComboBox()
        self.comboBox_src.addItems(lang_keys)
        self.comboBox_src.setFixedSize(100, 24)
        self.comboBox_src.setCurrentIndex(1)
        gridLayout.addWidget(self.comboBox_src, 2, 0, 1, 1)  # 第0行，第0列，占1行，占2列
        self.comboBox_src.setVisible(False)

        self.btnGainCode = QPushButton("获取激活码")
        self.btnGainCode.setFixedSize(128, 48)

        self.btnGainCode.clicked.connect(self.OnGainCode)

        self.btnGainCode.setStyleSheet("""
                                   QPushButton {
                                       background-color: #30438c; /* 按钮的默认背景色为绿色 */
                                       color: white; /* 设置按钮文字颜色为白色 */
                                       border: none; /* 移除边框 */
                                       padding: 10px; /* 内边距 */
                                       font-size: 18px; /* 文字大小 */
                                   }
                                   QPushButton:hover {
                                       background-color: #40539c; /* 鼠标悬停时按钮的背景色变深 */
                                   }
                                   QPushButton:pressed {
                                       background-color: #7986b5; /* 鼠标按下时按钮的背景色更深 */
                                   }
                               """)
        gridLayout.addWidget(self.btnGainCode, 2, 1, 1, 2)  # 第0行，第0列，占1行，占2列
        self.btnGainCode.setVisible(False)


        hlay4 = QHBoxLayout()
        hlay4.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        hlay4.addLayout(gridLayout)
        hlay4.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        mainVLay.addLayout(hlay4)

        mainVLay.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed))

        mainVLay.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))


        mainVLay.setContentsMargins(0, 0, 0, 0)
        outHLay.addLayout(mainVLay)

        self.setLayout(outHLay)

        if self.settings.value("activation_status", "") == "True":
            self.activationCodeEdit.setText(self.settings.value("activation_code", ""))

    def btn_close(self):
        self.close()

    def OnCheckCode(self):
        activation_code = self.activationCodeEdit.text()

        is_valid = validate_activation_code_with_device(self,activation_code)
        if is_valid:
            self.settings.setValue("activation_code", activation_code)
            self.settings.setValue("activation_status", "True")
        else:
            self.settings.setValue("activation_status", "False")
            self.settings.setValue("activation_code", '')
        msgbox = PopupMessageBox("提示", f"激活码是否有效:{is_valid}")

        msgbox.setFixedSize(250, 100)
        msgbox.exec()

    def OnGainCode(self):
        activation_code_type = self.comboBox_src.currentText()
        activation_code = generate_activation_code(activation_code_type)
        self.activation_code_gainEdit.setText(activation_code)

    def open_checkcode(self):
        self.exec()

# 校验激活码
def validate_activation_code_with_device(self,code: str) -> bool:
    try:
        fernet = Fernet('lvpWRiS8TmjvizHmWLha18gr75tmQwUMzrB4g1PW3i0 =')
        decrypted_code = fernet.decrypt(code.encode()).decode()
        duration_type, unique_id, checksum = decrypted_code.split('-')
        raw_string = f"{duration_type}-{unique_id}"
        # 重新生成校验位
        expected_checksum = hashlib.sha256(raw_string.encode()).hexdigest()[:6].upper()
        if expected_checksum != checksum:
            return False  # 校验位不匹配

        current_time = int(time.time())  # 当前时间戳

        # 获取当前设备指纹（可以通过硬件信息生成，如前面介绍的 get_device_fingerprint 方法）
        current_device_fingerprint = get_device_fingerprint()

        # 检查激活码是否已绑定设备和是否已经激活过

        if DatabaseHelper.verify_code(self.db,'keys',decrypted_code, current_device_fingerprint):
            device_info = DatabaseHelper.read(self.db,'keys','fingerprint',f'fingerprint=\'{current_device_fingerprint}\'')
            created_at = DatabaseHelper.read(self.db,'keys','created_at',f'fingerprint=\'{current_device_fingerprint}\'')
            if device_info[0] != current_device_fingerprint:
                return False  # 该激活码已绑定到其他设备
            # 检查激活码是否已过期
            duration_map = {
                'TEMP': 60,  # 临时码，1分钟
                '1M': 60,  # 1分钟码
                '1H': 3600,  # 1小时码
                '1D': 86400,  # 1天码
                '1W': 604800,  # 1周码
                '1MO': 2592000,  # 1个月码
                '6MO': 15552000,  # 6个月码
                'PERM': float('inf'),  # 永久码
            }

            valid_duration = duration_map.get(duration_type, 0)
            timeStamp = int(time.mktime(time.strptime(created_at[0],"%Y-%m-%d %H:%M:%S")))
            if current_time > timeStamp  + valid_duration:
                return False  # 激活码已过期
        else:
            DatabaseHelper.insert(self.db, 'keys',{
                'content' : code,
                'key': decrypted_code,
                'fingerprint': current_device_fingerprint,
                'created_at': datetime.datetime.fromtimestamp(current_time)
            })
        return True
    except Exception as e:
        return False  # 解析失败或错误

def get_device_fingerprint() -> str:
    # 获取设备的硬件信息，可以选择使用CPU、硬盘或主板信息
    device_info = platform.node() + platform.system() + platform.processor() + str(uuid.getnode())
    # 生成一个唯一的指纹（哈希值）
    fingerprint = hashlib.sha256(device_info.encode()).hexdigest()
    return fingerprint

# 生成激活码
def generate_activation_code(duration_type: str) -> str:
    unique_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=8))  # 8位唯一标识
    raw_string = f"{duration_type}-{unique_id}"

    # 生成校验位 (使用SHA-256哈希生成前6位)
    checksum = hashlib.sha256(raw_string.encode()).hexdigest()[:6].upper()

    fernet = Fernet('lvpWRiS8TmjvizHmWLha18gr75tmQwUMzrB4g1PW3i0 =')
    oldcode = f"{duration_type}-{unique_id}-{checksum}"
    newcode = fernet.encrypt(oldcode.encode()).decode()
    return newcode
