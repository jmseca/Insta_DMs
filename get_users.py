from re import X
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from time import sleep


option = webdriver.FirefoxOptions()
option.add_argument('--headless')
option.binary_location = '/usr/lib/firefox/firefox'
#option.binary_location = '/mnt/c/Program Files/Mozilla Firefox/firefox.exe'
driverService = Service('/mnt/c/Users/joaom/Documents/WebDrivers/geckodriver')
driver = webdriver.Firefox(service=driverService, options=option)
driver.get("https://www.instagram.com")


sleep(5)

el = driver.find_element(By.XPATH,'/html/body/div[1]/section/main/article/div[2]/div[3]/p')

driver.find_element(By.XPATH,"/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div[1]/div[1]/div/label/input").send_keys("jocas.mi")
sleep(1)
driver.find_element(By.XPATH,"/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div[1]/div[2]/div/label/input").send_keys("incorrect_passwd")
sleep(2)
#driver.find_element(By.XPATH,'/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div[1]/div[3]/button/div').click()
button = driver.find_element(By.XPATH,"/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div[1]/div[3]/button/div")
driver.execute_script("arguments[0].click();", button)

print('sleeping 5')
sleep(5)
validation = driver.find_element(By.XPATH,'/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div[2]/p')
print(validation.text)


driver.quit()