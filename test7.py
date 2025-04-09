import ctypes.wintypes
import threading
import tkinter as tk
import pystray
from PIL import Image
from pynput import keyboard
from ctypes import *


WM_CLOSE = 0x10
WM_SETTEXT = 0x0c
GWL_STYLE = -16
GWL_EXSTYLE = -20
SW_MINIMIZE = 6
SW_MAXIMIZE = 3
SW_RESTORE = 9
WS_BORDER = 0x800000
WS_CAPTION = 0xC00000 # WS_BORDER Or WS_DLGFRAME
WS_CHILD = 0x40000000
WS_CLIPCHILDREN = 0x2000000
WS_CLIPSIBLINGS = 0x4000000
WS_POPUP = 0x80000000
WS_DLGFRAME = 0x400000
WS_DISABLED = 0x8000000
WS_OVERLAPPEDWINDOW = 0xcf0000
WS_THICKFRAME = 0x40000
WS_VISIBLE = 0x10000000
WS_EX_APPWINDOW = 0x40000
WS_EX_DLGMODALFRAME = 0x1
WS_EX_ACCEPTFILES = 0x10
WS_EX_CLIENTEDGE= 0x200
WS_EX_TOOLWINDOW = 0x80
WS_EX_WINDOWEDGE = 0x100
LWA_ALPHA = 0x2;LWA_COLORKEY=0x1
WS_EX_LAYERED = 0x80000

