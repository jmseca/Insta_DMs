import random
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from tags import InstaXpaths


def get_firefox_driver(url):
    option = webdriver.FirefoxOptions()
    option.add_argument('--headless')
    option.binary_location = '/usr/lib/firefox/firefox' #path to firefox.exe
    driverService = Service('/mnt/c/Users/joaom/Documents/WebDrivers/geckodriver') #path to firefox driver
    driver = webdriver.Firefox(service=driverService, options=option)
    driver.get(url)
    return driver

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
        # TODO Is it better to check the text of a tag, instead of a tag only?
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
            finally:
                fails+=1
                print(fails)
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
    
    def __init__(self,uname,passwd):
        super().__init__(get_firefox_driver("https://www.instagram.com"))
        self.uname=uname
        self.passwd=passwd
        self.xpaths = InstaXpaths()
    
    def log_in(self):
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
        
    def go_to_profile(self,profile_uname):
        """Searches and goes to a new profile

        Args:
            profile_uname (str): profile username
        """
        self.write_input_human(self.xpaths.search_bar(),profile_uname)
        self.click_on(self.xpaths.search_first_profile())
        
    def get_profile_name(self):
        return self.get_text_xpath(self.xpaths.profile_name())
    
    def open_followers(self):
        self.click_on(self.xpaths.followers())
        self.wait_for_page(self.xpaths.fol_tag())
        
    def open_following(self):
        self.click_on(self.xpaths.following())
    
    def get_fol_simple(self,fol_number=10,following=True):
        """Gets fol_number fol's (followers or following), depending on the flag following.
        This function does not know how to scroll down, so maximum is 10

        Args:
            fol_number (int, optional): Number of Fols. Defaults to 10.
            following (bool, optional): Following if True, Followers else. Defaults to True.

        Raises:
            Exception: When fol_number>10
        """
        if (fol_number>10):
            raise Exception('Max fol_number is 10. To get more, use get_fol_complex')
        fols = fol_number*['']
        max_range = fol_number+1
        for i in range(1,max_range):
            fols[(i-1)] = self.get_text_xpath(self.xpaths.nth_fol(i,following))
        return fols
    
    def scroll_fols(self,n,fol_frame):
        """Scrolls one of the fols frames 'n' times
        """
        i=0
        while i < n: # scroll 5 times
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;", fol_frame)
            sleep(0.05)
            i += 1
        self.sleep_between_actions()

        
    
    def get_fol_complex(self,fol_number,following=True,scrolls=20):
        fols = ['a'*20]*fol_number
        found = False
        fol_frame = self.driver.find_element(By.XPATH,self.xpaths.fol_frame)
        while not(found):
            try:
                last_fol = self.get_text_xpath(self.xpaths.nth_fol(fol_number,following))
                found = True
            except:
                self.scroll_fols(scrolls,fol_frame)
        for i in range(fol_number):
            fols[i] = self.get_text_xpath(self.xpaths.nth_fol((i+1),following))
        return fols
    
    
    
class InstaSpiderBot(InstaBot):
    
    def __init__(self,uname,passwd,*follows):
        super().__init__(uname,passwd)
        self.follows = follows
        self.queue_max = 2000
        self.queue = ['a'*20]*self.queue_max
        
    def profile_follow_points(self):
        if self.is_profile_private():
            return 0
        simple_following = self.get_fol_simple()
        points = 0
        for fol in self.follows:
            if fol in simple_following:
                points += 1
        return points
    
    def following_or_followers(self):
        """Chooses if we check the followers or following to scrape.
        
        Returns: (following, n)
        Where n is the number of fols to scrape
        """
        pass
        
            
        
        
    
#Bombsite
    
tester = InstaBot('jocas.mi','PlsN0H4ck')
sleep(4)
tester.log_in()
sleep(3)


tester.go_to_profile('catarinatrmachado')
sleep(3)
print(tester.get_profile_name())
tester.open_following()
print('ok')

tika_fols_300 = tester.get_fol_complex(300)
print(tika_fols_300)

"""
fBody  = tester.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]")
scroll = 0
while scroll < 20: # scroll 5 times
    tester.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;", fBody)
    sleep(1)
    print(scroll)
    scroll += 1

n=1
try:
    while True:
        print(tester.get_text_xpath(f'/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[{n}]/div[2]/div[1]/div/div/span/a/span/div'))
        n+=1
except:
    print(f"Falhou no {n}")
    
scroll=0
while scroll < 5: # scroll 5 times
    tester.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;", fBody)
    sleep(1)
    print(scroll)
    scroll += 1
    
while True:
    print(tester.get_text_xpath(f'/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[{n}]/div[2]/div[1]/div/div/span/a/span/div'))
    n+=1
"""

    
    
    
    