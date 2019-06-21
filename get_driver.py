from selenium import webdriver  # 导入selenium,注意不能使用import selenium



# if drivername.lower() == "google" or drivername == "chrome":
# driver = webdriver.Chrome()  # driver = webdriver.Chrome()# 谷歌浏览器 driverChrome 放在了/usr/bin 下,忘记了可使用whereis 查询
# if drivername.lower() == "firebox":
#     driver = webdriver.Firefox()  # 初始化一个火狐浏览器实例：driver   火狐浏览器驱动器为geckodriver
# if drivername.lower() == "ie":
# driver = webdriver.Firefox()




# def open_url(url):
#     driver = webdriver.Chrome()
#     driver.implicitly_wait(5)
#     driver.maximize_window()  # 最大化浏览器
#     driver.get(url)  # 通过get()方法，打开一个url站点


driver = webdriver.Chrome()# 初始化一个谷歌浏览器实例：driver