class InstaXpaths:
    
    def __init__(self):
        self.login_base = '/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div[1]/'
        self.login_xpaths = {
            'Uname Input':  'div[1]/div/label/input',
            'Passwd Input': 'div[2]/div/label/input',
            'LogIn Btn':    'div[3]/button/div', 
        }

        self.validation_base = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[1]/'
        self.validation_xpaths = {1:'div[1]/button/div',
                                  2:'div[2]/div/div/div[1]/div[1]/a/div/div[2]/div/div/div/div'}
        
        self.go_to_profile_base = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/'
        self.go_to_profile_xpaths = {
            1:'div[1]/span',
            2: 'div[2]/div/div[2]/div[1]/a'
        }
        
        self.profile_base = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/'
        self.profile_xpaths = {
            'Private': 'div/article/div[1]/div/h2',
            'Following Frame': 'header/section/ul/li[3]/a',
            'Following Number': 'header/section/ul/li[3]/a/div/span',
            'Followers Frame': 'header/section/ul/li[2]/a',
            'Followers Number': 'header/section/ul/li[2]/a/div/span'
        }
        
    def uname_input(self):
        return self.login_base + self.login_xpaths['Uname Input']
    def passwd_input(self):
        return self.login_base + self.login_xpaths['Passwd Input']
    def login_btn(self):
        return self.login_base + self.login_xpaths['LogIn Btn']
    
    
    def validation_1(self):
        return self.validation_base + self.validation_xpaths[1]
    def validation_2(self):
        return self.validation_base + self.validation_xpaths[2]
    
    def go_profile_1(self):
        return self.go_to_profile_base + self.go_to_profile_xpaths[1]
    def go_profile_2(self):
        return self.go_to_profile_base + self.go_to_profile_xpaths[2]
    
    def private(self):
        return self.profile_base + self.profile_xpaths['Private']
        