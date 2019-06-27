from chatbot import DingtalkChatbot, ActionCard, FeedLink, CardItem

webhook = 'https://oapi.dingtalk.com/robot/send?access_token=febec6b869bf218de1798a25469fee9b34ff27c71a5d7f32348d0183dd9ee7eb'
# 用户手机号列表
# at_mobiles = ['*************************这里填写需要提醒的用户的手机号码，字符串或数字都可以****************************']
# 初始化机器人小丁
xiaoding = DingtalkChatbot(webhook)
# FeedCard类型
# title="AG"+"---"+str(app_score["AG"])
#
# card1 = CardItem(title="Web产品加载性能排行榜(Desktop)",
#                  url="https://www.yuque.com/docs/share/56975e6b-ba1b-42da-ad20-f49fb068d150",
#                  pic_url="https://raw.githubusercontent.com/yaoguanfei/auto_Pagespeed_insight/master/screen_shot/PageSpeed_Insight.png")
# card2 = CardItem(
#         title="1、有米官网 ",
#         url="https://www.yuque.com/docs/share/56975e6b-ba1b-42da-ad20-f49fb068d150",
#         pic_url="https://raw.githubusercontent.com/yaoguanfei/auto_Pagespeed_insight/master/screen_shot/youmi_logo3.png")
# desktop_cards=[card1,card2]
# xiaoding.send_feed_card(desktop_cards)

i = 0
app_result = [["AG通用版", "A",
               "https://raw.githubusercontent.com/yaoguanfei/auto_Pagespeed_insight/master/screen_shot/AG--desktop--2019-06-23%2010%3A58%3A46.887305.png",
               "https://raw.githubusercontent.com/yaoguanfei/auto_Pagespeed_insight/master/screen_shot/ag_logo.png", 85],
              [
                  "AG通用版", "A", "https://raw.githubusercontent.com/yaoguanfei/auto_Pagespeed_insight/master/screen_shot/AG--desktop--2019-06-23%2010%3A58%3A46.887305.png",
                  "https://raw.githubusercontent.com/yaoguanfei/auto_Pagespeed_insight/master/screen_shot/ag_logo.png", 85]]
title = '# **Web产品加载性能排行榜(Desktop)** \n '
summary_text = title
for i in range(2):
    text = "- %s、" % (i + 1) + app_result[i][0] + "(跑分%s): " % app_result[i][4] + "性能**%s**级" % app_result[i][1] + '\n' + \
           '>![logo](%s)\n' % app_result[i][3] + \
           '>![结果截图](%s)\n' % app_result[i][2]
    summary_text = summary_text + text
xiaoding.send_markdown(title='Web产品加载性能排行榜', text=summary_text , is_at_all=True)
