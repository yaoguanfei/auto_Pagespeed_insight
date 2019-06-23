from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from read_csv import read_csv2
import time
from save_screenshot import s
from get_driver import driver
from chatbot import DingtalkChatbot, ActionCard, FeedLink, CardItem
from push_pic_github import picture_to_github

if __name__ == '__main__':
    #记录产品名和对应分数
    app_score = {}
    desktop_score = {}
    # 记录产品名和对应检测等级
    app_level = {}
    desktop_level = {}

    # 记录产品检测结果截图的url
    app_addr ={}
    desktop_addr ={}
    # driver.maximize_window()  # 最大化浏览器
    driver.implicitly_wait(2)
    driver.get("https://developers.google.com/speed/pagespeed/insights")  # 通过get()方法，打开一个url站点
    time.sleep(5)
    input = driver.find_element_by_name("url")
    #读取到的webdata.csv 的每一行数据
    csvresult = read_csv2("webdata.csv")
    # 遍历读取到数据，逐一进行检测，获取分数，上传截图到git上并返回图片url
    for i in range(len(csvresult)):
        name = str(csvresult[i][0])
        url = str(csvresult[i][1])
        input.clear()
        input.send_keys(url)
        input.send_keys(Keys.ENTER)
        wait = WebDriverWait(driver, 300)  # 显式等待，引入WebDriverWait，规定最大等待时长
        try:
            # 调用until方法，传入等待方法（节点出现）
            # 出现该元素是检测成功且完毕的必要条件
            # tag1 = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text() = '移动设备']")))
            tag1 = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text() = '实测数据']")))
        except Exception:
            print(name + "检测失败")
            continue
        score1 = driver.find_element_by_class_name("lh-gauge__percentage")
        app_score[name] = score1.text
        print(score1.text)
        time.sleep(5)
        p1 = s.screenshot(name, "移动设备")
        print(p1)
        app_addr[name] = str(picture_to_github(p1))

        tag2 = driver.find_element_by_xpath("//div[text() = '桌面设备']")
        tag2.click()
        time.sleep(2)
        score2 = driver.find_element_by_xpath(
            "//*[@id='page-speed-insights']/div[2]/div[2]/div[2]/div[2]/div[1]/div/div[1]/a/div[2]")
        desktop_score[name] = score2.text
        p2 = s.screenshot(name, "桌面设备")
        print(p2)
        desktop_addr[name] = str(picture_to_github(p2))
    print(app_score)
    print(desktop_score)
    print(app_addr)
    print(desktop_addr)
    # 对获取的分数进行排序，评级
    # 95-100：S   90-94： A    80-89：B   70-79： C   60-69：D  <60 :不及格
    # app_score={"ag":88,"youtou":45,"ying":77}
    app_level = [[0 for i in range(2)] for j in range(10)]  #列表生成式法生成二维数组
    tuple_app_score = sorted(app_score.items(), key=lambda item: item[1],reverse=True)#排序后结果[(AG,90),(youtou,88)...]
    for i in range(len(tuple_app_score)):
        n = tuple_app_score[i][0]
        f = tuple_app_score[i][1]
        app_level[i][0] = n
        if f >= 95 :
            app_level[i][1] ="S"
        elif f >= 90:
            app_level[i][1] = "A"
        elif f >= 80:
            app_level[i][1] = "B"
        elif f >= 70:
            app_level[i][1] = "C"
        elif f >= 70:
            app_level[i][1] = "D"
        else:
            app_level[i][1] = "不及格"
    print(app_level)
    # *************************************这里填写自己钉钉群自定义机器人的token*****************************************
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=febec6b869bf218de1798a25469fee9b34ff27c71a5d7f32348d0183dd9ee7eb'
    # 用户手机号列表
    at_mobiles = ['*************************这里填写需要提醒的用户的手机号码，字符串或数字都可以****************************']
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # FeedCard类型
    # title="AG"+"---"+str(app_score["AG"])
    print(app_addr[0])
    print(app_addr[1])
    card1 = CardItem(title="PageSpeed Insights--针对移动设备检测结果",
                     url="https://developers.google.com/speed/?hl=zh-CN&utm_source=PSI&utm_medium=incoming-link&utm_campaign=PSI",
                     pic_url="https://raw.githubusercontent.com/yaoguanfei/auto_Pagespeed_insight/master/screen_shot/PageSpeed_Insight.png")
    card2 = CardItem(title=app_level[0][0]+"---"+app_level[0][1], url=app_addr[0],
                     pic_url="http://www.11506.com/uploadfile/2018/1024/20181024102305336.jpg")
    card3 = CardItem(title=app_level[1][0]+"---"+app_level[0][1], url=app_addr[1],
                     pic_url="http://www.11506.com/uploadfile/2018/1024/20181024102305336.jpg")
    card4 = CardItem(title=app_level[2][0]+"---"+app_level[0][1], url=app_addr[1],
                     pic_url="http://www.11506.com/uploadfile/2018/1024/20181024102305336.jpg")
    cards = [card1, card2, card3,card4]
    xiaoding.send_feed_card(cards)
