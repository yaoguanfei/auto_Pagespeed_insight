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
from summary_result import summary_result
from config import Chinese_to_English

if __name__ == '__main__':
    # 记录产品名和对应分数
    app_score = {}
    desktop_score = {}
    # 记录产品名和对应logo的线上地址
    name_logo = {}

    # 记录产品检测结果截图的url
    app_addr = {}
    desktop_addr = {}

    driver.implicitly_wait(1)
    driver.get("https://developers.google.com/speed/pagespeed/insights")  # 通过get()方法，打开一个url站点
    time.sleep(2)
    input = driver.find_element_by_name("url")
    # 读取到的webdata.csv 的每一行数据
    csvresult = read_csv2("webdata.csv")
    # 遍历读取到数据，逐一进行检测，获取分数，上传截图到git上并返回图片url
    for i in range(len(csvresult)):
        name = str(csvresult[i][0])
        english_name = Chinese_to_English[name]
        url = str(csvresult[i][1])
        logo = str((csvresult[i][2]))
        name_logo[name] = logo
        input.clear()
        input.send_keys(url)
        input.send_keys(Keys.ENTER)
        wait = WebDriverWait(driver, 500)  # 显式等待，引入WebDriverWait，规定最大等待时长
        try:
            # 调用until方法，传入等待方法（节点出现）
            # 出现该元素是检测成功且完毕的必要条件
            tag1 = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text() = '实测数据']")))
        except Exception:
            print(name + "检测失败")
            continue
        score1 = driver.find_element_by_class_name("lh-gauge__percentage")
        app_score[name] = score1.text
        print(score1.text)
        time.sleep(2)
        p1 = s.screenshot(english_name, "app")
        print(p1)
        app_addr[name] = str(picture_to_github(p1))
        time.sleep(2)
        tag2 = driver.find_element_by_xpath("//div[text() = '桌面设备']")
        tag2.click()
        time.sleep(2)
        score2 = driver.find_element_by_xpath(
            "//*[@id='page-speed-insights']/div[2]/div[2]/div[2]/div[2]/div[1]/div/div[1]/a/div[2]")
        desktop_score[name] = score2.text
        p2 = s.screenshot(english_name, "desktop")
        print(p2)
        desktop_addr[name] = str(picture_to_github(p2))

    driver.quit()

    app_result = summary_result(app_score, app_addr, name_logo)
    desktop_result = summary_result(desktop_score, desktop_addr, name_logo)
    print("桌面设备检查结果：")
    print(desktop_result)
    print("移动设备检查结果：")
    print(app_result)

    # *************************************这里填写自己钉钉群自定义机器人的token*****************************************
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=febec6b869bf218de1798a25469fee9b34ff27c71a5d7f32348d0183dd9ee7eb'
    # 用户手机号列表
    # at_mobiles = ['*************************这里填写需要提醒的用户的手机号码，字符串或数字都可以****************************']
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # FeedCard类型
    # title="AG"+"---"+str(app_score["AG"])

    card1 = CardItem(title="桌面设备-加载性能排行榜",
                     url="https://www.yuque.com/youmiqa/wiki/kshrho",
                     pic_url="https://raw.githubusercontent.com/yaoguanfei/auto_Pagespeed_insight/master/screen_shot/PageSpeed_Insight.png")
    card2 = CardItem(
        title="No.1 " + desktop_result[0][0] + "(%s分)" % desktop_result[0][4] + "---" + desktop_result[0][1],
        url=desktop_result[0][2],
        pic_url=desktop_result[0][3])
    card3 = CardItem(
        title="No.2 " + desktop_result[1][0] + "(%s分)" % desktop_result[1][4] + "---" + desktop_result[1][1],
        url=desktop_result[1][2],
        pic_url=desktop_result[1][3])
    card4 = CardItem(
        title="No.3 " + desktop_result[2][0] + "(%s分)" % desktop_result[2][4] + "---" + desktop_result[2][1],
        url=desktop_result[2][2],
        pic_url=desktop_result[2][3])
    card5 = CardItem(
        title="No.4 " + desktop_result[3][0] + "(%s分)" % desktop_result[3][4] + "---" + desktop_result[3][1],
        url=desktop_result[2][2],
        pic_url=desktop_result[3][3])
    desktop_cards = [card1, card2, card3, card4, card5]
    xiaoding.send_feed_card(desktop_cards)

    card1 = CardItem(title="移动设备-加载性能排行榜",
                     url="https://www.yuque.com/youmiqa/wiki/kshrho",
                     pic_url="https://raw.githubusercontent.com/yaoguanfei/auto_Pagespeed_insight/master/screen_shot/PageSpeed_Insight.png")
    card2 = CardItem(title="No.1 " + app_result[0][0] + "(%s分)" % app_result[0][4] + "---" + app_result[0][1],
                     url=app_result[0][2],
                     pic_url=app_result[0][3])
    card3 = CardItem(title="No.2 " + app_result[1][0] + "(%s分)" % app_result[1][4] + "---" + app_result[1][1],
                     url=app_result[1][2],
                     pic_url=app_result[1][3])
    card4 = CardItem(title="No.3 " + app_result[2][0] + "(%s分)" % app_result[2][4] + "---" + app_result[2][1],
                     url=app_result[2][2],
                     pic_url=app_result[2][3])
    card5 = CardItem(title="No.4 " + app_result[3][0] + "(%s分)" % app_result[3][4] + "---" + app_result[3][1],
                     url=app_result[3][2],
                     pic_url=app_result[3][3])
    app_cards = [card1, card2, card3, card4, card5]
    xiaoding.send_feed_card(app_cards)
