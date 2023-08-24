# 这是一个示例 Python 脚本。

import pandas as pd

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
fm = pd.read_excel(r"C:\Users\Administrator\Desktop\2023File\2023_MCM-ICM_Problems\InputData.xlsx",
                   sheet_name="matcalc")
# 用该方法读取表格和表单里的单元格的数据
count1 = [0] * 26
count2 = [0] * 26
count3 = [0] * 26
count4 = [0] * 26
count5 = [0] * 26
sum_miu1 = [0] * 26
sum_miu2 = [0] * 26
sum_miu3 = [0] * 26
sum_miu4 = [0] * 26
sum_miu5 = [0] * 26

# data = [count1, sum_miu1, count2, sum_miu2, count3, sum_miu3, count4, sum_miu4, count5, sum_miu5]

def calfrequecny(count, sum_miu, k):
    for i in range(0, 358):
        ch = fm["Word"][i][k]
        count[ord(ch) - 97] = count[ord(ch) - 97] + 1
        sum_miu[ord(ch) - 97] = sum_miu[ord(ch) - 97] + fm["miu"][i]


calfrequecny(count1, sum_miu1, 0)
print(count1, sum_miu1)
calfrequecny(count2, sum_miu2, 1)
print(count2, sum_miu2)
calfrequecny(count3, sum_miu3, 2)
print(count3, sum_miu3)
calfrequecny(count4, sum_miu4, 3)
print(count4, sum_miu4)
calfrequecny(count5, sum_miu5, 4)
print(count5, sum_miu5)
data = [count1, sum_miu1, count2, sum_miu2, count3, sum_miu3, count4, sum_miu4, count5, sum_miu5]
print(data)
'''
 for k in range(0, 4):
     for j in range(0, 10, 2):
        calfrequecny(data[j], data[j + 1], k)
        print(data[j], data[j + 1])

print("--------------------------")
print([count1, sum_miu1, count2, sum_miu2, count3, sum_miu3, count4, sum_miu4, count5, sum_miu5])
'''
df = pd.DataFrame({"count1": count1, "sum_miu1": sum_miu1, "count2": count2, "sum_miu2": sum_miu2, "count3": count3,
                   "sum_miu3": sum_miu3, "count4": count4, "sum_miu4": sum_miu4, "count5": count5,
                   "sum_miu5": sum_miu5})
df.to_excel(r"C:\Users\Administrator\Desktop\2023File\2023_MCM-ICM_Problems\PythonData.xlsx", sheet_name='Sheet1',
            index=False)



def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
