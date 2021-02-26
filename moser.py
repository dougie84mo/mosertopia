import os, sys, datetime, email, imaplib, json, ssl, smtplib, requests, time, asyncio
import xlsxwriter, xlwings, openpyxl
from xlutils.copy import copy
from prettyprinter import cpprint, pprint
from pyppeteer import launch
import aiofiles

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
    __temp_files = []

    def __init__(self):
        with open("data/config.json") as jconfig:
            jcon = json.load(jconfig)
            self.jcon = jcon
        with open("data/lots.json") as lots:    
            lots_data = json.load(lots)
            self.lots_data = lots_data
        
        # try to build log folder
        for project_id, project_info in enumerate(self.jcon['projectInfo']):
            if len(self.lots_data) < project_id:
                self.lots_data[project_id] = {
                    "info": {"name": project_info[1], "id": project_id, "in": project_info[0]},
                    "lots": {}
                }
                self.__save_lots_data()
                time.sleep(1)
                print(f'Project {project_info[1]} added to lots data')
        
        while self.__project_id is None:
            project = str(input("What Project would you like to view?\n(0: Marsh Lea, 1: Custom Homes, 2: T. Moser Land)\n"))
            project_int = int(project)
            if len(jcon["projectInfo"]) >= project_int and project_int >= 0:
                self.__project_id = project_int
                self._pinfo = self.jcon["projectInfo"][project_int]

        while self.__action_id is None:
            action = str(input("Would you like to see warranty or current selections?\n(0: Selections, 1: Warranty, -1: Reset Lot Info) \n"))
            action_int = int(action)
            if action_int == 1 or action_int == 0:
                self.__action_id = action_int
                self.__action = self.jcon["paths"]["action"][action_int]
            elif action_int == -1: 
                self.__action_id = action_int

        loop = asyncio.get_event_loop()
        if self.__action_id == -1:
            loop.run_until_complete(self.lot_reference_update())
            
        elif self.__action_id >= 0 and self.__project_id is not None:
            # If initialization information is correct then start asynchronousity
            loop.run_until_complete(self.mosertopia_login_buildtopia())

        loop.close()
    

    async def mosertopia_login_buildtopia(self):
        # - Default Viewport creats viewport maxmiuzzed to browser window size
        # - args [start-max..] for maximum browser size [args=['--start-maximized'],]
        await self.lot_selection_check()
        browser = await self.moser_browser()
        page = await self.open_mosertopia_page(browser)
        if not os.path.exists(self.get_lot_directory(file_name='lot_info.xlsx')):
            print(f'Please run -1 command for action to get lot info registered for Lot #{self.current_lot["ln"]} in project: {self._pinfo[1]}')
        #Gather project info
        elif self.__action_id == 0:
            
            
            # SHOULD set NSO and Option list and check len(nso) to avoid looping through items again
            ######### OPTIONS LIST
            await self.selection_element_cycle(page, 0, file_selector="td:last-child > a")
            ########## NSO LIST
            await self.selection_element_cycle(page, 1, file_selector="td:nth-child(6) > a")
            ########## FILE_LIST
            
                
            ########## EXCEL UPDATE


            
        elif self.__action_id == 1:
            ################################
            # Warranty Action
            ################################
            
            await page.goto(self.abs_path(self.current_lot["warranty_url"]))
            # //*[@id="bodyWapper"]/table[2]/tbody/tr/td[5]/table/tbody/tr[4]/td/table[2]/tbody/tr[2]/td[1]/table[3]
            
            warranty_summary_els = await Moser.get_tr_background(page)
            warranty_groups = []
            for warranty_el in warranty_summary_els:
                summary_info = await warranty_el.querySelectorEval("td:nth-child(1) a", '''
                    (node) => (
                        return [node.innerText, node.getAttribute("href")];
                    )
                ''')
                request_info = {
                    "summary": await warranty_el.Jeval("td:nth-child(2)", "node => node.innerText"),
                    "request_url": summary_info[1],
                    "request_id": summary_info[0],
                }
                warranty_groups.append(request_info)
            
            warranty_items = []
            for warranty_group in warranty_groups:
                request_trs = await Moser.get_tr_background(page, warranty_group[1], .1)
                for tr in request_trs:
                    status = await tr.Jeval("td:nth-child(2)", "node => node.innerText")
                    wi = {
                        "description": await tr.Jeval("td:nth-child(3)", "node => node.innerText"),
                        "status": status,
                        "is_open": bool(status.strip() == "Open")
                    }
                    if wi["is_open"]:
                        wi["urls"] = [
                            await tr.Jeval("td:last-child > a:nth-child(2)", 'node => node.getAttribute("href")'),
                            await tr.Jeval("td:last-child > a:nth-child(1)", 'node => node.getAttribute("href")'),
                        ]
                    warranty_items.append(wi+warranty_group)

            for warranty_item in warranty_items:
                if "urls" in warranty_item:
                    await page.goto(warranty_item["urls"])
                    await page.waitForSelector("#middle_left")
                    sub_info_rows = await page.querySelectorAll("#middle_left > table:nth-child(1) > tbody > tr")
                    warranty_item["internal_details"] = await sub_info_rows[1].Jeval("td:nth-child(2) > textarea", 'node => node.innerText')
                    # tr:nth-child(2) > td:nth-child(2) > textarea
                    defective_group = await sub_info_rows[5].Jeval('td:nth-child(6) > option[selected="selected"]', 'node => node.innerText')
                    defective_group = defective_group.split(' ', 1)
                    warranty_item["defect_group_name"] = defective_group[1]
                    warranty_item["defect_code"] = defective_group[0]
                    # tr:nth-child(6) > td:nth-child(2) > 



        await browser.close()
            
            # generate excel file from buildtopia

            # Check if you want to update buildtopia or generate warranty list


    async def lot_reference_update(self):
        browser = await self.moser_browser()
        page = await self.open_mosertopia_page(browser)
        await page.goto(self.jcon["paths"]["homepage"])

        await page.waitForSelector(self._pinfo[2])
        await page.click(f'{self._pinfo[2]} > td:nth-child(4) > a')
        
        lots_el_li = await self.get_tr_background(page)

        for lot in lots_el_li:
            #start writing to file data if needed
            ln = str(await lot.querySelectorEval("td:nth-child(2) > a", 'node => node.innerText'))
            address = await lot.querySelectorEval('td:nth-child(3)', 'node => node.innerText')
            model_plan = await lot.querySelectorEval('td:nth-child(4)', 'node => node.innerText')
            plan_id = model_plan.split("ML")
            # modeL = plan_id[1].trim if len(plan_id) == 2 else plan_id[0]
            lot_url = await lot.querySelectorEval('td:nth-child(1) > a', 'node => node.getAttribute("href")')
            nso_url = await lot.querySelectorEval('td:last-child > a:nth-child(6)', 'node => node.getAttribute("href")')
            options_url = await lot.querySelectorEval('td:last-child > a:nth-child(4)', 'node => node.getAttribute("href")')
            
            lot_info = {
                "ln": ln,
                "address": address.replace("\t", ""), 
                "model": plan_id[1].replace("\t", "").strip(),
                "urls": [options_url, nso_url, lot_url],
                "nsos": {}, 
                "options": {},
                "selection_files": {},
                "warranty_url": False,
                "contact_one": [],
                "contact_two": []
            }

            temp_dir = self.get_lot_directory(lot_str=ln)
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

                # create 
            selection_file = f'{temp_dir}\\lot_info.xlsx'
            if not os.path.exists(selection_file):
                temp_sel_workbook = xlsxwriter.Workbook(selection_file)
                workbook_vars = {
                    "general": ["Lot Id", "Address", "Model"],
                    "options": ["Id", "Name", "Desciption", "Selection Notes", "Quantity", "See Files"],
                    "nsos": ["Accepted", "Sub Category", "Description", "Location", "Red. Description", "File Names"],
                    "warranty": ["Id", "Summary", "Sub Description", "Openned", "Internal Details", "Defect Code", "Defect Name"],
                }
                
                for worksheet_name, worksheet in workbook_vars.items():
                    temp_worksheet = temp_sel_workbook.add_worksheet(worksheet_name.title())
                    Moser.xslx_write(temp_worksheet, worksheet)
                    if worksheet_name == "general":
                        general_info = [ln, lot_info["address"], lot_info["model"]]
                        Moser.xslx_write(temp_worksheet, general_info, 1)

                temp_sel_workbook.close()

                await asyncio.sleep(1)
                # TODO: also initialize warranty and selection xcel sheets if possible
            self.get_lot_dict()[ln] = lot_info

                #  lot_url = lot.querySelectorEval('td:nth-child(3) > a', 'node => node.getAttribute("href")')

        await page.goto("https://app.buildtopia.com/english_exec/service-owners")
        pf = 'select[name="ProjectFilter"]'
        cf = f'{pf} > [value="{self._pinfo[1]}"]'
        c = self._pinfo[1]
        # cf = f'[value="{self._pinfo[1]}"]'
        # options = f'{pf} > option'
        print(cf)
        await page.waitForSelector(pf)
        await page.click(pf)
        await asyncio.sleep(3)
    
        await page.waitForSelector(cf)
        await page.select(pf, c)
        await asyncio.sleep(3)
        war_lots = await self.get_tr_background(page)
        for war_lot in war_lots:
            ln = str(await war_lot.querySelectorEval("td:nth-child(3)", 'node => node.innerText'))
            # print(ln)
            ln = ln.strip()
            if ln in self.get_lot_dict() and self.get_lot_dict()[ln]["warranty_url"] == False:
                self.get_lot_dict()[ln]["warranty_url"] = await war_lot.Jeval('td:nth-child(1) > a', 'node => node.getAttribute("href")')

        await browser.close()
        self.__save_lots_data()

        await asyncio.sleep(10)


    # async def update_selections(self, info):
    #     if not os.path.exists(workbook_name):
    #             # create new file;
    #         workbook = xlsxwriter.Workbook(self.get_lot_directory(file_name=f'{self.__action[1]}.xslx'))


    # async def update_warranty(self, workbook_name, info):
    #     if not os.path.exists(workbook_name):
    #             # create new file;
    #         workbook = xlsxwriter.Workbook(workbook_name)
    # async def create_warranty(self):

    async def moser_browser(self):
        return await launch(headless=self.jcon['production'], defaultViewport=None)

    async def open_mosertopia_page(self, browser):
        pages  = await browser.pages()
        page = pages[0]
        await page.goto(self.jcon["paths"]["login"])
        await Moser.pyp_signin(page, login=self.jcon["sign_in"])
        # print("Should result to next page")
        return page

    @staticmethod
    async def get_tr_background(page, url=None, wait_sec=3):
        await asyncio.sleep(wait_sec)
        if url is not None:
            await page.goto(url)
        await page.waitForSelector("tr.background")
        return await page.querySelectorAll("tr.background, tr.altbackground")
    

    def get_project_dict(self):
        return self.lots_data[self.__project_id]

    def get_lot_dict(self):
        return self.get_project_dict()["lots"]
        
    def get_in_lot_dict(self, lot):
        return self.get_lot_dict()[lot]
    
    def get_lot_directory(self, lot_str=None, file_name=None, download_path=None):
        lot_name = self.current_lot["ln"] if lot_str is None else lot_str
        a = f'{self.__log_dir}\\{self._pinfo[0]}\\{lot_name}'
        if download_path == True:
            return f'{a}\\'
        return f'{a}\\{file_name}' if file_name is not None else a

    def __save_lots_data(self):
        if self.current_lot is not None and self.__project_id is not None:
            self.lots_data[self.__project_id][self.current_lot["ln"]] = self.current_lot

        with open(f'data/lots.json', 'w') as lots:
            json.dump(self.lots_data, lots)
   
    async def __aysave_lots_data(self):
        if self.current_lot is not None and self.__project_id is not None:
            self.lots_data[self.__project_id][self.current_lot["ln"]] = self.current_lot

        async with aiofiles.open(f'data/lots.json', 'w+') as lots:
            lots.write(json.dump(self.lots_data, lots))

    async def lot_selection_check(self):
        lnum = None
        while lnum is None or lnum not in self.get_lot_dict():
            print("Choose from list")
            print(", ".join(self.get_lot_dict().keys()))
            lnum = str(input("What Lot number? \n"))
        self.current_lot = self.get_lot_dict().get(lnum)

                
        # only if all keys are not found in lots_data

    @staticmethod
    def xslx_write(wrksheet, arr, row=0):
        column = 0
        for a in arr:
            wrksheet.write(row, column, a)
            column += 1
    
    def abs_path(self, url):
        return f'{self.jcon["paths"]["base"]}{url}'


    async def selection_element_cycle(self, page, hid=0, file_selector=None):
        # file_urls = {}
        sel_name = "nsos" if hid == 1 else "options" 
        url = self.current_lot["urls"][hid]
        buildtopia_url = f'{self.jcon["paths"]["base"]}{url}'
        options_list_els = await Moser.get_tr_background(page, buildtopia_url)
        completion_callback = Moser.option_element_cycle if hid == 0 else Moser.nso_element_cycles
        for row in options_list_els:
            tds = await row.querySelectorAll("td")
            td_result = await completion_callback(page, tds)

            # Gets file page url
            if file_selector is not None:
                file_request = await row.querySelectorEval(file_selector, '''
                    (node) => {
                        i = node.innerText
                        return i == "0" ? 0 : node.getAttribute("href")
                    }
                ''')
                if file_request != "0":
                    td_result["file_page_url"] = file_request
                    self.__temp_files.append(file_request)
                    # GO back later and find this files
            
            self.current_lot[sel_name][td_result["id"]] = td_result

        # len_files = len(file_urls)
        # if file_urls and len_files != len(self.current_lot[sel_name]):
        #     # remove all files besides .xslx files in folder
        #     self.current_lot["file_url_count"] = len_files
        #     for file_url in file_urls:
        #         file_li_el = await Moser.get_tr_background(page=page, url=file_url, wait_sec=.5)
        #         for fi in file_li_el:
        #             file_anchor = await fi.J("a")
        #             name = await file_anchor.evaluate('node => node.innerText')
        #             name = name.replace("\t", "").replace(" ", "")
                    # if name not in self.current_lot["file_names"]:
                    #     cdp = await file_anchor.evaluate('node => node.getAttribute("href")').createCDPSession()
                    #     await cdp.send("Page.setDownloadBehavior", {'behavior': 'allow', "downloadPath": self.get_lot_directory(download_path=True)})
        self.__save_lots_data()
        print("Saved lot selection data\nNow uploading files...")

        for selection in self.current_lot[sel_name]:
            if "file_page_url" in selection:
                await page.goto(selection["file_page_url"])
                current_file_page = await self.get_tr_background(page)
                await page._client.send('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': self.get_lot_directory()})
                # cdp = await page.target.createCDPSession();
                for file_item in current_file_page:
                    file_name = await page.evaluate('(element) => element.innerText', file_item)


    async def possible_warranty_notes(self, page, info_table_selector):
        await page.waitForSelector(info_table_selector)

        info_table_trs = await page.querySelectorAll(f'{info_table_selector} > tr')
        contact_one = {
            "name": await info_table_trs[0].Jeval("td:nth-child(2)", "node => node.innerText"),
            "email": await info_table_trs[0].Jeval("td:nth-child(4)", "node => node.innerText"),
            "phone": await info_table_trs[3].Jeval("td:nth-child(4)", "node => node.innerText")
        }
        homeowner_lot_info = {
            "contacts": [contact_one],
            "address": await info_table_trs[1].Jeval("td:nth-child(2)", "node => node.innerText"),
            "settlement_date": await info_table_trs[3].Jeval("td:nth-child(2)", "node => node.innerText") 
        }
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

        return homeowner_lot_info

        
    @staticmethod
    async def option_element_cycle(page, tds):
        option_id = await page.evaluate('(element) => element.innerText', tds[1])
        option_code_split = option_id.strip().split(" ", 1)
        description = await page.evaluate('(element) => element.innerText', tds[2])
        selection_notes = await page.evaluate('(element) => element.innerText', tds[3])
        quantity = await page.evaluate('(element) => element.innerText', tds[4])
        return {
            "id": option_code_split[0],
            "name": option_code_split[1],
            "description": description.strip(),
            "selection_notes": selection_notes.strip(),
            "quantity": quantity.strip(),
        }

    @staticmethod
    async def nso_element_cycles(page, tds):
        accepted_str = await page.evaluate('(element) => element.innerText', tds[2]).strip()
        accepted = False if accepted_str not in NSO_ACCEPTED else accepted_str
        desc = await page.evaluate('(element) => element.innerText', tds[4])
        pone, ptwo = desc.replace("&nbsp;", "").split("<hr>")
        sub_cat, sub_desc = pone.split(" - ")
        sub_cat_red, sub_desc_red = pone.split(" - ")


        location = await page.evaluate('(element) => element.innerText', tds[3]).strip()

        return {
            "id": await page.evaluate('(element) => element.innerText', tds[1]).strip(),
            "accepted": accepted,
            "sub_category": sub_cat,
            "description": sub_desc,
            "second_desc": sub_desc_red,
            "location": location if location != "Selections" else "NA",
            "accepted_text": accepted_str,
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
