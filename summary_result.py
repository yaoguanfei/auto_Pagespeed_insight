
def summary_result(score,addr,logo):
    result = [[0 for i in range(5)] for j in range(10)]  #列表生成式法生成二维数组[[AG,等级,截图，logo,具体分数],[],[]...]
    tuple_app_score = sorted(score.items(), key=lambda item: item[1],reverse=True)#排序后结果[(AG,90),(youtou,88)...]
    print(tuple_app_score)
    for i in range(len(tuple_app_score)):
        n = tuple_app_score[i][0]
        if tuple_app_score[i][1] is not None:
            f = int(tuple_app_score[i][1])
        result[i][0] = n
        if f >= 95 :
            result[i][1] = "S"
        elif f >= 90:
            result[i][1] = "A"
        elif f >= 80:
            result[i][1] = "B"
        elif f >= 70:
            result[i][1] = "C"
        elif f >= 70:
            result[i][1] = "D"
        else:
            result[i][1] = "不及格"

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