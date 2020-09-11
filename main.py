# This is a sample Python script.

# Use a breakpoint in the code line below to debug your script.
# Press ⌘F8 to toggle the breakpoint.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
import requests
from prettyprinter import pprint, cpprint
from getpass import getpass
import time


class SimpleAT:

    def __init__(self, log_url, open_tasks={}):
        # should just be the initial url to get to for the website
        self.log_url = log_url


        self.open_tasks = open_tasks


    # Press the green button in the gutter to run the script.

    # def startSession(self, cookieItem):
    #     self.s.cookies =

    def setLogin(self, user_info):
        # USER_INFO includes, password, username, email, phone_number, card_info

        # storeLogins in a database or something similar
        # TODO: Always check for errors, delete current "session" data and form data
        with requests.Session() as sess:
            # log_page = sess.get(self.log_url)
            log_into_page = sess.post(self.log_url, user_info)
            pprint(log_into_page.text)
            api_cookies = log_into_page.cookies
            print(api_cookies)
            # if login and data.cookieSessions is determined
            #  try to start session with cookies
            # elseif login and data.form_data is determined try to login
            # else try to login through random attempts
            # if the login request fails try the next soup form html
            # set proper cookies
            # insert a genuine referer code

            # headers = {'Referer': 'https://'}
            # use another url if available on form

    def grabCookies(self, url):
        with requests.Session() as sess:
            cookiesPage = sess.get(url)

    def getLoginPageForm(self, user_info):
        d = webdriver.Chrome(executable_path='drivers/chromedriver', options={"enable_automation"})
        d.get(self.log_url)
        d.find_element_by_name('username').send_keys(user_info['username'])
        d.find_element_by_name('password').send_keys(user_info['password'])

        d.find_element_by_class_name('signIn-btn').click()
        time.sleep(40)
        d.quit()

        # log_form = BeautifulSoup(log_page.text, 'lxml')
        # field_uname = log_form.find('input', {'name': 'username'})
        # if field_uname is None:
        #     field_uname = log_form.find('input', {'name': 'email'})
        # field_pass = log_form.find('input', {'name': 'password'})


#headers={"Referere"}
#get user info from a selector and data
user_info = dict(password='6106371972', username= 'aj@moserhomes.com')
#same for login url
login_url = 'https://app.buildtopia.com/english_exec/login'
obj = SimpleAT(login_url)
obj.getLoginPageForm(user_info)



#def theSoup(text):
#   html = BeautifulSoup(text, 'lxml')