keys = set()
hwnd = 0    # 窗口句柄

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('窗口透明化工具')
        self.root.geometry("400x90")
        # 当用户点击窗口右上角的关闭按钮时，Tkinter将自动发送WM_DELETE_WINDOW关闭事件。通过对其进行处理并调用self.hide_window()方法，可以改为将窗口隐藏到系统托盘中。
        # 该方法用于将程序窗口隐藏到系统托盘中而非直接退出应用程序
        self.root.protocol('WM_DELETE_WINDOW', self.hide_window)
        # 添加菜单和图标
        self.create_systray_icon()
        # 绘制界面
        frame1 = tk.Frame(self.root)
        frame1.pack(side='top')
        l1 = tk.Label(frame1,
                      text='【窗口透明化操作】点击窗口，按Ctrl + Alt + [0-9]使其透明化。\nCtrl + Alt + 1：全透明\nCtrl + Alt + 5：半透明\nCtrl + Alt + 0：全填充\n')
        l1.pack()
        # 开启键盘监听
        t = threading.Thread(target=self.new_thread_start)
        # 开启守护线程，这样在GUI意外关闭时线程能正常退出
        t.setDaemon(True)
        t.start()


    """
    [1]最小化托盘
    """
    def create_systray_icon(self):
        # 使用 Pystray 创建系统托盘图标
        menu = (
            pystray.MenuItem('显示', self.show_window, default=True),
            pystray.Menu.SEPARATOR,  # 在系统托盘菜单中添加分隔线
            pystray.MenuItem('退出', self.quit_window))
        image = Image.open("TPWin.ico")
        self.icon = pystray.Icon("icon", image, "图标名称", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()

    def hide_window(self):
        # 关闭窗口时隐藏窗口，并将 Pystray 图标放到系统托盘中
        self.root.withdraw()

    def show_window(self):
        # 打开主窗口
        self.icon.visible = True
        self.root.deiconify()

    def quit_window(self, icon: pystray.Icon):
        # 退出程序
        icon.stop()  # 停止 Pystray 的事件循环
        self.root.quit()  # 终止 Tkinter 的事件循环
        self.root.destroy()  # 销毁应用程序的主窗口和所有活动


    """
    [2]键盘操作
    """
    def on_key_press(self, key):
        if key == keyboard.Key.alt_l or key == keyboard.Key.alt_gr:
            keys.add('Alt')
        elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            keys.add('Ctrl')
        elif str(key) == r"<48>":   # ctrl + 0组合键
            keys.add('0')
        elif str(key) == r"<49>":   # ctrl + 1组合键
            keys.add('1')
        elif str(key) == r"<50>":   # ctrl + 2组合键
            keys.add('2')
        elif str(key) == r"<51>":   # ctrl + 3组合键
            keys.add('3')
        elif str(key) == r"<52>":   # ctrl + 4组合键
            keys.add('4')
        elif str(key) == r"<53>":   # ctrl + 5组合键
            keys.add('5')
        elif str(key) == r"<54>":   # ctrl + 6组合键
            keys.add('6')
        elif str(key) == r"<55>":   # ctrl + 7组合键
            keys.add('7')
        elif str(key) == r"<56>":   # ctrl + 8组合键
            keys.add('8')
        elif str(key) == r"<57>":   # ctrl + 9组合键
            keys.add('9')

        if all(k in keys for k in ['Alt', 'Ctrl', '0']):
            self.set_transparency(0)
        elif all(k in keys for k in ['Alt', 'Ctrl', '1']):
            self.set_transparency(1)
        elif all(k in keys for k in ['Alt', 'Ctrl', '2']):
            self.set_transparency(2)
        elif all(k in keys for k in ['Alt', 'Ctrl', '3']):
            self.set_transparency(3)
        elif all(k in keys for k in ['Alt', 'Ctrl', '4']):
            self.set_transparency(4)
        elif all(k in keys for k in ['Alt', 'Ctrl', '5']):
            self.set_transparency(5)
        elif all(k in keys for k in ['Alt', 'Ctrl', '6']):
            self.set_transparency(6)
        elif all(k in keys for k in ['Alt', 'Ctrl', '7']):
            self.set_transparency(7)
        elif all(k in keys for k in ['Alt', 'Ctrl', '8']):
            self.set_transparency(8)
        elif all(k in keys for k in ['Alt', 'Ctrl', '9']):
            self.set_transparency(9)

    def on_key_release(self, key):
        if key == keyboard.Key.alt_l or key == keyboard.Key.alt_gr:
            keys.remove('Alt')
        elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            keys.remove('Ctrl')
        elif str(key) == r"<48>":  # ctrl + 0组合键
            keys.remove('0')
        elif str(key) == r"<49>":  # ctrl + 1组合键
            keys.remove('1')
        elif str(key) == r"<50>":  # ctrl + 2组合键
            keys.remove('2')
        elif str(key) == r"<51>":  # ctrl + 3组合键
            keys.remove('3')
        elif str(key) == r"<52>":  # ctrl + 4组合键
            keys.remove('4')
        elif str(key) == r"<53>":  # ctrl + 5组合键
            keys.remove('5')
        elif str(key) == r"<54>":  # ctrl + 6组合键
            keys.remove('6')
        elif str(key) == r"<55>":  # ctrl + 7组合键
            keys.remove('7')
        elif str(key) == r"<56>":  # ctrl + 8组合键
            keys.remove('8')
        elif str(key) == r"<57>":  # ctrl + 9组合键
            keys.remove('9')
        if key == keyboard.Key.esc:
            return False  # 释放了esc 键，停止监听

    def new_thread_start(self):
        key_listen_thread = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
        # 运行线程
        key_listen_thread.start()

    """
    [3]设置透明度操作（Ctrl + Alt + [0-9]）
    """
    def set_transparency(self, set_tp):
        global hwnd
        hwnd = ctypes.windll.user32.WindowFromPoint(self.get_mouse_position())  # 获取窗口句柄

        p = create_string_buffer(256)
        windll.user32.GetWindowTextW(hwnd, byref(p), 256)  # 获取窗口标题
        title = str(p.raw, encoding='utf-16').strip('\x00')

        exstyle = windll.user32.GetWindowLongA(hwnd, GWL_EXSTYLE)
        exstyle |= WS_EX_LAYERED  # 使窗口具有能设置透明度的样式
        windll.user32.SetWindowLongA(hwnd, GWL_EXSTYLE, exstyle)    # 获取窗口名
        if set_tp == 0:
            alpha = 255
        else:
            alpha = set_tp * 25
        windll.user32.SetLayeredWindowAttributes(hwnd, 0, alpha, LWA_ALPHA) # 设置透明度
        print('窗口 ' + title + ' 透明度设置为 ' + str(set_tp) + '\n')


    def get_mouse_position(self):
        point = ctypes.wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
        return point




if __name__ == '__main__':
    # 主界面
    TKDemo = GUI()
    TKDemo.root.mainloop()



