import shutil
import stat
import time
import zipfile
import requests
import os
import re
import bs4
from deal_xlsx import write_excel
from deal_xlsx import merged_deal_xlsx
from deal_xlsx import openpy_read_xlsx
from deal_xls import merged_deal_xls
from pathlib import Path
import pdb

listces = [
        '[<li><em>05-14</em><a href="http://www.shiyebian.net/xinxi/376489.html" target="_blank">2021年杭州住房公积金管理中心桐庐分中心招聘编外人员公告</a></li>]',
        '[<li><em>05-14</em><a href="http://www.shiyebian.net/xinxi/382934.html" target="_blank">2021年杭州市桐庐县商务局（桐庐迎春商务区管理委员会）招聘编外人员公告</a></li>]',
        '[<li><em>05-13</em><a href="http://www.shiyebian.net/xinxi/376344.html" target="_blank">2021年杭州市桐庐县行政服务中心招聘编外人员公告</a></li>]']

org = ['[更新日期]08-24  http://www.shiyebian.net/xinxi/387025.html  [主题]2021年浙江师范大学招聘公告（第三批）',
       '[更新日期]08-24  http://www.shiyebian.net/xinxi/387024.html  [主题]2021年浙江杭州电子科技大学招聘公告（第四批）',
       '[更新日期]08-24  http://www.shiyebian.net/xinxi/387023.html  [主题]2021年浙江工商大学招聘公告（第三批）']
# print(org)

def read_file(file,needall=False):
    """
    读取输入路径下的所有xlsx&xls文件，并返回一个列表，默认不遍历子文件夹
    """
    filexl = []
    if needall:
        for root, dirs, files in os.walk(file):
            for f in files:
                if os.path.splitext(os.path.join(root, f))[1] == '.xlsx':
                    filexl.append(os.path.join(root, f))
                if os.path.splitext(os.path.join(root, f))[1] == '.xls':
                    filexl.append(os.path.join(root, f))
    else:
        # tf = file.split("/")[:-1]
        # tf = '/'.join(tf)
        # pdb.set_trace()
        for f in os.listdir(file):
            if os.path.splitext(f)[1] == '.xlsx':
                filexl.append(os.path.join(file, f))
            if os.path.splitext(f)[1] == '.xls':
                filexl.append(os.path.join(file, f))

    if len(filexl) == 0:
        print("当前路径下.xlsx及.xls文件为0")
    # print(filexl)
    return filexl

def down_excel(list):
    """
    入参为organize_data()处理过的数据列表，读取其中的url地址并遍历去请求，
    获取每一个url地址对应的所有xlsx及xls的文件，并下载到本地
    """
    urls = []
    excel_urls = []
    for i in list:
        url = re.findall(r" (.+?) ", i)
        url = ''.join(url)
        url = url.strip(' ')
        urls.append(url)
    #遍历urls去下载excel
    for url in urls:
        res = requests.get(url)
        with open('/Users/jackrechard/PycharmProjects/crawl_syb/data/detail_result.txt', 'wb') as detail_result:
            for line in res.iter_content(200000):
                detail_result.write(line)
        detail_result.close()
        soup = bs4.BeautifulSoup(
            open('/Users/jackrechard/PycharmProjects/crawl_syb/data/detail_result.txt', 'r', encoding='gbk'), 'html.parser')
        name = soup.select('body > div.main > div.mleft.fl > div.content > h1')
        name = re.findall(r"<h1>(.+?)</h", str(name))
        # print(name[0]) #每一个待下载的标题
        #查找所有为标签a的数据
        hrefs = str(soup.find_all("a"))
        #以逗号为分割将上面提取的数据转为列表
        hrefs = hrefs.split(',')
        #创建以日期命名的文件夹
        t = time.strftime("%Y-%m-%d", time.localtime())
        if os.path.exists(f'/Users/jackrechard/PycharmProjects/crawl_syb/download/{t}') == True:
            pass
        else:
            os.mkdir(f'/Users/jackrechard/PycharmProjects/crawl_syb/download/{t}')
        #正则匹配hrefs列表里包含xlsx的数据
        for i in hrefs:
            excel_url1 = re.findall(r'http.*.xlsx"', i)
            excel_url1 = ''.join(excel_url1)
            excel_url1 = excel_url1.strip('"')
            excel_url2 = re.findall(r'http.*.xls"', i)
            excel_url2 = ''.join(excel_url2)
            excel_url2 = excel_url2.strip('"')
            if len(excel_url1) > 0:
                excel_urls.append(excel_url1)
                res2 = requests.get(excel_url1)
                print("dwonloading file xlsx...")
                with open(f'/Users/jackrechard/PycharmProjects/crawl_syb/download/{t}/{name[0]}.xlsx', 'wb') as f:
                    f.write(res2.content)
            if len(excel_url2) > 0:
                excel_urls.append(excel_url2)
                res3 = requests.get(excel_url2)
                print("dwonloading file xls...")
                with open(f'/Users/jackrechard/PycharmProjects/crawl_syb/download/{t}/{name[0]}.xlsx', 'wb') as f:
                    f.write(res3.content)
    print('down success~')
    return f'/Users/jackrechard/PycharmProjects/crawl_syb/download/{t}'

