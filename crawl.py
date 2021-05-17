import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import webbrowser
import pyperclip
import requests
import bs4
import re

# webbrowser.open('http://www.shiyebian.net/zhejiang/hangzhou/')
res = requests.get('http://www.shiyebian.net/zhejiang/hangzhou/')
# print(type(res))
# res.status_code == requests.codes.ok
res.raise_for_status()
#将页面源码写入本地
with open('data/result.txt','wb') as result:
    for line in res.iter_content(200000):
        result.write(line)
result.close()

#转成bs4，方便提取html信息
soup = bs4.BeautifulSoup(open('data/result.txt','r',encoding='gbk'), 'html.parser')
print(type(soup))
# elements = soup.select('div')
# print(len(elements))
#查找每日公告
# info = soup.find_all('ul', class_='lie1')
# print(info)
#获取所有的文本信息
# info_text = info[0].getText()
# print(info_text)

#获取前五十个招考信息
def get_50():
    result_2 = []
    i = 1
    while i <= 50:
        info = soup.select(
            f'body > div.main > div.listl.fl > div.listrr.fr > div > div.listlie > ul> li:nth-child({i})')
        print(info)
        i = i + 1
        result_2.append(info)
    return result_2

# print(result_2)
# body > div.main > div.listl.fl > div.listrr.fr > div > div.listlie > ul> li:nth-child(6)
# print(res)
#传入列表初步记录到本地的函数
def record(list):
    with open('data/record.txt','w') as record:
        for line in list:
            record.write(str(line) + '\n')

#读取历史保存的文件并转换成列表
def reopen():
    reopen_list =[]
    with open('data/record.txt','r') as refile:
        rerecord = refile.readlines()
        for line in rerecord:
            #去掉换行符
            line = line.strip('\n')
            reopen_list.append(line)
    print(reopen_list)
    return reopen_list

#传入两个列表，输出需要的列表
def judge(listnew,listold):
    a = [x for x in listnew if x in listold]  # 两个列表表都存在
    b = [y for y in (listnew + listold) if y not in a]
    # print(f'same is:{a}')
    # print(f'notsame is:{b}')
    c = []
    for z in b:
        if z in listnew:
            c.append(z)
    print(c)
    return c

#将要输出的数据进行处理
def organize_data():
    listces = [
        '[<li><em>05-14</em><a href="http://www.shiyebian.net/xinxi/376489.html" target="_blank">2021年杭州住房公积金管理中心桐庐分中心招聘编外人员公告</a></li>]',
        '[<li><em>05-14</em><a href="http://www.shiyebian.net/xinxi/376488.html" target="_blank">2021年杭州市桐庐县商务局（桐庐迎春商务区管理委员会）招聘编外人员公告</a></li>]',
        '[<li><em>05-13</em><a href="http://www.shiyebian.net/xinxi/376344.html" target="_blank">2021年杭州市桐庐县行政服务中心招聘编外人员公告</a></li>]']
    for line in listces:
        time = re.findall(r"<li><em>(.+?)</em>", line)
        url = re.findall(r'href="(.+?)" target', line)
        title = re.findall(r'_blank">(.+?)</a', line)
        print(f'时间：{time}+url：{url}+主题：{title}')

def sendmail():
    smtpserver = 'smtp.qq.com'
    username = 'chengdgccc@qq.com'
    password = 'glgfdpxlnhiogaji'
    sender = 'chengdgccc@qq.com'
    receivers = ['chengdegang@ezxr.com']

    subject = 'syb reminder'

    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = 'QA_CCC'
    msg['To'] = 'qa'

    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.baidu.com\nces1018"
    text_plain = MIMEText(text, 'plain', 'utf-8')
    msg.attach(text_plain)

    smtp = smtplib.SMTP_SSL(smtpserver)
    smtp.connect(smtpserver, '465')
    smtp.login(username, password)
    smtp.sendmail(sender, receivers, msg.as_string())
    print("send success")
    smtp.quit()

# record(get_50())
# reopen()
organize_data()