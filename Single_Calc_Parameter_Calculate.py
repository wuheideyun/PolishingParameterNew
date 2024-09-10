import numpy as np
import math
def single_num_calculate(v1,ceramic_width,between_beam,R,overlap,a,beam_speed_up):
    # 计算模式同 同步摆，磨头间距为固定值
    # 计算相叠overlap  mm 斜率（已知磨头间距为between）
    v2=beam_speed_up
    theta = math.atan(v2 / v1)
    between = (2*R-overlap)/math.sin(theta)
    # 中间计算(边部停留时长为单倍磨头间距)
    B = (ceramic_width + 120) - 2 * R           # 摆幅（要求两极限位置各伸出80mm）
    t_a = v2 / a                      # 加速时间
    t_e = (B - a * t_a ** 2) / v2     # 匀速时间
    t_between = between / v1          # 边部停留时长
    period_1 = 4 * t_a + 2 * t_e + 2 * t_between     # 单周期时间
    num_1 = math.ceil(v1 * period_1 / between)       # 同粒度磨头数目
    t_beam = (num_1 * between - 2 * between) / (2 * v1)   # 2 * t_a + t_e
    #
    # f_1 = a * t_a ^ 2 - t_beam * a * t_a + B;
    #
    if (t_beam * a) ** 2 - 4 * a * B >= 0:
        t_a = (-((t_beam * a) ** 2 - 4 * a * B) ** 0.5 + a * t_beam) / (2 * a)
        # t1 = (((t_beam * a) ^ 2 - 4 * a * B) ^ 0.5 + a * t_beam) / (2 * a)
    else:
        t_a = t_beam / 2
        str='摆幅不够'
    v2 = round(t_a * a, 2)
    t_e = round(t_beam - 2 * t_a, 2)
    # 延时时间计算
    t_delay=round((between_beam-between)/v1,2)
    # 结果输出
    result = np.zeros((2, 8))
    # 方案一 节能方案
    result[0,0] = round(v1,2)
    result[0,1] = round(v2,2)
    result[0,2] = round(t_e,2)
    result[0,3] = round(t_between,2)
    result[0,4] = round(num_1)
    result[0,5] = t_delay
    result[0,6] = round(a*t_a**2+t_e*a*t_a,2)
    result[0,7] = round(between, 2)
    # 方案二 高光泽度方案
    result[1,0] = round(v1,2)
    result[1,1] = round(v2,2)
    result[1,2] = round(t_e,2)
    result[1,3] = round(t_between * 2,2)
    result[1,4] = round(num_1 + 2,2)
    result[1,5] = t_delay
    result[1,6] = round(a*t_a**2+t_e*a*t_a,2)
    result[1,7] = round(between, 2)
    return result