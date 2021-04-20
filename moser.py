import os, sys, datetime, email, imaplib, json, ssl, smtplib, requests, time, asyncio, re
import xlsxwriter, xlwings, openpyxl
from xlutils.copy import copy
from prettyprinter import cpprint, pprint
from pyppeteer import launch
import aiofiles
import urllib.request
import wget
import csv
import string


NSO_ACCEPTED = [
    "NSO to PO",
    "Buyer Accepted",
    "Released",
    "Approved"
]
LOG_DIR = ".\\log"
WARRANT_DIR = ".\\warranty"
RESET = 0
SELECTIONS = 1
WARRANTY = 2
GATHER_WARRANTY_INFO = 3
with open("data/config.json") as jconfig:
    jcon = json.load(jconfig)
    JCONFIG = jcon


class Moser:

    current_lot = None
    __action_lots = []
    __action_id = None
    __project_id = None

    def __init__(self, argv):
        with open("data/lots.json") as lots:    
            lots_data = json.load(lots)
            self.lots_data = lots_data
        
        # try to build log folder
        for project_id, project_info in enumerate(JCONFIG['projectInfo']):
            if len(self.lots_data) < project_id:
                self.lots_data[project_id] = {
                    "info": {"name": project_info[1], "id": project_id, "in": project_info[0]},
                    "lots": {}
                }
                self.__save_lots_data()
                print(f'Project {project_info[1]} added to lots data')
                time.sleep(1)

        largv = len(argv)
        print(argv)
        if largv > 1:
            project_int = int(argv[1])
            self.set_project_id(project_int)
        if largv > 2:
            action_int = int(argv[2])
            self.set_action_id(action_int)
        if largv > 3 and self.__action_id is not None and self.__project_id is not None:
            lot_action = str(argv[3])
            self.lot_selection_check(lot_action)

        while self.__project_id is None:
            project = str(input("What Project would you like to view?\n(0: Marsh Lea, 1: Custom Homes, 2: T. Moser Land)\n"))
            project_int = int(project)
            self.set_project_id(project_int)

        while self.__action_id is None:
            action = str(input("Would you like to see warranty or current selections?\n(0: : Reset Lot Info, 1: Selections, 2: Warranty, 3: Gather Open Warranty Items) \n"))
            action_int = int(action)
            self.set_action_id(action_int)

        if self.__project_id is not None and self.__action_id is not None:
            loop = asyncio.get_event_loop()
            if self.__action_id == 0:
                loop.run_until_complete(self.lot_reference_update())
            elif self.__action_id == 1 or self.__action_id == 2:
                loop.run_until_complete(self.lot_information_scrap())
            elif self.__action_id == 3:
                loop.run_until_complete(self.project_lot_warranty())
            loop.close()

    def set_project_id(self, project_int):
        if len(JCONFIG["projectInfo"]) >= project_int and project_int >= 0:
            self.__project_id = project_int
            self._pinfo = JCONFIG["projectInfo"][project_int]

    def set_action_id(self, action_int):
        if action_int >= 0 and action_int < 4:
            self.__action_id = action_int
    
    def set_current_lot(self, lnum):
        self.current_lot = self.get_lot_dict().get(lnum)    

    def lot_selection_check(self, lot_nums=None):
        if not self.__action_lots:
            # lnum = None
            while len(self.__action_lots) == 0:
                if lot_nums is None:
                    print("Choose from the list with ',' separated lots for multiple options")
                    print(", ".join(self.get_lot_dict().keys()))
                    lstr = str(input("What Lot numbers? \n"))
                else:
                    lstr = str(lot_nums)
                lstr = lstr.split(',')
                print(lstr)
                for lot in lstr:
                    lot = str(lot)
                    if len(lot) == 1:
                        lot = f'0{lot}'
                    if self.in_lot_dict(lot):
                        self.__action_lots.append(lot)
                    else:
                        lot_nums = None
                        print(f'Lot {lot} is not in project {"All" if self.__project_id is None else self.__project_id}')
                print(self.__action_lots)
                # lnum = lstr
        else:
            print("Lots have already been selected")
        # self.set_current_lot(lnum)

    async def project_lot_warranty(self):
        for lot in self.__action_lots:
            l = lot
        # CHANGE THE LOT QUESTION TO INCORPORATE MANY LOTS
        # get all of the lots
        # loop through lots in 

    async def lot_information_scrap(self):
        # - Default Viewport creats viewport maxmiuzzed to browser window size
        # - args [start-max..] for maximum browser size [args=['--start-maximized'],]
        self.lot_selection_check()
        await asyncio.sleep(5)
        browser = await self.moser_browser()
        page = await self.open_mosertopia_page(browser)
        for lot in self.__action_lots:
            self.set_current_lot(lot)
            if self.__action_id == 1:
                ######### OPTIONS LIST
                await self.selection_element_cycle(page, 0, file_selector="td:last-child > a")
                ########## NSO LIST
                await self.selection_element_cycle(page, 1, file_selector="td:nth-child(6) > a")                

            elif self.__action_id == 2:
                ########## Warranty Action            
                await page.goto(self.abs_path(self.current_lot["warranty_url"]))            
                warranty_info = await self.gather_warranty_info(page)
                    
        # Puppeteer is complete
        await browser.close()
        ########## EXCEL UPDATE
        self.update_lot_info_file()
        # Clean up trash
        await asyncio.sleep(4)


    async def lot_reference_update(self):
        browser = await self.moser_browser()
        page = await self.open_mosertopia_page(browser)
        await page.goto(JCONFIG["paths"]["homepage"])
        await page.waitForSelector(self._pinfo[2])
        await page.click(f'{self._pinfo[2]} > td:nth-child(4) > a')
        
        lots_el_li = await MoserStatic.get_tr_background(page)

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
            MoserStatic.generate_new_lot_excel(temp_dir)

            await asyncio.sleep(1)
                # TODO: also initialize warranty and selection xcel sheets if possible
            self.get_lot_dict()[ln] = lot_info
                #  lot_url = lot.querySelectorEval('td:nth-child(3) > a', 'node => node.getAttribute("href")')
        await page.goto("https://app.buildtopia.com/english_exec/service-owners")
        pf = 'select[name="ProjectFilter"]'
        cf = f'{pf} > [value="{self._pinfo[1]}"]'
        c = self._pinfo[1]
        print(cf)
        await page.waitForSelector(pf)
        await page.click(pf)
        await asyncio.sleep(3)
        await page.waitForSelector(cf)
        await page.select(pf, c)
        await asyncio.sleep(3)
        war_lots = await MoserStatic.get_tr_background(page)
        for war_lot in war_lots:
            ln = str(await war_lot.querySelectorEval("td:nth-child(3)", 'node => node.innerText'))
            # print(ln)
            ln = ln.strip()
            if ln in self.get_lot_dict() and self.get_lot_dict()[ln]["warranty_url"] == False:
                self.get_lot_dict()[ln]["warranty_url"] = await war_lot.Jeval('td:nth-child(1) > a', 'node => node.getAttribute("href")')
                
        await browser.close()
        self.__save_lots_data()
        await asyncio.sleep(10)


    def update_lot_info_file(self):
        lot_info = self.get_lot_directory(file_name='lot_info.xlsx')
        lot_file = openpyxl.load_workbook(lot_info)
        sheetnames = lot_file.sheetnames
        columns = string.ascii_uppercase
        len_cols = len(columns)
        for x in sheetnames:
            x = sheetnames[x].lower()
            if x in lot_file:
                currentSheet = lot_file[x]
                currentCsvFile = self.get_lot_directory(file_name=f'{x}.csv')
                if os.path.exists(currentCsvFile):
                    with open(currentCsvFile) as csvfile:
                        reader = csv.reader(csvfile)
                        row_num = 2
                        for row in reader:
                            for r in row:
                                if r <= len_cols: 
                                    cell_value = f'{columns[r]}{row_num}'
                                    currentSheet[cell_value] = row[r]
                            row_num += 1
        # get the lot csv files
        # openpxly then update each section
        # plus 1 after headers

    async def moser_browser(self):
        return await launch(headless=JCONFIG['production'], defaultViewport=None)

    async def open_mosertopia_page(self, browser):
        pages  = await browser.pages()
        page = pages[0]
        await page.goto(JCONFIG["paths"]["login"])
        await MoserStatic.pyp_signin(page, login=JCONFIG["sign_in"])
        # print("Should result to next page")
        return page

        
    def abs_path(self, url):
        return f'{JCONFIG["paths"]["base"]}{url}'

    def get_project_dict(self):
        return self.lots_data[self.__project_id]

    def get_lot_dict(self):
        return self.get_project_dict()["lots"]
        
    def in_lot_dict(self, ln):
        return ln in self.get_lot_dict()
            
    def set_lot(self, ln):
        if self.in_lot_dict():
            self.current_lot = self.get_lot_in_dict(ln)
        
    def get_lot_in_dict(self, lot):
        return self.get_lot_dict()[lot]
    
    def get_lot_directory(self, lot_str=None, file_name=None, download_path=None):
        lot_name = self.current_lot["ln"] if lot_str is None else lot_str
        a = f'{LOG_DIR}\\{self._pinfo[0]}\\{lot_name}'
        if download_path == True:
            return f'{a}\\'
        return f'{a}\\{file_name}' if file_name is not None else a

    def __save_lots_data(self):
        if self.current_lot is not None and self.__project_id is not None:
            self.lots_data[self.__project_id][self.current_lot["ln"]] = self.current_lot
        with open(f'data/lots.json', 'w') as lots:
            json.dump(self.lots_data, lots)

    
        # only if all keys are not found in lots_data


    async def gather_warranty_info(self, page):
        warranty_summary_els = await MoserStatic.get_tr_background(page)
        warranty_items = []
        if warranty_summary_els:
            warranty_groups = []
            for warranty_el in warranty_summary_els:
                summary = await warranty_el.Jeval("td:nth-child(2)", "node => node.innerText")
                summary_info = await warranty_el.Jeval("td:nth-child(1) a", '''
                    (node) => {
                        return [node.innerText, node.getAttribute("href")];
                    }
                ''')
                request_info = {
                    "summary": summary,
                    "request_url": summary_info[1],
                    "request_id": summary_info[0],
                }
                warranty_groups.append(request_info)
            
            for warranty_group in warranty_groups:
                warranty_group = warranty_groups[warranty_group]
                request_trs = await MoserStatic.get_tr_background(page, warranty_group["request_url"], .1)
                for tr in request_trs:
                    status = await tr.Jeval("td:nth-child(2)", "node => node.innerText")
                    description = await tr.Jeval("td:nth-child(3)", "node => node.innerText")
                    wi = {
                        "id": warranty_group["request_id "],
                        "status": status,
                        "summary": warranty_group["summary"],
                        "description": description,

                    }
                    if wi["is_open"]:
                        wi["edit_url"] = await tr.Jeval("td:last-child > a:nth-child(2)", 'node => node.getAttribute("href")'),
                        wi["close_url"] = await tr.Jeval("td:last-child > a:nth-child(1)", 'node => node.getAttribute("href")')
                    else:
                        wi["edit_url"] = False
                        wi["close_url"] = False

                    warranty_items.append(wi)

            warranty_csv_file = self.get_lot_directory(file_name=f'warranty.csv')
            with open(warranty_csv_file, 'w', newline='') as warranty_file:
                lot_warranty = csv.writer(warranty_file)
            
                for warranty_item in warranty_items:
                    warranty_item = warranty_items[warranty_item]
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

                        lot_warranty.write(warranty_item.values())
        else:
            print("No warranty is available for this lot")
        
        return warranty_items


    async def selection_element_cycle(self, page, hid=0, file_selector=None):
        # file_urls = {}
        sel_name = "nsos" if hid == 1 else "options" 
        url = self.current_lot["urls"][hid]
        buildtopia_url = f'{JCONFIG["paths"]["base"]}{url}'
        options_list_els = await MoserStatic.get_tr_background(page, buildtopia_url)
        completion_callback = MoserStatic.option_element_cycle if hid == 0 else MoserStatic.nso_element_cycles
        csv_file_location = self.get_lot_directory(file_name=f'{sel_name}.csv')
        # Open Excel file and get the correct selection
        with open(csv_file_location, "w", newline="") as csvfile:
            # write the file to csv without headers.
            lot_options = csv.writer(csvfile)
            for row in options_list_els:
                tds = await row.querySelectorAll("td")
                td_result = await completion_callback(page, tds)

                # Gets file page url
                
                if td_result is not None:
                    if file_selector is not None:
                        file_request = await row.querySelectorEval(file_selector, 'node => [node.innerText, node.getAttribute("href")]')
                        # print(file_request)
                        if file_request[0] != "0":
                            td_result["file_page_url"] = file_request[1]
                    lot_options.writerow(td_result.values())
                    self.current_lot[sel_name][td_result["id"]] = td_result

        
        print(f'Saved lot {sel_name} data\nNow uploading {sel_name} files...')
        ########## FILE_LIST

        for selection in self.current_lot[sel_name]:
            select_dict = self.current_lot[sel_name][selection]
            # print(selection)

            if "file_page_url" in select_dict:
                await page.goto(self.abs_path(select_dict["file_page_url"]))
                current_file_page = await MoserStatic.get_tr_background(page)
                # await page._client.send('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': self .get_lot_directory()})
                for file_item in current_file_page:
                    file_html = await file_item.J("td:nth-child(1) > a")
                    file_name = await page.evaluate('(element) => element.innerText', file_html)
                    file_name=f'{file_name}.pdf'
                    file_location = self.get_lot_directory(file_name=file_name)
                    if not os.path.exists(file_location):
                        file_url = await page.evaluate('(element) => element.getAttribute("href")', file_html)
                        print(file_name, file_url)
                        wget.download(self.abs_path(file_url), file_location)



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

    

