import os, datetime, email, imaplib, json, ssl, smtplib, requests, time, asyncio, xlsxwriter
from prettyprinter import cpprint, pprint
# from selenium import webdriver
# from selenium.webdriver.common.by import By
from pyppeteer import launch
from bs4 import BeautifulSoup

# from main import SimpleAT 

# class MoserApp:




class MoserHelpers:

    @staticmethod
    async def moser_hardcode_warranty_marsh_lea():


        results = MoserHelpers.moser_log_to_page(j, ["cs_requests", "cs_requests_list"])
        moser_data = { "address_lot": [], "description": [], "category": [], "status": [], "vendors": [], "opened_at": [], "closed_at": [], }
        # edit_request, open_request

        # for tr in results:
        #     pprint(tr)
        #     project_name = tr.find_element(By.CSS_SELECTOR, 'td:nth-child(8)').text
        #     pprint(project_name)
        #     # Maybe in Customs Homes, something different
        #     if 'Marsh Lea' in project_name or 'Custom Homes' in project_name:
        #         url = tr.find_element(By.CSS_SELECTOR, 'td:nth-child(1) a').get_attribute('href')

        #         try:
        #             with SimpleAT.selenium_start(url) as other_tab:
        #                 w_table = other_tab.find_elements(By.CSS_SELECTOR, '#listTable > tbody > tr')
        #                 w_table.pop(0)
        #                 lot_id = other_tab.find_element(By.XPATH, j["xpaths"]["cs_lots"])

        #                 pprint(lot_id)
        #                 for el in w_table:
        #                     tds = el.find_elements_by_tag_name("td")
        #                     moser_data["address_lot"].append(lot_id)
        #                     descr = tds[2].text
        #                     moser_data["description"].append(descr)
        #                     opened = True if tds[1].text == "Open" else False
        #                     # AI.something
        #         except Exception as e:
        #             print(e)



                
    @staticmethod
    async def mosertopia_login_buildtopia():
        # update = input("Should we update the projects? (y/n)")
        with open("data/config.json") as jconfig:
            j = json.load(jconfig)
            paths = j["paths"]

        action = str(input("Would you like to see warranty or current selections? (0: Selections, 1: Warranty) \n"))
        action_int = int(action)
        project = str(input("What Project would you like to view? (0: Marsh Lea, 1: Custom Homes, 2: T. Moser Land) \n"))
        project_int = int(project)
        
        if (len(j["projects"]) < project_int or project_int < 0) or (action_int != 1 and action_int != 0):

            print("Project must be in projects list 0-2, Action must be 1 or 0")
            await MoserHelpers.mosertopia_login_buildtopia()
        else:
            # - Default Viewport creats viewport maxmiuzzed to browser window size
            # - args [start-max..] for maximum browser size [args=['--start-maximized'],]
            browser = await launch(headless=False, defaultViewport=None)
            pages  = await browser.pages()
            page = pages[0]
            apath = j["action_paths"][action_int]
            await page.goto(j["paths"]["login"])
            await SimpleAT.pyp_signin(page, login=j["sign_in"])
            # print(page)
            
            p =  j["projects"][project_int]
            project_dirname = j["project_abbrs"][project_int]
            if action_int == 0:
                print(p)
                await page.waitForSelector(p)
                await page.click(f'{p} > {apath}')
                # await page.waitForNavigation()
                await page.waitForSelector("tr.background")
                lots_el_li = await page.querySelectorAll("tr.background, tr.altbackground")

                # open lot json file
                with open('data/lots.json', 'r') as lots:    
                    lots_data = json.load(lots)
                    file_updated = 1

                for lot in lots_el_li:
                    #start writing to file data if needed
                    ln = str(lot.querySelectorEval('td:nth-child(2) > a', 'node => node.innerText'))

                    if ln not in lots_data:
                        file_updated = 0 
                        address = lot.querySelectorEval('td:nth-child(3)', 'node => node.innerText')
                        model_plan = lot.querySelectorEval('td:nth-child(4)', 'node => node.innerText').split("ML")
                        model_plan = model_plan[1].trim if len(model_plan) == 2 else model_plan[0]
                        nso_url = lot.querySelectorEval('td:last-child > a:nth-child(6)', 'node => node.getAttribute("href")')
                        options_url = lot.querySelectorEval('td:last-child > a:nth-child(4)', 'node => node.getAttribute("href")')
                        lot_url = lot.querySelectorEval('td:nth-child(2) > a', 'node => node.getAttribute("href")')
                        lot_info = {
                            lot: ln, 
                            lot_id: f'{project_dirname}{ln}', 
                            address: address, 
                            "model": model_plan, 
                            "urls": [nso_url, options_url, lot_url]
                            }
                        lots_data[ln] = lot_info
                    
                # only if all keys are not found in lots_data
                if file_updated is 0:
                    with open('data/lots.json', 'w') as lots:
                        json.dump(lots_data)
                    
                

                
                pprint(lots)
                print("Making sure")
                lot_num = int(input("What Lot number? \n"))
                lot_str = f'0{str(lot_num)}' if lot_num <= 9 else str(lot_num)


                lot_name = f'Lot{lot_str}'
                
                di = f'.\\log\\lots\\{project_dirname}\\{lot_name}'

                if not os.path.exists(di):
                    os.makedirs(di)

                workbook = xlsxwriter.Workbook(f'{di}\\{lot_name}.xlsx')
                
            elif action_int == 1:
                print("Warranty Chosen")
                project_name = j["project_name"][project_int]

                lots = {}
                await page.goto(apath)
                await page.waitForSelector('select[name="ProjectFilter"]')
                await page.querySelector('select[name="ProjectFilter"]').click(f'option[value="{project_name}"]')
                # If warranty
                workbook = xlsxwriter.Workbook(f'.\\log\\lots\\{project_dirname}\\warranty_list.xlsx')

            await browser.close()
            # go to project and a  ction url

    @staticmethod
    async def lot_selection_check(page, lot_info)
        urls = lot_info["urls"]
        await page.goto(apath)



            
            

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




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(MoserHelpers().mosertopia_login_buildtopia())
    loop.close()
    # await MoserHelpers().mosertopia_login_buildtopia()    
