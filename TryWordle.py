import re

word = "abcde"
ans = "xyzva"
print('[' + '^' + word + ']')
pattern1 = '[' + '^' + word + ']' #00000

# if check.contains(word[0]) #10000
    # if check.contains(word[1]) #11000
        #11100
        #11010
        #11001
    # if check.contains(word[2]) #10100
        #10110
        #10101
    # if check.contains(word[3]) #10010
        #10011
    # if check.contains(word[4]) #10001
# if check.contains(word[1]) #01000
    # if check.contains(word[2]) #01100
        #01110
        #01101
    # if check.contains(word[3]) #01010
        #01011
    # if check.contains(word[4]) #01001
# if check.contains(word[2]) #00100
    #00110
    #00101
# if check.contains(word[3]) #00010
    #00011
# if check.contains(word[4]) #00001

# if check.contains(word[4]) == -1 #11110
# if check.contains(word[3]) == -1 #11101
# if check.contains(word[2]) == -1 #11011
# if check.contains(word[1]) == -1 #10111
# if check.contains(word[0]) == -1 #01111

# pattern1 = '[' + '^' + word + ']' == -1 #11111

#20000

#else 20000, 2...., 1....









print(pattern1)
if re.match(pattern1, ans):
    print("match1")
if re.match(pattern2, ans):
    print("match2")

def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')
