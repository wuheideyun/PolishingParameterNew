import csv
from sklearn.linear_model import LinearRegression
import numpy as np

# 初始化一个空列表来存储第 5 列的数据
data = []
# 初始化计数器，用于记录当前处理的行数，从 1 开始
count = 1
# 初始化两个空列表分别存储前 100 项和后 100 项的偏差值
differences_first_100 = []
differences_last_100 = []

try:
    # 打开 CSV 文件，尝试使用 GBK 编码
    with open(r'D:\360data\重要数据\桌面\申报补充资料\SizeTest1_240703_184616.CSV', 'r', encoding='gbk') as file:
        print(f"成功以 {file.encoding} 编码打开文件")
        reader = csv.reader(file)
        # 跳过标题行
        next(reader)

        # 打印表头
        print("行号\t当前值\t预测值\t差值")

        for row in reader:
            # 检查计数器是否达到 201（因为从 1 开始计数，实际是前 200 行）
            if count > 100:
                break
            try:
                # 获取第 5 列的数据（索引为 4）
                current_value = float(row[4])

                # 如果数据列表长度大于 1，进行线性回归预测
                if len(data) > 1:
                    # 准备训练数据，使用之前所有数据
                    X = np.array(range(len(data))).reshape(-1, 1)
                    y = np.array(data)
                    # 创建线性回归模型
                    model = LinearRegression()
                    # 拟合模型
                    model.fit(X, y)
                    # 预测下一个值，基于之前所有数据
                    next_index = len(data)
                    prediction = model.predict(np.array([[next_index]]))[0]
                    # 计算差值
                    difference = current_value - prediction
                    # 保留两位小数
                    prediction = round(prediction, 2)
                    difference = round(difference, 2)
                    # 打印结果，使用制表符分隔列
                    print(f"{count}\t{current_value}\t{prediction}\t{difference}")

                    # 根据计数器的值将差值添加到相应的列表中
                    if count <= 100:
                        differences_first_100.append(difference)
                    else:
                        differences_last_100.append(difference)

                else:
                    # 打印结果，使用制表符分隔列
                    print(f"{count}\t{current_value}\t无\t无")

                # 如果数据列表长度超过 100，去掉最开始的一个数
                if len(data) >  50:
                    data = data[1:]
                # 将当前值添加到数据列表中
                data.append(current_value)

            except (IndexError, ValueError):
                # 处理可能的索引错误或值错误
                print(f"{count}\t跳过无效行\t无\t无")

            # 计数器加 1
            count += 1

    # 统计前 100 项偏差值的最大值、最小值和平均值
    if differences_first_100:
        max_difference_first_100 = max(differences_first_100)
        min_difference_first_100 = min(differences_first_100)
        avg_difference_first_100 = round(sum(differences_first_100) / len(differences_first_100), 2)
        print(f"前 100 项统计信息：\t最大值\t最小值\t平均值")
        print(f"\t{max_difference_first_100}\t{min_difference_first_100}\t{avg_difference_first_100}")
    else:
        print("前 100 项由于数据不足，未计算出有效的偏差值。")

    # 统计后 100 项偏差值的最大值、最小值和平均值
    if differences_last_100:
        max_difference_last_100 = max(differences_last_100)
        min_difference_last_100 = min(differences_last_100)
        avg_difference_last_100 = round(sum(differences_last_100) / len(differences_last_100), 2)
        print(f"后 100 项统计信息：\t最大值\t最小值\t平均值")
        print(f"\t{max_difference_last_100}\t{min_difference_last_100}\t{avg_difference_last_100}")
    else:
        print("后 100 项由于数据不足，未计算出有效的偏差值。")

except UnicodeDecodeError as e:
    print(f"文件读取失败：{e}")
    print("尝试使用其他编码，如 UTF-8 或 GB2312 等")
except FileNotFoundError:
    print("文件未找到，请检查文件路径是否正确")