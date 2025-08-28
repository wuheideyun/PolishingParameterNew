# 双头摆争先优化函数
import numpy as np
import math
import time as te
from PySide6.QtCore import Qt, Signal, QThread
# 构建子线程计算
class Double_self_whole_line_Thread(QThread):
    result_signal = Signal(list,list)  # 创建一个信号用于传递结果
    def __init__(self, v1,R,ceramic_width,mo,between,beam_between,head_count,a):
        super().__init__()
        self.v1 = v1
        self.R = R
        self.ceramic_width = ceramic_width
        self.mo = mo
        self.between = between
        self.beam_between = beam_between
        self.a = a
        self.head_count = head_count
    def run(self):
        all_params_gather, unique_items_gather_simulation_calculate = self.self_define_calculate_whole_line()
        self.result_signal.emit(all_params_gather,unique_items_gather_simulation_calculate)
    # 整线计算策略
    def self_define_calculate_whole_line(self):
        # 为了单次传入多个参数，传入的参数为整线的参数集合（列表）
        all_params_gather = []
        # 用于存储仿真计算的参数
        unique_items_gather_simulation_calculate = []
        # 抛光机数目
        machine_count = len(self.between)
        for i in range(0, machine_count):  # 第一台机至第四台机 进行循环迭代
            single_machine_params_gather = []
            # 存放第一台机 同粒度磨头数排布（eg.[4,6,4]）
            single_machine_head_gather = self.head_count[i]
            # 若出现奇数个磨头，对当前同粒度磨头数排布进行调整
            for k in single_machine_head_gather:
                if k % 2 == 0:
                    continue
                else:
                    if sum(single_machine_head_gather) == 16:
                        single_machine_head_gather = [16]
                    else:
                        single_machine_head_gather = [12, sum(single_machine_head_gather) - 12]
                    break
            # 统计单台机 同粒度磨头数有几种情况
            unique_count = len(set(single_machine_head_gather))
            # 如果想查看具体有哪些不同的数据--（注意转换为列表）
            unique_items = list(set(single_machine_head_gather))
            # 计算单台机 不同 同粒度磨头数目 的运动参数
            machine_between = self.between[i]
            machine_beam_between = self.beam_between[i]
            # 用于存储传输至PLC的数据
            unique_items_gather_transmission_PLC = {}
            params_2 = []
            for j in range(0, unique_count):
                num = unique_items[j]
                if num == 2:
                    params_1 = self.self_define_calculate_new()
                else:
                    params_1, params_2 = self.self_define_calculate_speed_boost(machine_between, machine_beam_between, num)
                unique_items_gather_transmission_PLC[num] = params_1
                unique_items_gather_simulation_calculate.append(params_2)
            # 参数匹配
            for j in range(0, len(single_machine_head_gather)):
                current_num = single_machine_head_gather[j]
                single_machine_params_gather.append(unique_items_gather_transmission_PLC[current_num])
            all_params_gather.append(single_machine_params_gather)
        return all_params_gather, unique_items_gather_simulation_calculate
    # 备用整线计算策略
    def self_define_calculate_whole_line_option_1(self):
        # 全局变量
        # global v1,R,ceramic_width,mo
        machine_count = len(self.between)
        # 用于存储仿真计算的参数
        unique_items_gather_simulation_calculate = []
        # 为了单次传入多个参数，传入的参数为整线的参数集合（列表）
        all_params_gather = []
        for i in range(0, machine_count):  # 第一台机至第四台机 进行循环迭代
            single_machine_params_gather = []
            # 存放第一台机 同粒度磨头数排布（eg.[4,6,4]）
            single_machine_head_gather = self.head_count[i]
            # 按照双头摆抛光机的加工特性 ， 直接给出最优磨头摆布
            single_machine_head_gather_sum = sum(single_machine_head_gather)
            if single_machine_head_gather_sum == 16:
                single_machine_head_gather = [16]
            elif single_machine_head_gather_sum == 14:
                single_machine_head_gather = [12, 2]
            else:
                single_machine_head_gather = [12, sum(single_machine_head_gather) - 12]
            # 统计单台机 同粒度磨头数有几种情况（1 或 2）
            unique_count = len(set(single_machine_head_gather))
            # 如果想查看具体有哪些不同的数据--（注意转换为列表）
            unique_items = list(set(single_machine_head_gather))
            # 计算单台机 不同 同粒度磨头数目 的运动参数
            machine_between = self.between[i]
            machine_beam_between = self.beam_between[i]
            # 用于存储传输至PLC的数据
            unique_items_gather_transmission_PLC = {}
            params_2 = []
            for j in range(0, unique_count):
                num = unique_items[j]
                if num == 2:
                    params_1 = self.self_define_calculate_new()
                else:
                    params_1, params_2 = self.self_define_calculate_speed_boost(machine_between, machine_beam_between,
                                                                                num)
                unique_items_gather_transmission_PLC[num] = params_1
                if len(params_2) != 0:
                    unique_items_gather_simulation_calculate.append(params_2)
            # 参数匹配
            for j in range(0, len(single_machine_head_gather)):
                current_num = single_machine_head_gather[j]
                single_machine_params_gather.append(unique_items_gather_transmission_PLC[current_num])
            all_params_gather.append(single_machine_params_gather)
        return all_params_gather, unique_items_gather_simulation_calculate
    # 自定义计算（提升摆动速度）
    def self_define_calculate_speed_boost(self,between, beam_between, num):
        # 定义全局变量
        # global v1,ceramic_width,R,mo
        B = self.ceramic_width + 200 - 2 * self.R
        # 赋默认值
        delay_time = 0
        self_delay_time = 0
        # 自动将磨头数进行划分
        if num % 4 == 0 and num / 4 != 1:
            group = num / 4
            num = 4
        else:
            group = 1

        params_gather = []  # 存放参数集
        for i in np.arange(0.1, 2.1, 0.1):  # 新增循环迭代，通过调整边部停留时间来寻得 横梁摆动速度分布
            t2 = round(float(i), 2)
            # --------------------横梁摆动提速策略--间距为 0.5*磨头间距------------------------
            distance_period = 2 * between  # between/(num/2) * num
            t_all = round(distance_period / self.v1, 2)
            # 边部停留时间设定
            t_a_in = (t_all - 2 * t2) / 2
            # t_a 加速时间
            # t_e 匀速时间
            # H 摆幅
            # t_总=2*t_a+t_e
            # f=a*t_a^2-a*t_a*t_总+H
            par_a = self.a
            par_b = -self.a * t_a_in
            par_c = B
            if par_b ** 2 - 4 * par_a * par_c >= 0:
                t_a = (-par_b - (par_b ** 2 - 4 * par_a * par_c) ** 0.5) / (2 * self.a)
                delay_time = round((beam_between - 1 / (num / 2) * between) / self.v1, 2)
                if group > 1:
                    self_delay_time = round(1 / (num / 2) * between / group / self.v1, 2)
                else:
                    self_delay_time = 0
            else:
                t_a = 0
            # -----------------------------------------------------------------------

            # -------------------常规计算--间距为单倍磨头间距-----------------------------
            if t_a == 0:  # 说明高速策略无解
                distance_period = between * num
                t_all = round(distance_period / self.v1, 2)
                # 边部停留时间设定
                t_a_in = (t_all - 2 * t2) / 2
                # t_a 加速时间
                # t_e 匀速时间
                # H 摆幅
                # t_总=2*t_a+t_e
                # f=a*t_a^2-a*t_a*t_总+H
                par_a = self.a
                par_b = -self.a * t_a_in
                par_c = B
                if par_b ** 2 - 4 * par_a * par_c >= 0:
                    t_a = (-par_b - (par_b ** 2 - 4 * par_a * par_c) ** 0.5) / (2 * self.a)
                    delay_time = round((beam_between - 2 * between) / self.v1, 2)
                    if group > 1:
                        self_delay_time = round(0.5 * between / group / self.v1, 2)
                    else:
                        self_delay_time = 0
                else:
                    # t_a=t_a_in/2
                    t_a = 0
                    ValueError('The swing cannot reach the set value!')
            # ------------------------------------------------------------------------

            # ------------------------均匀分布策略--------------------------------------
            '''
            if t_a == 0:   # 说明常规策略也无解
                t2 = 0 # 减小边部停留时间，此时应为有解
                distance_period = between * num
                t_all = round(distance_period / v1, 2)
                # 边部停留时间设定
                t_a_in = (t_all - 2 * t2) / 2
                # t_a 加速时间
                # t_e 匀速时间
                # H 摆幅
                # t_总=2*t_a+t_e
                # f=a*t_a^2-a*t_a*t_总+H
                par_a = a
                par_b = -a * t_a_in
                par_c = B
                if par_b ** 2 - 4 * par_a * par_c >= 0:
                    t_a = (-par_b - (par_b ** 2 - 4 * par_a * par_c) ** 0.5) / (2 * a)
                    delay_time = round((beam_between - 2 * between) / v1, 2)
                    self_delay_time = round(between / group / v1, 2)
                else:
                    # t_a=t_a_in/2
                    t_a = 0
                    ValueError('The swing cannot reach the set value!')
            '''
            # -------------（此刻再无解，说明用户输入参数不合理）--------------------------
            # t1 = t_a  # 加速时间
            t1 = round(t_a_in - 2 * t_a, 2)
            v2 = round(self.a * t_a, 2)
            # delay_time=round((beam_between-2*between)/v1,2)
            # self_delay_time=round(between/group/v1,2)
            # 多组磨头叠加延时时间计算
            delay_time_self_list = []
            for i in range(0, round(num / 2 * group)):
                current_delay_time = round(i * delay_time, 2)
                if (i * 2 / num) >= 1:
                    current_delay_time += math.floor(i * 2 / num) * self_delay_time
                delay_time_self_list.append(round(current_delay_time, 2))
            # 参数集
            params = {}
            params.update(
                {'lineEdit_belt_speed': self.v1, 'lineEdit_beam_swing_speed': v2, 'lineEdit_beam_constant_time': t1,
                 'lineEdit_stay_time_output': t2
                    , 'lineEdit_num_input': num, 'lineEdit_num_output': num * group, 'lineEdit_delay_time': delay_time,
                 'lineEdit_delay_time_list': delay_time_self_list
                    , 'lineEdit_stay_time_input': t2, 'lineEdit_swing': round(self.a * t_a ** 2 + v2 * t1, 2),
                 'lineEdit_ceramic_width': self.ceramic_width, 'lineEdit_group_count': group
                    , 'lineEdit_between': between, 'lineEdit_beam_between': beam_between, 'R': self.R,
                 'lineEdit_accelerate': self.a, 'self_delay_time': self_delay_time, 'lineEdit_grind_length': self.mo})
            params_gather.append(params)

        # ---------------------计算完毕，进行数据处理与筛选---------------------
        # 筛选出摆动速度值大于0的字典
        filtered_params_gather = [item for item in params_gather if item["lineEdit_beam_swing_speed"] > 0]
        # 按值降序排序
        sorted_data_params_gather = sorted(filtered_params_gather, key=lambda x: x["lineEdit_beam_swing_speed"],
                                           reverse=True)
        # 为降低计算时间，仅筛选前四组数据进行计算比较
        final_params_gather = sorted_data_params_gather[:5]
        # 计算均匀系数，将均匀系数最优的参数集筛选出来
        for i in final_params_gather:
            PDT = PolishingDistributionThread(**i)
            object_matrix, result = PDT.emit()
            i.update({'lineEdit_coefficient': result})
        # 筛选出最佳结果
        sorted_final_params_gather = sorted(final_params_gather, key=lambda x: x["lineEdit_coefficient"],
                                            reverse=False)
        final_params = sorted_final_params_gather[0]
        '''
        # 增加小砖算法
        if ceramic_width <= 800:
            if v2 <= 200:       # 若横梁摆动速度小于200则判定摆动速度过慢
                num_small = 2  # 针对小砖缩短单周期长度
                group_small  = num / 2  # 针对小砖增多叠加次数
                B = ceramic_width + 200 - 2 * R
                distance_period = between * num_small
                t_all = round(distance_period / v1, 2)
                # 边部停留时间设定
                t_a_in = (t_all - 2 * t2) / 2
                # t_a 加速时间
                # t_e 匀速时间
                # H 摆幅
                # t_总=2*t_a+t_e
                # f=a*t_a^2-a*t_a*t_总+H
                par_a = a
                par_b = -a * t_a_in
                par_c = B
                if par_b ** 2 - 4 * par_a * par_c >= 0:
                    t_a = (-par_b - (par_b ** 2 - 4 * par_a * par_c) ** 0.5) / (2 * a)
                else:
                    t_a = t_a_in / 2
                    ValueError('The swing cannot reach the set value!')
                # t1 = t_a  # 加速时间
                t1 = round(t_a_in - 2 * t_a, 2)
                v2 = round(a * t_a, 2)
                delay_time = round((beam_between - 2 * between) / v1, 2)
                self_delay_time = round(between / group_small*2 / v1, 2)
                # 多组磨头叠加延时时间计算
                delay_time_self_list = []
                for i in range(0, round(num_small / 2 * group_small)):
                    current_delay_time = round(i * delay_time, 2)
                    if (i * 2 / num_small) >= 1:
                        current_delay_time += math.floor(i * 2 / num_small) * self_delay_time
                    delay_time_self_list.append(round(current_delay_time, 2))
                # 参数集
                params = {}
                params.update(
                            {'lineEdit_belt_speed': v1, 'lineEdit_beam_swing_speed': v2, 'lineEdit_beam_constant_time': t1, 'lineEdit_stay_time_output': t2
                            ,'lineEdit_num_input':num, 'lineEdit_num_output': num_small*group_small, 'lineEdit_delay_time': delay_time, 'lineEdit_delay_time_list': delay_time_self_list
                            ,'lineEdit_stay_time_input':t2,'lineEdit_swing': round(a*t_a**2+v2*t1,2), 'lineEdit_ceramic_width': ceramic_width
                            ,'lineEdit_group_count':group, 'lineEdit_between': between, 'lineEdit_beam_between': beam_between, 'R': R
                            , 'lineEdit_accelerate': a,'self_delay_time':self_delay_time,'lineEdit_grind_length':mo})
        '''
        # 对计算出的结果进行处理（1.方便数据传输到PLC；2.方便数据传输至仿真动画计算端）
        keys_to_extract = ['lineEdit_belt_speed', 'lineEdit_beam_swing_speed', 'lineEdit_accelerate',
                           'lineEdit_stay_time_output'
            , 'lineEdit_swing', 'lineEdit_delay_time_list']
        # 使用字典推导式提取指定键
        final_params_transmission_PLC = {key: final_params[key] for key in keys_to_extract if key in final_params}
        final_params_transmission_PLC['mode'] = 'order'
        # 参数 final_params 用于仿真计算
        return final_params_transmission_PLC, final_params
    # 当磨头数小于等于 2 -计算单组参数
    def self_define_calculate_new(self):
        # 定义全局变量
        # global v1, ceramic_width, R, mo
        B = self.ceramic_width + 200 - 2 * self.R
        v2_max = (B / self.a) ** 0.5 * self.a
        # # 根据磨头间距、皮带速度计算单周期时间
        # period_time = between * num / v1
        # t2 = between * 0.6 / v1
        v2 = round(v2_max * 0.95, 2)
        t_a = round(v2 / self.a, 2)
        t_e = round((B - self.a * t_a ** 2) / v2, 2)
        t2 = round(0.2 * (2 * t_a + t_e), 2)
        period_time = (2 * t_a + t_e + t2) * 2

        group = 1
        delay_time = 0
        self_delay_time = 0
        delay_time_self_list = [0]

        # params = {'lineEdit_belt_speed': v1, 'lineEdit_beam_swing_speed': v2, 'lineEdit_beam_constant_time': t_e,'lineEdit_stay_time_output': t2
        #     , 'lineEdit_num_input': num, 'lineEdit_num_output': num * group, 'lineEdit_delay_time': delay_time,'lineEdit_delay_time_list': delay_time_self_list
        #     , 'lineEdit_stay_time_input': t2, 'lineEdit_swing': round(a * t_a ** 2 + v2 * t_e, 2),'lineEdit_ceramic_width': ceramic_width, 'lineEdit_group_count': group
        #     , 'lineEdit_between': between, 'lineEdit_beam_between': beam_between, 'R': R, 'lineEdit_accelerate': a, 'self_delay_time': self_delay_time, 'lineEdit_grind_length': mo}
        params = {'lineEdit_belt_speed': self.v1, 'lineEdit_beam_swing_speed': v2, 'lineEdit_stay_time_output': t2
            , 'lineEdit_delay_time_list': delay_time_self_list, 'lineEdit_swing': round(self.a * t_a ** 2 + v2 * t_e, 2),
                  'lineEdit_accelerate': self.a}

        return params