def testrequest():
    print("dwonloading file...")
    res = requests.get('http://d.shiyebian.net/shiyebian/d/2021/20210709/2021年杭州市临安区部分基层医疗卫生事业单位统一公开招聘工作人员计划表c.xlsx')
    with open('test.xlsx','wb') as f:
        f.write(res.content)

def deal_excel(flist):
    """
    输入为一个xlsx&xls的路径列表,输出为根据deal_xlsx与deal_xls筛选条件筛选的列表，列表为excel的文件名
    :return:
    """
    attention = []
    for f in flist:
        # pdb.set_trace()
        #区分xls及xlsx并处理
        # print(os.path.splitext(f))
        if os.path.splitext(f)[1] == '.xlsx':
            ff = f
            try:
                write_excel(file=ff, data=merged_deal_xlsx(ff), sheetname='tempxlsx')
                data = openpy_read_xlsx(file=ff, sheetname='tempxlsx',
                                    rvalue1='序号',rvalue2='专业',cvalue='电气工程')
                # print(len(data)) #无数据时等于1
                if len(data) > 1:
                    info = ff.split("/")[:-1]
                    attention.append(info)
                    print(f'xlsx找到符合条件的数据了~ 它是: {ff}')
                write_excel(file=ff, data=data, sheetname='finalxlsx')
            except zipfile.BadZipFile:
                print(f'文件异常，请检查,路径为：{ff}')
        if os.path.splitext(f)[1] == '.xls':
            ff = f
            writeff = f'{os.path.splitext(ff)[0]}_cg.xlsx'
            write_excel(file=writeff, data=merged_deal_xls(ff), sheetname='tempxlsx')
            # shutil.move(str(f'{os.getcwd()}/file/{f_name}'), f'{newdir}/')
            newdir = Path(f"{'/'.join(ff.split('/')[:-1])}/xls/")
            if newdir.exists():
                print('cunz')
            else:
                os.mkdir(newdir)
            shutil.move(str(ff),newdir)#写入后将原始文件移动
            data = openpy_read_xlsx(file=writeff, sheetname='tempxlsx',
                                    rvalue1='序号',rvalue2='专业',cvalue='电气工程')
            if len(data) > 1:
                info = ff.split("/")[:-1]
                attention.append(info)
                print(f'xls找到符合条件的数据了~ 它是: {ff}')
            write_excel(file=writeff, data=data, sheetname='finalxlsx')
    print(attention)
    return attention

def del_file(path,d=True):
    # if d == True:
    #     try:
    #         os.remove('/ces')
    #         print('delete ok~')
    #     except Exception:
    #         print('delete failed ..')
    # os.chmod(path, stat.S_IXUSR)
    os.remove(path)

if __name__ == '__main__':
    print("调用了downloadDealFile~~~")
    # read_file(file='/Users/jackrechard/PycharmProjects/testexcel/file',needall=False)
    # organize_data(listces)
    # down_excel(org)
    # testrequest()
    #遍历下载文件的路径下所有的xls及xlsx文件并处理
    # deal_excel(read_file(file='/Users/jackrechard/PycharmProjects/crawl_syb/download/2021-09-08'))
    # del_file(path='ces')

