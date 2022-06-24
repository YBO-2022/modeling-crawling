from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
import csv

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

# 크롬 웹드라이버 설정
options = Options()
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

#파일 생성
f=open(r'C:\Users\s137\OneDrive\바탕 화면\statiz_crawling\타자kt.csv','w',encoding='cp949',newline='')
csvWriter = csv.writer(f)

# 웹페이지 주소로 이동
driver.get("http://www.statiz.co.kr/main.php")

#로딩 될때까지 기다리기
driver.implicitly_wait(10)

#기록실로 이동
move = driver.find_element(By.XPATH,"/html/body/div/header/nav[2]/div/div[1]/div[3]")
move.click()
driver.implicitly_wait(10)

#연도 선택
year = driver.find_element(By.XPATH,"/html/body/div/div[1]/div/section[2]/div/div[2]/div[1]/div/div[2]/div[1]/button")
year.send_keys(Keys.ENTER)
time.sleep(3)

#연도를 2018~2022로 필터링
year_filter = driver.find_element(By.XPATH,"/html/body/div/div[1]/div/section[2]/div/div[2]/div[1]/div/div[2]/div[1]/ul/div/button[38]")
year_filter.send_keys(Keys.ENTER)
time.sleep(3)

#규정타석 선택
reg = driver.find_element(By.XPATH,"/html/body/div/div[1]/div/section[2]/div/div[2]/div[1]/div/div[7]/button")
reg.send_keys(Keys.ENTER)
time.sleep(3)

#규정타석 50타석 이상으로 필터링
reg_50 = driver.find_element(By.XPATH,"/html/body/div/div[1]/div/section[2]/div/div[2]/div[1]/div/div[7]/ul/div/button[10]")
reg_50.send_keys(Keys.ENTER)
time.sleep(3)

#옵션 클릭
option = driver.find_element(By.XPATH,"/html/body/div/div[1]/div/section[2]/div/div[2]/div[1]/div/div[9]/button")
option.send_keys(Keys.ENTER)
time.sleep(3)

#출력 클릭
expand = driver.find_element(By.XPATH,"/html/body/div/div[1]/div/section[2]/div/div[2]/div[2]/div[2]/div[5]/form/select")
expand.click()
time.sleep(3)

#100개로 확장
expand_100 = driver.find_element(By.XPATH,"/html/body/div/div[1]/div/section[2]/div/div[2]/div[2]/div[2]/div[5]/form/select/option[5]")
expand_100.click()
time.sleep(3)

#kt 크롤링
team_move = driver.find_element(By.XPATH,"/html/body/div/div[1]/div/section[2]/div/div[2]/div[1]/div/div[3]/ul/div[1]/button[11]")
driver.execute_script("arguments[0].click();", team_move)
driver.implicitly_wait(10)
    
for j in range(1,85):
    try :
        player_data = driver.find_element(By.XPATH,"/html/body/div/div[1]/div/section[2]/div/div[2]/div[5]/div/div/div[2]/table/tbody/tr["+str(j)+"]")
        #데이터 쓰기
        csvWriter.writerow([player_data.text])
    except :
        pass

driver.close()