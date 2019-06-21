from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(8)
driver.get("http://www.google.com")
element=driver.find_element_by_name("q")
element.clear()
element.send_keys("姚观菲",Keys.ENTER)
sleep(1)
driver.quit()