class MoserStatic:

    @staticmethod
    def generate_new_lot_excel(temp_dir):
        selection_file = f'{temp_dir}\\lot_info.xlsx'
        if os.path.exists(selection_file):
            # Delete file first
            os.remove(selection_file)

        temp_sel_workbook = xlsxwriter.Workbook(selection_file)
        workbook_vars = {
            "lot": ["Lot Id", "Address", "Model"],
            "options": ["Id", "Name", "Description", "Selection Notes", "Quantity", "File Names"],
            "nsos": ["Id", "Accepted", "Location", "Sub Location", "Description", "File Names"],
            "warranty": ["Id", "Description", "Sub Description", "Status", "Internal Details", "Defect Code", "Defect Name"],
        }
        
        for worksheet_name, worksheet in workbook_vars.items():
            temp_worksheet = temp_sel_workbook.add_worksheet(worksheet_name.title())
            MoserStatic.xslx_write(temp_worksheet, worksheet)
            if worksheet_name == "general":
                general_info = [ln, lot_info["address"], lot_info["model"]]
                MoserStatic.xslx_write(temp_worksheet, general_info, 1)

        temp_sel_workbook.close()

    @staticmethod
    async def get_tr_background(page, url=None, wait_sec=3):
        await asyncio.sleep(wait_sec)
        if url is not None:
            await page.goto(url)
        await page.waitForSelector("tr.background")
        return await page.querySelectorAll("tr.background, tr.altbackground")

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
            await MoserStatic.pyp_signin(page, login, count)
    
    @staticmethod
    def xslx_write(wrksheet, arr, row=0):
        column = 0
        for a in arr:
            wrksheet.write(row, column, a)
            column += 1

        
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
        accepted_str = await page.evaluate('(element) => element.innerText', tds[2])
        accepted = False if accepted_str.strip() not in NSO_ACCEPTED else accepted_str.strip()
        print(accepted_str, accepted)
        if accepted:
            location = await page.evaluate('(element) => element.innerText', tds[3])
            nso_id = await page.evaluate('(element) => element.innerText', tds[1])
            info = {
                "id": nso_id.strip(),
                "accepted": accepted,
                "location": location.strip() if location != "Selections" else "NA",
            }
            desc = await page.evaluate('(element) => element.innerText', tds[4])
            item_description = desc.replace("&nbsp;", "").split("QUOTED: ")
            desc = re.split(' - |: ', item_description[0].strip().replace(u'\xa0', ''), 2)
            info['sub_location'] = False       
            if len(item_description) > 1:
                quoted = re.split(' - |: ', item_description[1].strip().replace(u'\xa0', ''), 2)
                # if len(quoted) == 3:
                #     info["category"] = quoted[0]
                if len(quoted) > 1:
                    info['sub_location'] = quoted[0]
                info["description"] = quoted[-1]
                print(quoted)
            else:
                info['description'] = desc[-1] if len(desc) > 1 else desc[0]

            print(desc)
            return info 

        return None


if __name__ == '__main__':
    Moser(sys.argv)
    # await Moser().lot_information_scrap()    
