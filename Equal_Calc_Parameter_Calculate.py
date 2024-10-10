import numpy as np
import math
# 第一版算法
def equal_num_calculate(v1,ceramic_width,between,R,overlap,a):
    # 计算最佳斜率（轨迹重叠overlap mm）
    theta = math.asin((2 * R - overlap) / between)
    v2_mid = v1 * math.tan(theta)
    # 磨头摆动速度上限设为beam_speed_up mm/s
    if v2_mid <= beam_speed_up:
        v2 = v2_mid
    else:
        v2 = beam_speed_up
    # 中间计算(边部停留时长为单倍磨头间距)
    B = (ceramic_width + 120) - 2 * R                    # 摆幅（要求两极限位置各伸出60mm）
    t1_ = v2 / a                             # 加速时间
    t2_ = (B - a * t1_ ** 2) / v2            # 匀速时间
    t3_ = between / v1                       # 边部停留时长
    period_1 = 4 * t1_ + 2 * t2_ + 2 * t3_      # 单周期时间
    num_1 = math.ceil(v1 * period_1 / between)   # 同粒度磨头数目
    t_beam = (num_1 * between - 2 * between) / (2 * v1)   # 2 * t1 + t2
    # 方程求解
    #f_1 = a * t1_ ** 2 - t_beam * a * t1_ + B
    #
    if (t_beam * a) ** 2 - 4 * a * B >= 0:
        t1 = (-((t_beam * a) ** 2 - 4 * a * B) ** 0.5 + a * t_beam) / (2 * a)
    else:
        t1 = t_beam / 2
    # 输出项
    result=np.zeros((2,6))
    # 模式一
    # 磨头速度变小、摆动时间增加来圆整单周期磨头数
    result[0,0] = v1
    v2 = round(a * t1, -2)  #磨头摆动速度变小
    result[0,1] = v2
    t_e = round(t_beam - 2 * t1, 2)  # 匀速时间
    result[0, 2] = t_e
    t2 = round(between / v1, 2)     # 边部停顿时间
    result[0, 3] = t2
    result[0, 4] = num_1  # 圆整磨头数
    result[0, 5] = B
    # 模式二
    result[1, 0] = v1
    result[1, 1] = v2
    result[1, 2] = t_e
    result[1, 3] = t2*2
    result[1, 4] = num_1+2  # 圆整磨头数
    result[1, 5] = B
    return result
# 第二版算法
def equal_num_calculate_new_1(v1,ceramic_width,between,R,t_a):
    # 初步计算  为了增加摆频，忽略匀速阶段，直接：加速-减速-停顿-加速-减速-停顿
    B = (ceramic_width + 120) - 2 * R  # 摆幅（要求两极限位置各伸出60mm）
    # a = B/t_a/t_a
    # 边部停留时间直接固定  1.2s   1.5s
    t_stay_1=1.2
    t_stay_2=1.5
    period_1=4*t_a+2*t_stay_1
    period_2=4*t_a+2*t_stay_2
    num_1=math.ceil(v1 * period_1 / between)
    num_2=math.ceil(v1 * period_2 / between)
    t_e_1=(num_1*between/v1-period_1)/2
    t_e_2=(num_2*between/v1-period_2)/2
    # a*t_a**2 + a * t_a * t_e_1 = B
    a_1=B/(t_a**2+t_a*t_e_1)
    a_2=B/(t_a**2+t_a*t_e_2)
    # 输出项
    result=np.zeros((2,6))
    # 模式一
    result[0,0] = v1
    result[0,1] = round(a_1 * t_a, 2)    # 横梁摆动速度
    result[0, 2] = round(t_e_1,2)        # 匀速时间
    result[0, 3] = t_stay_1              # 边部停顿时间
    result[0, 4] = num_1                 # 圆整磨头数
    result[0, 5] = a_1*t_a**2+a_1*t_a*t_e_1
    # 模式二
    result[1, 0] = v1
    result[1, 1] = round(a_2 * t_a, 2)   # 横梁摆动速度
    result[1, 2] = round(t_e_2,2)
    result[1, 3] = t_stay_2
    result[1, 4] = num_2                 # 圆整磨头数
    result[1, 5] = a_2*t_a**2+a_2*t_a*t_e_2
    return result