# 引入均匀系数计算
class PolishingDistributionThread():
    def __init__(self, **kwargs):
        # 基本运动参数
        self.v1 = round(kwargs.get('lineEdit_belt_speed', 0), 2)
        self.v2 = round(kwargs.get('lineEdit_beam_swing_speed', 0), 2)
        self.constant_time = round(kwargs.get('lineEdit_beam_constant_time', 0), 2)
        self.stay_time = round(kwargs.get('lineEdit_stay_time_output', 0), 2)
        self.a = round(kwargs.get('lineEdit_accelerate', 650), 2)
        self.between = round(kwargs.get('lineEdit_between', 0), 2)
        self.beam_between = round(kwargs.get('lineEdit_beam_between', 0), 2)
        self.num = kwargs.get('lineEdit_num_input', 0)
        self.R = kwargs.get('R', 270)
        self.mo = kwargs.get('lineEdit_grind_length', 150)
        # 顺序摆参数
        self.delay_time = kwargs.get('self_delay_time', 0)
        # 自定义计算参数
        self.group = kwargs.get('lineEdit_group_count', 0)
        if self.group >= 2:
            # 当前模式
            self.mode = 'self_order'
        else:
            self.mode = 'order'

        self.w = 600  # 转速
        accelerate_t = round(self.v2 / self.a, 2)
        self.t1 = accelerate_t
        self.t2 = self.constant_time
        self.t3 = accelerate_t
        self.t4 = self.stay_time
        self.t5 = accelerate_t
        self.t6 = self.constant_time
        self.t7 = accelerate_t
        self.t8 = self.stay_time
        self.period = self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6 + self.t7 + self.t8

        cover_width = math.ceil(math.ceil(self.v2 * self.t2 + self.a * self.t1 ** 2 + 2 * self.R))
        x_plus = cover_width * 8
        self.n = math.ceil(x_plus / (self.period * self.v1)) + 3

        self.c_length_cell = 10  # 统计区域长度最小单位
        self.c_width_cell = 10  # 统计区域宽度最小单位

        # 以10*10为最小单位 ，将瓷砖离散化，以每个格子的中心作为每个格子的坐标(0.5,0.5)
        c_length = math.ceil(self.v1 * self.period * self.n + 2 * self.R + 50)  # 统计区域长度
        c_width = math.ceil(self.v2 * self.t2 + self.a * self.t1 ** 2 + 2 * self.R + 100)  # 统计区域宽度

        self.c_length_percell = round(
            math.ceil(self.v1 * self.period + 2 * self.R + 100) / self.c_length_cell)  # 统计区域长度方向总单元格数目
        self.c_length_mulcell = round(c_length / self.c_length_cell)  # 统计区域长度方向总单元格数目
        self.c_width_mulcell = round(c_width / self.c_width_cell)  # 统计区域宽度方向总单元格数目

    # 输出端口
    def emit(self):
        self.mod_rho, self.mod_theta = self.mod_information_calculate()
        matrix_results = self.polishing_cal()

        if self.mode == 'order':
            object_matrix, result = self.order_matrix_cal(matrix_results)
        elif self.mode == 'self_order':
            object_matrix, result = self.self_order_matrix_cal(matrix_results)
        else:   # 输出空集
            object_matrix = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
            result = 0

        return object_matrix, result

    def mod_information_calculate(self):
        size = 0.01  # 时间步长
        # 磨块离散化计算   以磨块 长 64mm 宽 110mm 为例
        # 仅仅计算单磨头，为了减少计算量，后续磨头直接进行叠加；
        mod_length = 64  # 磨块长度
        mod_width = self.mo  # 磨块宽度

        mod_width_cell = 5  # 磨块单元（宽度）
        mod_length_cell = 4  # 磨块单元（长度）

        mod_width_mulcell = math.floor(mod_width / mod_width_cell)  # 磨块宽度方向单元格总数量
        mod_length_mulcell = math.floor(mod_length / mod_length_cell)  # 磨块长度方向单元格总数量

        mod_x = np.zeros((mod_width_mulcell, mod_length_mulcell))
        mod_y = np.zeros((mod_width_mulcell, mod_length_mulcell))
        # 储存坐标(仅需要极径长度和角度,以坐标原点为磨头中心)
        for i in range(0, mod_length_mulcell):
            mod_x[:, i] = -mod_length / 2 + mod_length_cell / 2 + (i - 1) * mod_length_cell
        for i in range(0, mod_width_mulcell):
            mod_y[i, :] = mod_width - mod_width_cell / 2 - (i - 1) * mod_width_cell
        mod_y = mod_y + self.R - self.mo  # 第一个磨块位置
        # 计算单个磨块
        mod_rho = np.zeros((mod_width_mulcell, mod_length_mulcell))  # 储存单个磨块极径
        mod_theta = np.zeros((mod_width_mulcell, mod_length_mulcell))  # 储存单个磨粒角度
        # 计算磨块各个点离磨头中心距离  角度
        for i in range(0, mod_width_mulcell):
            for j in range(0, mod_length_mulcell):
                mod_rho[i, j] = (mod_x[i, j] ** 2 + mod_y[i, j] ** 2) ** 0.5
                mod_theta[i, j] = math.atan(mod_y[i, j] / mod_x[i, j])
                if mod_theta[i, j] < 0:
                    mod_theta[i, j] = math.pi + mod_theta[i, j]
        return mod_rho, mod_theta

    # 顺序摆模式计算
    def order_matrix_cal(self, H_all):
        sin_period = math.floor((2 * self.R + self.period * self.v1) / self.c_length_cell)  # 单个周期累加区域
        mid_period = math.floor((self.period * self.v1) / self.c_length_cell)  # 递增宽度
        H_period = H_all[:, 5:5 + sin_period]
        H_mid = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        for i in range(0, self.n):
            H_mid[:, i * mid_period:i * mid_period + sin_period] = H_mid[:,
                                                                   i * mid_period:i * mid_period + sin_period] + H_period
        # 多磨头叠加
        mul_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        between_cell = math.floor(self.between / self.c_length_cell)
        delay_cell = math.floor(self.delay_time * self.v1 / self.c_length_cell)
        for i in range(0, 2):
            mul_H[:, between_cell * i:self.c_length_mulcell - 1] = (
                    mul_H[:, between_cell * i:self.c_length_mulcell - 1] +
                    H_mid[:, 0:self.c_length_mulcell - between_cell * i - 1])
        num_two = math.floor(self.num / 2)
        all_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        beam_between_cell = math.floor(self.beam_between / self.c_length_cell)
        for i in range(0, num_two):
            all_H[:, (beam_between_cell - delay_cell) * i:self.c_length_mulcell - 1] = (
                    all_H[:, (beam_between_cell - delay_cell) * i:self.c_length_mulcell - 1] +
                    mul_H[:, 0:self.c_length_mulcell - (beam_between_cell - delay_cell) * i - 1])
        # 计算 抛磨变异系数
        # 如果要计算此模块，周期数必须大于等于3
        cover_width = math.ceil(math.ceil(self.v2 * self.t2 + self.a * self.t1 ** 2 + 2 * self.R) / 10)
        begin_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2)
        terminate_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2) + cover_width

        cover_length = cover_width * 4
        begin_length = math.ceil((50 + self.v1 * 3 * self.period) / 10)
        terminate_length = begin_length + cover_length

        object_matrix = all_H[begin_width + 1:terminate_width, begin_length + 1:terminate_length]
        equal_subsample = np.mean(object_matrix)  # 子样平均数
        middle_matrix = np.power(object_matrix, 2) - np.power(equal_subsample, 2)
        variance_matrix = np.mean(middle_matrix)  # 子样方差
        result = format(variance_matrix ** 0.5 / equal_subsample, '.4f')  # 抛磨变异系数
        return object_matrix, result

    # 自定义模式计算
    def self_order_matrix_cal(self, H_all):
        sin_period = math.floor((2 * self.R + self.period * self.v1) / self.c_length_cell)  # 单个周期累加区域
        mid_period = math.floor((self.period * self.v1) / self.c_length_cell)  # 递增宽度
        H_period = H_all[:, 5:5 + sin_period]
        H_mid = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        for i in range(0, self.n):
            H_mid[:, i * mid_period:i * mid_period + sin_period] = H_mid[:,
                                                                   i * mid_period:i * mid_period + sin_period] + H_period
        # 多磨头叠加
        mul_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        between_cell = math.floor(self.between / self.c_length_cell)
        delay_cell = math.floor(self.delay_time * self.v1 / self.c_length_cell)
        for i in range(0, 2):
            mul_H[:, between_cell * i:self.c_length_mulcell - 1] = (
                    mul_H[:, between_cell * i:self.c_length_mulcell - 1] +
                    H_mid[:, 0:self.c_length_mulcell - between_cell * i - 1])
        num_two = math.floor(self.num / 2)
        all_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        beam_between_cell = math.floor(self.beam_between / self.c_length_cell)
        for i in range(0, num_two):
            all_H[:, (beam_between_cell - delay_cell) * i:self.c_length_mulcell - 1] = (
                    all_H[:, (beam_between_cell - delay_cell) * i:self.c_length_mulcell - 1] +
                    mul_H[:, 0:self.c_length_mulcell - (beam_between_cell - delay_cell) * i - 1])
        # 组数叠加
        group = round(self.group)
        group_size = math.floor(self.between / self.group / self.c_length_cell)
        all_group_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        for i in range(0, group):
            all_group_H[:, group_size * i:self.c_length_mulcell - 1] = (
                    all_group_H[:, group_size * i:self.c_length_mulcell - 1] +
                    all_H[:, 0:self.c_length_mulcell - group_size * i - 1])
        # 计算 抛磨变异系数
        # 如果要计算此模块，周期数必须大于等于3
        # cover_length = math.ceil(math.ceil(v1 * period + 2 * R) / 10)
        cover_width = math.ceil(math.ceil(self.v2 * self.t2 + self.a * self.t1 ** 2 + 2 * self.R) / 10)
        begin_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2)
        terminate_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2) + cover_width

        cover_length = cover_width * 4
        begin_length = math.ceil((50 + self.v1 * 3 * self.period) / 10)
        terminate_length = begin_length + cover_length

        # object_matrix = np.zeros((terminate_width - begin_width, terminate_length - begin_length))
        object_matrix = all_group_H[begin_width + 1:terminate_width, begin_length + 1:terminate_length]

        equal_subsample = np.mean(object_matrix)  # 子样平均数
        middle_matrix = np.power(object_matrix, 2) - np.power(equal_subsample, 2)
        variance_matrix = np.mean(middle_matrix)  # 子样方差
        result = format(variance_matrix ** 0.5 / equal_subsample, '.4f')  # 抛磨变异系数
        return object_matrix, result

    def polishing_cal(self):
        # 赋值操作
        v1 = self.v1
        v2 = self.v2
        constant_t = self.constant_time
        stay_t = self.stay_time
        a = self.a
        R = self.R
        mod_rho = self.mod_rho
        mod_theta = self.mod_theta
        mo = self.mo
        # 计算
        accelerate_t = round(v2 / a, 2)
        t1 = accelerate_t
        t2 = constant_t
        t3 = accelerate_t
        t4 = stay_t
        t5 = accelerate_t
        t6 = constant_t
        t7 = accelerate_t
        t8 = stay_t
        period = 4 * accelerate_t + 2 * stay_t + 2 * constant_t
        # 计算
        w = 600  # 转速
        size = 0.01  # 时间步长
        n = 6
        mod_width_cell = 5  # 磨块单元（宽度）
        mod_length_cell = 4  # 磨块单元（长度）

        c_length_cell = 10  # 统计区域长度最小单位
        c_width_cell = 10  # 统计区域宽度最小单位

        mod_length = 64  # 磨块长度
        mod_width = mo  # 磨块宽度

        c_width = math.ceil(v2 * t2 + a * t1 ** 2 + 2 * R + 100)  # 统计区域宽度

        c_length_percell = round(math.ceil(v1 * period + 2 * R + 100) / c_length_cell)  # 统计区域长度方向（单周期）总单元格数目
        c_width_mulcell = round(c_width / c_width_cell)  # 统计区域宽度方向总单元格数目

        mod_width_mulcell = math.floor(mod_width / mod_width_cell)  # 磨块宽度方向单元格总数量
        mod_length_mulcell = math.floor(mod_length / mod_length_cell)  # 磨块长度方向单元格总数量

        H = np.zeros((c_width_mulcell, c_length_percell))  # 存放速度和
        time = np.arange(0, period, size)  # 时间变量
        end_time = math.floor(period / size)  # 单周期步长
        # 计算单个周期磨头抛磨量分布
        for k in range(0, end_time):
            t = time[k]  # 时间
            # 第一段
            if t >= 0 and t < t1:
                x_0 = v1 * t + R + 50
                y_0 = 0.5 * a * t ** 2 + R + 50
            elif t >= t1 and t < t1 + t2:
                # 第二段
                x_0 = v1 * t + R + 50
                y_0 = 0.5 * a * t1 ** 2 + v2 * (t - t1) + R + 50
            # 第三段
            elif t >= (t1 + t2) and t < (t1 + t2 + t3):
                x_0 = v1 * t + R + 50
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * (t - t1 - t2) - 0.5 * a * (t - t1 - t2) ** 2 + R + 50
            # 第四段
            elif t >= (t1 + t2 + t3) and t < (t1 + t2 + t3 + t4):
                x_0 = v1 * t + R + 50
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 + R + 50
            # 第五段
            elif t >= (t1 + t2 + t3 + t4) and t < (t1 + t2 + t3 + t4 + t5):
                x_0 = v1 * t + R + 50
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 - 0.5 * a * (
                        t - t1 - t2 - t3 - t4) ** 2 + R + 50
            # 第六段
            elif t >= (t1 + t2 + t3 + t4 + t5) and t < (t1 + t2 + t3 + t4 + t5 + t6):
                x_0 = v1 * t + R + 50
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 - 0.5 * a * t5 ** 2 - v2 * (
                        t - t1 - t2 - t3 - t4 - t5) + R + 50
            # 第七段
            elif t >= (t1 + t2 + t3 + t4 + t5 + t6) and t < (t1 + t2 + t3 + t4 + t5 + t6 + t7):
                x_0 = v1 * t + R + 50
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 - 0.5 * a * t5 ** 2 - v2 * t6 - v2 * (
                        t - t1 - t2 - t3 - t4 - t5 - t6) + 0.5 * a * (t - t1 - t2 - t3 - t4 - t5 - t6) ** 2 + R + 50
            # 第八段
            elif t >= (t1 + t2 + t3 + t4 + t5 + t6 + t7) and t <= (t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8):
                x_0 = v1 * t + R + 50
                y_0 = R + 50
            # 磨头中心速度方程
            v_x_0 = v1
            # 第一段
            if t >= 0 and t < t1:
                v_y_0 = a * t
            # 第二段
            elif t >= t1 and t < t1 + t2:
                v_y_0 = a * t1
            # 第三段
            elif t >= t1 + t2 and t < t1 + t2 + t3:
                v_y_0 = a * t1 - a * (t - t1 - t2)
            # 第四段
            elif t >= (t1 + t2 + t3) and t < (t1 + t2 + t3 + t4):
                v_y_0 = 0
            # 第五段
            elif t >= (t1 + t2 + t3 + t4) and t < (t1 + t2 + t3 + t4 + t5):
                v_y_0 = -a * (t - t1 - t2 - t3 - t4)
            # 第六段
            elif t >= (t1 + t2 + t3 + t4 + t5) and t < (t1 + t2 + t3 + t4 + t5 + t6):
                v_y_0 = -a * t5
            # 第七段
            elif t >= (t1 + t2 + t3 + t4 + t5 + t6) and t < (t1 + t2 + t3 + t4 + t5 + t6 + t7):
                v_y_0 = -a * t5 + a * (t - t1 - t2 - t3 - t4 - t5 - t6)
            # 第八段
            elif t >= (t1 + t2 + t3 + t4 + t5 + t6 + t7) and t <= (t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8):
                v_y_0 = 0
            # 计算磨粒
            for i_mod in range(0, 6):  # 磨块数为1-6
                for i_width in range(0, mod_width_mulcell):
                    for i_length in range(0, mod_length_mulcell):
                        r = mod_rho[i_width, i_length]
                        theta_1 = mod_theta[i_width, i_length] + i_mod * math.pi / 3
                        # 磨粒运动轨迹方程
                        theta = w * math.pi / 30 * t
                        x = r * math.cos(theta) * math.cos(theta_1) + r * math.sin(theta) * math.sin(theta_1) + x_0
                        y = -r * math.sin(theta) * math.cos(theta_1) + r * math.cos(theta) * math.sin(theta_1) + y_0
                        # 磨粒速度方程
                        v_x = -r * w * math.pi / 30 * math.sin(w * math.pi / 30 * t + theta_1) - v_x_0
                        v_y = r * w * math.pi / 30 * math.cos(w * math.pi / 30 * t + theta_1) + v_y_0
                        v_common = ((v_x ** 2 + v_y ** 2) ** 0.5)
                        # 判断该点所在磨削区域的单元
                        m_x = math.ceil(x / c_length_cell)
                        m_y = math.ceil(y / c_width_cell)
                        H[m_y, m_x] = H[m_y, m_x] + v_common  # 统计各个磨削区域速度和
        return H
