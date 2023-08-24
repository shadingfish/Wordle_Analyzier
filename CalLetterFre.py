import numpy as np
import pandas as pd


def count_letter(alist, word, count):
    for index, ele in enumerate(alist):
        if word is np.nan:
            count[index] = -1
            continue
        if ele in word:
            count[index] = count[index] + word.count(ele)


fm = pd.read_excel(r"C:\Users\Administrator\Desktop\2023File\2023_MCM-ICM_Problems\data.xlsx",
                   sheet_name="Sheet1")

letter_list = ['e', 'a', 'r', 'o', 't', 'l', 'i', 'n', 's', 'c', 'h', 'p', 'u', 'y', 'm', 'd', 'g', 'k',
               'f', 'b', 'w', 'v', 'x', 'q', 'z', 'j']

container = np.array([0] * 360 * 26).reshape(-1, 26)

for i in range(0, 360):
    word = fm["Word"][i]
    count_letter(letter_list, word, container[i])

df = pd.DataFrame(container,
                  columns=['e', 'a', 'r', 'o', 't', 'l', 'i', 'n', 's', 'c', 'h', 'p', 'u', 'y', 'd', 'm', 'g', 'k',
                           'f', 'b', 'w', 'v', 'x', 'q', 'z', 'j'])
df.to_excel(r"C:\Users\Administrator\Desktop\2023File\2023_MCM-ICM_Problems\FrequencyTable.xlsx", sheet_name='Sheet1',
            index=False)


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')
