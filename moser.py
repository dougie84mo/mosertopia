import os, sys, json, time, asyncio, re
import xlsxwriter, xlwings, openpyxl
from xlsxwriter import workbook, Workbook
from xlutils.copy import copy
from prettyprinter import cpprint, pprint
from pyppeteer import launch
import wget
import csv
import string
import datetime

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
NNI = 'node => node.innerText'
NGA_HREF = 'node => node.getAttribute("href")'
ANCHOR_ATTR = 'node => return [node.innerText, node.getAttribute("href")]'
# example = await page.evaluate(NNI, item)

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
            project = str(
                input("What Project would you like to view?\n(0: Marsh Lea, 1: Custom Homes, 2: T. Moser Land)\n"))
            project_int = int(project)
            self.set_project_id(project_int)

        while self.__action_id is None:
            action = str(input("Would you like to see warranty or current selections?\n(0: Reset Lot Info, 1: Selections, 2: Warranty, 3: Gather Open Warranty Items) \n"))
            action_int = int(action)
            self.set_action_id(action_int)

        if self.__action_id == 4:
            self.update_lot_xcel()
        elif self.__project_id is not None and self.__action_id is not None:
            loop = asyncio.get_event_loop()
            if self.__action_id == 0:
                loop.run_until_complete(self.lot_reference_update())
            elif self.__action_id == 1 or self.__action_id == 2:
                loop.run_until_complete(self.lot_information_scrap())
            elif self.__action_id == 3:
                loop.run_until_complete(self.project_lot_warranty())
            loop.close()

    async def project_lot_warranty(self):
        info = await MoserStatic.mosertopia_signin()
        self.lot_selection_check()
        lot_numbers_name = 'L'.join(self.__action_lots)
        file_name = f'warranty_{datetime.datetime.now().timestamp()}_{lot_numbers_name}'
        workbook: Workbook = xlsxwriter.Workbook(f'{LOG_DIR}\\{self._pinfo[0]}\\{file_name}')
        print("Supposed to be at login")
        if len(self.__action_lots) > 0:
            for lot in self.__action_lots:
                self.set_current_lot(lot)
                workbook = workbook.add_worksheet(lot)
                await page.goto(self.current_lot["warranty_url"])
                warranty_items = await MoserStatic.gather_warranty_info(page)
                # self.get_lot_directory(lot, 'warranty.csv')

                print(warranty_items)
                await asyncio.sleep(20)
        else:
            print('No lots were entered')
        await moser_browser.close()
        # get all of the lots
        # loop through lots in 

    '''
    Scrap the lot information and save data.
    '''

    async def lot_information_scrap(self):
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
                warranty_info = await MoserStatic.gather_warranty_info(page)

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

        lots_el_li = await self.get_tr_background(page)

        for lot in lots_el_li:
            # start writing to file data if needed
            ln = str(await lot.querySelectorEval("td:nth-child(2) > a", NNI))
            address = await lot.querySelectorEval('td:nth-child(3)', NNI)
            model_plan = await lot.querySelectorEval('td:nth-child(4)', NNI)
            plan_id = model_plan.split("ML")
            # modeL = plan_id[1].trim if len(plan_id) == 2 else plan_id[0]
            lot_url = await lot.querySelectorEval('td:nth-child(1) > a', NGA_HREF)
            nso_url = await lot.querySelectorEval('td:last-child > a:nth-child(6)', NGA_HREF)
            options_url = await lot.querySelectorEval('td:last-child > a:nth-child(4)',
                                                      NGA_HREF)

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
            #  lot_url = lot.querySelectorEval('td:nth-child(3) > a', NGA_HREF)
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
        war_lots = await self.get_tr_background(page)
        for war_lot in war_lots:
            ln = str(await war_lot.querySelectorEval("td:nth-child(3)", 'node => node.innerText'))
            # print(ln)
            ln = ln.strip()
            if ln in self.get_lot_dict() and self.get_lot_dict()[ln]["warranty_url"] is False:
                self.get_lot_dict()[ln]["warranty_url"] = await war_lot.Jeval('td:nth-child(1) > a',
                                                                              NGA_HREF)

        await browser.close()
        self.__save_lots_data()
        await asyncio.sleep(10)

    def update_lot_xcel(self):
        # Loop through every lot folder and update every
        for lot in self.__action_lots:
            self.set_current_lot(lot)
            self.update_lot_info_file()

    # NON ACTIONS

    def update_lot_info_file(self):
        lot_info = self.get_lot_directory(file_name='lot_info.xlsx')
        lot_file = openpyxl.load_workbook(lot_info)
        sheetnames = lot_file.sheetnames
        print(sheetnames)
        columns = string.ascii_uppercase
        len_cols = len(columns)
        for x in sheetnames:
            x = sheetnames[x]
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

    def abs_path(self, url):
        return f'{JCONFIG["paths"]["base"]}{url}'

    def get_project_dict(self):
        return self.lots_data[self.__project_id]

    def get_lot_dict(self):
        return self.get_project_dict()["lots"]

    def in_lot_dict(self, ln):
        return ln in self.get_lot_dict()

    def get_lot_in_dict(self, lot):
        return self.get_lot_dict()[lot]

    def set_lot(self, ln):
        if self.in_lot_dict(ln):
            self.current_lot = self.get_lot_in_dict(ln)

    def get_lot_directory(self, lot_str=None, file_name=None, download_path=None):
        lot_name = self.current_lot["ln"] if lot_str is None else lot_str
        return MoserStatic.lot_dir(self._pinfo[0], lot_name, file_name, download_path)

    def __save_lots_data(self):
        if self.current_lot is not None and self.__project_id is not None:
            self.lots_data[self.__project_id][self.current_lot["ln"]] = self.current_lot
        with open(f'data/lots.json', 'w') as lots:
            json.dump(self.lots_data, lots)

        # only if all keys are not found in lots_data

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
                        file_request = await row.querySelectorEval(file_selector,
                                                                   'node => [node.innerText, node.getAttribute("href")]')
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
                # await page._client.send('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': self
                # .get_lot_directory()})
                for file_item in current_file_page:
                    file_html = await file_item.J("td:nth-child(1) > a")
                    file_name = await page.evaluate('(element) => element.innerText', file_html)
                    file_name = f'{file_name}.pdf'
                    file_location = self.get_lot_directory(file_name=file_name)
                    if not os.path.exists(file_location):
                        file_url = await page.evaluate('(element) => element.getAttribute("href")', file_html)
                        print(file_name, file_url)
                        try:
                            wget.download(self.abs_path(file_url), file_location)
                        except Exception:
                            print(f'The file {file_url} was not able to be downloaded.')
                            print(f'Please visit url: {select_dict["file_page_url"]} to try and download the file')

    def set_project_id(self, project_int):
        if len(JCONFIG["projectInfo"]) >= project_int >= 0:
            self.__project_id = project_int
            self._pinfo = JCONFIG["projectInfo"][project_int]

    def set_action_id(self, action_int):
        if 0 <= action_int < 5:
            self.__action_id = action_int

    def set_current_lot(self, lnum):
        self.current_lot = self.get_lot_dict().get(lnum)

    def lot_selection_check(self, lot_nums=None):
        if not self.__action_lots:
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
                        print(
                            f'Lot {lot} is not in project {"All" if self.__project_id is None else self.__project_id}')
                print(self.__action_lots)
        else:
            print("Lots have already been selected")