# 第三版算法
def equal_num_calculate_new_2(v1,ceramic_width,between,R,t_a):
    # 初步计算  为了增加摆频，忽略匀速阶段，直接：加速-减速-停顿-加速-减速-停顿
    B = (ceramic_width + 120) - 2 * R  # 摆幅（要求两极限位置各伸出60mm）
    # a = B/t_a/t_a
    # 边部停留时间直接固定  1.2s   1.5s
    t_stay_1=0.6
    t_stay_2=1.5
    period_1=4*t_a+2*t_stay_1
    period_2=4*t_a+2*t_stay_2
    num_1=math.ceil(v1 * period_1 / between)
    num_2=math.ceil(v1 * period_2 / between)
    t_zeng_1=(num_1*between/v1-period_1)/2
    t_zeng_2=(num_2*between/v1-period_2)/2
    # a*t_a**2 + a * t_a * t_e_1 = B
    a_1=B/t_a**2
    a_2=B/t_a**2
    # 输出项
    result=np.zeros((2,6))
    # 模式一
    result[0,0] = v1
    result[0,1] = round(a_1 * t_a, 2)    # 横梁摆动速度
    result[0, 2] = 0                     # 匀速时间
    result[0, 3] = round(t_stay_1+t_zeng_1,2)              # 边部停顿时间
    result[0, 4] = num_1                 # 圆整磨头数
    result[0, 5] = a_1*t_a**2
    # 模式二
    result[1, 0] = v1
    result[1, 1] = round(a_2 * t_a, 2)   # 横梁摆动速度
    result[1, 2] = 0
    result[1, 3] = round(t_stay_2+t_zeng_2,2)
    result[1, 4] = num_2                 # 圆整磨头数
    result[1, 5] = a_2*t_a**2
    return result
# 第四版算法
def equal_num_calculate_new_3(v1,ceramic_width,between,R,a):
    # 初步计算  为了增加摆频，忽略匀速阶段，直接：加速-减速-停顿-加速-减速-停顿
    B = (ceramic_width + 120) - 2 * R  # 摆幅（要求两极限位置各伸出60mm）
    # a = B/t_a/t_a
    # 边部停留时间直接固定  1.2s   1.5s
    t_a=(B/a)**0.5
    t_stay_1=1.5
    t_stay_2=2.81
    period_1=4*t_a+2*t_stay_1
    period_2=4*t_a+2*t_stay_2
    num_1=math.ceil(v1 * period_1 / between)
    num_2=math.ceil(v1 * period_2 / between)
    t_zeng_1=(num_1*between/v1-period_1)/2
    t_zeng_2=(num_2*between/v1-period_2)/2
    # a*t_a**2 + a * t_a * t_e_1 = B
    a_1=B/t_a**2
    a_2=B/t_a**2
    # 输出项
    result=np.zeros((2,7))
    # 模式一
    result[0, 0] = v1
    result[0, 1] = round(a_1 * t_a, 2)            # 横梁摆动速度
    result[0, 2] = 0                              # 匀速时间
    result[0, 3] = round(t_stay_1+t_zeng_1,2)     # 边部停顿时间
    result[0, 4] = num_1                          # 圆整磨头数
    result[0, 5] = a_1*t_a**2
    result[0, 6] = round(t_a,2)
    # 模式二
    result[1, 0] = v1
    result[1, 1] = round(a_2 * t_a, 2)   # 横梁摆动速度
    result[1, 2] = 0
    result[1, 3] = round(t_stay_2+t_zeng_2,2)
    result[1, 4] = num_2                 # 圆整磨头数
    result[1, 5] = a_2*t_a**2
    result[1, 6] = round(t_a, 2)
    return result
# 第五版算法
def equal_num_calculate_new_4(v1,ceramic_width,between,R,a):
    # 初步计算  为了增加摆频，忽略匀速阶段，直接：加速-减速-停顿-加速-减速-停顿
    B = (ceramic_width + 120) - 2 * R  # 摆幅（要求两极限位置各伸出60mm）
    # a = B/t_a/t_a
    # 边部停留时间直接固定  1.2s   1.5s
    t_a=(B/a)**0.5
    t_stay_1=0.8
    t_stay_2=1.5
    period_1=4*t_a+2*t_stay_1
    period_2=4*t_a+2*t_stay_2
    num_1=math.ceil(v1 * period_1*2 / between)
    num_2=math.ceil(v1 * period_2*2 / between)
    t_zeng_1=(num_1*between/v1-period_1*2)/4
    t_zeng_2=(num_2*between/v1-period_2*2)/4
    # a*t_a**2 + a * t_a * t_e_1 = B
    a_1=B/t_a**2
    a_2=B/t_a**2
    # 输出项
    result=np.zeros((2,7))
    # 模式一
    result[0, 0] = v1
    result[0, 1] = round(a_1 * t_a, 2)            # 横梁摆动速度
    result[0, 2] = 0                              # 匀速时间
    result[0, 3] = round(t_stay_1+t_zeng_1,2)     # 边部停顿时间
    result[0, 4] = num_1                          # 圆整磨头数
    result[0, 5] = a_1*t_a**2
    result[0, 6] = round(t_a,2)
    # 模式二
    result[1, 0] = v1
    result[1, 1] = round(a_2 * t_a, 2)   # 横梁摆动速度
    result[1, 2] = 0
    result[1, 3] = round(t_stay_2+t_zeng_2,2)
    result[1, 4] = num_2                 # 圆整磨头数
    result[1, 5] = a_2*t_a**2
    result[1, 6] = round(t_a, 2)
    return result
