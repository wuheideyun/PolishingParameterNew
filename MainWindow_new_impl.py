from MainWindow_New_Interface import MainWindow
from PySide6.QtGui import QMovie
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import colorbar
from mpl_toolkits.axes_grid1 import make_axes_locatable
import multiprocessing
from matplotlib.patches import Rectangle  # 导入 Rectangle
from functools import partial
# 函数导入
from Double_Function import DoubleWorkerThread,double_num_calculate,self_define_calculate
from Single_Function import SingleWorkerThread,single_num_calculate,single_self_define_calculate
class MainWindow_impl(MainWindow):
    def __init__(self):
        super().__init__()
        # 单头摆-参数汇总
        self.single_parameter_intelligent = {}  # 字典-用于储存输入参数
        self.single_parameter_manual = {}  # 字典-用于储存输出参数（包括输入参数）

        # 双头摆-参数汇总
        self.double_parameter_intelligent = {}  # 字典-用于储存输入参数
        self.double_parameter_manual = {}  # 字典-用于储存输出参数（包括输入参数）

        # 同步摆-参数汇总
        equal_parameter_intelligent = {}  # 字典-用于储存输入参数
        equal_parameter_manual = {}  # 字典-用于储存输出参数（包括输入参数）

        # 主机参数-双头摆- self.host_param_double_frame
        host_param_double_line_edit_names = [
            "lineEdit_between", "lineEdit_beam_between", "lineEdit_diameter", "lineEdit_grind_length"
        ]
        for i in host_param_double_line_edit_names:
            self.double_parameter_intelligent[i] = self.host_param_double_frame.content_layout.get_line_edit_value(i)
            self.double_parameter_manual[i] = self.host_param_double_frame.content_layout.get_line_edit_value(i)
        # 监听参数变更信息，并更新到数据集中
        self.host_param_double_frame.content_layout.textChanged.connect(
            partial(self.line_eidt_textchange, list=self.double_parameter_intelligent))
        self.host_param_double_frame.content_layout.textChanged.connect(
            partial(self.line_eidt_textchange, list=self.double_parameter_manual))

        # 主机参数-单头摆- self.host_param_single_frame
        host_param_single_line_edit_names = [
            "lineEdit_beam_between", "lineEdit_diameter", "lineEdit_grind_length"
        ]
        for i in host_param_single_line_edit_names:
            self.single_parameter_intelligent[i] = self.host_param_single_frame.content_layout.get_line_edit_value(i)
            self.single_parameter_manual[i] = self.host_param_single_frame.content_layout.get_line_edit_value(i)
        # 监听参数变更信息，并更新到数据集中
        self.host_param_single_frame.content_layout.textChanged.connect(
            partial(self.line_eidt_textchange, list=self.single_parameter_intelligent))
        self.host_param_single_frame.content_layout.textChanged.connect(
            partial(self.line_eidt_textchange, list=self.single_parameter_manual))

        # 运动输入参数- self.motion_in_param_frame
        motion_in_param_line_edit_names = [
            "lineEdit_production_volume", "lineEdit_ceramic_width", "lineEdit_accelerate", "lineEdit_overlap",
            "lineEdit_num_input"
            , "lineEdit_group_count", "lineEdit_stay_time_input"
        ]
        for i in motion_in_param_line_edit_names:
            self.single_parameter_intelligent[i] = self.motion_in_param_frame.content_layout.get_line_edit_value(i)
            self.double_parameter_intelligent[i] = self.motion_in_param_frame.content_layout.get_line_edit_value(i)
        # 监听参数变更信息，并更新到数据集中
        self.motion_in_param_frame.content_layout.textChanged.connect(
            partial(self.line_eidt_textchange, list=self.single_parameter_intelligent))
        self.motion_in_param_frame.content_layout.textChanged.connect(
            partial(self.line_eidt_textchange, list=self.double_parameter_intelligent))

        # 运动输出参数 and 产品质量参数- self.motion_out_param_frame
        motion_out_param_line_edit_names = [
            "lineEdit_belt_speed", "lineEdit_beam_swing_speed", "lineEdit_beam_constant_time",
            "lineEdit_stay_time_output", "lineEdit_swing", "lineEdit_num_output"
        ]
        motion_out_param_line_edit_names_2 = [
            "lineEdit_coefficient"
        ]
        for i in motion_out_param_line_edit_names:
            self.single_parameter_intelligent[i] = self.motion_out_param_frame.content_up_layout.get_line_edit_value(i)
            self.double_parameter_intelligent[i] = self.motion_out_param_frame.content_up_layout.get_line_edit_value(i)
        for i in motion_out_param_line_edit_names_2:
            self.single_parameter_intelligent[i] = self.motion_out_param_frame.content_down_layout.get_line_edit_value(i)
            self.double_parameter_intelligent[i] = self.motion_out_param_frame.content_down_layout.get_line_edit_value(i)
        # 监听参数变更信息，并更新到数据集中
        self.motion_out_param_frame.content_up_layout.textChanged.connect(
            partial(self.line_eidt_textchange, list=self.single_parameter_intelligent))
        self.motion_out_param_frame.content_up_layout.textChanged.connect(
            partial(self.line_eidt_textchange, list=self.double_parameter_intelligent))

        self.motion_out_param_frame.content_down_layout.textChanged.connect(
            partial(self.line_eidt_textchange, list=self.single_parameter_intelligent))
        self.motion_out_param_frame.content_down_layout.textChanged.connect(
            partial(self.line_eidt_textchange, list=self.double_parameter_intelligent))

        # 运动参数-人工寻优界面--运动输入参数 and 运动输出参数 and 产品质量参数- self.motion_input_out_param_manual_frame
        motion_out_param_param_manual__line_edit_names = [
            "lineEdit_production_volume", "lineEdit_beam_swing_speed", "lineEdit_beam_constant_time",
            "lineEdit_stay_time_input", "lineEdit_num_input", "lineEdit_accelerate", "lineEdit_ceramic_width",
            "lineEdit_delay_time"
        ]
        # 运动输出参数
        motion_out_param_param_manual__line_edit_names_2 = [
            "lineEdit_belt_speed", "lineEdit_swing"
        ]
        # 产品质量参数
        motion_out_param_param_manual__line_edit_names_3 = ["lineEdit_coefficient"]
        for i in motion_out_param_param_manual__line_edit_names:
            self.single_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_up_layout.get_line_edit_value(
                i)
            self.double_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_up_layout.get_line_edit_value(
                i)
        for i in motion_out_param_param_manual__line_edit_names_2:
            self.single_parameter_manual[
                i] = self.motion_input_out_param_manual_frame.content_middle_layout.get_line_edit_value(i)
            self.double_parameter_manual[
                i] = self.motion_input_out_param_manual_frame.content_middle_layout.get_line_edit_value(i)
        for i in motion_out_param_param_manual__line_edit_names_3:
            self.single_parameter_manual[
                i] = self.motion_input_out_param_manual_frame.content_bottom_layout.get_line_edit_value(i)
            self.double_parameter_manual[
                i] = self.motion_input_out_param_manual_frame.content_bottom_layout.get_line_edit_value(i)
        # 监听参数变更信息，并更新到数据集中
        self.motion_input_out_param_manual_frame.content_up_layout.textChanged.connect(
            partial(self.line_eidt_textchange, list=self.single_parameter_manual))
        self.motion_input_out_param_manual_frame.content_up_layout.textChanged.connect(
            partial(self.line_eidt_textchange, list=self.double_parameter_manual))
        self.motion_input_out_param_manual_frame.content_middle_layout.textChanged.connect(
            partial(self.line_eidt_textchange, list=self.single_parameter_manual))
        self.motion_input_out_param_manual_frame.content_middle_layout.textChanged.connect(
            partial(self.line_eidt_textchange, list=self.double_parameter_manual))
        self.motion_input_out_param_manual_frame.content_bottom_layout.textChanged.connect(
            partial(self.line_eidt_textchange, list=self.single_parameter_manual))
        self.motion_input_out_param_manual_frame.content_bottom_layout.textChanged.connect(
            partial(self.line_eidt_textchange, list=self.double_parameter_manual))

        print(self.single_parameter_manual)


        # -------------------------按钮逻辑部分---------------------
        self.button_energy_project.clicked.connect(self.enerage_project_clicked)
        self.button_efficient_project.clicked.connect(self.efficient_project_clicked)
        self.button_selfdefine_project.clicked.connect(self.self_define_project_clicked)

        self.button_synchronization_mode.clicked.connect(self.syn_project)
        self.button_cross_mode.clicked.connect(self.cross_project)
        self.button_order_mode.clicked.connect(self.order_project)
        # 界面所有编辑框收集
        # self.lineEdit_beam_between.setText(600)
        self.button_list=[self.button_energy_project,self.button_efficient_project,self.button_selfdefine_project
                     ,self.button_synchronization_mode,self.button_cross_mode,self.button_order_mode]

    # 按钮点击槽函数(计算)
    def enerage_project_clicked(self):
        # 按钮不可用
        self.button_disable(self.button_list)
        # 字符类型转换
        single_parameter_intelligent = self.dict_value_float(self.single_parameter_intelligent)
        double_parameter_intelligent = self.dict_value_float(self.double_parameter_intelligent)
        if self.current_mode == 1:     # 单头摆
            self.single_enerage_project(animation_name='111',**single_parameter_intelligent)
        elif self.current_mode == 2:   # 双头摆
            self.double_enerage_project(animation_name='111',**double_parameter_intelligent)
        elif self.current_mode == 3:   # 同步摆
            # 待开发---
            return

    def efficient_project_clicked(self):
        # 按钮不可用
        self.button_disable(self.button_list)
        # 字符类型转换
        single_parameter_intelligent = self.dict_value_float(self.single_parameter_intelligent)
        double_parameter_intelligent = self.dict_value_float(self.double_parameter_intelligent)
        if self.current_mode == 1:
            self.single_efficient_project(animation_name='111',**single_parameter_intelligent)
        elif self.current_mode == 2:
            self.double_efficient_project(animation_name='111',**double_parameter_intelligent)
        elif self.current_mode == 3:
            # 待开发---
            return

    def self_define_project_clicked(self):
        self.button_disable(self.button_list)
        # 字符类型转换
        single_parameter_intelligent = self.dict_value_float(self.single_parameter_intelligent)
        double_parameter_intelligent = self.dict_value_float(self.double_parameter_intelligent)
        if self.current_mode == 1:
            self.single_self_project(animation_name='111',**single_parameter_intelligent)
        elif self.current_mode == 2:
            self.double_self_project(animation_name='111',**double_parameter_intelligent)
        elif self.current_mode == 3:
            # 待开发---
            return

    # 按钮点击槽函数(仿真)
    def syn_project(self):
        self.button_disable(self.button_list)
        # 字符类型转换
        single_parameter_manual = self.dict_value_float(self.single_parameter_manual)
        double_parameter_manual = self.dict_value_float(self.double_parameter_manual)
        if self.current_mode == 1:
            self.single_synchronization_project(animation_name='111',**single_parameter_manual)
        elif self.current_mode == 2:
            self.double_synchronization_project(animation_name='111',**double_parameter_manual)
        elif self.current_mode == 3:
            # 待开发---
            return

    def cross_project(self):
        self.button_disable(self.button_list)
        # 字符类型转换
        single_parameter_manual = self.dict_value_float(self.single_parameter_manual)
        double_parameter_manual = self.dict_value_float(self.double_parameter_manual)
        if self.current_mode == 1:
            self.single_cross_project(animation_name='111',**single_parameter_manual)
        elif self.current_mode == 2:
            self.double_cross_project(animation_name='111',**double_parameter_manual)
        elif self.current_mode == 3:
            # 待开发---
            return

    def order_project(self):
        self.button_disable(self.button_list)
        # 字符类型转换
        single_parameter_manual = self.dict_value_float(self.single_parameter_manual)
        double_parameter_manual = self.dict_value_float(self.double_parameter_manual)
        if self.current_mode == 1:
            self.single_order_project(animation_name='111',**single_parameter_manual)
        elif self.current_mode == 2:
            self.double_order_project(animation_name='111',**double_parameter_manual)
        elif self.current_mode == 3:
            # 待开发---
            return

    # -------------------------单头摆-智能计算逻辑函数---------------------------------
    def single_enerage_project(self,animation_name,**kwargs):
        v1 = kwargs.get('lineEdit_belt_speed')
        ceramic_width = kwargs.get('lineEdit_ceramic_width')
        beam_between = kwargs.get('lineEdit_beam_between')
        R = kwargs.get('lineEdit_diameter')/2
        a = kwargs.get('lineEdit_accelerate')
        mo = kwargs.get('lineEdit_grind_length')
        # 绘图、动画模块子线程
        params = single_num_calculate(v1,ceramic_width,beam_between,R,a,mo,mode='enerage')
        # 计算结果-数据集更新
        self.single_parameter_intelligent.update(params)

        params.update({'mode': 'order', 'fig': self.canvas.fig})
        self.worker_thread_plot = SingleWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.single_intelligent_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程

    def single_efficient_project(self,animation_name,**kwargs):
        # 参数赋值
        v1 = kwargs.get('lineEdit_belt_speed')
        ceramic_width = kwargs.get('lineEdit_ceramic_width')
        beam_between = kwargs.get('lineEdit_beam_between')
        R = kwargs.get('lineEdit_diameter')/2
        a = kwargs.get('lineEdit_accelerate')
        mo = kwargs.get('lineEdit_grind_length')
        # 绘图、动画模块子线程
        params = single_num_calculate(v1, ceramic_width, beam_between, R, a, mo, mode='efficient')
        # 计算结果-数据集更新
        self.single_parameter_intelligent.update(params)

        params.update({'mode': 'order', 'fig': self.canvas.fig})
        self.worker_thread_plot = SingleWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.single_intelligent_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程

    def single_self_project(self,animation_name,**kwargs):
        v1 = kwargs.get('lineEdit_belt_speed')
        ceramic_width = kwargs.get('lineEdit_ceramic_width')
        beam_between = kwargs.get('lineEdit_beam_between')
        R = kwargs.get('lineEdit_diameter')/2
        a = kwargs.get('lineEdit_accelerate')
        num_input = kwargs.get('lineEdit_num_input')
        group = kwargs.get('lineEdit_group_count')
        stay_time = kwargs.get('lineEdit_stay_time_input')
        mo = kwargs.get('lineEdit_grind_length')

        # 绘图、动画模块子线程
        params = single_self_define_calculate(v1, ceramic_width, beam_between, R, a,num_input,group,stay_time,mo, mode='self_order')
        # 计算结果-数据集更新
        self.single_parameter_intelligent.update(params)

        params.update({'mode': 'self_order', 'fig': self.canvas.fig})
        self.worker_thread_plot = SingleWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.single_intelligent_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程

    # -------------------------单头摆-人工寻优逻辑函数--------------------------------
    def single_synchronization_project(self,animation_name,**kwargs):
        v1 = kwargs.get('lineEdit_belt_speed')
        v2 = kwargs.get('lineEdit_beam_swing_speed')
        constant_time = kwargs.get('lineEdit_beam_constant_time')
        stay_time = kwargs.get('lineEdit_stay_time_input')
        a = kwargs.get('lineEdit_accelerate')
        beam_between = kwargs.get('lineEdit_beam_between')
        mo = kwargs.get('lineEdit_grind_length')
        num = kwargs.get('lineEdit_num_input')
        R = kwargs.get('lineEdit_diameter')/2
        ceramic_width = kwargs.get('lineEdit_ceramic_width')
        params = {
            'mode': 'equal',
            'fig': self.canvas.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_input': stay_time,
            'lineEdit_accelerate': a,
            #'between': between,
            'lineEdit_beam_between': beam_between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_input': num,
            'lineEdit_diameter': R,
            'animation_name': animation_name,
            'lineEdit_ceramic_width': ceramic_width,
            # 顺序摆参数
            # 'delay_time': delay_time,
            # 自定义计算参数
            # 'group': group,
        }
        self.worker_thread_plot = SingleWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.single_manual_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程

    def single_cross_project(self,animation_name,**kwargs):
        v1 = kwargs.get('lineEdit_belt_speed')
        v2 = kwargs.get('lineEdit_beam_swing_speed')
        constant_time = kwargs.get('lineEdit_beam_constant_time')
        stay_time = kwargs.get('lineEdit_stay_time_input')
        a = kwargs.get('lineEdit_accelerate')
        beam_between = kwargs.get('lineEdit_beam_between')
        mo = kwargs.get('lineEdit_grind_length')
        num = kwargs.get('lineEdit_num_input')
        R = kwargs.get('lineEdit_diameter')/2
        ceramic_width = kwargs.get('lineEdit_ceramic_width')
        params = {
            'mode': 'cross',
            'fig': self.canvas.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_input': stay_time,
            'lineEdit_accelerate': a,
            # 'between': between,
            'lineEdit_beam_between': beam_between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_input': num,
            'R': R,
            'animation_name': animation_name,
            'lineEdit_ceramic_width': ceramic_width,
            # 顺序摆参数
            # 'delay_time': delay_time,
            # 自定义计算参数
            # 'group': group,
        }
        self.worker_thread_plot = SingleWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.single_manual_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程

    def single_order_project(self,animation_name,**kwargs):
        v1 = kwargs.get('lineEdit_belt_speed')
        v2 = kwargs.get('lineEdit_beam_swing_speed')
        constant_time = kwargs.get('lineEdit_beam_constant_time')
        stay_time = kwargs.get('lineEdit_stay_time_input')
        a = kwargs.get('lineEdit_accelerate')
        beam_between = kwargs.get('lineEdit_beam_between')
        mo = kwargs.get('lineEdit_grind_length')
        num = kwargs.get('lineEdit_num_input')
        R = kwargs.get('lineEdit_diameter')/2
        ceramic_width = kwargs.get('lineEdit_ceramic_width')
        delay_time = kwargs.get('lineEdit_delay_time')

        params = {
            'mode': 'order',
            'fig': self.canvas.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_input': stay_time,
            'lineEdit_accelerate': a,
            #'between': between,
            'lineEdit_beam_between': beam_between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_input': num,
            'R': R,
            'animation_name': animation_name,
            'lineEdit_ceramic_width': ceramic_width,
            # 顺序摆参数
            'lineEdit_delay_time': delay_time,
            # 自定义计算参数
            # 'group': group,
        }

        self.worker_thread_plot = SingleWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.single_manual_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程

