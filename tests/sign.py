"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-24 20:19:33
LastEditTime: 2024-05-24 23:44:33
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import requests

from datetime import datetime

now = datetime.now()

current_month = now.strftime("%m")

headers = {
    "Host": "api.kurobbs.com",
    # 'content-length': '95',
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "sec-ch-ua": "Chromium;v=124, Android",
    "source": "android",
    "sec-ch-ua-mobile": "?1",
    "user-agent": "Mozilla/5.0 (Linux; Android 14; 22081212C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.179 Mobile Safari/537.36 Kuro/2.2.0 KuroGameBox/2.2.0",
    "content-type": "application/x-www-form-urlencoded",
    "accept": "application/json, text/plain, */*",
    "devcode": "111.181.85.154, Mozilla/5.0 (Linux; Android 14; 22081212C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.179 Mobile Safari/537.36 Kuro/2.2.0 KuroGameBox/2.2.0",
    "token": "eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVkIjoxNzE2NTQ2Mzg2NTg1LCJ1c2VySWQiOjExMzgyOTM4fQ.82MBrGX5AGrFHZRYIcFH7HaSzsduGzvvW3LmR7rR2bo",
    "sec-ch-ua-platform": "Android",
    "origin": "https://web-static.kurobbs.com",
    "x-requested-with": "com.kurogame.kjq",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    # 'accept-encoding': 'gzip, deflate, br, zstd',
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "priority": "u=1, i",
}

data = {
    "gameId": "3",
    "serverId": "76402e5b20be2c39f095a152090afddc",
    "roleId": "103288838",
    "userId": "11382938",
    "reqMonth": current_month,
}

response = requests.post(
    "https://api.kurobbs.com/encourage/signIn/v2", headers=headers, data=data
)
data = response.json()
print(data)