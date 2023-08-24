import pandas as pd
import numpy as np

def count_reapet(word, count):
    for i in range(97, 123):
        ch = chr(i)
        if word.count(ch) == 2:
            count[0] = count[0] + 1
        if word.count(ch) == 3:
            count[1] = count[1] + 1

count = [0] * 359
count_ = [[count], [count]]
input = np.array(count_).reshape(-1,2)
print(input.shape)

fm = pd.read_excel(r"C:\Users\Administrator\Desktop\2023File\2023_MCM-ICM_Problems\InputData.xlsx",
                   sheet_name="matcalc")

for i in range(0,359):
    word = fm["Word"][i]
    print(word)
    count_reapet(word, input[i])

df = pd.DataFrame(input, columns=['2repeats', '3repeats'])
df.to_excel(r"C:\Users\Administrator\Desktop\2023File\2023_MCM-ICM_Problems\CountRepeat.xlsx", sheet_name='Sheet1',
            index=False)


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')
