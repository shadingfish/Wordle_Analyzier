import pandas as pd
import numpy as np


def count_atri(Atri, word, count):
    for index, atri in enumerate(Atri):
        if word is np.nan:
            count[index] = -1
            continue
        if atri in word:
            count[index] = count[index] + 1


Atri = ['vt.', 'vi.', 'n.', 'adj.', 'adv.', 'pron.', 'prep.']

count = [0] * 360
count_ = [[count], [count], [count], [count], [count], [count], [count]]
input = np.array(count_).reshape(-1, 7)
print(input.shape)

fm = pd.read_excel(r"C:\Users\Administrator\Desktop\2023File\2023_MCM-ICM_Problems\WaitFind.xlsx",
                   sheet_name="Sheet1")
print(fm["Text"][0])
print(type(fm["Text"][0]))

for i in range(0, 360):
    ch = fm["Text"][i]
    count_atri(Atri, ch, input[i])

print(input)

df = pd.DataFrame(input, columns=['vt.', 'vi.', 'n.', 'adj.', 'adv.', 'pron.', 'prep.'])
df.to_excel(r"C:\Users\Administrator\Desktop\2023File\2023_MCM-ICM_Problems\CountAtri.xlsx", sheet_name='Sheet1',
            index=False)


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')
