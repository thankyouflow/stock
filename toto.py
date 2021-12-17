import requests
from bs4 import BeautifulSoup
from datetime import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import threading
import pandas as pd
import datetime
from email.mime.text import MIMEText
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def Dividend_temp():
    url = 'http://oddsdata365.com/?Sport_Name_Kor=야구&Location_Name_Kor=&League_Name_Kor=&team_se='
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    dic = {}
    tbody = soup.find('tbody')
    tr = tbody.find_all('tr')
    for a in tr:
        cs = str(a).split('\n')[0].split('\"')[1]
        tr1 = tbody.find('tr', {'class': '{}'.format(cs)})
        if tr1:
            if float(tr1.find_all('td')[8].text) >= 2 or float(tr1.find_all('td')[10].text) >= 2:
                dic[cs] = [float(tr1.find_all('td')[8].text),
                           float(tr1.find_all('td')[10].text),
                           tr1.find_all('td')[3].text,
                           tr1.find_all('td')[7].text,
                           tr1.find_all('td')[5].text,
                           tr1.find_all('td')[6].text,
                           'w' if float(tr1.find_all('td')[8].text) > float(tr1.find_all('td')[10].text) else 'l']

    return dic

def Dividend_now(dic_temp):
    url = 'http://oddsdata365.com/?Sport_Name_Kor=야구&Location_Name_Kor=&League_Name_Kor=&team_se='
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')


    tbody = soup.find('tbody')

    dic = {}

    for key in dic_temp.keys():
        tr = tbody.find('tr', {'class': '{}'.format(key)})
        if tr:
            result = 'w' if float(tr.find_all('td')[8].text) > float(tr.find_all('td')[10].text) else 'l'
            if result != dic_temp[key][5]:
                dic[key] = dic_temp[key]
                dic[key] = float(tr.find_all('td')[8].text)
                dic[key] = float(tr.find_all('td')[10].text)
                dic[key] = result

    return dic


while True:
    print('===================================')
    print('temp 시작')
    dic_temp = Dividend_temp()
    print('temp 성공')

    time.sleep(20)

    print('now 시작')
    time_now = str(datetime.datetime.today())[11:16]
    dic = Dividend_now(dic_temp)
    print('now 성공')



    print('확인')
    if dic:
        data = {
            '키값': [],
            '이전': [],
            '배당': [],
            '기준': [],
            '마켓': [],
            '경기': []
        }

        for key in dic.keys():
            data['키값'].append(key)
            data['경기'].append(dic[key][4] + ' VS ' + dic[key][5])
            data['마켓'].append(dic[key][2])
            data['기준'].append(dic[key][3])
            data['배당'].append(str(dic[key][0]) + ' - ' + str(dic[key][1]))
            data['이전'].append(str(dic[key][0]) + ' - ' + str(dic[key][1]))

        print('발견 !')
        df = pd.DataFrame(data)
        filename = 'baseball_{}.xlsx'.format(time_now)
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='야구')
        writer.close()

        # 세션 생성

        s = smtplib.SMTP('smtp.gmail.com', 587)

        # TLS 보안 시작

        s.starttls()

        # 로그인 인증

        s.login('jshi2525@gmail.com', 'iwktyocpixixffgd')

        # 제목, 본문 작성
        msg = MIMEMultipart()
        msg['Subject'] = filename
        msg.attach(MIMEText('건승!', 'plain'))

        # 첨부파일 경로/이름 지정하기
        attachment = open(filename, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + filename)
        msg.attach(part)

        # 메일 보내기

        s.sendmail("jshi2525@gmail.com", "jshi25@naver.com", msg.as_string())

        # 세션 종료

        s.quit()

        path = "/Users/tyflow/Downloads/chromedriver"
        driver = webdriver.Chrome(path)

    else:
        print('발견 X')