'''
STATIC MOSER CLASS:
 - lot dir : project AND lot DIRECTORY STRING
 - gather warranty info : SNAKES THROUGH WARRANTY INFO AND RETURNS A LIST OF INFO
'''


class MoserStatic:

    @staticmethod
    def lot_dir(project_name, lot_str, file_name=None, download_path=None):
        a = f'{LOG_DIR}\\{project_name}\\{lot_str}'
        if download_path:
            return f'{a}\\'
        return f'{a}\\{file_name}' if file_name is not None else a

    @staticmethod
    async def mosertopia_browser():
        return await launch(headless=JCONFIG['production'], defaultViewport=None)

    @staticmethod
    async def mosertopia_signin(browser, count=0):
        pages = await browser.pages()
        page = pages[0]
        await page.goto(JCONFIG["paths"]["login"])
        login = JCONFIG["sign_in"]
        # print("Should result to next page")
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
            await MoserStatic.mosertopia_signin(browser, count)
        await asyncio.sleep(2)
        # news_button_str = ""
        # news_button_cont = await page.querySelector(news_button_str)
        # if news_button_cont:
        #     # firstly click through all the "Dont Ask me again buttons"
        #     await page.click(news_button_str)
        #     await asyncio.sleep(2)
        
        return page

    @staticmethod
    async def non_sync_loop(util_action):
        browser = await MoserStatic.mosertopia_browser()
        page = await MoserStatic.mosertopia_signin()
        await util_action(page)
        await browser.close()

    @staticmethod
    async def page_select(selector_id, click=None):
        if selector_id is not None:
            if click is not None and type(click) is str:
                await page.select(selector_id, click)
                return True
            else:
                options = await page.querySelectorAll(f'select#{selector_id} options')
                actual_options = {}
                for option in options:
                    item = options[option]
                    value = await page.evaluate('node => node.getAttribute("value")', item)
                    Title = await page.evaluate(NNI, item)

                return actual_options

    @staticmethod
    def choosable_str_dict(choices: dict, question: str = 'What choice do you pick?'):
        i = 0
        temp_arr = []
        for choice, rvalue in choices.items():
            print(f'[{i}]: {choice}')
            i += 1
            temp_arr.append(rvalue)
        answer = None
        while answer is None:
            response = int(input(question))
            if response <= len(temp_arr) - 1:
                answer = temp_arr[response]
            else:
                print('Choice is not available')
        return answer

    @staticmethod
    async def gather_warranty_info(page):
        warranty_summary_els = await MoserStatic.get_tr_background(page)
        warranty_items = []
        if warranty_summary_els:
            warranty_groups = []
            # Gather all 
            for warranty_el in warranty_summary_els:
                summary = await warranty_el.Jeval("td:nth-child(2)", NNI)
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
                        "id": warranty_group["request_id"],
                        "status": status,
                        "summary": warranty_group["summary"],
                        "description": description,

                    }
                    if wi["is_open"]:
                        wi["edit_url"] = await tr.Jeval("td:last-child > a:nth-child(2)", NGA_HREF),
                        wi["close_url"] = await tr.Jeval("td:last-child > a:nth-child(1)", NGA_HREF)
                    else:
                        wi["edit_url"] = False
                        wi["close_url"] = False

                    warranty_items.append(wi)


        else:
            print("No warranty is available for this lot")

        return warranty_items



    @staticmethod
    async def warranty_csv(page, warranty_items, lot_dir):
        warranty_csv_file = lot_dir
        with open(warranty_csv_file, 'w', newline='') as warranty_file:
            lot_warranty = csv.writer(warranty_file)

            for warranty_item in warranty_items:
                warranty_item = warranty_items[warranty_item]
                if "urls" in warranty_item:
                    await page.goto(warranty_item["urls"])
                    await page.waitForSelector("#middle_left")
                    sub_info_rows = await page.querySelectorAll("#middle_left > table:nth-child(1) > tbody > tr")
                    warranty_item["internal_details"] = await sub_info_rows[1].Jeval("td:nth-child(2) > textarea", NNI)
                    # tr:nth-child(2) > td:nth-child(2) > textarea
                    defective_group = await sub_info_rows[5].Jeval('td:nth-child(6) > option[selected="selected"]', NNI)
                    defective_group = defective_group.split(' ', 1)
                    warranty_item["defect_group_name"] = defective_group[1]
                    warranty_item["defect_code"] = defective_group[0]

                    lot_warranty.write(warranty_item.values())



    @staticmethod
    def generate_new_lot_excel(temp_dir, ln, lot_info):
        selection_file = f'{temp_dir}\\lot_info.xlsx'
        if os.path.exists(selection_file):
            # Delete file first
            os.remove(selection_file)

        temp_sel_workbook = xlsxwriter.Workbook(selection_file)
        workbook_vars = {
            "lot": ["Lot Id", "Address", "Model"],
            "options": ["Id", "Name", "Description", "Selection Notes", "Quantity", "File Names"],
            "nsos": ["Id", "Accepted", "Location", "Sub Location", "Description", "File Names"],
            "warranty": ["Id", "Description", "Sub Description", "Status", "Internal Details", "Defect Code",
                         "Defect Name"],
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
    def xslx_write(wrksheet, arr, row=0):
        column = 0
        for a in arr:
            wrksheet.write(row, column, a)
            column += 1

    @staticmethod
    async def option_element_cycle(page, tds):
        option_id = await page.evaluate(NNI, tds[1])
        option_code_split = option_id.strip().split(" ", 1)
        description = await page.evaluate(NNI, tds[2])
        selection_notes = await page.evaluate(NNI, tds[3])
        quantity = await page.evaluate(NNI, tds[4])
        return {
            "id": option_code_split[0],
            "name": option_code_split[1],
            "description": description.strip(),
            "selection_notes": selection_notes.strip(),
            "quantity": quantity.strip(),
        }

    @staticmethod
    async def nso_element_cycles(page, tds):
        accepted_str = await page.evaluate(NNI, tds[2])
        accepted = False if accepted_str.strip() not in NSO_ACCEPTED else accepted_str.strip()
        # print(accepted_str, accepted)
        if accepted:
            location = await page.evaluate(NNI, tds[3])
            nso_id = await page.evaluate(NNI, tds[1])
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
                if len(quoted) > 1:
                    info['sub_location'] = quoted[0]
                info["description"] = quoted[-1]
                # print(quoted)
            else:
                info['description'] = desc[-1] if len(desc) > 1 else desc[0]

            # print(desc)
            return info

        return None

    @staticmethod
    async def possible_warranty_contact_info(page, info_table_selector):
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


if __name__ == '__main__':
    Moser(sys.argv)
    # await Moser().lot_information_scrap()
