import itertools
import os

import numpy as np

count = [0] * 359
count_ = [[count], [count], [count], [count], [count]]
input = np.array(count_).reshape(-1,5)
print(input.shape)



def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')
