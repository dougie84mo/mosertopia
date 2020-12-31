import datetime, email, imaplib, json, ssl, smtplib, requests, time
from prettyprinter import cpprint, pprint
# from selenium import webdriver
# from selenium.webdriver.common.by import By
from pyppeteer import launch
from bs4 import BeautifulSoup

from main import SimpleAT


class MoserHelpers:

    @staticmethod
    async def moser_hardcode_warranty_marsh_lea():

        # # may need to add urls to array first then loop and catch
        # r_table = sbrowser.find_elements_by_css_selector('#bottom tr')
        # r_table.pop(0)
        # for r in table_body:

        results = MoserHelpers.moser_log_to_page(j, ["cs_requests", "cs_requests_list"])
        moser_data = {
            "address_lot": [],
            "description": [],
            "category": [],
            "status": [],
            "vendors": [],
            "opened_at": [],
            "closed_at": [],
        }
        # edit_request, open_request

        for tr in results:
            pprint(tr)
            project_name = tr.find_element(By.CSS_SELECTOR, 'td:nth-child(8)').text
            pprint(project_name)
            # Maybe in Customs Homes, something different
            if 'Marsh Lea' in project_name or 'Custom Homes' in project_name:
                url = tr.find_element(By.CSS_SELECTOR, 'td:nth-child(1) a').get_attribute('href')

                try:
                    with SimpleAT.selenium_start(url) as other_tab:
                        w_table = other_tab.find_elements(By.CSS_SELECTOR, '#listTable > tbody > tr')
                        w_table.pop(0)
                        lot_id = other_tab.find_element(By.XPATH, j["xpaths"]["cs_lots"])

                        pprint(lot_id)
                        for el in w_table:
                            tds = el.find_elements_by_tag_name("td")
                            moser_data["address_lot"].append(lot_id)
                            descr = tds[2].text
                            moser_data["description"].append(descr)
                            opened = True if tds[1].text == "Open" else False
                            # AI.something
                except Exception as e:
                    print(e)


    @staticmethod
    def marsh_lea_pm():
            results = MoserHelpers.moser_log_to_page(j, ["cs_requests", "cs_requests_list"])
            moser_data = {
                "address_lot": [],
                "description": [],
                "category": [],
                "status": [],
                "vendors": [],
                "opened_at": [],
                "closed_at": [],
                "files": []
            }

    @staticmethod
    def moser_log_to_page(path_names=None):
        with open("data/moser/config.json") as j:
            j = json.load(j)
            paths = j["paths"]
            sbrowser = SimpleAT.selenium_start(url=paths["login_url"])
            SimpleAT.selenium_signin(sbrowser, login=j["sign_in"], names=j["sign_in_cls"])
            print(sbrowser.find_element_by_name("password"))
            if sbrowser.find_element_by_name("password") is not None:
                SimpleAT.selenium_signin(sbrowser, login=j["sign_in"], names=j["sign_in_cls"])
            # return sbrowser
            if path_names is not None:
                sbrowser.get(paths[path_names[0]])
                # Technically uneccessary
                # sbrowser.find_element_by_name("ProjectFilter").find_element_by_css_selector(paths["pro"]).click()
                results = sbrowser.find_element_by_css_selector(paths["cs_requests_list"]).find_elements_by_tag_name("tr")
                results.pop(0)
                return results
            else:
                return None
                
    @staticmethod
    def mosertopia_login_buildtopia(path_names=None):
        
        browser = await launch
        page  = await browser.newPage


        with open("data/moser/config.json") as j:
            j = json.load(j)
            paths = j["paths"]
            sbrowser = SimpleAT.selenium_start(url=paths["login_url"])
            SimpleAT.selenium_signin(sbrowser, login=j["sign_in"], names=j["sign_in_cls"])
            print(sbrowser.find_element_by_name("password"))
            if sbrowser.find_element_by_name("password") is not None:
                SimpleAT.selenium_signin(sbrowser, login=j["sign_in"], names=j["sign_in_cls"])
            # return sbrowser
            if path_names is not None:
                sbrowser.get(paths[path_names[0]])
                # Technically uneccessary
                # sbrowser.find_element_by_name("ProjectFilter").find_element_by_css_selector(paths["pro"]).click()
                results = sbrowser.find_element_by_css_selector(paths["cs_requests_list"]).find_elements_by_tag_name("tr")
                results.pop(0)
                return results
            else:
                return None

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




if __name__ == '__main__':
    MoserApp().run()
