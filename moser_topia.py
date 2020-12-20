from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSizePolicy, QWidget
from PyQt5.QtCore import QSize, QRect
from pages.tab_pages import RealTimePage, HomePage, WarrantyPage, SettingPage
from utils import QVC
from prettyprinter import pprint, cpprint
import json
import smtplib
import sys, os, imaplib, email, datetime, ssl


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self._styles = [
            "border: none;",
            "background-color: transparent;border: none;",
        ]
        self.setGeometry(QRect(0, 0, 1100, 600))
        self.setWindowTitle("Moser Topia")
        self.setgui(self)
        self.show()

    def setgui(self, MainWindow):
        self.main_widg = QWidget(MainWindow)
        # self.main_widg.setStyleSheet()
        #
        self.menubar = QWidget(self.main_widg)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 100, 601))
        self.menubar.setStyleSheet("background-color: #232323;border-right: 1px solid #2e2d2d;")
        pprint(self.menubar)
        tab_widgets = {
            "home": [QRect(0, 85, 60, 45), "Home"],
            "warranty": [QRect(0, 130, 60, 45), "Warranty"],
            "realtime": [QRect(0, 175, 60, 45), "Current"],
            "settings": [QRect(0, 220, 60, 45), "Settings"]
        }
        self.set_tabs(tab_widgets)
        # self.logo = QtWidgets.QLabel(self.menubar)
        # self.logo.setGeometry(QtCore.QRect(10, 23, 41, 41))
        # self.logo.setStyleSheet("border: none;")
        # self.logo.setText("")
        # self.logo.setPixmap(QtGui.QPixmap(":/images/birdbot.png"))
        # self.logo.setScaledContents(True)
        self.home_page = HomePage(self.main_widg)
        # self.createdialog = CreateDialog(self)
        # self.createdialog.addtask_btn.clicked.connect(self.create_task)
        # self.createdialog.setWindowIcon(QtGui.QIcon("images/birdbot.png"))
        # self.createdialog.hide()
        self.warranty_page = WarrantyPage(self.main_widg)
        self.warranty_page.hide()
        self.realtime_page = RealTimePage(self.main_widg)
        self.realtime_page.hide()
        self.settings_page = SettingPage(self.main_widg)
        self.settings_page.hide()
        #

        MainWindow.setCentralWidget(self.main_widg)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.set_functions()


    def set_tabs(self, tabs=None):
        if tabs is not None and isinstance(tabs, dict):
            for k, tab in tabs.items():
                if k == "home":
                    styles = [
                        "background-color: #5D43FB;border: none;",
                        "background-color: #272342;border: none;"
                    ]
                else:
                    styles = [
                        "background-color: transparent;border: none;",
                        "background-color: transparent;border: none;"
                    ]
                menubar_tab = QVC.add_widget(self.menubar, tab[0], style=styles[0])
                setattr(self, f'{k}_tab', menubar_tab)

                setattr(self, f'{k}_active_tab', QVC.add_widget(getattr(self, f'{k}_tab'), QRect(0, 0, 4, 45), style=styles[1]))
                setattr(self, f'{k}_icon', QVC.add_label(getattr(self, f'{k}_tab'), QtCore.QRect(21, 13, 20, 20), style="border: none;", text=tab[1]))


    def set_functions(self):
        self.current_page = "home"
        self.home_tab.mousePressEvent = lambda event: self.change_page(event, "home")
        self.warranty_tab.mousePressEvent = lambda event: self.change_page(event, "warranty")
        self.settings_tab.mousePressEvent = lambda event: self.change_page(event, "settings")
        self.realtime_tab.mousePressEvent = lambda event: self.change_page(event, "realtime")


    def change_page(self, event, current_page):
        eval('self.{}_active_tab.setStyleSheet("background-color: transparent;border: none;")'.format(self.current_page))
        eval('self.{}_icon.setPixmap(QtGui.QPixmap(":/images/{}.png"))'.format(self.current_page,self.current_page))
        eval('self.{}_tab.setStyleSheet("background-color: transparent;border: none;")'.format(self.current_page))
        eval("self.{}_page.hide()".format(self.current_page))
        self.current_page = current_page
        eval('self.{}_active_tab.setStyleSheet("background-color: #5D43FB;border: none;")'.format(self.current_page))
        eval('self.{}_icon.setPixmap(QtGui.QPixmap(":/images/{}_alt.png"))'.format(self.current_page,self.current_page))
        eval('self.{}_tab.setStyleSheet("background-color: #272342;border: none;")'.format(self.current_page))
        eval("self.{}_page.show()".format(self.current_page))


if __name__ == '__main__':
    ui_app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    os._exit(ui_app.exec())
