from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# path에 \ 하나씩 더 추가 (Web driver)
path = "C:\\Users\\Lenovo\\Desktop\\cloud-service\\webdriver\\chromedriver.exe"
driver = webdriver.Chrome(path)

# github login 페이지 - tab의 이름 출력
driver.get("https://www.github.com/login")
print(driver.title) 

# ID/PW 필드에 대한 정보 
elem_email = driver.find_element_by_id("login_field")     
elem_email.send_keys("['email']")    # email 입력
elem_pass = driver.find_element_by_id("password") 
elem_pass.send_keys("['password']") # password 입력

elem_email.send_keys(Keys.RETURN) 
#elem_pass.send_keys(Keys.RETURN)   


