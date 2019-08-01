from chatbot import DingtalkChatbot, ActionCard, FeedLink, CardItem

if __name__ == '__main__':
    # *************************************这里填写自己钉钉群自定义机器人的token*****************************************
    # 个人群，供调试
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=febec6b869bf218de1798a25469fee9b34ff27c71a5d7f32348d0183dd9ee7eb'

    # 内部群，供预览
    # webhook = 'https://oapi.dingtalk.com/robot/send?access_token=5ad36dff315ca4eab91c8aa0b9ef50ce163a64ba782ec6539309b4004ed20c7d'

    # 产研交流群，正式发布
    # webhook = 'https://oapi.dingtalk.com/robot/send?access_token=e03e3afd79b94d46d50b72f225a0b3027bdb6a161f31ac8ba791c4fe99e6cc7b'
    # 用户手机号列表
    # at_mobiles = ['*************************这里填写需要提醒的用户的手机号码，字符串或数字都可以****************************']
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    improve_team = ["AG", "JJ", "GGG"]
    team_str = ""
    for i in range(len(improve_team)):
        team_str = team_str + " @" + str(improve_team[i]) + "团队 "

    xiaoding.send_text(
        msg='温馨提示：\n Dear all, Web产品加载性能排行榜已公布,性能A级及以上'
            '团队将获得质量之星积分的奖励，性能C级及以下的团队%s需要及时跟进优化哦,让产品质量更上一个台阶～\n'
            '更多详情敬请查看：http://kks.me/br6Nb  ' % team_str,
        is_at_all=True)

