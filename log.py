import logging
import datetime
import sys
from pathlib import Path
# from sweetest.lib.path import mkdir

def mkdir(p):
    '''
    创建目录
    :param p: 目录名
    '''

    p = Path(p)
    # 若不存在该目录，则创建它
    if not p.is_dir():
        p.mkdir()

def nowtime():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d_%H%M%S')


# 获取logger实例，如果参数为空则返回root logger
logger = logging.getLogger("sweetest")

# 指定logger输出格式
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(filename)s line:%(lineno)d: %(message)s')

# 新建日志存放目录
mkdir('log')
# 文件日志
log_file = Path('log') / f'{nowtime()}.log'

file_handler = logging.FileHandler(filename=log_file, encoding="utf-8")
file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值

# 为logger添加的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 指定日志的最低输出级别，默认为WARN级别
# DEBUG，INFO，WARNING，ERROR，CRITICAL
logger.setLevel(logging.INFO)
