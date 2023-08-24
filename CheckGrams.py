import pandas as pd
import numpy as np

def count_grams(bi, tri, word, count):
    for bigram in bi:
        if bigram in word:
            count[0] = count[0] + 1
    for trigram in tri:
        if trigram in word:
            count[1] = count[1] + 1

bigrams = ['th', 'he', 'in', 'en', 'nt', 're', 'er', 'an', 'ti', 'es', 'on', 'at', 'se', 'nd', 'or', 'ar', 'al', 'te',
           'co', 'de', 'to', 'ra', 'et', 'ed', 'it', 'sa', 'em', 'ro']
trigrams = ['the', 'and', 'tha', 'ent', 'ing', 'ion', 'tio', 'for', 'nde', 'has', 'nce', 'edt', 'tis', 'oft', 'sth',
            'men']
count = [0] * 359
count_ = [[count], [count]]
input = np.array(count_).reshape(-1,2)
print(input.shape)

fm = pd.read_excel(r"C:\Users\Administrator\Desktop\2023File\2023_MCM-ICM_Problems\InputData.xlsx",
                   sheet_name="matcalc")

for i in range(0,359):
    ch = fm["Word"][i]
    count_grams(bigrams, trigrams, ch, input[i])

df = pd.DataFrame(input, columns=['bigram', 'trigram'])
df.to_excel(r"C:\Users\Administrator\Desktop\2023File\2023_MCM-ICM_Problems\CountGrams.xlsx", sheet_name='Sheet1',
            index=False)

def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')
