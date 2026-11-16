# rate.py
import requests

# 接口地址：查询USD美元的最新汇率
url = "https://open.er-api.com/v6/latest/USD"

try:
    # get：向网址发送请求，timeout=10 最多等10秒，防止卡死
    resp = requests.get(url, timeout=10)

    # 等价判断：如果状态码不是200，直接抛出错误
    resp.raise_for_status()

    # 把返回的json字符串，转成Python字典，方便取值
    data = resp.json()

    # 取rates里面的CNY，就是美元兑人民币汇率
    cny_rate = data["rates"]["CNY"]
    eur_rate = data["rates"]["EUR"]
    jpy_rate = data["rates"]["JPY"]

    print("===== 实时汇率（1美元兑换）=====")
    print(f"人民币 CNY：{cny_rate:.2f}")
    print(f"欧元 EUR：{eur_rate:.2f}")
    print(f"日元 JPY：{jpy_rate:.2f}")

except requests.RequestException as e:
    # 网络超时、连不上、服务器报错都会进这里
    print(f"请求失败：{e}")