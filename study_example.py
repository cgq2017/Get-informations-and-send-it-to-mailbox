import re
import requests
import urllib.request
from bs4 import BeautifulSoup
import csv
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from lxml import etree
from bs4 import BeautifulSoup

def craw_spider(url):
    headers = {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE'
    }
    html=requests.get(url,headers=headers)
    html=html.text.encode(html.encoding).decode('utf-8')
    return html

file_name=open('111.csv','w',newline='')
f=csv.writer(file_name)
l=input("输入要抓取的网址网址:")
for i in range(91):
    if(i==0):
        url='http://'+l+'/mov/HHMP4/index.html'
    else:
        url='http://'+l+'/mov/HHMP4/index-{}.html'.format(i)
    html=craw_spider(url)

    s = re.findall('<li.*?href="(.*?)".*?alt="(.*?)".*?target="_blank".*?img.*?src="(.*?)".*?class="movie_date">(.*?)<.*?</li>', html, re.S)
    for i in range(len(s)):
        # urllib.request.urlretrieve(s[i][2], 'img/{}.jpg'.format(s[i][1]))
        f.writerow((s[i][1],'http://'+l+s[i][0],s[i][3]))
        print(s[i][1],'http://'+l+s[i][0],s[i][3])
file_name.close()

def mail(text):
    '''邮件发送'''
    my_sender = '1447559371@qq.com'  # 发件人邮箱账号
    my_pass = 'vdmxhejbkxxdgheh'  # 发件人邮箱授权密码
    my_user = '18722376525@163.com'  # 收件人邮箱账号，我这边发送给自己

    try:
        msg=MIMEMultipart()
        content1 = MIMEText(text, 'plain', 'utf-8')
        msg['From'] = formataddr(["FromRunoob", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "您好！"  # 邮件的主题，也可以说是标题
        msg.attach(content1)
        filename = r'111.csv'
        if os.path.exists(filename):
            att1 = MIMEApplication(open(filename, 'rb').read())
            att1.add_header('Content-Disposition', 'attachment', filename='data_qcwy.csv')
            msg.attach(att1)
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        print("邮件发送成功")
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print("邮件发送失败")

mail("好资源")

