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
    app_score = {}
    desktop_score = {}
    driver.implicitly_wait(2)
    app_addr = []
    desktop_addr = []
    # driver.maximize_window()  # 最大化浏览器
    driver.get("https://developers.google.com/speed/pagespeed/insights")  # 通过get()方法，打开一个url站点
    time.sleep(5)
    input = driver.find_element_by_name("url")
    csvresult = read_csv2("webdata.csv")
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
            tag1 = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text() = '移动设备']")))
        except Exception:
            print(name + "检测失败")
            continue
        score1 = driver.find_element_by_class_name("lh-gauge__percentage")
        print(score1)
        app_score[name] = score1.text
        print(score1.text)
        time.sleep(5)
        p1 = s.screenshot(name, "移动设备")
        print(p1)
        app_addr.append(str(picture_to_github(p1)))

        tag2 = driver.find_element_by_xpath("//div[text() = '桌面设备']")
        tag2.click()
        time.sleep(2)
        score2 = driver.find_element_by_xpath(
            "//*[@id='page-speed-insights']/div[2]/div[2]/div[2]/div[2]/div[1]/div/div[1]/a/div[2]")
        desktop_score[name] = score2.text
        p2 = s.screenshot(name, "桌面设备")
        print(p2)
        desktop_addr.append(str(picture_to_github(p2)))
    print(app_score)
    print(desktop_score)
    # app_score = {"AG":90}
    # *************************************这里填写自己钉钉群自定义机器人的token*****************************************
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=febec6b869bf218de1798a25469fee9b34ff27c71a5d7f32348d0183dd9ee7eb'
    # 用户手机号列表
    at_mobiles = ['*************************这里填写需要提醒的用户的手机号码，字符串或数字都可以****************************']
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # FeedCard类型
    # title="AG"+"---"+str(app_score["AG"])
    card1 = CardItem(title="PageSpeed Insights--针对移动设备检测结果",
                     url="https://raw.githubusercontent.com/yaoguanfei/auto_Pagespeed_insight/master/screen_shot/PageSpeed_Insight.png",
                     pic_url="https://developers.google.com/speed/docs/insights/about?hl=zh-CN&utm_source=PSI&utm_medium=incoming-link&utm_campaign=PSI")
    card2 = CardItem(title="AG", url="http://www.11506.com/uploadfile/2018/1024/20181024102305336.jpg",
                     pic_url=app_addr[0])
    card3 = CardItem(title="优投", url="https://www.dingtalk.com/",
                     pic_url=app_addr[1])
    cards = [card1, card2, card3]
    xiaoding.send_feed_card(cards)
