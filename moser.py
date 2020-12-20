from selenium import webdriver
from selenium.webdriver.common.by import By
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


class MoserHelpers:

    @staticmethod
    def moser_hardcode_warranty_marsh_lea():

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
