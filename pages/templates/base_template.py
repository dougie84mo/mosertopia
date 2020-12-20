from PyQt5 import QtCore, QtGui, QtWidgets
from sites.walmart import Walmart
from sites.bestbuy import BestBuy
from pages.createdialog import CreateDialog
from pages.pollbrowser import PollBrowserDialog
from utils import get_profile, get_proxy, BirdLogger, return_data, write_data, open_browser
import urllib.request,sys,platform
import settings

def no_abort(a, b, c):
    sys.__excepthook__(a, b, c)
sys.excepthook = no_abort
logger = BirdLogger()


class TempatePage(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(TempatePage, self).__init__(parent)
        self.load_info()
        self.setupUi(self)

    def setupUi(self, homepage):
        pass

    def load_info(self):
        pass

class TaskTab(QtWidgets.QWidget):
    def __init__(self,site,product,profile,proxies,monitor_delay,error_delay,max_price,stop_all,parent=None):
        super(TaskTab, self).__init__(parent)
        self.task_id = str(int(tasks_total_count.text())+1)
        tasks_total_count.setText(self.task_id)
        self.site,self.product,self.profile,self.proxies,self.monitor_delay,self.error_delay,self.max_price,self.stop_all = site,product,profile,proxies,monitor_delay,error_delay,max_price,stop_all
        self.setupUi(self)
        tasks.append(self)
        tasks_data = return_data("./data/tasks.json")
        task_data = {"task_id": self.task_id,"site":self.site,"product": self.product,"profile": self.profile,"proxies": self.proxies,"monitor_delay": self.monitor_delay,"error_delay": self.error_delay,"max_price": self.max_price}
        tasks_data.append(task_data)
        write_data("./data/tasks.json",tasks_data)
