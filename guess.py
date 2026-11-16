import random
while True:
    answer=random.randint(1,100)
    count=0
    while count<7:
       guess=int(input("猜一个数："))
       count+=1
       if guess>answer:
           print("大了")
       elif guess<answer:
           print("小了")
              
       else:
           print(f"对了,你用了{count}次")
           break
    else:
       print(f"机会用完了，答案是：{answer}")
    again=input("还继续吗，继续请输(j/n):")
    if again!="j":
        break
