# -*- coding:utf8 -*-
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
from push_pic_github import picture_to_gitlab
from summary_result import summary_result
from config import Chinese_to_English
import sys

if __name__ == '__main__':
    # 记录产品名和对应分数
    # app_score = {}
    desktop_score = {}
    # 记录产品名和对应logo的线上地址
    name_logo = {}

    # 记录产品检测结果截图的url
    # app_addr = {}
    desktop_addr = {}

    driver.implicitly_wait(3)

    driver.get("https://developers.google.com/speed/pagespeed/insights")  # 通过get()方法，打开一个url站点
    driver.get_screenshot_as_file('/opt/lampp/htdocs/img/google/home.png')
    # import requests
    # res = requests.get('https://developers.google.com/speed/pagespeed/insights').text
    # print(res)
    # print(driver.current_url)
    time.sleep(300)
    page = driver.page_source
    print(page)
    # input = driver.find_element_by_name("url")

    input = driver.find_element_by_class_name("label-input-label")
    # 读取到的webdata.csv 的每一行数据
    csvresult = read_csv2("webdata.csv")
    # 清除浏览器cookies
    cookies = driver.get_cookies()
    print(f"main: cookies = {cookies}")
    driver.delete_all_cookies()
    # 遍历读取到数据，逐一进行检测，获取分数，上传截图到github上并返回图片url
    for i in range(len(csvresult)):
        name = str(csvresult[i][0])
        english_name = Chinese_to_English[name]
        url = str(csvresult[i][1])
        logo = str((csvresult[i][2]))
        name_logo[name] = logo
        input.clear()
        input.send_keys(url)
        print(url)
        input.send_keys(Keys.ENTER)
        wait = WebDriverWait(driver, 300)  # 显式等待，引入WebDriverWait，规定最大等待时长
        try:
            # 调用until方法，传入等待方法（节点出现）
            # 出现该元素是检测成功且完毕的必要条件
            # 有头
            # tag1 = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text() = '实测数据']")))
            # tag1 = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-speed-insights']/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/span[1]")))
            tag1 = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text() = 'Opportunities']")))
        except Exception:
            driver.refresh()  # 刷新方法 重新检查
            print("此次检测失败，已重新开始")
            try:
                tag1 = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text() = 'Opportunities']")))
            except Exception:
                print("再次检测失败，结束程序")
                driver.quit()
                sys.exit()
        # score1 = driver.find_element_by_class_name("lh-gauge__percentage")
        # score1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "lh-gauge__percentage")))
        # app_score[name] = int(score1.text)
        print('%s检测成功' % name)
        time.sleep(2)
        # page = driver.page_source
        # print(page)
        # 暂时不需要输出mobile 的排行榜，先隐藏

        # p1 = s.screenshot(english_name, "app")
        # print(p1)
        # pic_addr = "https://raw.githubusercontent.com/yaoguanfei/auto_Pagespeed_insight/master/screen_shot%s" % p1
        # app_addr[name] = str(pic_addr)
        # time.sleep(2)

        # tag2 = driver.find_element_by_xpath("//div[text() = '桌面设备']")
        tag2 = driver.find_element_by_class_name('tab-desktop')
        tag2.click()
        time.sleep(2)
        score = driver.find_elements_by_class_name("lh-gauge__percentage")
        print(score)
        score2 = int(score[1].text)

        print('desktop分数为：' + str(score2))
        desktop_score[name] = score2
        p2 = s.screenshot(english_name, "desktop")
        pic_addr = " http://uc-test-manage-00.umlife.net/img/google%s" % p2
        # pic_addr = "https://raw.githubusercontent.com/yaoguanfei/auto_Pagespeed_insight/master/screen_shot%s" % p2

        desktop_addr[name] = str(pic_addr)
    # 一次性上传所有的截图
    # picture_to_gitlab()
    driver.quit()

    # app_result = summary_result(app_score, app_addr, name_logo)
    desktop_result = summary_result(desktop_score, desktop_addr, name_logo)
    print("桌面设备检查结果：")
    print(desktop_result)
    # print("移动设备检查结果：")
    # print(app_result)

    # *************************************这里填写自己钉钉群自定义机器人的token*****************************************
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=5ad36dff315ca4eab91c8aa0b9ef50ce163a64ba782ec6539309b4004ed20c7d'
    # 用户手机号列表
    # at_mobiles = ['*************************这里填写需要提醒的用户的手机号码，字符串或数字都可以****************************']
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # FeedCard类型

    card1 = CardItem(title="Web产品加载性能排行榜(Desktop)",
                     url="https://www.yuque.com/docs/share/56975e6b-ba1b-42da-ad20-f49fb068d150",
                     pic_url=" http://uc-test-manage-00.umlife.net/img/google/PageSpeed_Insight.png")
    desktop_cards = [card1]

    for i in range(7):
        card = CardItem(
            title="%s、" % str(i + 1) + desktop_result[i][0] + "(跑分%s): " % str(desktop_result[i][4]) + "性能%s级" %
                  desktop_result[i][1],
            url=desktop_result[i][2],
            pic_url=desktop_result[i][3])
        desktop_cards.append(card)
    xiaoding.send_feed_card(desktop_cards)

    # card1 = CardItem(title="Web产品加载性能排行榜(Mobile)",
    #                  url="https://www.yuque.com/docs/share/56975e6b-ba1b-42da-ad20-f49fb068d150",
    #                  pic_url="https://raw.githubusercontent.com/yaoguanfei/auto_Pagespeed_insight/master/screen_shot/PageSpeed_Insight.png")
    #
    # app_cards = [card1]
    # for i in range(7):
    #     card = CardItem(title="%s、" % (i+1) + app_result[i][0] + "(跑分%s): " % app_result[i][4] + "性能%s级" % app_result[i][1],
    #                     url=app_result[i][2],
    #                     pic_url=app_result[i][3])
    #     app_cards.append(card)
    # xiaoding.send_feed_card(app_cards)

    # Markdown类型
    # title = '# **Web产品加载性能排行榜(Desktop)** \n ' + \
    #         ">![PageSpeed Insight](https://raw.githubusercontent.com/yaoguanfei/auto_Pagespeed_insight/master/screen_shot/PageSpeed_Insight.png)\n" + \
    #         "> ## [了解更多详情](https://www.yuque.com/docs/share/56975e6b-ba1b-42da-ad20-f49fb068d150)\n"
    # summary_text = title
    # for i in range(7):
    #     text = "- %s、" % (i + 1) + desktop_result[i][0] + "(跑分%s): " % desktop_result[i][4] + "性能**%s**级" % \
    #            desktop_result[i][
    #                1] + '\n' + \
    #            '>![结果截图](%s)\n' % desktop_result[i][2]
    #     summary_text = summary_text + text
    # xiaoding.send_markdown(title='Web产品加载性能排行榜', text=summary_text, is_at_all=True)
