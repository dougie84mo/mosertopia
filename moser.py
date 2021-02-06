import os, sys, datetime, email, imaplib, json, ssl, smtplib, requests, time, asyncio
import xlsxwriter, xlwings, openpyxl
from xlutils.copy import copy
from prettyprinter import cpprint, pprint
from pyppeteer import launch

global NSO_ACCEPTED
NSO_ACCEPTED = [
    "NSO to PO"
]
class Moser:

    current_lot = None
    __log_dir = ".\\log"
    __action_id = None
    __project_id = None
    __excel_info = []

    def __init__(self):
        with open("data/config.json") as jconfig:
            jcon = json.load(jconfig)
            self.jcon = jcon
        with open("data/lots.json") as lots:    
            lots_data = json.load(lots)
            self.lots_data = lots_data
        
        # try to build log folder
        for project_id, project_info in enumerate(self.jcon['projectInfo']):
            if str(project_id) not in self.lots_data:
                self.lots_data[str(project_id)] = {
                    "info": {"name": project_info[1], "id": project_id, "in": project_info[0]},
                    "lots": {}
                }
                self.__save_lots_data()
                time.sleep(3)
        
        while self.__action_id is None:
            action = str(input("Would you like to see warranty or current selections? (0: Selections, 1: Warranty) \n"))
            action_int = int(action)
            if action_int == 1 or action_int == 0:
                self.__action_id = action_int
                self.__action = self.jcon["paths"]["action"][action_int]

        while self.__project_id is None:
            project = str(input("What Project would you like to view? (0: Marsh Lea, 1: Custom Homes, 2: T. Moser Land) \n"))
            project_int = int(project)
            if len(jcon["projectInfo"]) >= project_int and project_int >= 0:
                self.__project_id = project_int
                self._pinfo = self.jcon["projectInfo"][project_int]

        if self.__action_id is not None and self.__project_id is not None:
            # If initialization information is correct then start asynchronousity
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.mosertopia_login_buildtopia())
            loop.close()

    async def mosertopia_login_buildtopia(self):
        # - Default Viewport creats viewport maxmiuzzed to browser window size
        # - args [start-max..] for maximum browser size [args=['--start-maximized'],]
        browser = await launch(headless=False, defaultViewport=None)
        pages  = await browser.pages()
        page = pages[0]
        await page.goto(self.jcon["paths"]["login"])
        await Moser.pyp_signin(page, login=self.jcon["sign_in"])
        # print("Should result to next page")
        await page.goto(self.jcon["paths"]["homepage"])
        #Gather project info
        if self.__action_id == 0:
            
            await page.waitForSelector(self._pinfo[2])
            await page.click(f'{self._pinfo[2]} > {self.__action[0]}')
            await self.lot_reference_update(page)
            await self.lot_selection_check()
            # SHOULD set NSO and Option list and check len(nso) to avoid looping through items again
            ######### OPTIONS LIST
            await self.selection_element_cycle(page, 0, file_selector="td:last-child > a")
            ########## NSO LIST
            await self.selection_element_cycle(page, 1, file_selector="td:nth-child(6) > a")
            #  Set values of lot to compare against other values
            ########## FILE_LIST

            
        elif self.__action_id == 1:
            ################################
            # Warranty Action
            ################################
            await page.goto(self.__action[0])
            print("Warranty Chosen:")
            await asyncio.sleep(3)
            await page.waitForSelector('select[name="ProjectFilter"]')
            await page.click(f'select[name="ProjectFilter"] > option[value="{self._pinfo[1]}"]')
            await self.lot_reference_update(page, "td:nth-child(3)")
            await self.lot_selection_check()

            await page.goto(self.current_lot["warranty_url"])
            await page.waitForSelector(info_table_selector)
            # //*[@id="bodyWapper"]/table[2]/tbody/tr/td[5]/table/tbody/tr[4]/td/table[2]/tbody/tr[2]/td[1]/table[3]
            
            warranty_el_li = await Moser.get_tr_background(page)
            warranty_urls = []
            warranty_items = []
            for warranty_el in warranty_el_li:
                request_info = await warranty_el.querySelectorEval("td:nth-child(1) a", '''
                    (node) => (
                        return [node.innerText, node.getAttribute("href")];
                    )
                ''')
                request_info.append(await warranty_el.Jeval("td:nth-child(2)", "node => node.innerText"))
                warranty_urls.append(request_info)
            
            for warranty_url in warranty_urls:
                request_trs = await Moser.get_tr_background(page, warranty_url[1], .1)
                for tr in request_trs:
                    status = await tr.Jeval("td:nth-child(2)", "node => node.innerText")
                    is_open = bool(status.strip() == "Open")
                    wi = {
                        "n": await tr.Jeval("td:first-child", "node => node.innerText"),
                        "description": await tr.Jeval("td:nth-child(3)", "node => node.innerText"),
                        "status": status,
                        "is_open": is_open
                    }
                    if is_open:
                        wi["urls"] = [
                            await tr.Jeval("td:last-child > a:nth-child(1)", 'node => node.getAttribute("href")'),
                            await tr.Jeval("td:last-child > a:nth-child(2)", 'node => node.getAttribute("href")'),
                        ]
                    warranty_items.append(wi)
                # generate excel file from buildtopia
                # eventually check if file is created and edit that one. 
                # What type of information?

            # If lot checked does not exist then generate warranty workbook. Ask question below after generation
            # Check if you want to update buildtopia or generate warranty list

        await browser.close()


    async def update_selections(self, info):
        if not os.path.exists(workbook_name):
                # create new file;
            workbook = xlsxwriter.Workbook(self.get_lot_directory(fid=f'{self.__action[1]}.xslx'))


    async def update_warranty(self, workbook_name, info):
        if not os.path.exists(workbook_name):
                # create new file;
            workbook = xlsxwriter.Workbook(workbook_name)
    # async def create_warranty(self):

    @staticmethod
    async def get_tr_background(page, url=None, wait_sec=3):
        await asyncio.sleep(wait_sec)
        if url is not None:
            await page.goto(url)
        await page.waitForSelector("tr.background")
        return await page.querySelectorAll("tr.background, tr.altbackground")
    
    @staticmethod
    async def warranty_edit_request(tr):
        return {
            
        }


    def get_project_dict(self):
        pid_str = str(self.__project_id)
        return self.lots_data[pid_str]

    def get_lot_dict(self):
        return self.get_project_dict()["lots"]
        
    def get_in_lot_dict(self, lot):
        return self.get_lot_dict(lot)[lot]
    
    def get_lot_directory(self, lot_str=None, fid=None, download_path=None):
        lot_name = self.current_lot["ln"] if lot_str is None else lot_str
        a = f'{self.__log_dir}\\{self._pinfo[0]}\\{lot_name}'
        if download_path == True:
            return f'{a}\\'
        return f'{a}\\{fid}' if fid is not None else a

    def __save_lots_data(self):
        if self.current_lot is not None and self.__project_id is not None:
            self.lots_data[self.__project_id][self.current_lot["ln"]] = self.current_lot

        with open(f'data/lots.json', 'w') as lots:
            json.dump(self.lots_data, lots)

    async def lot_selection_check(self):
        lnum = None
        while lnum is None or lnum not in self.get_lot_dict():
            print("Choose from list")
            pprint(self.get_lot_dict().keys())
            lnum = str(input("What Lot number? \n"))
        self.current_lot = self.get_lot_dict().get(lnum)

    async def lot_reference_update(self, page, lot_selector="td:nth-child(2) > a"):
        await page.waitForSelector("tr.background")
        lots_el_li = await page.querySelectorAll("tr.background, tr.altbackground")

        for lot in lots_el_li:
            #start writing to file data if needed
            ln = str(await lot.querySelectorEval(lot_selector, 'node => node.innerText'))
            lot_in_dir = bool(ln in self.get_lot_dict())
            if not lot_in_dir and self.__action_id === 0:
                address = await lot.querySelectorEval('td:nth-child(3)', 'node => node.innerText')
                model_plan = await lot.querySelectorEval('td:nth-child(4)', 'node => node.innerText')
                plan_id = model_plan.split("ML")
                # modeL = plan_id[1].trim if len(plan_id) == 2 else plan_id[0]
                lot_url = await lot.querySelectorEval('td:nth-child(1) > a', 'node => node.getAttribute("href")')
                nso_url = await lot.querySelectorEval('td:last-child > a:nth-child(6)', 'node => node.getAttribute("href")')
                options_url = await lot.querySelectorEval('td:last-child > a:nth-child(4)', 'node => node.getAttribute("href")')
                
                lot_info = {
                    "ln": ln
                    "address": address.replace("\t", ""), 
                    "model": plan_id[1].replace("\t", "").strip(),
                    "urls": [options_url, nso_url, lot_url],
                    "nsos": [{}, {}], 
                    "options": [{}, {}],
                    "warranty_url": False,
                    "contact_one": [],
                    "contact_two": []
                }

                print(f'Newly generated : {ln}')
                temp_dir = self.get_lot_directory(lot_str=ln)
                if not os.path.exists(temp_dir):
                    os.makedirs(temp_dir)
                    # create 
                    selection_file = f'{temp_dir}\\lot_info.xlsx'
                    temp_sel_workbook = xlsxwriter.Workbook(selection_file)
                    workbook_vars = {
                        "General Info": [],
                        "Options": [],
                        "Nsos": [],
                        "Warranty": [],
                    }
                    
                    for worksheet_name, worksheet in workbook_vars.items():
                        temp_worksheet = temp_sel_workbook.add_worksheet(worksheet_name)
                        row = 0
                        column = 0
                        for header in worksheet
                            temp_worksheet.write(row, column, header)
                            column += 1
                            
                    temp_sel_workbook.close()

                    await asyncio.sleep(4)
                    # TODO: also initialize warranty and selection xcel sheets if possible
                self.get_lot_dict()[ln] = lot_info

                #  lot_url = lot.querySelectorEval('td:nth-child(3) > a', 'node => node.getAttribute("href")')
            elif self.__action_id === 1 and (lot_in_dir and self.get_lot_dict()[ln]["warranty_url"] === False):
                self.get_lot_dict()[ln]["warranty_url"] = await lot.querySelectorEval('td:nth=child(1) > a', 'node => node.getAttribute("href")')

        self.__save_lots_data()            
        # only if all keys are not found in lots_data

    async def selection_element_cycle(self, page, hid=0, file_selector=None):
        file_urls = {}
        sel_name = "nsos" if hid === 1 else : "options" 
        url = self.current_lot["urls"][hid]
        options_list_els = await Moser.get_tr_background(page, url)
        completion_callback = Moser.option_element_cycle if hid is 0 else Moser.nso_element_cycles
        for row in options_list_els:
            tds = await row.querySelectorAll("td")
            td_result = completion_callback(tds)

            if file_selector is not None:
                file_request = await row.querySelectorEval(file_selector, '''
                    (node) => (
                        i = node.innerText;
                        return i == "0" ? 0 : node.getAttribute("href");
                    )
                ''')
                if file_request != "0":
                    td_result["file_url"] = file_request
                    self.current_lot[sel_name] = td_result[1].append(file_request)
            self.append(td_result)

        len_files = len(file_urls)
        if file_urls and len_files != len(self.current_lot[sel_name][hid][1]):
            # remove all files besides .xslx files in folder
            self.current_lot["file_url_count"] = len_files
            for file_url in file_urls:
                file_li_el = await Moser.get_tr_background(page=page, url=file_url, wait_sec=.5)
                for fi in file_li_el:
                    file_anchor = await fi.J("a")
                    name = await file_anchor.evaluate('node => node.innerText')
                    name = name.replace("\t", "").replace(" ", "")
                    # if name not in self.current_lot["file_names"]:
                    #     cdp = await file_anchor.evaluate('node => node.getAttribute("href")').createCDPSession()
                    #     await cdp.send("Page.setDownloadBehavior", {'behavior': 'allow', "downloadPath": self.get_lot_directory(download_path=True)})
        self.__save_lots_data()

    def possible_warranty_notes(self, page, info_table_selector):
        info_table_trs = await page.querySelectorAll(f'{info_table_selector} > tr')
        contact_one = {
            "name": await info_table_trs[0].Jeval("td:nth-child(2)", "node => node.innerText"),
            "email": await info_table_trs[0].Jeval("td:nth-child(4)", "node => node.innerText"),
            "phone": await info_table_trs[3].Jeval("td:nth-child(4)", "node => node.innerText")
        }
        address = await info_table_trs[1].Jeval("td:nth-child(2)", "node => node.innerText")
        settlement_date = await info_table_trs[3].Jeval("td:nth-child(2)", "node => node.innerText")
        contact_two_link = await info_table_trs[4].Jeval("td:nth-child(2)", '''
            (node) => (
                i = node.innerText.trim();
                if (i != "") {
                    a = node.querySelector("a");
                    return [a.getAttribute("href"), a.innerText.trim()];
                } else {
                    return false;
                }
            )
        ''')
        
    @staticmethod
    async def option_element_cycle(tds):
        option_name = await tds[1].evaluate('(element) => element.innerText').strip()
        option_code_split = option_name.split(" ", 1)
        return {
            "id": option_code_split[0],
            "name": option_code_split[1],
            "description": await tds[2].evaluate('(element) => element.innerText').strip(),
            "selection_notes": await tds[3].evaluate('(element) => element.innerText').strip(),
            "quantity": await tds[4].evaluate('(element) => element.innerText').strip(),
        }

    @staticmethod
    async def nso_element_cycles(tds):
        accepted_str = await tds[2].evaluate('(element) => element.innerText').strip()
        accepted = False if accepted_str not in NSO_ACCEPTED else accepted_str

        return {
            "id": await tds[1].evaluate('(element) => element.innerText').strip(),
            "location": await tds[4].evaluate('(element) => element.innerText').strip(),
            "description": await tds[5].evaluate('(element) => element.innerText').strip(),
            "accepted": accepted
        }

    @staticmethod
    async def pyp_signin(page, login, count=0):
        # webbrowser.get('chrome').open_new_tab(login_url)
        # time.sleep(10)
        query_sel = login["selectors"]
        await page.type(query_sel[0], login["username"])
        await page.type(query_sel[1], login["password"])
        await page.click(query_sel[2])
        await asyncio.sleep(1)
        still_login = await page.querySelector(query_sel[1])
        # print("Await Nav")
        if still_login is not None and count < 5:
            count = count + 1
            # print(count)
            await Moser.pyp_signin(page, login, count)

    


if __name__ == '__main__':
    Moser()
    # await Moser().mosertopia_login_buildtopia()    