# -----自定义计算（提升摆动速度）--计算单组参数--------------------------------
def self_define_calculate_speed_boost(v1,R,ceramic_width,mo,between,beam_between,a,num):
    # 定义全局变量
    # global v1,ceramic_width,R,mo
    B=ceramic_width+200-2*R
    # 赋默认值
    delay_time = 0
    self_delay_time = 0
    # 自动将磨头数进行划分
    if num % 4 == 0 and num / 4 != 1:
        group = num / 4
        num = 4
    else:
        group = 1

    params_gather = []  # 存放参数集
    for i in np.arange(0.1,2.1,0.1):   # 新增循环迭代，通过调整边部停留时间来寻得 横梁摆动速度分布
        t2 = round(float(i),2)
        # --------------------横梁摆动提速策略--间距为 0.5*磨头间距------------------------
        distance_period = 2 * between  # between/(num/2) * num
        t_all = round(distance_period / v1, 2)
        # 边部停留时间设定
        t_a_in = (t_all - 2 * t2) / 2
        # t_a 加速时间
        # t_e 匀速时间
        # H 摆幅
        # t_总=2*t_a+t_e
        # f=a*t_a^2-a*t_a*t_总+H
        par_a = a
        par_b = -a * t_a_in
        par_c = B
        if par_b ** 2 - 4 * par_a * par_c >= 0:
            t_a = (-par_b - (par_b ** 2 - 4 * par_a * par_c) ** 0.5) / (2 * a)
            delay_time = round((beam_between - 1/(num/2) * between) / v1, 2)
            if group > 1:
                self_delay_time = round(1/(num/2) * between / group / v1, 2)
            else:
                self_delay_time = 0
        else:
            t_a = 0
        # -----------------------------------------------------------------------

        # -------------------常规计算--间距为单倍磨头间距-----------------------------
        if t_a == 0:    # 说明高速策略无解
            distance_period=between*num
            t_all=round(distance_period/v1,2)
            # 边部停留时间设定
            t_a_in=(t_all-2*t2)/2
            # t_a 加速时间
            # t_e 匀速时间
            # H 摆幅
            # t_总=2*t_a+t_e
            # f=a*t_a^2-a*t_a*t_总+H
            par_a=a
            par_b=-a*t_a_in
            par_c=B
            if par_b**2-4*par_a*par_c>=0:
                t_a=(-par_b-(par_b**2-4*par_a*par_c)**0.5)/(2*a)
                delay_time = round((beam_between - 2 * between) / v1, 2)
                if group > 1:
                    self_delay_time = round(0.5 * between / group / v1, 2)
                else:
                    self_delay_time = 0
            else:
                # t_a=t_a_in/2
                t_a = 0
                ValueError('The swing cannot reach the set value!')
        #------------------------------------------------------------------------

        #------------------------均匀分布策略--------------------------------------
        '''
        if t_a == 0:   # 说明常规策略也无解
            t2 = 0 # 减小边部停留时间，此时应为有解
            distance_period = between * num
            t_all = round(distance_period / v1, 2)
            # 边部停留时间设定
            t_a_in = (t_all - 2 * t2) / 2
            # t_a 加速时间
            # t_e 匀速时间
            # H 摆幅
            # t_总=2*t_a+t_e
            # f=a*t_a^2-a*t_a*t_总+H
            par_a = a
            par_b = -a * t_a_in
            par_c = B
            if par_b ** 2 - 4 * par_a * par_c >= 0:
                t_a = (-par_b - (par_b ** 2 - 4 * par_a * par_c) ** 0.5) / (2 * a)
                delay_time = round((beam_between - 2 * between) / v1, 2)
                self_delay_time = round(between / group / v1, 2)
            else:
                # t_a=t_a_in/2
                t_a = 0
                ValueError('The swing cannot reach the set value!')
        '''
        # -------------（此刻再无解，说明用户输入参数不合理）--------------------------
        #t1 = t_a  # 加速时间
        t1 = round(t_a_in - 2*t_a,2)
        v2 = round(a * t_a, 2)
        # delay_time=round((beam_between-2*between)/v1,2)
        # self_delay_time=round(between/group/v1,2)
        # 多组磨头叠加延时时间计算
        delay_time_self_list = []
        for i in range(0, round(num/2 * group)):
            current_delay_time = round(i * delay_time, 2)
            if (i*2 / num) >= 1:
                current_delay_time += math.floor(i*2 / num) * self_delay_time
            delay_time_self_list.append(round(current_delay_time, 2))
        # 参数集
        params = {}
        params.update(
            {'lineEdit_belt_speed': v1, 'lineEdit_beam_swing_speed': v2, 'lineEdit_beam_constant_time': t1,'lineEdit_stay_time_output': t2
        , 'lineEdit_num_input': num, 'lineEdit_num_output': num * group, 'lineEdit_delay_time': delay_time,'lineEdit_delay_time_list': delay_time_self_list
        , 'lineEdit_stay_time_input': t2, 'lineEdit_swing': round(a * t_a ** 2 + v2 * t1, 2),'lineEdit_ceramic_width': ceramic_width, 'lineEdit_group_count': group
        , 'lineEdit_between': between, 'lineEdit_beam_between': beam_between, 'R': R, 'lineEdit_accelerate': a, 'self_delay_time': self_delay_time, 'lineEdit_grind_length': mo})
        params_gather.append(params)

    # ---------------------计算完毕，进行数据处理与筛选---------------------
    # 筛选出摆动速度值大于0的字典
    filtered_params_gather = [item for item in params_gather if item["lineEdit_beam_swing_speed"] > 0]
    # 按值降序排序
    sorted_data_params_gather = sorted(filtered_params_gather, key=lambda x: x["lineEdit_beam_swing_speed"], reverse=True)
    # 为降低计算时间，仅筛选前四组数据进行计算比较
    final_params_gather = sorted_data_params_gather[:5]
    # 计算均匀系数，将均匀系数最优的参数集筛选出来
    for i in final_params_gather:
        PDT = PolishingDistributionThread(**i)
        object_matrix, result = PDT.emit()
        i.update({'lineEdit_coefficient':result})
    # 筛选出最佳结果
    sorted_final_params_gather = sorted(final_params_gather, key=lambda x: x["lineEdit_coefficient"],
                                       reverse=False)
    final_params = sorted_final_params_gather[0]
    '''
    # 增加小砖算法
    if ceramic_width <= 800:
        if v2 <= 200:       # 若横梁摆动速度小于200则判定摆动速度过慢
            num_small = 2  # 针对小砖缩短单周期长度
            group_small  = num / 2  # 针对小砖增多叠加次数
            B = ceramic_width + 200 - 2 * R
            distance_period = between * num_small
            t_all = round(distance_period / v1, 2)
            # 边部停留时间设定
            t_a_in = (t_all - 2 * t2) / 2
            # t_a 加速时间
            # t_e 匀速时间
            # H 摆幅
            # t_总=2*t_a+t_e
            # f=a*t_a^2-a*t_a*t_总+H
            par_a = a
            par_b = -a * t_a_in
            par_c = B
            if par_b ** 2 - 4 * par_a * par_c >= 0:
                t_a = (-par_b - (par_b ** 2 - 4 * par_a * par_c) ** 0.5) / (2 * a)
            else:
                t_a = t_a_in / 2
                ValueError('The swing cannot reach the set value!')
            # t1 = t_a  # 加速时间
            t1 = round(t_a_in - 2 * t_a, 2)
            v2 = round(a * t_a, 2)
            delay_time = round((beam_between - 2 * between) / v1, 2)
            self_delay_time = round(between / group_small*2 / v1, 2)
            # 多组磨头叠加延时时间计算
            delay_time_self_list = []
            for i in range(0, round(num_small / 2 * group_small)):
                current_delay_time = round(i * delay_time, 2)
                if (i * 2 / num_small) >= 1:
                    current_delay_time += math.floor(i * 2 / num_small) * self_delay_time
                delay_time_self_list.append(round(current_delay_time, 2))
            # 参数集
            params = {}
            params.update(
                        {'lineEdit_belt_speed': v1, 'lineEdit_beam_swing_speed': v2, 'lineEdit_beam_constant_time': t1, 'lineEdit_stay_time_output': t2
                        ,'lineEdit_num_input':num, 'lineEdit_num_output': num_small*group_small, 'lineEdit_delay_time': delay_time, 'lineEdit_delay_time_list': delay_time_self_list
                        ,'lineEdit_stay_time_input':t2,'lineEdit_swing': round(a*t_a**2+v2*t1,2), 'lineEdit_ceramic_width': ceramic_width
                        ,'lineEdit_group_count':group, 'lineEdit_between': between, 'lineEdit_beam_between': beam_between, 'R': R
                        , 'lineEdit_accelerate': a,'self_delay_time':self_delay_time,'lineEdit_grind_length':mo})
    '''
    # 对计算出的结果进行处理（1.方便数据传输到PLC；2.方便数据传输至仿真动画计算端）
    keys_to_extract = ['lineEdit_belt_speed', 'lineEdit_beam_swing_speed', 'lineEdit_accelerate','lineEdit_stay_time_output'
                        ,'lineEdit_swing', 'lineEdit_delay_time_list']
    # 使用字典推导式提取指定键
    final_params_transmission_PLC = {key: final_params[key] for key in keys_to_extract if key in final_params}
    final_params_transmission_PLC['mode'] = 'order'
    # 参数 final_params 用于仿真计算
    return final_params_transmission_PLC,final_params
