# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
import time

from crawl import sendmail
from downloadDealFile import deal_excel, read_file


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def write(file):
    path = file.split('/')[:-1]
    print(path)

def osc():
    t = time.strftime("%Y-%m-%d", time.localtime())
    os.mkdir(f'download/{t}')
def ces2(d = 3):
    import pdb
    a = "aaa"
    pdb.set_trace()
    # pdb.pm()
    b = "bbb"
    c = "ccc"
    final = a + b + c
    print(final)
    return final

# Press the green button in the gutter to run the script.
result2 = ['[更新日期]08-24  http://www.shiyebian.net/xinxi/387025.html  [主题]（第三批）',
       '[更新日期]08-24  http://www.shiyebian.net/xinxi/387024.html  [主题]（第四批）',]
atten = ['xxx.xlsx','xxx2.xls']
if __name__ == '__main__':
    # osc()
    # write('/Users/jackrechard/Desktop/ces.xlsx')
    # ces2()
    # ddir = '/Users/jackrechard/PycharmProjects/crawl_syb/download/2021-09-08'
    # atte = deal_excel(read_file(ddir))
    # print(atte)
    mesg = result2 + atten
    # sendmail(mesg=result2, atten=atte)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
