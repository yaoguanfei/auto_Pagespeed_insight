# -*- coding: utf-8 -*-
# from imp import reload
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
#必须加上上面四行,否则各种编码的错误爆出

import os
def picture_to_github(path):
    os.system("cd /home/youmi/PycharmProjects/selenium_study && git add . && git status && git commit -a -m 'update' && git push  origin master")
    pic_addr = "https://raw.githubusercontent.com/yaoguanfei/PageSpeed_insight_picture/master/screen_shot%s" % path
    return pic_addr