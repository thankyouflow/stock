import requests
from bs4 import BeautifulSoup

def findStockNum(targetNum, name, beforResult):
    url = 'https://finance.naver.com/item/main.nhn?code=' + targetNum
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    tempDiv = soup.find_all('dd')[3].get_text().split(" ")
    if tempDiv[5] == '마이너스':
        result = '-' + tempDiv[6] + '%'
    else:
        result = '+' + tempDiv[6] + '%'

    if beforResult != result:
        print(name + ':' + result)
    return result
# 042370
# 대상 주가 확인
dic = {'d': ['012510',''], 'b': ['042370','']}
# dic = {'다보링크': ['340360',''], '미래나노텍': ['095500','']}

while True:
    for key in dic.keys():
        dic[key][1] = findStockNum(dic[key][0], key, dic[key][1])
