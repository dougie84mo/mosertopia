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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.tabbedpanel import *
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from main import SimpleAT


class AppGrid(GridLayout):
    __tabs = ["Mosertopia", "Vendors", "Projects", "Schedule"]
    cols = 1
    # login = ObjectProperty(None)
    # tabbed_header = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(AppGrid, self).__init__(**kwargs)
        # configjson = open('assets/moser/user.json')
        # login = json.load(configjson)
        tabbed = TabbedPanel()
        tabbed.do_default_tab = False

        # configjson.close()
        for x in range(len(self.__tabs)):
            tab_name = self.__tabs[x]
            tabbed_header = TabbedPanelHeader(text=tab_name)
            tabbed.add_widget(tabbed_header)
            layout = GridLayout(cols=1)
            if tab_name == self.__tabs[0]:
                tabbed_header.content = MosertopiaPage(layout)
            elif tab_name == self.__tabs[1]:
                tabbed_header.content = VendorsPage(layout)
            elif tab_name == self.__tabs[2]:
                tabbed_header.content = ProjectsPage(layout)
            else:
                tabbed_header.content = SchedulePage(layout)

            # panel = TabbedPanelContent(tabbed_header.content)

            # print(tabbed_header)

        print(tabbed.content)
        self.add_widget(tabbed)

        # self.add_widget(self.tab_content)
        # Open login page and make all other pages
        # On init, show the first page


# class MosertopiaPage(GridLayout):
#     cols = 1
#
#     def __init__(self, **kwargs):
#         super(MosertopiaPage, self).__init__(**kwargs)
#
#
# class VendorsPage(GridLayout):
#     cols = 1
#     def __init__(self, **kwargs):
#         super(VendorsPage, self).__init__(**kwargs)
#
#
# class ProjectsPage(GridLayout):
#     cols = 1
#     def __init__(self, **kwargs):
#         super(ProjectsPage, self).__init__(**kwargs)
#
#
# class SchedulePage(GridLayout):
#     cols = 1
#
#     def __init__(self, **kwargs):
#         super(SchedulePage, self).__init__(**kwargs)



def MosertopiaPage(layout):
    return layout


def VendorsPage(layout):
    return layout


def ProjectsPage(layout):
    return layout


def SchedulePage(layout):
    return layout




class MoserApp(App):

    def build(self):
        return AppGrid()

    # def build_settings(self, settings):
    #     jsondata = open('assets/moser/settings_config.json')
    #     j = json.load(jsondata)
    #     settings.add_json_data('')
    #     jsondata.close()


if __name__ == '__main__':
    MoserApp().run()
