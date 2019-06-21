from selenium.webdriver.support.ui import Select   # Select类用于处理下拉框
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import datetime
from get_driver import driver


class save:
    def screenshot(self,name,type):
        #i=1
        scrpath = '/home/youmi/PycharmProjects/selenium_study/screenshot'  # 指定的保存目录
        timeee = datetime.datetime.now()# 2019-01-10 17:18:20.310134
        capturename = '/' + name + '--' + type + '--'+ str(timeee)+'.png'  # 自定义命名截图名字
        wholepath = scrpath + capturename
        if Path(scrpath).is_dir():  # 判断文件夹路径是否已经存在
            pass
        else:
            Path(scrpath).mkdir()  # 如果不存在，创建文件夹
        while Path(wholepath).exists():  # 判断文件是否已经存在，也可使用is_file()判断,若存在重新定义文件名
            i = 1
            capturename = '/' + str(i) + '.png'
            wholepath = scrpath + capturename
        #  driver.save_screenshot()
        driver.get_screenshot_as_file(wholepath)  # 不能接受Path类的值，只能是字符串，否则无法截图
        return capturename
s = save()