#--------------------------------------双头摆智能计算------------------------------------------------------------------------------
    # 双头摆-节能计算-子进程启动函数
    def double_enerage_project(self,animation_name,**kwargs):
        # 绘图、动画模块子线程
        v1 = kwargs.get('lineEdit_belt_speed')
        ceramic_width = kwargs.get('lineEdit_ceramic_width')
        between = kwargs.get('lineEdit_between')
        beam_between = kwargs.get('lineEdit_beam_between')
        R = kwargs.get('lineEdit_diameter')/2
        a = kwargs.get('lineEdit_accelerate')
        mo = kwargs.get('lineEdit_grind_length')

        params = double_num_calculate(v1,ceramic_width,between,beam_between,R,a,mo,mode = 'enerage')
        # 计算结果-数据集更新
        self.double_parameter_intelligent.update(params)

        params.update({'mode': 'order','fig': self.canvas.fig})
        self.worker_thread_plot = DoubleWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.double_intelligent_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程

    # 双头摆-高效计算-子进程启动函数
    def double_efficient_project(self,animation_name,**kwargs):
        v1 = kwargs.get('lineEdit_belt_speed')
        ceramic_width = kwargs.get('lineEdit_ceramic_width')
        between = kwargs.get('lineEdit_between')
        beam_between = kwargs.get('lineEdit_beam_between')
        R = kwargs.get('lineEdit_diameter')/2
        a = kwargs.get('lineEdit_accelerate')
        mo = kwargs.get('lineEdit_grind_length')
        # 参数计算
        params = double_num_calculate(v1, ceramic_width, between, beam_between, R, a, mo, mode='efficient')
        # 计算结果-数据集更新
        self.double_parameter_intelligent.update(params)

        params.update({'mode': 'order', 'fig': self.canvas.fig})
        self.worker_thread_plot = DoubleWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.double_intelligent_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程

    # 双头摆-自定义修正计算-子进程启动函数
    def double_self_project(self,animation_name,**kwargs):
        v1 = kwargs.get('lineEdit_belt_speed')
        t2 = kwargs.get('lineEdit_stay_time_input')
        ceramic_width = kwargs.get('lineEdit_ceramic_width')
        between = kwargs.get('lineEdit_between')
        beam_between = kwargs.get('lineEdit_beam_between')
        R = kwargs.get('lineEdit_diameter')/2
        a = kwargs.get('lineEdit_accelerate')
        num_input = kwargs.get('lineEdit_num_input')
        group = kwargs.get('lineEdit_group_count')
        mo = kwargs.get('lineEdit_grind_length')
        # 参数计算
        params = self_define_calculate(v1,t2,ceramic_width,between,beam_between,R,a,num_input,mo,group)
        # 计算结果-数据集更新
        self.double_parameter_intelligent.update(params)
        params.update({'mode': 'self_order', 'fig': self.canvas.fig})
        self.worker_thread_plot = DoubleWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.double_intelligent_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程

    # ------------------------------------双头摆人工寻优------------------------------------------------------------------------------
    # 双头摆-同步摆模式-子进程启动函数
    def double_synchronization_project(self,animation_name,**kwargs):
        v1 = kwargs.get('lineEdit_belt_speed')
        v2 = kwargs.get('lineEdit_beam_swing_speed')
        constant_time = kwargs.get('lineEdit_beam_constant_time')
        stay_time = kwargs.get('lineEdit_stay_time_input')
        a = kwargs.get('lineEdit_accelerate')
        between = kwargs.get('lineEdit_between')
        beam_between = kwargs.get('lineEdit_beam_between')
        num = kwargs.get('lineEdit_num_input')
        R = kwargs.get('lineEdit_diameter')/2
        mo = kwargs.get('lineEdit_grind_length')
        ceramic_width = kwargs.get('lineEdit_ceramic_width')

        params = {
            'mode': 'equal',
            'fig': self.canvas.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_input': stay_time,
            'lineEdit_accelerate': a,
            'lineEdit_between': between,
            'lineEdit_beam_between': beam_between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_input': num,
            'R': R,
            'animation_name': animation_name,
            'lineEdit_ceramic_width':ceramic_width,
            # 顺序摆参数
            #'delay_time': delay_time,
            # 自定义计算参数
            #'group': group,
        }
        self.worker_thread_plot = DoubleWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.double_manual_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程

    # 双头摆-交叉摆模式-子进程启动函数
    def double_cross_project(self,animation_name,**kwargs):
        v1 = kwargs.get('lineEdit_belt_speed')
        v2 = kwargs.get('lineEdit_beam_swing_speed')
        constant_time = kwargs.get('lineEdit_beam_constant_time')
        stay_time = kwargs.get('lineEdit_stay_time_input')
        a = kwargs.get('lineEdit_accelerate')
        between = kwargs.get('lineEdit_between')
        beam_between = kwargs.get('lineEdit_beam_between')
        mo = kwargs.get('lineEdit_grind_length')
        ceramic_width = kwargs.get('lineEdit_ceramic_width')
        num = kwargs.get('lineEdit_num_input')
        R = kwargs.get('lineEdit_diameter')/2

        params = {
            'mode': 'cross',
            'fig': self.canvas.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_input': stay_time,
            'lineEdit_accelerate': a,
            'lineEdit_between': between,
            'lineEdit_beam_between': beam_between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_input': num,
            'R': R,
            'animation_name': animation_name,
            'lineEdit_ceramic_width': ceramic_width,
            # 顺序摆参数
            # 'delay_time': delay_time,
            # 自定义计算参数
            # 'group': group,
        }

        self.worker_thread_plot = DoubleWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.double_manual_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程

    # 双头摆-顺序摆模式-子进程启动函数
    def double_order_project(self,animation_name,**kwargs):
        v1 = kwargs.get('lineEdit_belt_speed')
        v2 = kwargs.get('lineEdit_beam_swing_speed')
        constant_time = kwargs.get('lineEdit_beam_constant_time')
        stay_time = kwargs.get('lineEdit_stay_time_input')
        a = kwargs.get('lineEdit_accelerate')
        between = kwargs.get('lineEdit_between')
        beam_between = kwargs.get('lineEdit_beam_between')
        mo = kwargs.get('lineEdit_grind_length')
        num = kwargs.get('lineEdit_num_input')
        R = kwargs.get('lineEdit_diameter')/2
        ceramic_width = kwargs.get('lineEdit_ceramic_width')
        delay_time = kwargs.get('lineEdit_delay_time')

        params = {
            'mode': 'order',
            'fig': self.canvas.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_input': stay_time,
            'lineEdit_accelerate': a,
            'lineEdit_between': between,
            'lineEdit_beam_between': beam_between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_input': num,
            'R': R,
            'animation_name': animation_name,
            'lineEdit_ceramic_width': ceramic_width,
            # 顺序摆参数
            'lineEdit_delay_time': delay_time,
            # 自定义计算参数
            #'group': group,
        }

        self.worker_thread_plot = DoubleWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.double_manual_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程

    # 单头摆-智能计算-子进程信号接收函数
    def single_intelligent_thread_signal(self, result):
        # 刷新画布
        self.canvas.draw()
        # 清空 QLabel 中的内容
        self.animation_QLabel.clear()
        # 创建新的 QMovie 对象并设置到 QLabel
        self.movie = QMovie('donghua.gif')
        self.animation_QLabel.setMovie(self.movie)
        # 启动新的动画
        self.movie.start()
        self.button_enable(self.button_list)
        # 参数集更新
        self.single_parameter_intelligent['lineEdit_coefficient'] = result

    # 单头摆-人工寻优-子进程信号接收函数
    def single_manual_thread_signal(self, result):
        # 刷新画布
        self.canvas.draw()
        # 清空 QLabel 中的内容
        self.animation_QLabel.clear()
        # 创建新的 QMovie 对象并设置到 QLabel
        self.movie = QMovie('donghua.gif')
        self.animation_QLabel.setMovie(self.movie)
        # 启动新的动画
        self.movie.start()
        self.button_enable(self.button_list)
        # 参数集更新
        self.single_parameter_intelligent['lineEdit_coefficient'] = result

    # 双头摆-智能计算-子进程信号接收函数
    def double_intelligent_thread_signal(self, result):
        # 刷新画布
        self.canvas.draw()
        # 清空 QLabel 中的内容
        self.animation_QLabel.clear()
        # 创建新的 QMovie 对象并设置到 QLabel
        self.movie = QMovie('donghua.gif')
        self.animation_QLabel.setMovie(self.movie)
        # 启动新的动画
        self.movie.start()
        self.button_enable(self.button_list)
        # 参数集更新
        self.double_parameter_intelligent['lineEdit_coefficient'] = result

    # 双头摆-智能计算-子进程信号接收函数
    def double_manual_thread_signal(self, result):
        # 刷新画布
        self.canvas.draw()
        # 清空 QLabel 中的内容
        self.animation_QLabel.clear()
        # 创建新的 QMovie 对象并设置到 QLabel
        self.movie = QMovie('donghua.gif')
        self.animation_QLabel.setMovie(self.movie)
        # 启动新的动画
        self.movie.start()
        self.button_enable(self.button_list)
        # 参数集更新
        self.double_parameter_intelligent['lineEdit_coefficient'] = result

    # 当有计算运行时，屏蔽其他按钮功能
    def button_disable(self,button_list):
        for button in button_list:
            button.setEnabled(False)

    # 计算完毕，按钮恢复正常
    def button_enable(self,button_list):
        for button in button_list:
            button.setEnabled(True)

    # 将字典中所有的值转换为数值类型
    def dict_value_float(self,dict):
        dict_keys = dict.keys()
        for key in dict_keys:
            if dict[key] != '' and dict[key] is not None:
                dict[key] = float(dict[key])
        return dict

    # 编辑框值发生变化时，值同步到参数集合中-监听
    def line_eidt_textchange(self,name, text, list):
        list[name] = text
        # if list['lineEdit_production_volume'] != '' and list['lineEdit_ceramic_width'] != '':

