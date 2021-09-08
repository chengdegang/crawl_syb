# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
import time


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def write(file):
    path = file.split('/')[:-1]
    print(path)

def osc():
    t = time.strftime("%Y-%m-%d", time.localtime())
    os.mkdir(f'download/{t}')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    osc()
    # write('/Users/jackrechard/Desktop/ces.xlsx')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