# -----提速计算策略（当磨头数小于等于 2）--计算单组参数----（后续可优化为补抛策略）----------
def self_define_calculate_new(v1,R,ceramic_width,mo,between,beam_between,a,num):
    # 定义全局变量
    # global v1, ceramic_width, R, mo
    B = ceramic_width + 200 - 2 * R
    v2_max = (B / a) ** 0.5 * a
    # # 根据磨头间距、皮带速度计算单周期时间
    # period_time = between * num / v1
    # t2 = between * 0.6 / v1
    v2 = round(v2_max*0.95,2)
    t_a = round(v2/a,2)
    t_e = round((B - a*t_a**2)/v2,2)
    t2 = round(0.2 * (2 * t_a + t_e),2)
    period_time = (2 * t_a + t_e + t2) * 2

    group = 1
    delay_time = 0
    self_delay_time = 0
    delay_time_self_list = [0]

    # params = {'lineEdit_belt_speed': v1, 'lineEdit_beam_swing_speed': v2, 'lineEdit_beam_constant_time': t_e,'lineEdit_stay_time_output': t2
    #     , 'lineEdit_num_input': num, 'lineEdit_num_output': num * group, 'lineEdit_delay_time': delay_time,'lineEdit_delay_time_list': delay_time_self_list
    #     , 'lineEdit_stay_time_input': t2, 'lineEdit_swing': round(a * t_a ** 2 + v2 * t_e, 2),'lineEdit_ceramic_width': ceramic_width, 'lineEdit_group_count': group
    #     , 'lineEdit_between': between, 'lineEdit_beam_between': beam_between, 'R': R, 'lineEdit_accelerate': a, 'self_delay_time': self_delay_time, 'lineEdit_grind_length': mo}
    params = {'lineEdit_belt_speed': v1, 'lineEdit_beam_swing_speed': v2,'lineEdit_stay_time_output': t2
         ,'lineEdit_delay_time_list': delay_time_self_list, 'lineEdit_swing': round(a * t_a ** 2 + v2 * t_e, 2), 'lineEdit_accelerate': a}

    return params
