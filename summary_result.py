
def summary_result(score,addr,logo):
    print(score)
    result = [[0 for i in range(5)] for j in range(10)]  #列表生成式法生成二维数组[[AG,等级,截图，logo,具体分数],[],[]...]
    tuple_app_score = sorted(score.items(), key=lambda item: item[1],reverse=True)#排序后结果[(AG,90),(youtou,88)...]
    print(tuple_app_score)

    # 对获取的分数进行排序，评级
    # 95-100：S   90-94： A    80-89：B   70-79： C   60-69：D  <60 :不及格
    for i in range(len(tuple_app_score)):
        n = tuple_app_score[i][0]
        if tuple_app_score[i][1] == '':
            result[i][1] = "检测失败"
        else:
            f = int(tuple_app_score[i][1])

        result[i][0] = n
        if f == 100:
            result[i][1] = "S"
        elif f >= 95:
            result[i][1] = "A"
        elif f >= 85:
            result[i][1] = "B"
        elif f >= 50:
            result[i][1] = "C"
        else:
            result[i][1] = "D"

    # 根据排序后的数组，添加对应的截图,logo,分数
    for i in range(len(result)):
        a = result[i][0]
        if a in addr.keys():
            result[i][2] = addr[a]
        if a in logo.keys():
            result[i][3] = logo[a]
        if a in score.keys():
            result[i][4] = score[a]

    return result