import time
from PySide6.QtCore import QThread, Signal
from omron_plc_gui import PLCCommunicator

class ConnectionWorker(QThread):
    """
    在一个独立的线程中执行单个PLC的连接/断开操作，以避免UI卡顿。
    """
    # 信号定义：(行号, 是否成功, 结果)
    connection_finished = Signal(int, bool, object)
    disconnection_finished = Signal(int, bool, str)

    def __init__(self, row, ip, port, plc_instance=None, action='connect', parent=None):
        super().__init__(parent)
        self.row = row
        self.ip = ip
        self.port = port # 端口号暂时备用
        self.plc_instance = plc_instance
        self.action = action

    def run(self):
        if self.action == 'connect':
            try:
                plc = PLCCommunicator()
                plc.connect(self.ip)
                time.sleep(0.5) # 模拟网络延迟
                self.connection_finished.emit(self.row, True, plc)
            except Exception as e:
                self.connection_finished.emit(self.row, False, str(e))
        elif self.action == 'disconnect':
            try:
                if self.plc_instance:
                    self.plc_instance.disconnect()
                self.disconnection_finished.emit(self.row, True, "已断开")
            except Exception as e:
                self.disconnection_finished.emit(self.row, False, str(e))