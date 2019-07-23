def sort_result(products):
    sort_result = sorted(products.items(), key=lambda x: x[1]['score'], reverse=True)
    print(sort_result)
    #  [('有米官网', {'url': 'https://www.youmi.net/', 'score': 99, 'competing_products': {'score': 99}}), ('AG通用版', {'url': 'https://appgrowing.cn/', 'score': 33, 'competing_products': {'score': 93}})]
    return sort_result


def score2level(score):
    # 95-100：S   90-94： A    80-89：B   70-79： C   60-69：D  <60 :不及格

    if score == 100:
        level = "S"
    elif score >= 95:
        level = "A"
    elif score >= 85:
        level = "B"
    elif score >= 50:
        level = "C"
    elif score == 0:
        level = "未检测"
    else:
        level = "D"

    return level


if __name__ == '__main__':
    score = 0.0
    level = score2level(score)
    print(level)
