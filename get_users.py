import random
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from time import sleep


def sleep_between_actions():
    sleep(round(random.uniform(0.5,2),4))
    
def log_in(uname,passwd):
    """Logs In with a specific account

    Args:
        uname   (str): username
        passwd  (str): password
    """
    write_input_human(driver,'/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div[1]/div[1]/div/label/input',uname)
    write_input_human(driver,'/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div[1]/div[2]/div/label/input',passwd)
    click_on(driver,'/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div[1]/div[3]/button/div')
    
def search_and_go(uname):
    """Searches for a specific user and visits his page

    Args:
        uname (str): username
    """
    

def click_on(driver,xpath):
    """Clicks on a button given its xpath

    Args:
        driver  (selenium.webdriver):   webdriver
        xpath   (str):                  str with Button Xpath
    """
    button = driver.find_element(By.XPATH,xpath)
    driver.execute_script("arguments[0].click();", button)
    sleep_between_actions()
    
def write_input_human(driver,input_xpath,text,wpm=80):
    """Writes a string to an input box, simulating human writing speed, with it being given
    Assuming the average length of a word being 6
    
    Args:
        driver      (selenium.webdriver):   webdriver
        input_xpath (str):                  Input Box xpath
        text        (str):                  text to write
        wpm         (int):                  speed [80]
    """
    aver_word_size = 6
    spw = round(60/(wpm*aver_word_size),4)  #seconds p/letter
    size = len(text)
    input_box = driver.find_element(By.XPATH,input_xpath)
    for i in range(size):
        input_box.send_keys(text[i])
        sleep(spw)
    sleep_between_actions()
    
    


option = webdriver.FirefoxOptions()
option.add_argument('--headless')
option.binary_location = '/usr/lib/firefox/firefox'
#option.binary_location = '/mnt/c/Program Files/Mozilla Firefox/firefox.exe'
driverService = Service('/mnt/c/Users/joaom/Documents/WebDrivers/geckodriver')
driver = webdriver.Firefox(service=driverService, options=option)
driver.get("https://www.instagram.com")

#LOGIN
sleep(10)
write_input_human(driver,'/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div[1]/div[1]/div/label/input','jocas.mi')
write_input_human(driver,'/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div[1]/div[2]/div/label/input','PlsN0H4ck')

click_on(driver,'/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div[1]/div[3]/button/div')

print('sleeping 3')
sleep(10)

# Validation
click_on(driver,'/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[1]/div[1]/button/div')
validation = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[1]/div[2]/div/div/div[1]/div[1]/a/div/div[2]/div/div/div/div')
print(validation.text)

# Go to profile
click_on(driver,'/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[1]/span')
sleep(1)
click_on(driver,'/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[2]/div/div[2]/div[1]/a')
print('Loading profile')
sleep(5) 

#Go to Following
click_on(driver,'/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[3]/a')
                
                
print('Loading following')
sleep(3)
#print Tika
tika = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[1]/div[2]/div[1]/div/div/span/a/span/div')
print(tika.text)

driver.execute_script("window.scrollTo(0, 100)")
driver.execute_script("window.scrollTo(0, 100)")


sline = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[8]/div[2]/div[2]/div')  
print(sline.text)
driver.quit()

# To switch to main window, use
#driver.switch_to.default_content()