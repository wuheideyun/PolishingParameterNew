import tkinter as tk
from tkinter import messagebox
import time
from aphyt import omron
import sys
import struct

# 临时增加递归深度限制（仅用于调试）
sys.setrecursionlimit(1500)


class PLCCommunicator:
    def __init__(self):
        self.eip_conn = None
        self.connected = False

    def connect(self, ip_address):
        """连接到PLC"""
        if not ip_address:
            raise ValueError("请输入PLC IP地址")
        try:
            self.eip_conn = omron.NSeries(ip_address)
            self.connected = True
            return True
        except Exception as e:
            self.eip_conn = None
            self.connected = False
            raise Exception(f"连接失败: {str(e)}")

    def disconnect(self):
        """断开PLC连接"""
        if self.eip_conn:
            try:
                self.eip_conn = None  # 依赖NSeries内部机制释放连接
                self.connected = False
                return True
            except Exception as e:
                raise Exception(f"断开连接失败: {str(e)}")
        return True

    def is_connected(self):
        """检查连接状态"""
        return self.connected

    def read_bool(self, address, length=1):
        """读取布尔值"""
        if not self.eip_conn or not self.connected:
            raise Exception("未连接到PLC")
        try:
            value = self.eip_conn.read_variable(address)
            if length == 1:
                return [bool(value)]
            return [bool(value[i]) for i in range(length)]
        except Exception as e:
            raise Exception(f"读取布尔值失败: {str(e)}")

    def read_short(self, address, length=1):
        """读取16位短整数"""
        if not self.eip_conn or not self.connected:
            raise Exception("未连接到PLC")
        try:
            value = self.eip_conn.read_variable(address)
            if length == 1:
                return [int(value)]
            return [int(value[i]) for i in range(length)]
        except Exception as e:
            raise Exception(f"读取短整数失败: {str(e)}")

    def read_int(self, address, length=1):
        """读取32位整数"""
        if not self.eip_conn or not self.connected:
            raise Exception("未连接到PLC")
        try:
            value = self.eip_conn.read_variable(address)
            if length == 1:
                return [int(value)]
            return [int(value[i]) for i in range(length)]
        except Exception as e:
            raise Exception(f"读取整数失败: {str(e)}")

    def read_long(self, address, length=1):
        """读取长整数（32位无符号整数）"""
        if not self.eip_conn or not self.connected:
            raise Exception("未连接到PLC")
        try:
            value = self.eip_conn.read_variable(address)
            if length == 1:
                return [int(value)]
            return [int(value[i]) for i in range(length)]
        except Exception as e:
            raise Exception(f"读取长整数失败: {str(e)}")

    def read_float(self, address, length=1):
        """读取32位浮点数"""
        if not self.eip_conn or not self.connected:
            raise Exception("未连接到PLC")
        try:
            value = self.eip_conn.read_variable(address)
            if length == 1:
                return [float(value)]
            return [float(value[i]) for i in range(length)]
        except Exception as e:
            raise Exception(f"读取浮点数失败: {str(e)}")

    def write_bool(self, address, values):
        """写入布尔值"""
        if not self.eip_conn or not self.connected:
            raise Exception("未连接到PLC")
        try:
            if isinstance(values, list):
                for i, value in enumerate(values):
                    self.eip_conn.write_variable(f"{address}{i if i > 0 else ''}", bool(value))
            else:
                self.eip_conn.write_variable(address, bool(values))
            return True
        except Exception as e:
            raise Exception(f"写入布尔值失败: {str(e)}")

    def write_short(self, address, values):
        """写入16位短整数"""
        if not self.eip_conn or not self.connected:
            raise Exception("未连接到PLC")
        try:
            if isinstance(values, list):
                for i, value in enumerate(values):
                    self.eip_conn.write_variable(f"{address}{i if i > 0 else ''}", int(value))
            else:
                self.eip_conn.write_variable(address, int(values))
            return True
        except Exception as e:
            raise Exception(f"写入短整数失败: {str(e)}")

    def write_int(self, address, values):
        """写入32位整数"""
        if not self.eip_conn or not self.connected:
            raise Exception("未连接到PLC")
        try:
            if isinstance(values, list):
                for i, value in enumerate(values):
                    self.eip_conn.write_variable(f"{address}{i if i > 0 else ''}", int(value))
            else:
                self.eip_conn.write_variable(address, int(values))
            return True
        except Exception as e:
            raise Exception(f"写入整数失败: {str(e)}")

    def write_long(self, address, values):
        """写入长整数（32位无符号整数）"""
        if not self.eip_conn or not self.connected:
            raise Exception("未连接到PLC")
        try:
            if isinstance(values, list):
                for i, value in enumerate(values):
                    self.eip_conn.write_variable(f"{address}{i if i > 0 else ''}", int(value))
            else:
                self.eip_conn.write_variable(address, int(values))
            return True
        except Exception as e:
            raise Exception(f"写入长整数失败: {str(e)}")

    def write_float(self, address, values):
        """写入32位浮点数"""
        if not self.eip_conn or not self.connected:
            raise Exception("未连接到PLC")
        try:
            if isinstance(values, list):
                for i, value in enumerate(values):
                    self.eip_conn.write_variable(f"{address}{i if i > 0 else ''}", float(value))
            else:
                self.eip_conn.write_variable(address, float(values))
            return True
        except Exception as e:
            raise Exception(f"写入浮点数失败: {str(e)}")


class PLCInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("欧姆龙PLC通讯")
        self.communicator = PLCCommunicator()

        # GUI布局
        # IP地址框架
        self.ip_frame = tk.Frame(root)
        self.ip_frame.pack(pady=10)

        tk.Label(self.ip_frame, text="PLC IP地址:").pack(side=tk.LEFT)
        self.ip_entry = tk.Entry(self.ip_frame, width=20)
        self.ip_entry.insert(0, "192.168.2.1")
        self.ip_entry.pack(side=tk.LEFT, padx=5)

        # 连接/断开按钮
        self.connect_button = tk.Button(self.ip_frame, text="连接", command=self.connect_plc)
        self.connect_button.pack(side=tk.LEFT, padx=5)
        self.disconnect_button = tk.Button(self.ip_frame, text="断开", command=self.disconnect_plc, state=tk.DISABLED)
        self.disconnect_button.pack(side=tk.LEFT, padx=5)

        # 变量名框架
        self.var_frame = tk.Frame(root)
        self.var_frame.pack(pady=10)

        tk.Label(self.var_frame, text="变量名:").pack(side=tk.LEFT)
        self.var_entry = tk.Entry(self.var_frame, width=30)
        self.var_entry.insert(0, "横梁1未回零标志位")
        self.var_entry.pack(side=tk.LEFT, padx=5)

        # 写入值框架
        self.value_frame = tk.Frame(root)
        self.value_frame.pack(pady=10)

        tk.Label(self.value_frame, text="写入值:").pack(side=tk.LEFT)
        self.value_entry = tk.Entry(self.value_frame, width=20)
        self.value_entry.insert(0, "True")
        self.value_entry.pack(side=tk.LEFT, padx=5)

        # 操作按钮
        self.action_frame = tk.Frame(root)
        self.action_frame.pack(pady=10)

        self.query_button = tk.Button(self.action_frame, text="查询", command=self.query_variable, state=tk.DISABLED)
        self.query_button.pack(side=tk.LEFT, padx=5)
        self.write_button = tk.Button(self.action_frame, text="写入", command=self.write_variable, state=tk.DISABLED)
        self.write_button.pack(side=tk.LEFT, padx=5)

        # 显示框架
        self.display_frame = tk.Frame(root)
        self.display_frame.pack(pady=10)

        tk.Label(self.display_frame, text="读取值:").pack(side=tk.LEFT)
        self.display_var = tk.StringVar()
        self.display_label = tk.Label(self.display_frame, textvariable=self.display_var, width=30, relief=tk.SUNKEN)
        self.display_label.pack(side=tk.LEFT, padx=5)

    def connect_plc(self):
        ip_address = self.ip_entry.get()
        try:
            self.communicator.connect(ip_address)
            # messagebox.showinfo("成功", f"已连接到PLC: {ip_address}")
            self.connect_button.config(state=tk.DISABLED)
            self.disconnect_button.config(state=tk.NORMAL)
            self.query_button.config(state=tk.NORMAL)
            self.write_button.config(state=tk.NORMAL)
            self.ip_entry.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def disconnect_plc(self):
        try:
            self.communicator.disconnect()
            # messagebox.showinfo("成功", "已断开PLC连接")
            self.connect_button.config(state=tk.NORMAL)
            self.disconnect_button.config(state=tk.DISABLED)
            self.query_button.config(state=tk.DISABLED)
            self.write_button.config(state=tk.DISABLED)
            self.ip_entry.config(state=tk.NORMAL)
            self.display_var.set("")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def query_variable(self):
        variable_name = self.var_entry.get()
        if not variable_name:
            messagebox.showerror("错误", "请输入变量名")
            return

        try:
            value = self.communicator.read_short(variable_name)[0]  # 默认读取布尔值
            self.display_var.set(str(value))
        except Exception as e:
            messagebox.showerror("错误", str(e))
            self.display_var.set("")

    def write_variable(self):
        variable_name = self.var_entry.get()
        write_value = self.value_entry.get()

        if not variable_name:
            messagebox.showerror("错误", "请输入变量名")
            return

        try:
            if write_value.lower() == "true":
                write_value = True
            elif write_value.lower() == "false":
                write_value = False
            else:
                write_value = float(write_value) if '.' in write_value else int(write_value)

            if isinstance(write_value, bool):
                self.communicator.write_bool(variable_name, write_value)
            elif isinstance(write_value, int):
                self.communicator.write_int(variable_name, write_value)
            else:
                self.communicator.write_float(variable_name, write_value)

            messagebox.showinfo("成功", f"已写入 {write_value} 到 {variable_name}")

            time.sleep(0.5)
            value = self.communicator.read_bool(variable_name)[0]  # 默认验证布尔值
            self.display_var.set(str(value))
        except Exception as e:
            messagebox.showerror("错误", str(e))
            self.display_var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = PLCInterface(root)
    root.mainloop()