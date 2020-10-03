from selenium import webdriver
from prettyprinter import pprint, cpprint
import json
import smtplib
import ssl
import imaplib, email
import datetime
import xlsxwriter
import kivy
from kivy.app import App
from kivy.uix.treeview import TreeView, Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.label import Label
from kivy.uix.button import Button
from main import SimpleAT


class AppGrid(GridLayout):
    cols = 2
    tabs = ["Mosertopia", "Vendors", "Projects", "Schedule", "Warranty"]
    page = ''

    def __init__(self, **kwargs):
        super(AppGrid, self).__init__(**kwargs)
        loggedin = None
        configjson = open('assets/moser/config.json')
        config = json.load(configjson)
        configjson.close()
        if config['login']['loggedin'] and config['login']['loggedinas']:
            loggedin = True
            print(type(config['login']['loggedinas']))



        accordion = Accordion(orientation='vertical')
        for x in range(len(self.tabs)):
            tab_name = self.tabs[x]
            item = AccordionItem(title=f'{tab_name}')
            if tab_name == self.tabs[0]:
                wid = Label(text=tab_name, font_size=16)
            else:
                wid = Button(text=tab_name, font_size=14)
                wid.on_press()
            item.add_widget(wid)
            print(item)
            accordion.add_widget(item)
        self.add_widget(accordion)

        # Open login page and make all other pages
        # On init, show the first page



        # self.add_widget(self.current_page)


class VendorsPage(FloatLayout):
    pass


class MosertopiaPage(FloatLayout):
    pass


class WarrantyPage(FloatLayout):
    pass


class SchedulePage(FloatLayout):
    pass


class ProjectsPage(FloatLayout):
    pass


class MoserApp(App):
    signinparam = ['username', 'password', 'signIn-btn']

    def build(self):

        return AppGrid()


if __name__ == '__main__':
    MoserApp().run()
