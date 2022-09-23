import random
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from tags import InstaXpaths

class SeleniumBot:
    
    def __init__(self,driver):
        self.driver = driver
        
    def sleep_between_actions(self):
        sleep(round(random.uniform(0.5,2),4))
        
    def get_text_xpath(self,xpath):
        return self.driver.find_element(By.XPATH,xpath).text
        
    def click_on(self,xpath):
        """Clicks on a button given its xpath

        Args:
            driver  (selenium.webdriver):   webdriver
            xpath   (str):                  str with Button Xpath
        """
        button = self.driver.find_element(By.XPATH,xpath)
        self.driver.execute_script("arguments[0].click();", button)
        self.sleep_between_actions()
        
    def wait_for_page(self,xpath,timeout=10,default_sleep=2):
        """Waits for page to load

        Args:
            xpath (str): Xpath to the element to test
            timeout (int, optional): Times tested before timeout. Defaults to 10.
            default_sleep (int, optional): Sleep between each loop. Defaults to 2.

        Raises:
            TimeoutError: When cant find the requested element after many tentatives
        """
        fails=0
        success=False
        while fails<10:
            try:
                self.driver.find_element(By.XPATH,xpath)
                success=True
                pass
            except:
                sleep(default_sleep)
        if not(success):
            raise TimeoutError()
        
    def write_input_human(self,input_xpath,text,wpm=80):
        """Writes a string to an input box, simulating human writing speed, with it being given
        Assuming the average length of a word being 6
        
        Args:
            input_xpath (str):                  Input Box xpath
            text        (str):                  text to write
            wpm         (int):                  speed [80]
        """
        aver_word_size = 6
        spw = round(60/(wpm*aver_word_size),4)  #seconds p/letter
        size = len(text)
        input_box = self.driver.find_element(By.XPATH,input_xpath)
        for i in range(size):
            input_box.send_keys(text[i])
            sleep(spw)
        self.sleep_between_actions()
        
        
        
class InstaBot(SeleniumBot):
    
    def __init__(self,driver,uname,passwd):
        super().__init__(driver)
        self.uname=uname
        self.passwd=passwd
        self.xpaths = InstaXpaths()
    
    def log_in(self, driver):
        """Logs In with a specific account

        Args:
            uname   (str): username
            passwd  (str): password
        """
        self.write_input_human(self.xpaths.uname_input(),self.uname)    #Uname Input
        self.write_input_human(self.xpaths.passwd_input(),self.passwd)  #Passwd Input
        self.click_on(self.xpaths.login_btn())                          #Login Button
        
    def check_if_in_main(self):
        """
        Checks if Bot is in the main page (has logged in successfuly)
        """
        try:
            self.click_on(self.xpaths.validation_1())
            validation = self.get_text_xpath(self.xpaths.validation_2())
            return validation=='Following'
        except:
            return False
        
    def go_to_personal_profile(self):
        """
        Goes to personal profile
        """
        self.click_on(self.xpaths.go_profile_1())
        self.click_on(self.xpaths.go_profile_2())
        
    def is_profile_private(self):
        """Checks if the profile is private
        """
        try:
            text = self.get_text_xpath(self.xpaths.private())
            return text=='This Account is Private'
        except:
            return False
            
        
    
    
    
    