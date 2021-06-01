import requests
from bs4 import BeautifulSoup


def returnFloat(data):
    return float(data[1:].split('%')[0])

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


# 거래량 top10에서 기준에 따른 회사 추출
# result = {}
# term = {}
# targetNum = ''
# gigun = -2
# breakCheck = False
# url = 'https://finance.naver.com/sise/sise_quant.nhn?sosok=0'

# while True:
#     req = requests.get(url)
#     html = req.text
#     soup = BeautifulSoup(html, 'html.parser')
#     # print(soup)
#     # temp = str(soup.find_all ('tr')[7]).split('td')
#     tempDiv = soup.find('div','box_type_l')
#     tempTr = tempDiv.find_all('tr')
#     for i, tr in enumerate(tempTr):
#         # 변동값 구하기
#         if tr.find('a'):
#             if result.get(tr.find('a').get_text()) != tr.find_all('span')[1].get_text().lstrip().rstrip() and result.get(tr.find('a').get_text()):
#                 termData = (returnFloat(result[tr.find('a').get_text()]) - returnFloat(tr.find_all('span')[1].get_text().lstrip().rstrip())) * -1
#                 term[tr.find('a').get_text()] += termData
#                 if term[tr.find('a').get_text()] <= gigun:
#                     print(str(tr.find('a'))[43:49])
#                     targetNum = str(tr.find('a'))[43:49]
#                     print(tr.find('a').get_text())
#                     print(term[tr.find('a').get_text()])
#                     breakCheck = True
#                     break
#             if not result.get(tr.find('a').get_text()):
#                 term[tr.find('a').get_text()] = 0
#             result[tr.find('a').get_text()] = tr.find_all('span')[1].get_text().lstrip().rstrip()
#
#     if breakCheck:
#         break

# 우리기술투자 041190
# 갤럭시아머니트리 094480
# 제주맥주 276730
# 네이버 035420
# 아주IB투자 027360
# 이스타코 015020
# 삼보산업 009620
# 넥스트아이 137940
# 한네트 052600
# SBI 019550
# 대상 주가 확인
dic = {'한네트': ['052600', ''], '아주IB투자': ['027360', ''], 'SBI': ['019550', '']}
# dic = {'이스타코': ['015020', '']}
while True:
    for key in dic.keys():
        dic[key][1] = findStockNum(dic[key][0], key, dic[key][1])
