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
from summary_result import sort_result, score2level
from config import Chinese_to_English
import sys
import pysnooper

if __name__ == '__main__':
    products = {}
    # 构建数据结果存储相关产品和竞品的信息
    # products = {
    #     product1: {'url': '',
    #                'logo': '',
    #                'score': [],
    #                'level': 0,
    #                'competing_products':
    #                    {
    #                        'name':" "
    #                        'url': '',
    #                        'logo': '',
    #                        'score': [],
    #                        'level': 0,
    #                     }
    #                }
    #      product2: {}
    #      ...
    #       }

    csvresult = read_csv2("webdata.csv")
    for i in range(len(csvresult)):
        # 读取第1，3,5等单数行的name,作为product名
        if i % 2 == 0:
            product_name = str(csvresult[i][0])
            products[product_name] = {}
            url = str(csvresult[i][1])
            products[product_name]["url"] = url
            logo = str((csvresult[i][2]))
            products[product_name]["logo"] = logo
            products[product_name]["score"] = []
            products[product_name]["level"] = 0
        # 读取第2，4,6等双数行的数据，初始化竞品信息
        else:
            competing_products = {}
            name = str(csvresult[i][0])
            url = str(csvresult[i][1])
            logo = str((csvresult[i][2]))
            competing_products["logo"] = logo
            competing_products["url"] = url
            competing_products["name"] = name
            competing_products["score"] = []
            competing_products["level"] = 0
            products[product_name]["competing_products"] = competing_products

    driver.implicitly_wait(3)

    driver.get("https://developers.google.com/speed/pagespeed/insights")  # 通过get()方法，打开一个url站点
    time.sleep(1)
    # page = driver.page_source
    # print(page)
    # input = driver.find_element_by_name("url")

    input = driver.find_element_by_class_name("label-input-label")
    # 读取到的webdata.csv 的每一行数据

    # 进行多轮检测，一轮依次检测各个web 产品，循环进行多次：
    # ***********    一共需要检测n轮，则需要改为n          ********************
    for n in range(2):
        print("第%s轮检测开始" % (n + 1))
        # 清除浏览器cookies
        cookies = driver.get_cookies()
        driver.delete_all_cookies()

        # 逐一进行检测，获取分数并评级，并加信息入products
        for i in range(len(csvresult)):
            # 检测的产品为
            url = str(csvresult[i][1])
            name = str(csvresult[i][0])
            if url == '':
                continue
            input.clear()
            input.send_keys(url)
            input.send_keys(Keys.ENTER)
            wait = WebDriverWait(driver, 200)  # 显式等待，引入WebDriverWait，规定最大等待时长
            try:
                # 调用until方法，传入等待方法（节点出现）
                # 出现该元素是检测成功且完毕的必要条件
                # 有头
                tag1 = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text() = '实测数据']")))
                # tag1 = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-speed-insights']/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/span[1]")))
                # tag1 = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text() = 'Opportunities']")))
            except Exception:
                driver.refresh()  # 刷新方法 重新检查
                print("此次检测失败，已重新开始")
                try:
                    # tag1 = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text() = 'Opportunities']")))
                    tag1 = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text() = '实测数据']")))
                except Exception:
                    print("再次检测失败，结束程序")
                    driver.quit()
                    sys.exit()
            # score1 = driver.find_element_by_class_name("lh-gauge__percentage")
            # score1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "lh-gauge__percentage")))
            # app_score[name] = int(score1.text)
            print('%s检测成功' % name)
            time.sleep(1)
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
            time.sleep(3)
            # 会获取到两个分数，1个mibole,1个desktop
            score = driver.find_elements_by_class_name("lh-gauge__percentage")
            score2 = int(score[1].text)
            print('desktop分数为：' + str(score2))
            # 检测如是主产品，把分数填入主产品的score中
            if i % 2 == 0:
                mainname = name  # 如是新的主产品，需要更改名字
                products[mainname]["score"].append(score2)
            # 检测如是竞品，把分数填入主产品的竞品competing_products中的score中,主产品为上一次检测的
            else:
                products[mainname]["competing_products"]["score"].append(score2)
            # p2 = s.screenshot(english_name, "desktop")
            # pic_addr = "http://128.1.49.161%s" % p2
            # pic_addr = "https://raw.githubusercontent.com/yaoguanfei/auto_Pagespeed_insight/master/screen_shot%s" % p2

            # desktop_addr[name] = str(pic_addr)
    # 一次性上传所有的截图
    # picture_to_gitlab()
    print("多轮检测完毕")
    driver.quit()

    # 求各个web 产品检测分数的平均值
    # 求主产品的平均值；
    for key, value in products.items():
        for k, v in value.items():
            # 求主产品的平均值和进行评级；
            if k == "score":
                score_list = v
                s = 0
                for i in range(len(score_list)):
                    n = len(score_list)
                    s = s + score_list[i]
                average = (round(s / n, 2))  # 使结果保留两位小数
                value["score"] = average
                value["level"] = score2level(average)
            # 求竞品的平均值和评级；
            if k == "competing_products":
                for k1, v1 in v.items():
                    if k1 == "score":
                        score_list = v1
                        s = 0
                        for i in range(len(score_list)):
                            n = len(score_list)
                            s = s + score_list[i]
                        average = (round(s / n, 2))  # 使结果保留两位小数
                        v["score"] = average
                        v["level"] = score2level(average)
    print(products)

    # 将字典排序，返回[(),()]如此格式的数据
    desktop_result = sort_result(products)
    print("桌面设备检查结果：")
    print(desktop_result)

    # *************************************这里填写自己钉钉群自定义机器人的token*****************************************
    # 个人群，供调试
    # webhook = 'https://oapi.dingtalk.com/robot/send?access_token=febec6b869bf218de1798a25469fee9b34ff27c71a5d7f32348d0183dd9ee7eb'

    # 内部群，供预览
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=5ad36dff315ca4eab91c8aa0b9ef50ce163a64ba782ec6539309b4004ed20c7d'

    # 研发中心群，正式发布
    # webhook = 'https://oapi.dingtalk.com/robot/send?access_token=8f9e92f925336ebcaebe0c880fc957a9ed15526b45e6bc56830d18be7fd6c20e'
    # 用户手机号列表
    # at_mobiles = ['*************************这里填写需要提醒的用户的手机号码，字符串或数字都可以****************************']
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # FeedCard类型

    card1 = CardItem(title="Web产品加载性能排行榜(Desktop)",
                     url="https://www.yuque.com/docs/share/56975e6b-ba1b-42da-ad20-f49fb068d150",
                     pic_url="https://raw.githubusercontent.com/yaoguanfei/auto_Pagespeed_insight/master/screen_shot/PageSpeed_Insight.png")
    desktop_cards = [card1]

    # ***********      一共需要检测n个主产品，则需要改为n      *************
    for i in range(7):
        # 主产品信息
        # 竞品信息
        # 判断是否存在竞品信息
        # 存在和不存在输出信息不同
        if desktop_result[i][1]["competing_products"]["name"] == "暂无竞品":
            card = CardItem(
                title="%s、" % str(i + 1) + str(desktop_result[i][0]) + "(跑分%s): " % str(
                    desktop_result[i][1]["score"]) + "性能%s级" %
                      str(desktop_result[i][1]["level"]) + "\n" + "      ******** 暂无竞品 *********",
                url="https://www.yuque.com/docs/share/56975e6b-ba1b-42da-ad20-f49fb068d150",
                pic_url=desktop_result[i][1]["logo"])
        else:
            card = CardItem(
                title="%s、" % str(i + 1) + str(desktop_result[i][0]) + "(跑分%s): " % str(
                    desktop_result[i][1]["score"]) + "性能%s级" %
                      str(desktop_result[i][1]["level"]) + "\n"+ "      "+ str(
                    desktop_result[i][1]["competing_products"]["name"]) + "(跑分%s): " % str(
                    desktop_result[i][1]["competing_products"]["score"]) + "性能%s级" % str(
                    desktop_result[i][1]["competing_products"]["level"]),
                url="https://www.yuque.com/docs/share/56975e6b-ba1b-42da-ad20-f49fb068d150",
                pic_url=desktop_result[i][1]["logo"])
        desktop_cards.append(card)

        # title=str(desktop_result[i][1]["competing_products"]["name"]) + "(跑分%s): " % str(
        #     desktop_result[i][1]["competing_products"]["score"]) + "性能%s级" %
        #       str(desktop_result[i][1]["competing_products"]["level"]),
        # url="https://www.yuque.com/docs/share/56975e6b-ba1b-42da-ad20-f49fb068d150",
        # pic_url=desktop_result[i][1]["competing_products"]["logo"])

        # 最后添加powered by 信息
    card2 = CardItem(
        title="Powered by：Google PageSpeed           Insights",
        url="https://developers.google.com/speed/pagespeed/insights/",
        pic_url="https://raw.githubusercontent.com/yaoguanfei/auto_Pagespeed_insight/master/screen_shot/speed.jpg")
    desktop_cards.append(card2)
    xiaoding.send_feed_card(desktop_cards)

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
