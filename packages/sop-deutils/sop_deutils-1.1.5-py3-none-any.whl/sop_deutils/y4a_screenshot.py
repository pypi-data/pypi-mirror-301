from playwright.sync_api import sync_playwright
from .gg_api.y4a_drive import upload_file_to_gdrive
from .y4a_retry import retry_on_error
import time  


import logging
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

class ScreenshotService:
    '''
        Use for screenshot dashboard
    '''
    def __init__(self, acc_name, acc_password, creds_ggdrive, parent_directory_id, executable_path, path_file):
        self.__acc_name = acc_name
        self.__acc_password = acc_password
        self.__creds_ggdrive = creds_ggdrive
        self.__parent_directory_id = parent_directory_id
        self.__executable_path = executable_path
        self.__path_file = path_file

    def declare_dashboard_info(self, report_id, app_id, ctid, page_name, height, width):
        self.__report_id = report_id
        self.__app_id = app_id
        self.__ctid = ctid
        self.__page_name = page_name
        self.__height = height
        self.__width = width


    @retry_on_error(delay=20)
    def screenshot_dashboard_get_image_link(self) -> str:
        file_name = self.__run_screenshot() 
        gg_drive_file = upload_file_to_gdrive("GGChatBotImage", self.__parent_directory_id, self.__creds_ggdrive, self.__path_file,file_name)

        return gg_drive_file

    def __run_screenshot(self):
        with sync_playwright() as playwright:
            dashboard_url = f'https://app.powerbi.com/reportEmbed?reportId={self.__report_id}&appId={self.__app_id}&autoAuth=true&ctid={self.__ctid}&pageName={self.__page_name}'
            
            return self.__screenshot(playwright, dashboard_url)

    def __screenshot(self, playwright, url):
        logging.info("-------start screenshot")

        # step 1: go to page and wait
        logging.info("-------waiting")

        browser = playwright.chromium.launch(executable_path=self.__executable_path)
        page = browser.new_page()
        page.set_viewport_size({"width": self.__width, "height": self.__height})
        page.goto(url)
        page.wait_for_selector('input[name="loginfmt"]')
        page.wait_for_timeout(1500)

        # step 2: input the login account
        input_selector = 'input[name="loginfmt"]'
        page.fill(input_selector, self.__acc_name)
        button_id = 'idSIButton9'
        page.click(f'#{button_id}')
        page.wait_for_timeout(1500)

        
        # step 3: input the password account
        page.wait_for_selector('input[name="passwd"]')
        input_selector_pass = 'input[name="passwd"]'
        page.fill(input_selector_pass, self.__acc_password)
        button_id = 'idSIButton9'
        page.click(f'#{button_id}')
        page.wait_for_timeout(1500)

        # step 4: confirm no
        page.wait_for_selector('#idBtn_Back')
        button_id = 'idBtn_Back'
        page.click(f'#{button_id}')
        page.wait_for_timeout(1500) 

        # step 5: hidden filter
        page.wait_for_selector('.btn.collapseIcon.pbi-borderless-button.glyphicon.glyph-mini.pbi-glyph-doublechevronright')
        page.evaluate("() => { const element = document.querySelector('[data-automation-type=\"outspacePane\"]'); if (element) element.style.display = 'none'; }")

        # step 6: final
        page.wait_for_timeout(10000)
        nano_time = time.time_ns() 
        file_name = f'ss_img_{nano_time}.png'
        page.screenshot(path=f'{self.__path_file}{file_name}')

        # always close the browser
        page.close()
        browser.close()
        logging.info("-------done")

        return file_name
