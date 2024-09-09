import numpy as np
import math
def equal_num_calculate(v1,ceramic_width,between,R,overlap,a,beam_speed_up):
    # 计算最佳斜率（轨迹重叠overlap mm）
    theta = math.asin((2 * R - overlap) / between)
    v2_mid = v1 * math.tan(theta)
    # 磨头摆动速度上限设为beam_speed_up mm/s
    if v2_mid <= beam_speed_up:
        v2 = v2_mid
    else:
        v2 = beam_speed_up
    # 中间计算(边部停留时长为单倍磨头间距)
    B = (ceramic_width + 200) - 2 * R                    # 摆幅（要求两极限位置各伸出100mm）
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
    t1 = round(t_beam - 2 * t1, 2)  # 匀速时间
    result[0, 2] = t1
    t2 = round(between / v1, 2)     # 边部停顿时间
    result[0, 3] = t2
    result[0, 4] = num_1  # 圆整磨头数
    result[0, 5] = B
    # 模式二
    result[1, 0] = v1
    result[1, 1] = v2
    result[1, 2] = t1
    result[1, 3] = t2*2
    result[1, 4] = num_1+2  # 圆整磨头数
    result[1, 5] = B
    return result