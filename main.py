# This is a sample Python script.

# Use a breakpoint in the code line below to debug your script.
# Press ⌘F8 to toggle the breakpoint.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from bs4 import BeautifulSoup
import selenium
import requests

class SimpleAT:

    def __init__(self, profile, log_url, open_tasks):
        # includes, password, username, email, phone_number, card_info
        self.profile = profile
        # should just be the initial url to get to for the website
        self.log_url = log_url

        self.open_tasks = open_tasks


    # Press the green button in the gutter to run the script.

    # def startSession(self, cookieItem):
    #     self.s.cookies =

    def setLogin(self):
        # storeLogins in a database or something similar
        # TODO: Always check for errors, delete current "session" data and form data
        with requests.Session() as sess:
            log_page = sess.get(self.log_url)
            log_form = BeautifulSoup(log_page.text, 'lxml')
            field_uname = log_form.find('input', {'name': 'username'})
            if field_uname is None:
                field_uname = log_form.find('input', {'name': 'email'})

            # if login and data.cookieSessions is determined
            #  try to start session with cookies
            # elseif login and data.form_data is determined try to login
            # else try to login through random attempts
            field_pass = log_form.find('input', {'name': 'password'})
            print(field_uname, field_pass, self.profile)

#    def getFormData(self, postRequest):


user_info = {'password': '6106371972', 'username': 'aj@moserhomes.com'}
login_url = 'https://app.buildtopia.com/english_exec/login'
obj = SimpleAT(user_info, login_url)
obj.setLogin()

    # login
    #loginRequest = requests.post()

    # if the login request fails try the next soup form html
    # set proper cookies

#def theSoup(text):
#   html = BeautifulSoup(text, 'lxml')