# 第六版算法（单周期）
def equal_num_calculate_new(v1,ceramic_width,between,R,a):
    # 初步计算  为了增加摆频，忽略匀速阶段，直接：加速-减速-停顿-加速-减速-停顿
    B = (ceramic_width + 2*100) - 2 * R  # 摆幅（要求两极限位置各伸出60mm）
    # a = B/t_a/t_a
    # 边部停留时间直接固定  1.2s   1.5s
    t_stay_1=0.8
    t_stay_2=1.6
    t_a = (B / a) ** 0.5
    period_1=4*t_a+2*t_stay_1
    period_2=4*t_a+2*t_stay_2
    num_1=math.ceil(v1 * period_1  / between)
    num_2=math.ceil(v1 * period_2  / between)
    t_beam_all_1=(num_1*between/v1-2*t_stay_1)/2  #  2*t_a + t_e
    t_beam_all_2=(num_2*between/v1-2*t_stay_2)/2  #  2*t_a + t_e
    # 求解方程
    if (t_beam_all_1 * a) ** 2 - 4 * a * B >= 0:
        t_a_1 = (-((t_beam_all_1 * a) ** 2 - 4 * a * B) ** 0.5 + a * t_beam_all_1) / (2 * a)
    else:
        t_a_1 = 0

    if (t_beam_all_2 * a) ** 2 - 4 * a * B >= 0:
        t_a_2 = (-((t_beam_all_2 * a) ** 2 - 4 * a * B) ** 0.5 + a * t_beam_all_2) / (2 * a)
    else:
        t_a_2 = 0
    t_e_1 = t_beam_all_1-2*t_a_1
    t_e_2 = t_beam_all_2 - 2 * t_a_2
    # a*t_a**2 + a * t_a * t_e_1 = B
    # 输出项
    result=np.zeros((2,7))
    # 模式一
    result[0,0] = v1
    result[0,1] = round(a * t_a_1, 2)    # 横梁摆动速度
    result[0, 2] = round(t_e_1,2)        # 匀速时间
    result[0, 3] = t_stay_1              # 边部停顿时间
    result[0, 4] = num_1                 # 圆整磨头数
    result[0, 5] = a*t_a_1**2+a*t_a_1*t_e_1
    result[0, 6] = round(t_a_1,2)
    # 模式二
    result[1, 0] = v1
    result[1, 1] = round(a * t_a_2, 2)   # 横梁摆动速度
    result[1, 2] = round(t_e_2,2)
    result[1, 3] = t_stay_2
    result[1, 4] = num_2                 # 圆整磨头数
    result[1, 5] = a*t_a_2**2+a*t_a_2*t_e_2
    result[1, 6] = round(t_a_2, 2)
    return result
# 第六版算法（双周期）
def equal_num_calculate_new_(v1,ceramic_width,between,R,a):
    # 初步计算  为了增加摆频，忽略匀速阶段，直接：加速-减速-停顿-加速-减速-停顿
    B = (ceramic_width + 2*100) - 2 * R  # 摆幅（要求两极限位置各伸出60mm）
    # a = B/t_a/t_a
    # 边部停留时间直接固定  1.2s   1.5s
    t_stay_1=0.8
    t_stay_2=1.2
    t_a = (B / a) ** 0.5
    period_1=4*t_a+2*t_stay_1
    period_2=4*t_a+2*t_stay_2
    num_1=math.ceil(v1 * period_1 * 2 / between)
    num_2=math.ceil(v1 * period_2 * 2 / between)
    t_beam_all_1=(num_1*between/v1-4*t_stay_1)/4  #  2*t_a + t_e
    t_beam_all_2=(num_2*between/v1-4*t_stay_2)/4  #  2*t_a + t_e
    # 求解方程
    if (t_beam_all_1 * a) ** 2 - 4 * a * B >= 0:
        t_a_1 = (-((t_beam_all_1 * a) ** 2 - 4 * a * B) ** 0.5 + a * t_beam_all_1) / (2 * a)
    else:
        t_a_1 = 0

    if (t_beam_all_2 * a) ** 2 - 4 * a * B >= 0:
        t_a_2 = (-((t_beam_all_2 * a) ** 2 - 4 * a * B) ** 0.5 + a * t_beam_all_2) / (2 * a)
    else:
        t_a_2 = 0
    t_e_1 = t_beam_all_1-2*t_a_1
    t_e_2 = t_beam_all_2 - 2 * t_a_2
    # a*t_a**2 + a * t_a * t_e_1 = B
    # 输出项
    result=np.zeros((2,7))
    # 模式一
    result[0,0] = v1
    result[0,1] = round(a * t_a_1, 2)    # 横梁摆动速度
    result[0, 2] = round(t_e_1,2)        # 匀速时间
    result[0, 3] = t_stay_1              # 边部停顿时间
    result[0, 4] = num_1                 # 圆整磨头数
    result[0, 5] = a*t_a_1**2+a*t_a_1*t_e_1
    result[0, 6] = round(t_a_1,2)
    # 模式二
    result[1, 0] = v1
    result[1, 1] = round(a * t_a_2, 2)   # 横梁摆动速度
    result[1, 2] = round(t_e_2,2)
    result[1, 3] = t_stay_2
    result[1, 4] = num_2                 # 圆整磨头数
    result[1, 5] = a*t_a_2**2+a*t_a_2*t_e_2
    result[1, 6] = round(t_a_2, 2)
    return result