from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# path에 \ 하나씩 더 추가 (Web driver)
path = "C:\\Users\\Lenovo\\Desktop\\cloud-service\\webdriver\\chromedriver.exe"
driver = webdriver.Chrome(path)

# facebook으로 이동 - tab의 이름 출력
driver.get("https://www.facebook.com")
print(driver.title) 

# ID/PW 필드에 대한 정보 
elem_email = driver.find_element_by_id("email")     
elem_email.send_keys("['email']")   # email 입력 
elem_pass = driver.find_element_by_id("pass") 
elem_pass.send_keys("['password']") # password 입력

elem_email.send_keys(Keys.RETURN)   
#elem_pass.send_keys(Keys.RETURN)

# Profile Page
profile_a = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div/div/div[1]/ul/li/div/a')
print("Profile A =", profile_a.get_attribute('href'))

# Friends Page
friends_a = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div/div/div[1]/div[1]/ul/li[2]/div/a')
print("Friends A =", friends_a.get_attribute('href'))

# 이동
driver.get(profile_a.get_attribute('href'))
#driver.get(friends_a.get_attribute('href'))