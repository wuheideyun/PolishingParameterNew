import os
import sqlite3

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QMessageBox, QDialog

from MainWindow_New_Interface import MainWindow
from PySide6.QtGui import QMovie
from functools import partial
from PIL import Image, ImageSequence
# 函数导入
from Double_Function import DoubleWorkerThread,double_num_calculate,self_define_calculate
from OutputReportQWidget import OutputReportWidget
from WholeLineOutputReportWidget import WholeLineOutputReportWidget
from Single_Function import SingleWorkerThread,single_num_calculate,single_self_define_calculate
from Equal_Function import EqualWorkerThread,equal_num_calculate,equal_self_define_calculate
from WholeLineConfigDialog import WholeLineConfigDialog
from WholeLineConfigManager import WholeLineConfigManager
from Whole_line_calculate_Double import Double_self_whole_line_Thread

import json


class MainWindow_impl(MainWindow):
    def __init__(self):
        super().__init__()

        # 创建定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        # 1. 创建配置管理器的实例
        self.config_manager = WholeLineConfigManager()
        # 2. 调用 load_config() 方法，它会读取 whole_line_config.ini 并返回一个包含所有数据的字典
        self.whole_line_params = self.config_manager.load_config()

        self.output_report = OutputReportWidget(self.data_model, self.config_manager)
        self.whole_line_output_report = WholeLineOutputReportWidget(self.data_model, self.config_manager)
        # 获取当前目录下的database.db文件路径
        self.db_path = os.path.join(os.getcwd(), "database.db")
        # 单头摆-参数汇总
        self.single_parameter_intelligent = {}  # 字典-用于储存输入参数
        self.single_parameter_manual = {}  # 字典-用于储存输出参数（包括输入参数）

        # 双头摆-参数汇总
        self.double_parameter_intelligent = {}  # 字典-用于储存输入参数
        self.double_parameter_manual = {}  # 字典-用于储存输出参数（包括输入参数）

        # 同步摆-参数汇总
        self.equal_parameter_intelligent = {}  # 字典-用于储存输入参数
        self.equal_parameter_manual = {}  # 字典-用于储存输出参数（包括输入参数）

        # --- 新增：用于临时存储整线计算结果的实例变量 ---
        self.latest_whole_line_result = None

        # 主机参数-同步摆-self.host_param_equal_frame
        self.host_param_equal_line_edit_names = [
            "lineEdit_between", "lineEdit_diameter", "lineEdit_grind_length", "lineEdit_work_time"
        ]
        for i in self.host_param_equal_line_edit_names:
            self.equal_parameter_intelligent[i] = self.host_param_equal_frame.content_layout.get_line_edit_value(i)
            self.equal_parameter_manual[i] = self.host_param_equal_frame.content_layout.get_line_edit_value(i)
        # 监听参数变更信息，并更新到数据集中
        self.host_param_equal_frame.content_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.equal_parameter_intelligent))
        self.host_param_equal_frame.content_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.equal_parameter_manual))

        # 主机参数-双头摆- self.host_param_double_frame
        self.host_param_double_line_edit_names = [
            "lineEdit_between", "lineEdit_beam_between", "lineEdit_diameter", "lineEdit_grind_length", "lineEdit_work_time"
        ]
        for i in self.host_param_double_line_edit_names:
            self.double_parameter_intelligent[i] = self.host_param_double_frame.content_layout.get_line_edit_value(i)
            self.double_parameter_manual[i] = self.host_param_double_frame.content_layout.get_line_edit_value(i)
        # 监听参数变更信息，并更新到数据集中
        self.host_param_double_frame.content_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.double_parameter_intelligent))
        self.host_param_double_frame.content_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.double_parameter_manual))

        # 主机参数-单头摆- self.host_param_single_frame
        self.host_param_single_line_edit_names = [
            "lineEdit_beam_between", "lineEdit_diameter", "lineEdit_grind_length", "lineEdit_work_time"
        ]
        for i in self.host_param_single_line_edit_names:
            self.single_parameter_intelligent[i] = self.host_param_single_frame.content_layout.get_line_edit_value(i)
            self.single_parameter_manual[i] = self.host_param_single_frame.content_layout.get_line_edit_value(i)
        # 监听参数变更信息，并更新到数据集中
        self.host_param_single_frame.content_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.single_parameter_intelligent))
        self.host_param_single_frame.content_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.single_parameter_manual))

        # 运动输入参数- self.motion_in_param_frame
        self.motion_in_param_line_edit_names = [
            "lineEdit_production_volume", "lineEdit_ceramic_width", "lineEdit_accelerate", "lineEdit_overlap",
            "lineEdit_num_input", "lineEdit_group_count", "lineEdit_stay_time_input"
        ]
        for i in self.motion_in_param_line_edit_names:
            self.single_parameter_intelligent[i] = self.motion_in_param_frame.content_layout.get_line_edit_value(i)
            self.double_parameter_intelligent[i] = self.motion_in_param_frame.content_layout.get_line_edit_value(i)
            self.equal_parameter_intelligent[i] = self.motion_in_param_frame.content_layout.get_line_edit_value(i)
        # 监听参数变更信息，并更新到数据集中
        self.motion_in_param_frame.content_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.single_parameter_intelligent))
        self.motion_in_param_frame.content_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.double_parameter_intelligent))
        self.motion_in_param_frame.content_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.equal_parameter_intelligent))

        # 运动输出参数 and 产品质量参数- self.motion_out_param_frame
        self.motion_out_param_line_edit_names = [
            "lineEdit_belt_speed", "lineEdit_beam_swing_speed", "lineEdit_beam_constant_time",
            "lineEdit_stay_time_output", "lineEdit_swing", "lineEdit_num_output"
        ]
        self.motion_out_param_line_edit_names_2 = [
            "lineEdit_coefficient"
        ]
        for i in self.motion_out_param_line_edit_names:
            self.single_parameter_intelligent[i] = self.motion_out_param_frame.content_up_layout.get_line_edit_value(i)
            self.double_parameter_intelligent[i] = self.motion_out_param_frame.content_up_layout.get_line_edit_value(i)
            self.equal_parameter_intelligent[i] = self.motion_out_param_frame.content_up_layout.get_line_edit_value(i)
        for i in self.motion_out_param_line_edit_names_2:
            self.single_parameter_intelligent[i] = self.motion_out_param_frame.content_down_layout.get_line_edit_value(i)
            self.double_parameter_intelligent[i] = self.motion_out_param_frame.content_down_layout.get_line_edit_value(i)
            self.equal_parameter_intelligent[i] = self.motion_out_param_frame.content_down_layout.get_line_edit_value(i)
        # 监听参数变更信息，并更新到数据集中
        self.motion_out_param_frame.content_up_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.single_parameter_intelligent))
        self.motion_out_param_frame.content_up_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.double_parameter_intelligent))
        self.motion_out_param_frame.content_up_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.equal_parameter_intelligent))

        self.motion_out_param_frame.content_down_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.single_parameter_intelligent))
        self.motion_out_param_frame.content_down_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.double_parameter_intelligent))
        self.motion_out_param_frame.content_down_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.equal_parameter_intelligent))

        # 运动参数-方案验证界面--运动输入参数 and 运动输出参数 and 产品质量参数- self.motion_input_out_param_manual_frame
        self.motion_out_param_param_manual_line_edit_names = [
            "lineEdit_production_volume", "lineEdit_beam_swing_speed", "lineEdit_beam_constant_time",
            "lineEdit_stay_time_input", "lineEdit_num_input", "lineEdit_accelerate", "lineEdit_ceramic_width",
            "lineEdit_delay_time"
        ]
        # 运动输出参数
        self.motion_out_param_param_manual_line_edit_names_2 = [
            "lineEdit_belt_speed", "lineEdit_swing"
        ]
        # 产品质量参数
        self.motion_out_param_param_manual_line_edit_names_3 = ["lineEdit_coefficient"]

        for i in self.motion_out_param_param_manual_line_edit_names:
            self.single_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_up_layout.get_line_edit_value(i)
            self.double_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_up_layout.get_line_edit_value(i)
            self.equal_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_up_layout.get_line_edit_value(i)
        for i in self.motion_out_param_param_manual_line_edit_names_2:
            self.single_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_middle_layout.get_line_edit_value(i)
            self.double_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_middle_layout.get_line_edit_value(i)
            self.equal_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_middle_layout.get_line_edit_value(i)
        for i in self.motion_out_param_param_manual_line_edit_names_3:
            self.single_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_bottom_layout.get_line_edit_value(i)
            self.double_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_bottom_layout.get_line_edit_value(i)
            self.equal_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_bottom_layout.get_line_edit_value(i)
        # 监听参数变更信息，并更新到数据集中
        self.motion_input_out_param_manual_frame.content_up_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.single_parameter_manual))
        self.motion_input_out_param_manual_frame.content_up_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.double_parameter_manual))
        self.motion_input_out_param_manual_frame.content_up_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.equal_parameter_manual))

        self.motion_input_out_param_manual_frame.content_middle_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.single_parameter_manual))
        self.motion_input_out_param_manual_frame.content_middle_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.double_parameter_manual))
        self.motion_input_out_param_manual_frame.content_middle_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.equal_parameter_manual))

        self.motion_input_out_param_manual_frame.content_bottom_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.single_parameter_manual))
        self.motion_input_out_param_manual_frame.content_bottom_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.double_parameter_manual))
        self.motion_input_out_param_manual_frame.content_bottom_layout.sig_textChanged.connect(
            partial(line_eidt_textchange, list=self.equal_parameter_manual))
        # 主皮带速度初始-计算赋值
        self.edit_list = [self.single_parameter_intelligent, self.double_parameter_intelligent, self.equal_parameter_intelligent
            ,self.single_parameter_manual,self.double_parameter_manual,self.equal_parameter_manual]
        for i in self.edit_list:
            if belt_speed_value_empty(i):
                i['lineEdit_belt_speed'] = belt_speed_calculate(i)

        # -------------------------按钮逻辑部分---------------------
        # 节能方案
        self.button_energy_project.clicked.connect(self.enerage_project_clicked)
        # 高品质方案
        self.button_efficient_project.clicked.connect(self.efficient_project_clicked)
        # 自定义修正方案
        self.button_selfdefine_project.clicked.connect(self.self_define_project_clicked)

        # 同步摆动模式
        self.button_synchronization_mode.clicked.connect(self.syn_project)
        # 交叉摆动模式
        self.button_cross_mode.clicked.connect(self.cross_project)
        # 顺序摆动模式
        self.button_order_mode.clicked.connect(self.order_project)


        self.save_button.clicked.connect(self.on_save_btn)
        # 新增：连接“整线配置”按钮的点击事件
        self.line_config_button.clicked.connect(self.open_line_config_dialog)
        # 界面所有编辑框收集
        # self.lineEdit_beam_between.setText(600)
        self.button_list=[self.button_energy_project,self.button_efficient_project,self.button_selfdefine_project
                     ,self.button_synchronization_mode,self.button_cross_mode,self.button_order_mode]

    #更新字典值
    def update_values(self):

        for i in self.host_param_single_line_edit_names:
            self.single_parameter_intelligent[i] = self.host_param_single_frame.content_layout.get_line_edit_value(i)
            self.single_parameter_manual[i] = self.host_param_single_frame.content_layout.get_line_edit_value(i)

        for i in self.host_param_double_line_edit_names:
            self.double_parameter_intelligent[i] = self.host_param_double_frame.content_layout.get_line_edit_value(i)
            self.double_parameter_manual[i] = self.host_param_double_frame.content_layout.get_line_edit_value(i)

        for i in self.host_param_equal_line_edit_names:
            self.equal_parameter_intelligent[i] = self.host_param_equal_frame.content_layout.get_line_edit_value(i)
            self.equal_parameter_manual[i] = self.host_param_equal_frame.content_layout.get_line_edit_value(i)

        for i in self.motion_in_param_line_edit_names:
            self.single_parameter_intelligent[i] = self.motion_in_param_frame.content_layout.get_line_edit_value(i)
            self.double_parameter_intelligent[i] = self.motion_in_param_frame.content_layout.get_line_edit_value(i)
            self.equal_parameter_intelligent[i] = self.motion_in_param_frame.content_layout.get_line_edit_value(i)

        for i in self.motion_out_param_line_edit_names:
            self.single_parameter_intelligent[i] = self.motion_out_param_frame.content_up_layout.get_line_edit_value(i)
            self.double_parameter_intelligent[i] = self.motion_out_param_frame.content_up_layout.get_line_edit_value(i)
            self.equal_parameter_intelligent[i] = self.motion_out_param_frame.content_up_layout.get_line_edit_value(i)
        for i in self.motion_out_param_line_edit_names_2:
            self.single_parameter_intelligent[i] = self.motion_out_param_frame.content_down_layout.get_line_edit_value(i)
            self.double_parameter_intelligent[i] = self.motion_out_param_frame.content_down_layout.get_line_edit_value(i)
            self.equal_parameter_intelligent[i] = self.motion_out_param_frame.content_down_layout.get_line_edit_value(i)

        for i in self.motion_out_param_param_manual_line_edit_names:
            self.single_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_up_layout.get_line_edit_value(i)
            self.double_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_up_layout.get_line_edit_value(i)
            self.equal_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_up_layout.get_line_edit_value(i)
        for i in self.motion_out_param_param_manual_line_edit_names_2:
            self.single_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_middle_layout.get_line_edit_value(i)
            self.double_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_middle_layout.get_line_edit_value(i)
            self.equal_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_middle_layout.get_line_edit_value(i)
        for i in self.motion_out_param_param_manual_line_edit_names_3:
            self.single_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_bottom_layout.get_line_edit_value(i)
            self.double_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_bottom_layout.get_line_edit_value(i)
            self.equal_parameter_manual[i] = self.motion_input_out_param_manual_frame.content_bottom_layout.get_line_edit_value(i)
        for i in self.edit_list:
            if belt_speed_value_empty(i):
                i['lineEdit_belt_speed'] = belt_speed_calculate(i)

    def concatenate_values(self,params):
        result = []
        for value in params.values():
            if isinstance(value, list):
                # 将列表中的元素转换为字符串并用逗号连接
                list_str = ",".join(str(item) for item in value)
                result.append(list_str)
            else:
                # 直接转换为字符串
                result.append(str(value))
        # 用逗号连接所有处理后的值
        concatenated_string = ",".join(result)
        return concatenated_string
    def on_save_btn(self):
        if not self.ifcalcflag:
            QMessageBox.warning(self, "警告", "请先进行方案选择操作，计算出【运动输出参数】后再进行保存参数操作！")
            return
        params = {}
        swing_mode = ''
        # 判断当前设备
        if self.current_device == 1:
            if self.current_mode == 1:
                params = dict_value_to_float(self.single_parameter_intelligent)
                if self.solution_selection == 3:
                    swing_mode = '自定义'
                    params['mode'] = '3'
                else:
                    swing_mode = '顺序摆'
                    params['mode'] = '6'
            else:
                params = dict_value_to_float(self.single_parameter_manual)
                if self.solution_selection == 4:
                    swing_mode = '同步摆'
                    params['mode'] = '4'
                elif self.solution_selection == 5:
                    swing_mode = '交叉摆'
                    params['mode'] = '5'
                elif self.solution_selection == 6:
                    swing_mode = '顺序摆'
                    params['mode'] = '6'
            params['device'] = '1'
        elif self.current_device == 2:
            if self.current_mode == 1:
                params = dict_value_to_float(self.double_parameter_intelligent)
                if self.solution_selection == 3:
                    swing_mode = '自定义'
                    params['mode'] = '3'
                else:
                    swing_mode = '顺序摆'
                    params['mode'] = '6'
            else:
                params = dict_value_to_float(self.double_parameter_manual)
                if self.solution_selection == 4:
                    swing_mode = '同步摆'
                    params['mode'] = '4'
                elif self.solution_selection == 5:
                    swing_mode = '交叉摆'
                    params['mode'] = '5'
                elif self.solution_selection == 6:
                    swing_mode = '顺序摆'
                    params['mode'] = '6'
            params['device'] = '2'
        elif self.current_device == 3:
            if self.current_mode == 1:
                params = dict_value_to_float(self.equal_parameter_intelligent)
                params['lineEdit_delay_time'] = 0.0
            else:
                params = dict_value_to_float(self.equal_parameter_manual)
                params['lineEdit_delay_time'] = 0.0

            swing_mode = '同步摆'
            params['mode'] = '4'
            params['device'] = '3'
        # 判断摆动模式
        if self.current_mode == 2:
            current_mode = '方案验证'
            params['lineEdit_stay_time'] = params['lineEdit_stay_time_input']#方案验证的【边部停留时间】取input
        elif self.current_mode == 1:
            params['lineEdit_stay_time'] = params['lineEdit_stay_time_output']#智能寻优的【边部停留时间】取output
            current_mode = '智能寻优'
        device_name = self.device_mapping.get(self.current_device)
        # params['mode'] = self.solution_selection

        values = self.concatenate_values(params)

        # --- 步骤 3: 根据“整线计算”开关，决定调用哪个保存方法 ---
        line_config = self.config_manager.load_config()
        is_whole_line_mode = line_config.get('global', {}).get('whole_line_calc_enabled', False)
        if is_whole_line_mode:
            # --- 整线保存逻辑 ---
            print("[DEBUG] 执行整线参数保存...")

            if self.latest_whole_line_result is None:
                QMessageBox.warning(self, "操作失败", "没有可供保存的整线计算结果，请先执行一次计算。")
                return

            try:
                whole_line_params_json = json.dumps(self.latest_whole_line_result, indent=4, ensure_ascii=False)
            except TypeError as e:
                QMessageBox.critical(self, "错误", f"无法序列化整线参数: {e}")
                return

            # 调用新的保存方法，传入所有公共参数 和 新的整线参数
            if self.data_model.add_whole_line_data(params, current_mode, values, swing_mode, device_name,
                                                   whole_line_params_json):
                self.status_label.setText('整线方案参数已成功保存至数据库！')
                self.latest_whole_line_result = None  # 保存后清空
            else:
                self.status_label.setText('整线方案参数保存失败，请重试！')
        else:
            # --- 单机保存逻辑 (完全复用旧逻辑) ---
            print("[DEBUG] 执行单机参数保存...")

            if self.data_model.add_data(params, current_mode, values, swing_mode,self.device_mapping.get(self.current_device)):
                self.status_label.setText('                  参数已保存至数据库！')
            else:
                self.status_label.setText('                  参数保存失败，请重试！')

    # 检查是否满足运行按钮的条件
    def check_whole_line_mode_compatibility(self, button_name):
        # 1. 从配置文件加载最新的整线计算开关状态
        line_config = self.config_manager.load_config()
        is_whole_line_mode = line_config.get('global', {}).get('whole_line_calc_enabled', False)

        # 2. 如果不是整线模式，则直接通过，执行原始的单机逻辑
        if not is_whole_line_mode:
            return True
        # 3. 如果是整线模式，则进行兼容性检查
        if self.current_device == 2 and button_name == "自定义修正方案":
            return True
        else:
            QMessageBox.warning(self, "模式不兼容",
                                "当前处于整线计算模式，该模式下仅支持【双头摆】机型的【自定义修正方案】计算，请检查您的选择！")
            return False

    # 更新底部状态栏
    def update_status_label(self):
        self.timer.start(500)  # 每秒触发一次

        # 更新状态栏
    def update_status(self):
        # self.status_texts = ["正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。。", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。。。"]

        self.status_label.setText(self.status_texts[self.current_text_index])
        self.current_text_index = (self.current_text_index + 1) % len(self.status_texts)

    # 按钮点击槽函数(计算)
    def enerage_project_clicked(self):
        if not self.check_whole_line_mode_compatibility('节能方案'):
            return
        self.update_status_label()
        print("--- 已成功获取整线配置参数 ---")
        # print(json.dumps(self.whole_line_params, indent=4, ensure_ascii=False))
        # 获取抛光机总数
        # machine_count = self.whole_line_params.get('global', {}).get('machine_count', 0)
        # print(f"\n抛光机总数: {machine_count}")
        # 获取整线计算值
        whole_line_calc_enabled = self.whole_line_params.get('global', {}).get('whole_line_calc_enabled', 0)
        # print(f"\n整线计算值: {whole_line_calc_enabled}")
        # 获取第一台设备的参数
        # if machine_count > 0:
        #     first_device_params = self.whole_line_params.get('devices', [])[0]
        #     print(f"1号机机型: {first_device_params.get('type')}")
        #     print(f"1号机磨头数: {first_device_params.get('head_count')}")
        #     print(f"1号机磨块配比: {first_device_params.get('grinding_config')}")

        # 获取第一个设备间距
        # if machine_count > 1:
        #     first_spacing = self.whole_line_params.get('spacings', [])[0]
        #     print(f"1-2号机间距: {first_spacing}")

        self.update_values()
        self.ifcalcflag = True
        self.solution_selection = 1
        self.status_texts = ["正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。。", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。。。"]

        # 校验输入框
        # if not self.check_input_valid():
        #     return
        # 按钮不可用
        button_disable(self.button_list)
        # 字符类型转换
        single_parameter_intelligent = dict_value_to_float(self.single_parameter_intelligent)
        double_parameter_intelligent = dict_value_to_float(self.double_parameter_intelligent)
        equal_parameter_intelligent = dict_value_to_float(self.equal_parameter_intelligent)
        if self.current_device == 1:     # 单头摆
            self.single_enerage_project(animation_name=self.MatchAnimationName(single_parameter_intelligent,11,"SingleEnergyProject"),**single_parameter_intelligent)
        elif self.current_device == 2:   # 双头摆
            if whole_line_calc_enabled == True:
                return
            else:
                self.double_enerage_project(animation_name=self.MatchAnimationName(double_parameter_intelligent,12,"DoubleEnergyProject"),**double_parameter_intelligent)
        elif self.current_device == 3:   # 同步摆
            self.equal_enerage_project(animation_name=self.MatchAnimationName(equal_parameter_intelligent,11,"EqualEnergyProject"),**equal_parameter_intelligent)
            return

    def MatchAnimationName(self,data, count, name):
        # 获取前count个键值对的值
        values = list(data.values())[:count]

        # 将名字放在首位
        result = [name] + values

        # 用"_"拼接
        return "_".join(map(str, result))

    def efficient_project_clicked(self):
        if not self.check_whole_line_mode_compatibility('高品质方案'):
            return
        self.update_status_label()
        self.update_values()
        self.ifcalcflag = True
        self.solution_selection = 2
        self.status_texts = ["正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。。", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。。。"]

        # 校验输入框
        # if not self.check_input_valid():
        #     return
        # 按钮不可用
        button_disable(self.button_list)
        # 字符类型转换
        single_parameter_intelligent = dict_value_to_float(self.single_parameter_intelligent)
        double_parameter_intelligent = dict_value_to_float(self.double_parameter_intelligent)
        equal_parameter_intelligent = dict_value_to_float(self.equal_parameter_intelligent)
        if self.current_device == 1:
            self.single_efficient_project(animation_name=self.MatchAnimationName(single_parameter_intelligent,11,"SingleEfficientProject"),**single_parameter_intelligent)
        elif self.current_device == 2:
            self.double_efficient_project(animation_name=self.MatchAnimationName(double_parameter_intelligent,12,"DoubleEfficientProject"),**double_parameter_intelligent)
        elif self.current_device == 3:
            self.equal_efficient_project(animation_name=self.MatchAnimationName(equal_parameter_intelligent,11,"EqualEfficientProject"),**equal_parameter_intelligent)
            return

    def check_input_valid(self):
        if self.host_param_single_changed_flag:
            self.show_message('←主机参数区域进行了参数修改，请先进行保存参数操作！')
            return False
        elif self.current_mode == 1:
            if self.motion_input_intelligence_changed_flag:
                self.show_message('→运动输入参数区域进行了参数修改，请先进行保存参数操作！')
                return False
        elif self.current_mode == 2:
            if self.motion_input_manual_changed_flag:
                self.show_message('→运动输入参数区域进行了参数修改，请先进行保存参数操作！')
                return False
        return True
    def self_define_project_clicked(self):
        if not self.check_whole_line_mode_compatibility('自定义修正方案'):
            return
        self.update_status_label()
        self.update_values()
        self.ifcalcflag = True
        self.solution_selection = 3
        button_disable(self.button_list)
        self.status_texts = ["正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。。", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。。。"]

        # 字符类型转换
        single_parameter_intelligent = dict_value_to_float(self.single_parameter_intelligent)
        double_parameter_intelligent = dict_value_to_float(self.double_parameter_intelligent)
        print(f'double_parameter_intelligent = {double_parameter_intelligent}')
        equal_parameter_intelligent = dict_value_to_float(self.equal_parameter_intelligent)

        if self.current_device == 1:
            self.single_self_project(animation_name=self.MatchAnimationName(single_parameter_intelligent,11,"SingleSelfProject"),**single_parameter_intelligent)
        elif self.current_device == 2:
            # 整线计算判断位
            whole_line_calc_enabled = self.whole_line_params.get('global', {}).get('whole_line_calc_enabled', 0)
            if whole_line_calc_enabled == True:
                # 整线计算函数
                self.double_self_whole_calculate(animation_name=self.MatchAnimationName(double_parameter_intelligent,12,"DoubleSelfProject"),**double_parameter_intelligent)
            else:
                self.double_self_project(animation_name=self.MatchAnimationName(double_parameter_intelligent,12,"DoubleSelfProject"),**double_parameter_intelligent)
        elif self.current_device == 3:
            self.equal_self_project(animation_name=self.MatchAnimationName(equal_parameter_intelligent,11,"EqualSelfProject"),**equal_parameter_intelligent)
            return

    # 按钮点击槽函数(仿真)
    def syn_project(self):
        if not self.check_whole_line_mode_compatibility('同步摆动模式'):
            return
        self.update_status_label()
        self.update_values()
        self.solution_selection = 4
        self.ifcalcflag = True
        button_disable(self.button_list)
        self.status_texts = ["正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。。", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。。。"]

        # 字符类型转换
        single_parameter_manual = dict_value_to_float(self.single_parameter_manual)
        double_parameter_manual = dict_value_to_float(self.double_parameter_manual)
        equal_parameter_manual = dict_value_to_float(self.equal_parameter_manual)
        if self.current_device == 1:
            self.single_synchronization_project(animation_name=self.MatchAnimationName(single_parameter_manual,11,"SingleSynchronizationProject"),**single_parameter_manual)
        elif self.current_device == 2:
            self.double_synchronization_project(animation_name=self.MatchAnimationName(double_parameter_manual,12,"DoubleSynchronizationProject"),**double_parameter_manual)
        elif self.current_device == 3:
            self.equal_synchronization_project(animation_name=self.MatchAnimationName(equal_parameter_manual,11,"EqualSynchronizationProject"),**equal_parameter_manual)
            return

    def cross_project(self):
        if not self.check_whole_line_mode_compatibility('交叉摆动模式'):
            return
        self.update_status_label()
        self.update_values()
        self.ifcalcflag = True
        self.solution_selection = 5
        button_disable(self.button_list)
        self.status_texts = ["正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。。", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。。。"]

        # 字符类型转换
        single_parameter_manual = dict_value_to_float(self.single_parameter_manual)
        double_parameter_manual = dict_value_to_float(self.double_parameter_manual)
        if self.current_device == 1:
            self.single_cross_project(animation_name=self.MatchAnimationName(single_parameter_manual,11,"SingleCrossProject"),**single_parameter_manual)
        elif self.current_device == 2:
            self.double_cross_project(animation_name=self.MatchAnimationName(double_parameter_manual,11,"DoubleCrossProject"),**double_parameter_manual)
            return

    def order_project(self):
        if not self.check_whole_line_mode_compatibility('顺序摆动模式'):
            return
        self.update_status_label()
        self.update_values()
        self.ifcalcflag = True
        self.solution_selection = 6
        self.status_texts = ["正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。。", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。。。"]

        button_disable(self.button_list)
        # 字符类型转换
        single_parameter_manual = dict_value_to_float(self.single_parameter_manual)
        double_parameter_manual = dict_value_to_float(self.double_parameter_manual)
        if self.current_device == 1:
            self.single_order_project(animation_name=self.MatchAnimationName(single_parameter_manual,11,"SingleOrderProject"),**single_parameter_manual)
        elif self.current_device == 2:
            self.double_order_project(animation_name=self.MatchAnimationName(double_parameter_manual,11,"SingleOrderProject"),**double_parameter_manual)
            return

    # -------------------------单头摆-智能计算逻辑函数---------------------------------
    # 智能计算
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

        # 静态动画参数输入
        # params.update({'mode': 'order', 'fig': self.canvas.fig,'fig_2': self.canvas_animation.fig,'animation_name':animation_name})

        # 动态动画参数输入
        params.update({'mode': 'order', 'fig': self.canvas.fig, 'animation_name': animation_name})

        self.worker_thread_plot = SingleWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.single_intelligent_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程
    # 高效计算
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

        # 静态动画参数输入
        # params.update({'mode': 'order', 'fig': self.canvas.fig,'fig_2': self.canvas_animation.fig,'animation_name':animation_name})

        # 动态动画参数输入
        params.update({'mode': 'order', 'fig': self.canvas.fig, 'animation_name': animation_name})

        self.worker_thread_plot = SingleWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.single_intelligent_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程
    # 自定义计算
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

        # 静态动画参数输入
        # params.update({'mode': 'self_order', 'fig': self.canvas.fig,'fig_2': self.canvas_animation.fig,'animation_name':animation_name})
        # 动态动画参数输入
        params.update({'mode': 'self_order', 'fig': self.canvas.fig, 'animation_name': animation_name})

        self.worker_thread_plot = SingleWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.single_intelligent_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程
    # -------------------------单头摆-方案验证逻辑函数--------------------------------
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
        self.single_parameter_manual['lineEdit_swing'] = round(a*(v2/a)**2+v2*constant_time,2)
        self.single_parameter_manual['lineEdit_num_output'] = num

        # 静态动画参数集
        '''
        params = {
            'mode': 'equal',
            'fig': self.canvas.fig,
            'fig_2': self.canvas_animation.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_output': stay_time,
            'lineEdit_accelerate': a,
            #'between': between,
            'lineEdit_beam_between': beam_between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_output': num,
            'lineEdit_diameter': R,
            'animation_name': animation_name,
            'lineEdit_ceramic_width': ceramic_width,
            # 顺序摆参数
            # 'delay_time': delay_time,
            # 自定义计算参数
            # 'group': group,
        }
        '''
        # 动态动画参数及
        params = {
            'mode': 'equal',
            'fig': self.canvas.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_output': stay_time,
            'lineEdit_accelerate': a,
            # 'between': between,
            'lineEdit_beam_between': beam_between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_output': num,
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
        self.single_parameter_manual['lineEdit_swing'] = round(a * (v2 / a) ** 2 + v2 * constant_time, 2)
        self.single_parameter_manual['lineEdit_num_output'] = num

        # 静态动画参数集
        '''
        params = {
            'mode': 'cross',
            'fig': self.canvas.fig,
            'fig_2': self.canvas_animation.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_output': stay_time,
            'lineEdit_accelerate': a,
            # 'between': between,
            'lineEdit_beam_between': beam_between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_output': num,
            'R': R,
            'animation_name': animation_name,
            'lineEdit_ceramic_width': ceramic_width,
            # 顺序摆参数
            # 'delay_time': delay_time,
            # 自定义计算参数
            # 'group': group,
        }
        '''
        # 动态动画参数集
        params = {
            'mode': 'cross',
            'fig': self.canvas.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_output': stay_time,
            'lineEdit_accelerate': a,
            # 'between': between,
            'lineEdit_beam_between': beam_between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_output': num,
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
        num = round(kwargs.get('lineEdit_num_input'))
        R = kwargs.get('lineEdit_diameter')/2
        ceramic_width = kwargs.get('lineEdit_ceramic_width')
        delay_time = kwargs.get('lineEdit_delay_time')
        # 延时时间数组
        delay_time_list = []
        for i in range(0,num):
            delay_time_list.append(i*delay_time)
        self.single_parameter_manual['lineEdit_delay_time_list'] = delay_time_list
        self.single_parameter_manual['lineEdit_swing'] = round(a * (v2 / a) ** 2 + v2 * constant_time, 2)
        self.single_parameter_manual['lineEdit_num_output'] = num

        # 静态动画参数集
        '''
        params = {
            'mode': 'order',
            'fig': self.canvas.fig,
            'fig_2': self.canvas_animation.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_output': stay_time,
            'lineEdit_accelerate': a,
            #'between': between,
            'lineEdit_beam_between': beam_between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_output': num,
            'R': R,
            'animation_name': animation_name,
            'lineEdit_ceramic_width': ceramic_width,
            # 顺序摆参数
            'lineEdit_delay_time': delay_time,
            # 自定义计算参数
            # 'group': group,
        }
        '''
        # 动态动画参数集
        params = {
            'mode': 'order',
            'fig': self.canvas.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_output': stay_time,
            'lineEdit_accelerate': a,
            # 'between': between,
            'lineEdit_beam_between': beam_between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_output': num,
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
#--------------------------------------双头摆智能计算----------------------------------------------------------------------
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

        # 静态动画参数输入
        # params.update({'mode': 'order','fig': self.canvas.fig,'fig_2': self.canvas_animation.fig,'animation_name':animation_name})
        # 动态动画参数输入
        params.update({'mode': 'order', 'fig': self.canvas.fig, 'animation_name': animation_name})

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

        # 静态动画参数输入
        # params.update({'mode': 'order', 'fig': self.canvas.fig,'fig_2': self.canvas_animation.fig,'animation_name':animation_name})
        # 动态动画参数输入
        params.update({'mode': 'order', 'fig': self.canvas.fig,'animation_name': animation_name})

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

        # 静态动画参数输入
        # params.update({'mode': 'self_order', 'fig': self.canvas.fig,'fig_2': self.canvas_animation.fig,'animation_name':animation_name})
        # 动态动画参数输入
        params.update({'mode': 'self_order', 'fig': self.canvas.fig,'animation_name': animation_name})

        self.worker_thread_plot = DoubleWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.double_intelligent_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程

    # 双头摆-自定义整线计算
    def double_self_whole_calculate(self,animation_name,**kwargs):
        self.current_animation_name = animation_name
        # 界面参数获取（全局变量）
        # v1 = kwargs.get('lineEdit_belt_speed')
        # ceramic_width = kwargs.get('lineEdit_ceramic_width')
        R = kwargs.get('lineEdit_diameter') / 2
        a = kwargs.get('lineEdit_accelerate')
        mo = kwargs.get('lineEdit_grind_length')
        # 整线计算参数获取
        grind_summary = WholeLineConfigManager().get_grit_counts()  # 整线磨块目数汇总
        between_summary = WholeLineConfigManager().get_all_betweens()  # 整线抛光机磨头间距
        beam_between_summary = WholeLineConfigManager().get_all_beam_betweens()  # 整线抛光机横梁间距
        ceramic_width_summary = WholeLineConfigManager().get_all_ceramic_widths()  # 整线抛光机进砖宽度
        belt_speed_summary = WholeLineConfigManager().get_all_belt_speeds()  # 整线抛光机主皮带速度
        beam_swing_tempo_summary = WholeLineConfigManager().get_all_beam_swing_tempos()  # 整线抛光机横梁摆动快慢
        # 整线参数计算
        self.worker_thread = Double_self_whole_line_Thread(R,mo,between_summary,beam_between_summary,ceramic_width_summary,belt_speed_summary,beam_swing_tempo_summary,grind_summary,a)
        self.worker_thread.result_signal.connect(lambda result_1,result_2: self.double_whole_line_calculate_signal(result_1,result_2,self.current_animation_name))  # 连接子线程的信号
        self.worker_thread.start()  # 启动子线程
    # ------------------------------------双头摆方案验证-------------------------------------------------------------------
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
        self.double_parameter_manual['lineEdit_swing'] = round(a * (v2 / a) ** 2 + v2 * constant_time, 2)
        self.double_parameter_manual['lineEdit_num_output'] = num

        # 静态动画参数集
        '''
        params = {
            'mode': 'equal',
            'fig': self.canvas.fig,
            'fig_2': self.canvas_animation.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_output': stay_time,
            'lineEdit_accelerate': a,
            'lineEdit_between': between,
            'lineEdit_beam_between': beam_between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_output': num,
            'R': R,
            'animation_name': animation_name,
            'lineEdit_ceramic_width':ceramic_width,
            # 顺序摆参数
            #'delay_time': delay_time,
            # 自定义计算参数
            #'group': group,
        }
        '''
        # 动态动画参数集
        params = {
            'mode': 'equal',
            'fig': self.canvas.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_output': stay_time,
            'lineEdit_accelerate': a,
            'lineEdit_between': between,
            'lineEdit_beam_between': beam_between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_output': num,
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
        self.double_parameter_manual['lineEdit_swing'] = round(a * (v2 / a) ** 2 + v2 * constant_time, 2)
        self.double_parameter_manual['lineEdit_num_output'] = num

        # 静态动画参数集
        '''
        params = {
            'mode': 'cross',
            'fig': self.canvas.fig,
            'fig_2': self.canvas_animation.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_output': stay_time,
            'lineEdit_accelerate': a,
            'lineEdit_between': between,
            'lineEdit_beam_between': beam_between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_output': num,
            'R': R,
            'animation_name': animation_name,
            'lineEdit_ceramic_width': ceramic_width,
            # 顺序摆参数
            # 'delay_time': delay_time,
            # 自定义计算参数
            # 'group': group,
        }
        '''
        # 动态动画参数集
        params = {
            'mode': 'cross',
            'fig': self.canvas.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_output': stay_time,
            'lineEdit_accelerate': a,
            'lineEdit_between': between,
            'lineEdit_beam_between': beam_between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_output': num,
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
        # 延时时间数组
        delay_time_list = []
        for i in range(0, round(num/2)):
            delay_time_list.append(i * delay_time)
        self.double_parameter_manual['lineEdit_delay_time_list'] = delay_time_list
        self.double_parameter_manual['lineEdit_swing'] = round(a * (v2 / a) ** 2 + v2 * constant_time, 2)
        self.double_parameter_manual['lineEdit_num_output'] = num

        # 静态动画参数集
        '''
        params = {
            'mode': 'order',
            'fig': self.canvas.fig,
            'fig_2': self.canvas_animation.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_output': stay_time,
            'lineEdit_accelerate': a,
            'lineEdit_between': between,
            'lineEdit_beam_between': beam_between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_output': num,
            'R': R,
            'animation_name': animation_name,
            'lineEdit_ceramic_width': ceramic_width,
            # 顺序摆参数
            'lineEdit_delay_time': delay_time,
            # 自定义计算参数
            #'group': group,
        }
        '''
        # 动态动画参数集
        params = {
            'mode': 'order',
            'fig': self.canvas.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_output': stay_time,
            'lineEdit_accelerate': a,
            'lineEdit_between': between,
            'lineEdit_beam_between': beam_between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_output': num,
            'R': R,
            'animation_name': animation_name,
            'lineEdit_ceramic_width': ceramic_width,
            # 顺序摆参数
            'lineEdit_delay_time': delay_time,
            # 自定义计算参数
            # 'group': group,
        }

        self.worker_thread_plot = DoubleWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.double_manual_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程
    #------------双头-----------------------摆整线计算方案-----------------------------------------------------------------
    #

    # --------------------------------------同步摆智能计算------------------------------------------------------------------------------
    # 同步摆-节能计算-子进程启动函数
    def equal_enerage_project(self, animation_name, **kwargs):
        # 绘图、动画模块子线程
        v1 = kwargs.get('lineEdit_belt_speed')
        ceramic_width = kwargs.get('lineEdit_ceramic_width')
        between = kwargs.get('lineEdit_between')
        R = kwargs.get('lineEdit_diameter') / 2
        a = kwargs.get('lineEdit_accelerate')
        mo = kwargs.get('lineEdit_grind_length')

        params = equal_num_calculate(v1, ceramic_width, between, R, a, mo, mode='enerage')
        # 计算结果-数据集更新
        self.equal_parameter_intelligent.update(params)

        # 静态动画绘制
        # params.update({'mode': 'equal', 'fig': self.canvas.fig,'fig_2': self.canvas_animation.fig, 'animation_name': animation_name})
        # 动态动画绘制
        params.update({'mode': 'equal', 'fig': self.canvas.fig, 'animation_name': animation_name})

        self.worker_thread_plot = EqualWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.equal_intelligent_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程

    # 同步摆-高效计算-子进程启动函数
    def equal_efficient_project(self, animation_name, **kwargs):
        v1 = kwargs.get('lineEdit_belt_speed')
        ceramic_width = kwargs.get('lineEdit_ceramic_width')
        between = kwargs.get('lineEdit_between')
        R = kwargs.get('lineEdit_diameter') / 2
        a = kwargs.get('lineEdit_accelerate')
        mo = kwargs.get('lineEdit_grind_length')
        # 参数计算
        params = equal_num_calculate(v1, ceramic_width, between, R, a, mo, mode='efficient')
        # 计算结果-数据集更新
        self.equal_parameter_intelligent.update(params)

        # 静态动画绘制
        # params.update({'mode': 'equal', 'fig': self.canvas.fig,'fig_2': self.canvas_animation.fig, 'animation_name': animation_name})
        # 动态动画绘制
        params.update({'mode': 'equal', 'fig': self.canvas.fig, 'animation_name': animation_name})

        self.worker_thread_plot = EqualWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.equal_intelligent_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程

    # 同步摆-自定义修正计算-子进程启动函数
    def equal_self_project(self, animation_name, **kwargs):
        v1 = kwargs.get('lineEdit_belt_speed')
        t2 = kwargs.get('lineEdit_stay_time_input')
        ceramic_width = kwargs.get('lineEdit_ceramic_width')
        between = kwargs.get('lineEdit_between')
        R = kwargs.get('lineEdit_diameter') / 2
        a = kwargs.get('lineEdit_accelerate')
        num_input = kwargs.get('lineEdit_num_input')
        group = kwargs.get('lineEdit_group_count')
        mo = kwargs.get('lineEdit_grind_length')
        # 参数计算
        params = equal_self_define_calculate(v1, t2, ceramic_width, between,R, a, num_input, mo)
        # 计算结果-数据集更新
        self.equal_parameter_intelligent.update(params)

        # 静态动画绘制
        # params.update({'mode': 'self_order', 'fig': self.canvas.fig,'fig_2': self.canvas_animation.fig, 'animation_name': animation_name})
        # 动态动画绘制
        params.update({'mode': 'self_order', 'fig': self.canvas.fig, 'animation_name': animation_name})

        self.worker_thread_plot = EqualWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.equal_intelligent_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程

    # ------------------------------------同步摆方案验证------------------------------------------------------------------------------
    # 同步摆-同步摆模式-子进程启动函数
    def equal_synchronization_project(self, animation_name, **kwargs):
        v1 = kwargs.get('lineEdit_belt_speed')
        v2 = kwargs.get('lineEdit_beam_swing_speed')
        constant_time = kwargs.get('lineEdit_beam_constant_time')
        stay_time = kwargs.get('lineEdit_stay_time_input')
        a = kwargs.get('lineEdit_accelerate')
        between = kwargs.get('lineEdit_between')
        num = kwargs.get('lineEdit_num_input')
        R = kwargs.get('lineEdit_diameter') / 2
        mo = kwargs.get('lineEdit_grind_length')
        ceramic_width = kwargs.get('lineEdit_ceramic_width')
        self.equal_parameter_manual['lineEdit_swing'] = round(a * (v2 / a) ** 2 + v2 * constant_time, 2)
        self.equal_parameter_manual['lineEdit_num_output'] = num

        # 静态动画参数集
        '''
        params = {
            'mode': 'equal',
            'fig': self.canvas.fig,
            'fig_2': self.canvas_animation.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_output': stay_time,
            'lineEdit_accelerate': a,
            'lineEdit_between': between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_output': num,
            'R': R,
            'animation_name': animation_name,
            'lineEdit_ceramic_width': ceramic_width,
            # 顺序摆参数
            # 'delay_time': delay_time,
            # 自定义计算参数
            # 'group': group,
        }
        '''
        # 动态动画参数集
        params = {
            'mode': 'equal',
            'fig': self.canvas.fig,
            'lineEdit_belt_speed': v1,
            'lineEdit_beam_swing_speed': v2,
            'lineEdit_beam_constant_time': constant_time,
            'lineEdit_stay_time_output': stay_time,
            'lineEdit_accelerate': a,
            'lineEdit_between': between,
            'lineEdit_grind_length': mo,
            'lineEdit_num_output': num,
            'R': R,
            'animation_name': animation_name,
            'lineEdit_ceramic_width': ceramic_width,
            # 顺序摆参数
            # 'delay_time': delay_time,
            # 自定义计算参数
            # 'group': group,
        }

        self.worker_thread_plot = EqualWorkerThread(**params)
        self.worker_thread_plot.result_signal.connect(self.equal_manual_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程

    # ------------------------------------子进程信号接收函数------------------------------------------------------------------------
    # 单头摆-智能计算-子进程信号接收函数
    def single_intelligent_thread_signal(self, result):
        self.timer.stop()
        self.status_label.setText("【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算完毕，请查看计算结果。")

        # 动态动画显示
        self.canvas.draw()
        # 清空 QLabel 中的内容
        self.animation_QLabel.clear()

        # 释放旧的 QMovie 对象
        if hasattr(self, 'movie') and self.movie is not None:
            self.movie.stop()
            self.movie.deleteLater()
        # 释放旧的 QMovie 对象
        if hasattr(self, 'movie2') and self.movie2 is not None:
            self.movie2.stop()
            self.movie2.deleteLater()

        # 创建新的 QMovie 对象并设置到 QLabel
        animation_name = result[1]
        # self.movie = QMovie(ani)
        # self.animation_QLabel.setMovie(self.movie)
        # 加载GIF动画
        self.movie = QMovie('./animation/' + animation_name + '_1.gif')
        self.movie2 = QMovie('./animation/' + animation_name + '_2.gif')
        self.movie.updated.connect(self.updated)
        # self.movie.setloopCount(1)  # 设置只播放一次
        self.animation_QLabel.setMovie(self.movie)
        # 启动新的动画
        self.movie.start()
        button_enable(self.button_list)


        # 静态动画显示
        # self.canvas.draw()
        # self.canvas_animation.draw()  # 新增（静态轨迹动画）
        # button_enable(self.button_list)

        # 参数集更新
        self.single_parameter_intelligent['lineEdit_coefficient'] = result[0]
        # 字符转换
        dict_value_to_str(self.single_parameter_intelligent)
        # 界面输出参数赋值
        for i in self.motion_out_param_line_edit_names:
            self.motion_out_param_frame.content_up_layout.set_line_edit_value(i,self.single_parameter_intelligent[i])
        for i in self.motion_out_param_line_edit_names_2:
            self.motion_out_param_frame.content_down_layout.set_line_edit_value(i,self.single_parameter_intelligent[i])
        # print(self.single_parameter_intelligent)
        # self.single_parameter_intelligent['lineEdit_accelerate']  # 加速度
        # self.single_parameter_intelligent['lineEdit_beam_swing_speed']  # 摆动速度
        # self.single_parameter_intelligent['lineEdit_beam_constant_time']  # 匀速摆动时间
        # self.single_parameter_intelligent['lineEdit_stay_time_output']  # 边部停留时间
        # 从字典中获取各个参数并转换为float类型
        accelerate = float(self.single_parameter_intelligent['lineEdit_accelerate'])
        beam_swing_speed = float(self.single_parameter_intelligent['lineEdit_beam_swing_speed'])
        beam_constant_time = float(self.single_parameter_intelligent['lineEdit_beam_constant_time'])
        stay_time_output = float(self.single_parameter_intelligent['lineEdit_stay_time_output'])

        # 根据公式进行计算
        result = 60 / (beam_constant_time * 2 + stay_time_output * 2 + beam_swing_speed / accelerate * 4)
        result_str = "{:.4f}".format(result)
        self.motion_out_param_frame.content_down_layout.set_line_edit_value('lineEdit_frequency', result_str)

    # 单头摆-方案验证-子进程信号接收函数
    def single_manual_thread_signal(self, result):
        self.timer.stop()
        self.status_label.setText("【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算完毕，请查看计算结果。")

        # 静态动画显示
        # self.canvas.draw()
        # self.canvas_animation.draw()  # 新增（静态轨迹动画）
        # button_enable(self.button_list)

        # 动态动画显示
        self.canvas.draw()
        # 清空 QLabel 中的内容
        self.animation_QLabel.clear()
        # 释放旧的 QMovie 对象
        if hasattr(self, 'movie') and self.movie is not None:
            self.movie.stop()
            self.movie.deleteLater()
        # 释放旧的 QMovie 对象
        if hasattr(self, 'movie2') and self.movie2 is not None:
            self.movie2.stop()
            self.movie2.deleteLater()
        # 创建新的 QMovie 对象并设置到 QLabel
        animation_name = result[1]
        # self.movie = QMovie(ani)
        # self.animation_QLabel.setMovie(self.movie)
        # 加载GIF动画
        self.movie = QMovie('./animation/' + animation_name + '_1.gif')
        self.movie2 = QMovie('./animation/' + animation_name + '_2.gif')
        self.movie.updated.connect(self.updated)
        # self.movie.setloopCount(1)  # 设置只播放一次
        self.animation_QLabel.setMovie(self.movie)
        # 启动新的动画
        self.movie.start()
        button_enable(self.button_list)

        # 参数集更新
        self.single_parameter_manual['lineEdit_coefficient'] = result[0]
        # 字符转换
        dict_value_to_str(self.single_parameter_manual)
        # 界面输出参数赋值
        for i in self.motion_out_param_param_manual_line_edit_names_2:
            self.motion_input_out_param_manual_frame.content_middle_layout.set_line_edit_value(i,self.single_parameter_manual[i])
        for i in self.motion_out_param_param_manual_line_edit_names_3:
            self.motion_input_out_param_manual_frame.content_bottom_layout.set_line_edit_value(i,self.single_parameter_manual[i])

    # 双头摆-智能计算-子进程信号接收函数
    def double_intelligent_thread_signal(self, result):
        self.timer.stop()
        self.status_label.setText("【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算完毕，请查看计算结果。")

        # 静态动画显示
        # self.canvas.draw()
        # self.canvas_animation.draw()  # 新增（静态轨迹动画）

        # 动态动画显示
        self.canvas.draw()
        # 清空 QLabel 中的内容
        self.animation_QLabel.clear()
        # 释放旧的 QMovie 对象
        if hasattr(self, 'movie') and self.movie is not None:
            self.movie.stop()
            self.movie.deleteLater()
        # 释放旧的 QMovie 对象
        if hasattr(self, 'movie2') and self.movie2 is not None:
            self.movie2.stop()
            self.movie2.deleteLater()
        # 创建新的 QMovie 对象并设置到 QLabel
        animation_name = result[1]
        # self.movie = QMovie(ani)
        # self.animation_QLabel.setMovie(self.movie)
        # 加载GIF动画
        self.movie = QMovie('./animation/' + animation_name + '_1.gif')
        self.movie2 = QMovie('./animation/' + animation_name + '_2.gif')
        self.movie.updated.connect(self.updated)
        # self.movie.setloopCount(1)  # 设置只播放一次
        self.animation_QLabel.setMovie(self.movie)
        # 启动新的动画
        self.movie.start()

        button_enable(self.button_list)
        # 参数集更新
        self.double_parameter_intelligent['lineEdit_coefficient'] = result[0]
        # 字符转换
        dict_value_to_str(self.double_parameter_intelligent)
        # 界面输出参数赋值
        for i in self.motion_out_param_line_edit_names:
            self.motion_out_param_frame.content_up_layout.set_line_edit_value(i,self.double_parameter_intelligent[i])
        for i in self.motion_out_param_line_edit_names_2:
            self.motion_out_param_frame.content_down_layout.set_line_edit_value(i,self.double_parameter_intelligent[i])
        # print(self.double_parameter_intelligent)

        # self.double_parameter_intelligent['lineEdit_accelerate']  # 加速度
        # self.double_parameter_intelligent['lineEdit_beam_swing_speed']  # 摆动速度
        # self.double_parameter_intelligent['lineEdit_beam_constant_time']  # 匀速摆动时间
        # self.double_parameter_intelligent['lineEdit_stay_time_output']  # 边部停留时间
        # 从字典中获取各个参数并转换为float类型
        accelerate = float(self.double_parameter_intelligent['lineEdit_accelerate'])
        beam_swing_speed = float(self.double_parameter_intelligent['lineEdit_beam_swing_speed'])
        beam_constant_time = float(self.double_parameter_intelligent['lineEdit_beam_constant_time'])
        stay_time_output = float(self.double_parameter_intelligent['lineEdit_stay_time_output'])

        # 根据公式进行计算
        result = 60 / (beam_constant_time * 2 + stay_time_output * 2 + beam_swing_speed / accelerate * 4)
        result_str = "{:.4f}".format(result)
        self.motion_out_param_frame.content_down_layout.set_line_edit_value('lineEdit_frequency', result_str)
    # 双头摆-方案验证-子进程信号接收函数
    def double_manual_thread_signal(self, result):
        self.timer.stop()
        self.status_label.setText("【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算完毕，请查看计算结果。")

        # 静态动画显示
        # self.canvas.draw()
        # self.canvas_animation.draw()  # 新增（静态轨迹动画）

        # 动态动画显示
        self.canvas.draw()
        # 清空 QLabel 中的内容
        self.animation_QLabel.clear()
        # 释放旧的 QMovie 对象
        if hasattr(self, 'movie') and self.movie is not None:
            self.movie.stop()
            self.movie.deleteLater()
        # 释放旧的 QMovie 对象
        if hasattr(self, 'movie2') and self.movie2 is not None:
            self.movie2.stop()
            self.movie2.deleteLater()
        # 创建新的 QMovie 对象并设置到 QLabel
        animation_name = result[1]
        # self.movie = QMovie(ani)
        # self.animation_QLabel.setMovie(self.movie)
        # 加载GIF动画
        self.movie = QMovie('./animation/' + animation_name + '_1.gif')
        self.movie2 = QMovie('./animation/' + animation_name + '_2.gif')
        self.movie.updated.connect(self.updated)
        # self.movie.setloopCount(1)  # 设置只播放一次
        self.animation_QLabel.setMovie(self.movie)
        # 启动新的动画
        self.movie.start()

        button_enable(self.button_list)
        # 参数集更新
        self.double_parameter_manual['lineEdit_coefficient'] = result[0]
        # 字符转换
        dict_value_to_str(self.double_parameter_manual)
        # 界面输出参数赋值
        for i in self.motion_out_param_param_manual_line_edit_names_2:
            self.motion_input_out_param_manual_frame.content_middle_layout.set_line_edit_value(i,self.double_parameter_manual[i])
        for i in self.motion_out_param_param_manual_line_edit_names_3:
            self.motion_input_out_param_manual_frame.content_bottom_layout.set_line_edit_value(i,self.double_parameter_manual[i])
    # 双头摆-自定义整线计算-子进程信号接收函数
    def double_whole_line_calculate_signal(self,result_PLC,result_simulation,animation_name):
        params_transmit_PLC = result_PLC   # PLC 传参
        self.latest_whole_line_result = params_transmit_PLC
        print("[DEBUG] 整线计算的PLC参数结果已暂存到 self.latest_whole_line_result")
        # PLC传参打印
        print(json.dumps(params_transmit_PLC,indent=4,ensure_ascii=False))
        print(params_transmit_PLC)
        params_simulation_calculate = result_simulation
        # 筛选出磨抛效果最好的一组
        params_simulation_16 = {}
        params_simulation_12 = {}
        params_simulation_8 = {}
        params_simulation_4 = {}
        for i in params_simulation_calculate:
            if i['lineEdit_num_output'] == 16:
                params_simulation_16 = i
                break
            elif i['lineEdit_num_output'] == 12:
                params_simulation_12 = i
                break
            elif i['lineEdit_num_output'] == 8:
                params_simulation_8 = i
                break
            elif i['lineEdit_num_output'] == 4:
                params_simulation_4 = i
        if len(params_simulation_16) != 0:
            params_simulation = params_simulation_16
        elif len(params_simulation_12) != 0:
            params_simulation = params_simulation_12
        elif len(params_simulation_8) != 0:
            params_simulation = params_simulation_8
        elif len(params_simulation_4) != 0:
            params_simulation = params_simulation_4
        else:
            params_simulation = params_simulation_calculate[0]
        # 计算结果-数据集更新(界面参数与展示的动画仿真同步)
        self.double_parameter_intelligent.update(params_simulation)
        # 静态动画参数输入
        # params.update({'mode': 'self_order', 'fig': self.canvas.fig,'fig_2': self.canvas_animation.fig,'animation_name':animation_name})
        # 动态动画参数输入
        params_simulation.update({'mode': 'self_order', 'fig': self.canvas.fig, 'animation_name': animation_name})
        self.worker_thread_plot = DoubleWorkerThread(**params_simulation)
        self.worker_thread_plot.result_signal.connect(self.double_intelligent_thread_signal)  # 连接子线程的信号
        self.worker_thread_plot.start()  # 启动子线程

    # 同步摆-智能计算-子进程信号接收函数
    def equal_intelligent_thread_signal(self, result):
        self.timer.stop()
        self.status_label.setText("【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算完毕，请查看计算结果。")

        # 静态动画显示
        # self.canvas.draw()
        # self.canvas_animation.draw()  # 新增（静态轨迹动画）

        # 动态动画显示
        self.canvas.draw()
        # 清空 QLabel 中的内容
        self.animation_QLabel.clear()
        # 释放旧的 QMovie 对象
        if hasattr(self, 'movie') and self.movie is not None:
            self.movie.stop()
            self.movie.deleteLater()
        # 释放旧的 QMovie 对象
        if hasattr(self, 'movie2') and self.movie2 is not None:
            self.movie2.stop()
            self.movie2.deleteLater()
        # 创建新的 QMovie 对象并设置到 QLabel
        animation_name = result[1]
        # self.movie = QMovie(ani)
        # self.animation_QLabel.setMovie(self.movie)
        # 加载GIF动画
        self.movie = QMovie('./animation/' + animation_name + '_1.gif')
        self.movie2 = QMovie('./animation/' + animation_name + '_2.gif')
        self.movie.updated.connect(self.updated)
        # self.movie.setloopCount(1)  # 设置只播放一次
        self.animation_QLabel.setMovie(self.movie)
        # 启动新的动画
        self.movie.start()

        button_enable(self.button_list)
        # 参数集更新

        self.equal_parameter_intelligent['lineEdit_coefficient'] = result[0]
        # 字符转换
        dict_value_to_str(self.equal_parameter_intelligent)
        # self.motion_out_param_frame.content_down_layout.set_line_edit_value(i, self.equal_parameter_intelligent[i])
        # 界面输出参数赋值
        for i in self.motion_out_param_line_edit_names:
            self.motion_out_param_frame.content_up_layout.set_line_edit_value(i,self.equal_parameter_intelligent[i])
        for i in self.motion_out_param_line_edit_names_2:
            self.motion_out_param_frame.content_down_layout.set_line_edit_value(i,self.equal_parameter_intelligent[i])
        self.equal_parameter_intelligent['lineEdit_accelerate']#加速度
        self.equal_parameter_intelligent['lineEdit_beam_swing_speed']#摆动速度
        self.equal_parameter_intelligent['lineEdit_beam_constant_time']#匀速摆动时间
        self.equal_parameter_intelligent['lineEdit_stay_time_output']#边部停留时间
        # 从字典中获取各个参数并转换为float类型
        accelerate = float(self.equal_parameter_intelligent['lineEdit_accelerate'])
        beam_swing_speed = float(self.equal_parameter_intelligent['lineEdit_beam_swing_speed'])
        beam_constant_time = float(self.equal_parameter_intelligent['lineEdit_beam_constant_time'])
        stay_time_output = float(self.equal_parameter_intelligent['lineEdit_stay_time_output'])

        # 根据公式进行计算
        result = 60 / (beam_constant_time * 2 + stay_time_output * 2 + beam_swing_speed / accelerate * 4)
        result_str = "{:.4f}".format(result)
        self.motion_out_param_frame.content_down_layout.set_line_edit_value('lineEdit_frequency', result_str)
    # 同步摆-方案验证-子进程信号接收函数
    def equal_manual_thread_signal(self, result):
        self.timer.stop()
        self.status_label.setText("【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算完毕，请查看计算结果。")
        # 静态动画显示
        # self.canvas.draw()
        # self.canvas_animation.draw()  # 新增（静态轨迹动画）

        # 动态动画显示
        self.canvas.draw()
        # 清空 QLabel 中的内容
        self.animation_QLabel.clear()
        # 释放旧的 QMovie 对象
        if hasattr(self, 'movie') and self.movie is not None:
            self.movie.stop()
            self.movie.deleteLater()
        # 释放旧的 QMovie 对象
        if hasattr(self, 'movie2') and self.movie2 is not None:
            self.movie2.stop()
            self.movie2.deleteLater()
        # 创建新的 QMovie 对象并设置到 QLabel
        animation_name = result[1]
        # self.movie = QMovie(ani)
        # self.animation_QLabel.setMovie(self.movie)
        # 加载GIF动画
        self.movie = QMovie('./animation/' + animation_name + '_1.gif')
        self.movie2 = QMovie('./animation/' + animation_name + '_2.gif')
        self.movie.updated.connect(self.updated)
        # self.movie.setloopCount(1)  # 设置只播放一次
        self.animation_QLabel.setMovie(self.movie)
        # 启动新的动画
        self.movie.start()

        button_enable(self.button_list)
        # 参数集更新
        self.equal_parameter_manual['lineEdit_coefficient'] = result[0]
        # 字符转换
        dict_value_to_str(self.equal_parameter_manual)
        # 界面输出参数赋值
        for i in self.motion_out_param_param_manual_line_edit_names_2:
            self.motion_input_out_param_manual_frame.content_middle_layout.set_line_edit_value(i,self.equal_parameter_manual[i])
        for i in self.motion_out_param_param_manual_line_edit_names_3:
            self.motion_input_out_param_manual_frame.content_bottom_layout.set_line_edit_value(i,self.equal_parameter_manual[i])

    # 动画切换函数
    def updated(self):
        if self.movie.currentFrameNumber() == self.movie.frameCount() - 1:
            self.movie.stop()
            self.animation_QLabel.setMovie(self.movie2)
            self.movie2.start()
    # 新增：“整线配置”按钮的槽函数
    def open_line_config_dialog(self):
        """
        打开整线配置对话框，并在保存成功后刷新主窗口的参数实例变量。
        """
        print("“整线配置”按钮被点击！正在打开新窗口...")
        dialog = WholeLineConfigDialog(self)

        # 打开对话框并等待其关闭
        result = dialog.exec()

        # 只有当用户点击了“保存配置”按钮（对话框返回 Accepted）时，才执行刷新
        if result == QDialog.DialogCode.Accepted:
            print("检测到配置已保存，正在刷新主窗口的参数...")

            # --- 核心步骤：重新加载配置到 self.whole_line_params ---
            self.whole_line_params = self.config_manager.load_config()

            # 现在，self.whole_line_params 已经是最新版本了
            # 我们可以安全地使用它
            print("\n--- 主窗口的 self.whole_line_params 已刷新为最新值 ---")
            # print(json.dumps(self.whole_line_params, indent=4, ensure_ascii=False))

            # 例如，更新状态栏以示反馈
            machine_count = self.whole_line_params.get('global', {}).get('machine_count', 0)
            self.status_label.setText(f"整线配置更新成功，共 {machine_count} 台设备。")
        else:
            print("用户取消了配置，主窗口参数未作修改。")


    # 编辑框值发生变化时，值同步到参数集合中-监听
def line_eidt_textchange(name, text, list):
    list[name] = text
    # 实时更新住皮带速度
    if belt_speed_value_empty(list):
        list['lineEdit_belt_speed'] = belt_speed_calculate(list)

# 当有计算运行时，屏蔽其他按钮功能
def button_disable(button_list):
    for button in button_list:
        button.setEnabled(False)

# 计算完毕，按钮恢复正常
def button_enable(button_list):
    for button in button_list:
        button.setEnabled(True)

# 将字典中所有的值转换为数值类型
def dict_value_to_float(my_dict):
    dict_keys = my_dict.keys()
    for key in dict_keys:
        if my_dict[key] != '' and my_dict[key] is not None and not isinstance(my_dict[key], list):
            my_dict[key] = float(my_dict[key])
    return my_dict

# 将字典中所有的值转换为字符类型
def dict_value_to_str(my_dict):
    dict_keys = my_dict.keys()
    for key in dict_keys:
        if my_dict[key] != '' and my_dict[key] is not None and not isinstance(my_dict[key], list):
            my_dict[key] = str(my_dict[key])
    return my_dict

# 判断计算主皮带速度的值是否为空
def belt_speed_value_empty(my_dict):
    line_edit_names = ["lineEdit_work_time","lineEdit_production_volume", "lineEdit_ceramic_width"]
    for i in line_edit_names:
        if my_dict[i] == '':
            return False
        else:
            continue
    return True

# 计算主皮带速度
def belt_speed_calculate(my_dict):
    line_edit_names = ["lineEdit_work_time", "lineEdit_production_volume", "lineEdit_ceramic_width"]
    work_time = float(my_dict["lineEdit_work_time"])
    # print(my_dict["lineEdit_production_volume"])
    volume = float(my_dict["lineEdit_production_volume"])
    ceramic_width = float(my_dict["lineEdit_ceramic_width"])
    # 产量 = 主皮带速度 * 进砖宽度 * 工作时长
    belt_speed = round(volume/ceramic_width/work_time/0.0036,2)
    return str(belt_speed)
