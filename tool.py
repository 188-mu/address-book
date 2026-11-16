def add(a,b):
    return a + b

# 只有直接运行 tool.py 才会执行下面这段
if __name__ == '__main__':
    print("我直接运行tool文件才会打印这句话")
    print(add(1,1))