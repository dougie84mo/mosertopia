# This is a sample Python script.
# Use a breakpoint in the code line below to debug your script.
# Press ⌘F8 to toggle the breakpoint.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from selenium import webdriver
# from selenium.webdriver import Chrome, ChromeOptions
# import webbrowser
# from bs4 import BeautifulSoup
import requests
# import datetime
import time
import json
import smtplib
import imaplib
# import datetime
import xlsxwriter
import pandas as pd
from prettyprinter import pprint
from moser import MoserHelpers

global MASTER_MOSER_DATA


class SimpleAT:

    def __init__(self, open_tasks=None):
        # should just be the initial url to get to for the website
        self.open_tasks = {} if open_tasks is None else open_tasks


    # Press the green button in the gutter to run the script.

    # def startSession(self, cookieItem):
    #     self.s.cookies =

    def setLogin(self, user_info, log_url):
        # USER_INFO includes, password, username, email, phone_number, card_info

        # storeLogins in a database or something similar
        # TODO: Always check for errors, delete current "session" data and form data
        with requests.Session() as sess:
            # log_page = sess.get(self.log_url)
            log_into_page = sess.post(log_url, user_info)
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


    def textMessagingScheduleInit(self):
        with open('data/moser/config.json') as c:
            j = json.load(c)

    def textMessagingSchedule(self, vendor, dt, lots=None):
        if lots is None:
            lots = []



    @staticmethod
    def email_startup(gmail=0, imap=1, port=587, message_details=None):
        with open("data/gmails.json", "r") as gmails:
            gmails = json.load(gmails)
            server = gmails["imap"] if imap == 1 else gmails["smtp"]
            email_info = gmails["fresh"][gmail]
            if imap == 1:
                try:
                    s = imaplib.IMAP4_SSL(server)
                    s.login(email_info[0], email_info[1])
                    s.select('ETest')

                    print(f'These emails are found: {email_info[0]}')
                except Exception as e:
                    mails = None
                    print(e)

            elif port == 465 and imap == 0:

                with smtplib.SMTP_SSL(server, port, context=context) as server:
                    server.login(email_info[0], email_info[1])
            elif port == 587 and imap == 0:
                try:
                    s = smtplib.SMTP(server, port)
                    s.ehlo()
                    s.starttls(context=context)
                    s.login(email_info[0], email_info[1])
                    mails = s.mail(email_info[0])
                    # do something then
                    print(mails)
                    s.close()
                    print(f'This email was logged in: {email_info[0]}')
                except Exception as e:
                    print(e)

    def test_email(self, email_to_info, gmail=0, port=587):
        # dummy info
        self.email_startup(gmail, imap=0, port=port, message_details=email_to_info)

    @staticmethod
    def selenium_start(url):
        d = webdriver.Chrome(executable_path='drivers/chromedriver')
        d.get(url)
        return d

    @staticmethod
    def selenium_signin(sbrowser: webdriver.Chrome, login, names=[], count=0):

        # webbrowser.get('chrome').open_new_tab(login_url)
        # time.sleep(10)
        sbrowser.find_element_by_name(names[0]).send_keys(login["username"])
        sbrowser.find_element_by_name(names[1]).send_keys(login["password"])
        sbrowser.find_element_by_class_name(names[2]).click()

        while sbrowser.find_element_by_name(names[1]) is not None and count < 5:
            SimpleAT.selenium_signin(sbrowser, login, names)
            count = count + 1

        pprint(sbrowser.get_cookies())



    @staticmethod
    def find_element_func_click(page: webdriver.Chrome, element_dict={}):
        for element in element_dict:
            if 2 in element and element[2] is not None:
                elements = page.find_elements(element[0], element[1])
                # TODO: add search advanced by element function
                #  - associate with the element in loop search
                i = element[2] - 1
                new_element = elements[i]
            elif 1 in element and element[1] is not None:
                new_element = page.find_element(element[0], element[1])
            else:
                new_element = page.find_element(element[0])
            new_element.click()
            #try and change this function to a dynamic one if possible



    # def get_to_page():
    # def monitorSiteByHtml(site_url, monitor_refresh_rate=60000, proxies=[]):
    #     # for

MoserHelpers.moser_hardcode_warranty_marsh_lea()