# 整线优化策略计算
def self_define_calculate_whole_line(v1,R,ceramic_width,mo,between,beam_between,head_count,a):
    # 全局变量
    # global v1,R,ceramic_width,mo
    # 为了单次传入多个参数，传入的参数为整线的参数集合（列表）
    all_params_gather = []
    # 用于存储仿真计算的参数
    unique_items_gather_simulation_calculate = []
    # 抛光机数目
    machine_count = len(between)
    for i in range(0,machine_count):    # 第一台机至第四台机 进行循环迭代
        single_machine_params_gather = []
        # 存放第一台机 同粒度磨头数排布（eg.[4,6,4]）
        single_machine_head_gather = head_count[i]
        # 若出现奇数个磨头，对当前同粒度磨头数排布进行调整
        for k in single_machine_head_gather:
            if k % 2 == 0:
                continue
            else:
                if sum(single_machine_head_gather) == 16:
                    single_machine_head_gather = [16]
                else:
                    single_machine_head_gather = [12,sum(single_machine_head_gather)-12]
                break
        # 统计单台机 同粒度磨头数有几种情况
        unique_count = len(set(single_machine_head_gather))
        # 如果想查看具体有哪些不同的数据--（注意转换为列表）
        unique_items = list(set(single_machine_head_gather))
        # 计算单台机 不同 同粒度磨头数目 的运动参数
        machine_between = between[i]
        machine_beam_between = beam_between[i]
        # 用于存储传输至PLC的数据
        unique_items_gather_transmission_PLC = {}
        params_2 = []
        for j in range(0,unique_count):
            num = unique_items[j]
            if num == 2:
                params_1 = self_define_calculate_new(v1,R,ceramic_width,mo,machine_between, machine_beam_between,a,num)
            else:
                params_1,params_2 = self_define_calculate_speed_boost(v1,R,ceramic_width,mo,machine_between, machine_beam_between, a, num)
            unique_items_gather_transmission_PLC[num] = params_1
            unique_items_gather_simulation_calculate.append(params_2)
        # 参数匹配
        for j in range(0,len(single_machine_head_gather)):
            current_num = single_machine_head_gather[j]
            single_machine_params_gather.append(unique_items_gather_transmission_PLC[current_num])
        all_params_gather.append(single_machine_params_gather)
    return all_params_gather,unique_items_gather_simulation_calculate
