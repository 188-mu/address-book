import random
def make_secret():
    """生成 1-100 的随机答案"""
    return random.randint(1, 100)

def read_guess():
    """读玩家输入的猜测，返回整数"""
    return int(input("猜一个数："))

def check(guess, answer):
    """比较猜测和答案，返回 '大了' / '小了' / '对了'"""
    if guess > answer:
        return "大了"
    elif guess < answer:
        return "小了"
    else:
        return "对了"
def main():
    while True:
        answer = make_secret()
        count = 0
        result = ""                    # ← 注意：它在循环外面先定义

        while count < 7:
            guess = read_guess()
            count += 1
            result = check(guess, answer)

            if result == "对了":
                print(f"对了！你用了 {count} 次")
                break

            print(result)
        if result !="对了":
            print(f"机会用完了。答案是：{answer}")
        again=input("再来一局?(y/n):")
        if again !="y":
            break
main()