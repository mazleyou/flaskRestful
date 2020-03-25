from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome('drivers/chromedriver')
driver.implicitly_wait(3)

# Naver 페이 들어가기
driver.get('https://order.pay.naver.com/home')
print("Page Title is : %s" %driver.title)