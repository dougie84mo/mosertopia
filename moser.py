import os, sys, datetime, email, imaplib, json, ssl, smtplib, requests, time, asyncio
import xlsxwriter, xlwings, openpyxl
from xlutils.copy import copy
from prettyprinter import cpprint, pprint
from pyppeteer import launch
from utils import SimpleAT

class Moser:

    __log_dir = ".\\log"
    __action_id = None
    __project_id = None

    def __init__(self, jcon=None):
        if jcon is None:
            with open("data/config.json") as jconfig:
                jcon = json.load(jconfig)
                self.jcon = jcon
            # TODO: try to build log folder
            
        else:
            self.jcon = jcon
        
        if self.__action_id is None:
            action = str(input("Would you like to see warranty or current selections? (0: Selections, 1: Warranty) \n"))
            action_int = int(action)
            if action_int != 1 and action_int != 0:
                self.__init__(jcon)
            else:
                self.__action_id = action_int
                self.__action_lot_data_file = "warranty" if action_int == 1 else "lots" 
                
        if self.__project_id is None:
            project = str(input("What Project would you like to view? (0: Marsh Lea, 1: Custom Homes, 2: T. Moser Land) \n"))
            project_int = int(project)
            if len(jcon["projectInfo"]) < project_int or project_int < 0:
                self.__init__(jcon)
            else:
                self.__project_id = project_int
                self._pinfo = self.jcon["projectInfo"][project_int]   

        if self.__action_id is not None and self.__project_id is not None:
            # If initialization information is correct then start asynchronousity
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.mosertopia_login_buildtopia())
            loop.close()


    async def mosertopia_login_buildtopia(self):
        # update = input("Should we update the projects? (y/n)")
    
        # - Default Viewport creats viewport maxmiuzzed to browser window size
        # - args [start-max..] for maximum browser size [args=['--start-maximized'],]
        browser = await launch(headless=False, defaultViewport=None)
        pages  = await browser.pages()
        page = pages[0]
        await page.goto(self.jcon["paths"]["login"])
        await SimpleAT.pyp_signin(page, login=self.jcon["sign_in"])
        #Gather project info
        apath = self.jcon["action_paths"][self.__action_id]

        with open(f'data/{self.__action_lot_data_file}.json') as lots:    
            lots_data = json.load(lots)
            self.lots_data = lots_data
        if self.__action_id == 0:
            await page.waitForSelector(self._pinfo[2])
            await page.click(f'{self._pinfo[2]} > {apath}')
            await self.lot_reference_update(page, "td:nth-child(2) > a", self.selections_lot_reference)
            
            lot = await self.lot_selection_check()

            # ld = self.lots_data[lot]
            di = f'{self.__log_dir}\\{self._pinfo[0]}\\{lot["ln"]}'
            di_path = f'{di}\\'
            workbook_name = f'{di_path}Selections.xlsx'
            if not os.path.exists(di):
                os.makedirs(di)
            file_urls = {}
            opts = []
            nsos = []
            # SHOULD set NSO and Option list and check len(nso) to avoid looping through items again
            ######### OPTIONS LIST
            Moser.element_cycle(page, lot["urls"][0], holding_array=opts, completion_callback=Moser.option_element_cycle, files=file_urls, file_selector="td:last-child > a")
            ########## NSO LIST
            Moser.element_cycle(page, lot["urls"][1], holding_array=nsos, completion_callback=Moser.nso_element_cycles, files=file_urls, file_selector="td:nth-child(6) > a")
            #  Set values of lot to compare against other values
            # self.lots_data[self.__action_id][lot["ln"]]["file_count"] = len(file_urls)
            ########## FILE_LIST
            if file_urls:
                for file_url in file_urls:
                    file_li_el = await Moser.get_tr_background(page=page, url=file_url, wait_sec=.5)
                    for fi in file_li_el:
                        cdp = await fi.Jeval("a", 'node => node.getAttribute("href")').createCDPSession()
                        await cdp.send("Page.setDownloadBehavior", {'behavior': 'allow', "downloadPAth": di_path})

            if not os.path.exists(workbook_name):
                # create new file;
                workbook = xlsxwriter.Workbook(workbook_name)

            else:
                # update old file dont use xlsxwriter
                workbook = xlsxwriter.Workbook(workbook_name)
            
        elif self.__action_id == 1:
            print("Warranty Chosen:")
            ################################
            # Warranty Action
            ################################

            await asyncio.wait([
                page.goto(apath),
                asyncio.sleep(3),
                page.waitForSelector('select[name="ProjectFilter"]'),
                page.querySelector('select[name="ProjectFilter"]').click(f'option[value="{self._pinfo[1]}"]')
            ])

            await self.lot_reference_update(page, "td:nth-child(3)", self.warranty_lot_reference)
            # If lot checked does not exist then generate warranty workbook. Ask question below after generation
            # Check if you want to update buildtopia or generate warranty list
        
        await browser.close()

    @staticmethod
    async def get_tr_background(page, url, wait_sec=3):
        await asyncio.wait([
            asyncio.sleep(wait_sec),
            page.goto(url),
            page.waitForSelector("tr.background")
        ])
        return await page.querySelectorAll("tr.background, tr.altbackground")
    


    async def lot_selection_check(self):
        action_lot_data = self.lots_data[self.__action_id]
        print("Choose from list")
        pprint(action_lot_data.keys())
        lnum = str(input("What Lot number? \n"))

        if lnum not in action_lot_data:
            print("Lot Number is not available, choose from the following lot numbers above")
            lnum = await Moser.lot_selection_check(action_lot_data)
        return action_lot_data[lnum]

    def get_lot_dict(self):
        if self.__project_id not in self.lots_data:
            self.lots_data[self.__project_id] = {"info": {"project_lot_value": 0}}
        return self.lots_data[self.__project_id]

    def __save_lots_data(self):
        with open(f'data/{self.__action_lot_data_file}.json', 'w') as lots:
            json.dumps(self.lots_data, lots)


    async def lot_reference_update(self, page, lot_selector="td:nth-child(2) > a", callback=None):
        await page.waitForSelector("tr.background")
        lots_el_li = await page.querySelectorAll("tr.background, tr.altbackground")

        #TODO: Value of elements in array
        tr_value = len(lots_el_li)
        plv = self.get_lot_dict()["info"]["project_lot_value"]
        if plv != len(tr_value):
            new_lots = []
            for lot in lots_el_li:
                #start writing to file data if needed
                ln = str(await lot.querySelectorEval(lot_selector, 'node => node.innerText'))
                if ln not in self.get_lot_dict():
                    new_lots.append(ln)
                    lot_info = await callback(lot)
                    lot_info["ln"] = ln
                    pprint(lot_info)
                    #  lot_url = lot.querySelectorEval('td:nth-child(3) > a', 'node => node.getAttribute("href")')
                    if lot_info is not None:
                        self.get_lot_dict()[ln] = lot_info
            print(f'The following lots are newly generated in {self.__action_lot_data_file.upper()}: \n {", ".join(new_lots)}')
            self.__save_lots_data()
            

        
            
        # only if all keys are not found in lots_data

    @staticmethod
    async def element_cycle(page, url, holding_array, completion_callback=None, file_selector=None, files=None):
        options_list_els = await Moser.get_tr_background(page, url)
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
                    td_result["has_file"] = True
                    files.append(files)
            holding_array.append(td_result)
    
    @staticmethod
    async def option_element_cycle(tds):
        return {
            "option_code": await tds[1].evaluate('(element) => element.innerText').strip(),
            "description": await tds[2].evaluate('(element) => element.innerText').strip(),
            "selection_notes": await tds[3].evaluate('(element) => element.innerText').strip(),
            "q": await tds[4].evaluate('(element) => element.innerText').strip(),
        }

    @staticmethod
    async def nso_element_cycles(tds):
        return {
            "nso_num": await tds[1].evaluate('(element) => element.innerText').strip(),
            "description": await tds[3].evaluate('(element) => element.innerText').strip(),
            "selection_notes": await tds[4].evaluate('(element) => element.innerText').strip(),
            "q": await tds[5].evaluate('(element) => element.innerText').strip(),
        }

    @staticmethod
    async def selections_lot_reference(lot):
        address = await lot.querySelectorEval('td:nth-child(3)', 'node => node.innerText')
        model_plan = await lot.querySelectorEval('td:nth-child(4)', 'node => node.innerText')
        plan_id = model_plan.split("ML")
        # modeL = plan_id[1].trim if len(plan_id) == 2 else plan_id[0]
        lot_url = await lot.querySelectorEval('td:nth-child(1) > a', 'node => node.getAttribute("href")')
        nso_url = await lot.querySelectorEval('td:last-child > a:nth-child(6)', 'node => node.getAttribute("href")')
        options_url = await lot.querySelectorEval('td:last-child > a:nth-child(4)', 'node => node.getAttribute("href")')
        return {
            "address": address.replace("\t", ""), 
            "model": plan_id[1].replace("\t", "").strip(),
            "urls": [options_url, nso_url, lot_url]
        }
    
    @staticmethod
    async def warranty_lot_reference(lot):
        lot_url = await lot.querySelectorEval('td:first-child > a', 'node => node.getAttribute("href")')
        address = await lot.querySelectorEval('td:nth-child(4)', 'node => node.innerText')
        return {
            "address": address, 
            "url": lot_url
        }




if __name__ == '__main__':
    Moser()
    # await Moser().mosertopia_login_buildtopia()    
