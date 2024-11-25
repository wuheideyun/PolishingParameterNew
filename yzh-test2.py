import inspect

list1 = [1, 2, 3]

# 获取当前局部变量
for name, value in inspect.currentframe().f_locals.items():
    if value == list1:
        print(f"Name of the list: {name}")