# 整线优化策略备选方案一（磨头输入个数为偶数个）
def self_define_calculate_whole_line_option_1(v1,R,ceramic_width,mo,between,beam_between,machine_count,head_count,a):
    # 全局变量
    # global v1,R,ceramic_width,mo
    # 为了单次传入多个参数，传入的参数为整线的参数集合（列表）
    all_params_gather = []
    for i in range(0,machine_count):    # 第一台机至第四台机 进行循环迭代
        single_machine_params_gather = []
        # 存放第一台机 同粒度磨头数排布（eg.[4,6,4]）
        single_machine_head_gather = head_count[i]
        # 按照双头摆抛光机的加工特性 ， 直接给出最优磨头摆布
        single_machine_head_gather_sum = sum(single_machine_head_gather)
        if single_machine_head_gather_sum == 16:
            single_machine_head_gather = [16]
        elif single_machine_head_gather_sum == 14:
            single_machine_head_gather = [12,2]
        else:
            single_machine_head_gather = [12, sum(single_machine_head_gather) - 12]
        # 统计单台机 同粒度磨头数有几种情况（1 或 2）
        unique_count = len(set(single_machine_head_gather))
        # 如果想查看具体有哪些不同的数据--（注意转换为列表）
        unique_items = list(set(single_machine_head_gather))
        # 计算单台机 不同 同粒度磨头数目 的运动参数
        machine_between = between[i]
        machine_beam_between = beam_between[i]
        unique_items_gather = {}
        for j in range(0,unique_count):
            num = unique_items[j]
            if num == 2:
                params = self_define_calculate_new(v1,R,ceramic_width,mo,machine_between, machine_beam_between,a,num)
            else:
                params = self_define_calculate_speed_boost(v1,R,ceramic_width,mo,machine_between, machine_beam_between, a, num)
            unique_items_gather[num] = params
        # 参数匹配
        for j in range(0,len(single_machine_head_gather)):
            current_num = single_machine_head_gather[j]
            single_machine_params_gather.append(unique_items_gather[current_num])
        all_params_gather.append(single_machine_params_gather)
    return all_params_gather

# if __name__ == '__main__':
#     # 全局变量
#     v1=500
#     ceramic_width=1200
#     R = 270
#     a = 1000
#     mo = 140
#     # 方法传参
#     between = [650,600,650]
#     beam_between = [1906,1906,1906]
#     machine_count = 3
#     head_count = [[4,6,4],[5,7,4],[7,5,2]]
#     # B = ceramic_width + 200 - 2 * R
#     # v2_max = (B/a)**0.5 * a
#     # print(v2_max)
#
#     start_time = te.time()  # 记录开始时间
#     # params_1 : PLC接收参数 ; params_2 : 仿真计算接收参数
#     params_1,params_2= self_define_calculate_whole_line(between, beam_between, head_count, a)
#     end_time = te.time()  # 记录结束时间
#     duration = end_time - start_time  # 计算执行时间
#     print(f"程序运行时间：{duration}秒")
#
#     import json
#     print(json.dumps(params_1, indent=4, ensure_ascii=False))
#     print(json.dumps(params_2, indent=4, ensure_ascii=False))
#
#     # params_3 = self_define_calculate_new(v1,ceramic_width,between,beam_between,R,a,num,mo)
#     # print(params_3)