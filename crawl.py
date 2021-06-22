import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import bs4
import re

#master
# webbrowser.open('http://www.shiyebian.net/zhejiang/hangzhou/')
# res = requests.get('http://www.shiyebian.net/zhejiang/hangzhou/')
# print(type(res))
# res.status_code == requests.codes.ok
# res.raise_for_status()

#转成bs4，方便提取html信息
# soup = bs4.BeautifulSoup(open('data/result.txt','r',encoding='gbk'), 'html.parser')
# print(type(soup))
# elements = soup.select('div')
# print(len(elements))
#查找每日公告
# info = soup.find_all('ul', class_='lie1')
# print(info)
#获取所有的文本信息
# info_text = info[0].getText()
# print(info_text)

#获取前五十个招考信息,作为一个新的列表
def get_50():
    res = requests.get('http://www.shiyebian.net/zhejiang/hangzhou/')
    res.raise_for_status()
    # 将页面源码写入本地
    with open('/Users/jackrechard/PycharmProjects/crawl_syb/data/result.txt', 'wb') as result:
        for line in res.iter_content(200000):
            result.write(line)
    result.close()
    soup = bs4.BeautifulSoup(open('/Users/jackrechard/PycharmProjects/crawl_syb/data/result.txt', 'r', encoding='gbk'), 'html.parser')
    result_2 = []
    i = 1
    while i <= 50:
        info = soup.select(
            f'body > div.main > div.listl.fl > div.listrr.fr > div > div.listlie > ul> li:nth-child({i})')
        info = str(info)
        i = i + 1
        #不去除【】，现去除后格式不一致影响判断
        # info = info.lstrip('[')
        # info = info.rstrip(']')
        # print(info)
        result_2.append(info)
    # 去掉列表括号
    # result_2 = ''.join(result_2)
    # print(result_2)
    return result_2


# print(result_2)
# body > div.main > div.listl.fl > div.listrr.fr > div > div.listlie > ul> li:nth-child(6)
# print(res)
#传入列表初步记录到本地的函数
def record(list):
    with open('/Users/jackrechard/PycharmProjects/crawl_syb/data/record.txt','w') as record:
        for line in list:
            record.write(str(line) + '\n')

#读取历史保存的文件并转换成列表
def reopen():
    reopen_list =[]
    with open('/Users/jackrechard/PycharmProjects/crawl_syb/data/record.txt','r') as refile:
        rerecord = refile.readlines()
        for line in rerecord:
            #去掉换行符
            line = line.strip('\n')
            reopen_list.append(line)
    # print(reopen_list)
    return reopen_list

#传入两个列表，输出需要的列表1
def judge(listnew,listold):
    a = [x for x in listnew if x in listold]  # 两个列表表都存在
    b = [y for y in (listnew + listold) if y not in a]
    # print(f'same is:{a}')
    # print(f'notsame is:{b}')
    c = []
    for z in b:
        if z in listnew and z in listold :
            continue
        else:
            if z in listnew:
                c.append(z)
    print(c)
    return c

#传入两个列表，输出需要的列表2,简单方式
def judge2(listnew,listold):
    c = []
    for z in listnew:
        if z in listold:
            continue
        else:
            c.append(z)

    # print(c)
    return c

#list参考格式
listces = [
        '[<li><em>05-14</em><a href="http://www.shiyebian.net/xinxi/376489.html" target="_blank">2021年杭州住房公积金管理中心桐庐分中心招聘编外人员公告</a></li>]',
        '[<li><em>05-14</em><a href="http://www.shiyebian.net/xinxi/376488.html" target="_blank">2021年杭州市桐庐县商务局（桐庐迎春商务区管理委员会）招聘编外人员公告</a></li>]',
        '[<li><em>05-13</em><a href="http://www.shiyebian.net/xinxi/376344.html" target="_blank">2021年杭州市桐庐县行政服务中心招聘编外人员公告</a></li>]']
#将要输出的数据进行处理
def organize_data(list):
    res = []
    for line in list:
        #通过正则匹配每行对应的内容
        time = re.findall(r"<li><em>(.+?)</em>", line)
        time = ''.join(time)
        url = re.findall(r'href="(.+?)" target', line)
        url = ''.join(url)
        title = re.findall(r'_blank">(.+?)</a', line)
        title = ''.join(title)
        mes =  f'更新日期:{time}  url:{url}  主题:{title}'
        # print(mes)
        res.append(mes)
    # print(res)
    return res

def sendmail(mesg):
    smtpserver = 'smtp.qq.com'
    username = 'chengdgccc@qq.com'
    password = 'glgfdpxlnhiogaji'
    sender = 'chengdgccc@qq.com'
    receivers = ['18868890069@163.com']

    subject = 'syb reminder'

    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = 'QA_CCC'
    msg['To'] = 'ccc'

    #处理入参数据
    mesg_2 = ''
    for i in range(len(mesg)):
        mesg_2 = mesg_2 + mesg[int(i)] + '\n'

    text = f"Hi!\nThis is the mes u care about:\n{mesg_2}"
    text_plain = MIMEText(text, 'plain', 'utf-8')
    msg.attach(text_plain)

    smtp = smtplib.SMTP_SSL(smtpserver)
    smtp.connect(smtpserver, '465')
    smtp.login(username, password)
    smtp.sendmail(sender, receivers, msg.as_string())
    print("send success")
    smtp.quit()

#第一步，获取当日最新的数据
#第二步，将当日的数据与昨日的数据对比并处理结果数据到可用程度
result = judge2(get_50(),reopen())
#第四步，做判断，若result有更新即大于0，则运行组织函数及发信函数
if len(result) > 0 :
    print("今天更新了")
    result2 = organize_data(result)
    sendmail(result2)
else:
    print("今天没有更新")

#第五步，保存今日的数据并覆盖历史数据
record(get_50())

# organize_data(listces)

# result2 = organize_data(listces)
# sendmail(result2)