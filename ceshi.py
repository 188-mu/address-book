count = 0
def bump():
    global count
    count = count + 1          # 函数内赋值让 count 变成局部变量
    return count
print(bump())