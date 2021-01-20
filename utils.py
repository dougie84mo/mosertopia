from datetime import datetime
from webhook import DiscordWebhook, DiscordEmbed
# from chromedriver_py import binary_path as driver_path
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import QSize, QRect



#TODO: Enable this as an app setting for user to choose their own optional key & regenerate key on the fly button
# try:
#   with open("data/vault.json","r") as file:
#       keys = json.load(file)
# except FileNotFoundError:
#   generateKeySecret = "".join(random.choices(string.ascii_letters + string.digits, k=16))
#   write_data("data/vault.json",[{ "generated_key_secret": generateKeySecret }])
#   with open("data/vault.json","r") as file:
#       keys = json.load(file)
#
# e_key = keys[0]['generated_key_secret'].encode()
class SimpleAT:

        
    @staticmethod
    async def pyp_signin(page, login, count=0):
        # webbrowser.get('chrome').open_new_tab(login_url)
        # time.sleep(10)
        query_sel = login["selectors"]
        await page.type(query_sel[0], login["username"])
        await page.type(query_sel[1], login["password"])
        await page.click(query_sel[2])
        # print("Await Nav")
        while await page.querySelector(query_sel[1]) is not None and count < 5:
            count = count + 1
            print(count)
            await SimpleAT.pyp_signin(page, login, count)
        # await asyncio.sleep(20)


    # Press the green button in the gutter to run the script.

    # def startSession(self, cookieItem):
    #     self.s.cookies =

    def grabCookies(self, url):
        with requests.Session() as sess:
            cookiesPage = sess.get(url)


    def textMessagingScheduleInit(self):
        with open('data/moser/config.json') as c:
            j = json.load(c)

    def textMessagingSchedule(self, vendor, dt, lots=None):
        if lots is None:
            lots = []


class QVC:

    nborder = "border: none;"
    trans_border = "background-color: transparent;border: none;"



    @staticmethod
    def add_label(parent, geo=None, style=None, text=""):
        # QWidget widget
        widget = QtWidgets.QLabel(parent)
        if style is not None:
            widget.setStyleSheet(style)
        if geo is not None:
            widget.setGeometry(geo)
        widget.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        widget.setScaledContents(True)
        widget.setText(text)
        return widget


    @staticmethod
    def add_widget(parent, geo=None, style=None, scaled=None, add_cursor=True):
        # QWidget widget
        widget = QWidget(parent)
        if geo is not None:
            widget.setGeometry(geo)
        if add_cursor is True:
            widget.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        if style is not None:
            widget.setStyleSheet(style)
        if scaled is True:
            widget.setScaledContents(True)
        return widget


    @staticmethod
    def new_font(size=None, family='Arial', bold=False, weight=None):
        font = QtGui.QFont()
        font.setFamily(family)
        if size is not None:
            font.setPointSize(size)
        font.setBold(bold)
        if weight is not None:
            font.setWeight(weight)


# def start_browser(link,cookies):
#     caps = DesiredCapabilities().CHROME
#     caps["pageLoadStrategy"] = "eager" 
#     chrome_options = ChromeOptions()
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option("useAutomationExtension", False)
#     driver = Chrome(desired_capabilities=caps, executable_path=driver_path, options=chrome_options)
#     driver.execute_cdp_cmd(
#             "Page.addScriptToEvaluateOnNewDocument",
#             {
#                 "source": """
#         Object.defineProperty(window, 'navigator', {
#             value: new Proxy(navigator, {
#               has: (target, key) => (key === 'webdriver' ? false : key in target),
#               get: (target, key) =>
#                 key === 'webdriver'
#                   ? undefined
#                   : typeof target[key] === 'function'
#                   ? target[key].bind(target)
#                   : target[key]
#             })
#         })
#                   """
#             },
#     )
#     driver.get(link)
#     for cookie in cookies:
#         driver.add_cookie({
#             "name": cookie["name"],
#             "value" : cookie["value"],
#             "domain" : cookie["domain"]
#         })
#     driver.get(link)

def random_delay(delay, start, stop):
    """
    Returns the delay argument combined with a random number between start
    and stop dividied by 1000.
    """
    return delay + (random.randint(int(start), int(stop)) / 1000)
