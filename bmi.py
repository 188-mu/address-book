height=float(input("请输入身高（米）:"))
weight=float(input("请输入体重（公斤）:"))

bmi=weight/height**2

print(f"身高是 {height:g}  体重是 {weight:g}   BMI是{bmi:.1f}")
if bmi>25:
    print ("胖")
elif bmi<22:
    print ("瘦")
else:
    print("真好")
