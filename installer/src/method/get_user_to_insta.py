# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/utage_csv_to_gss/installer/src"
# export PYTHONPATH="/Users/nyanyacyan/Desktop/Project_file/utage_csv_to_drive/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time
from datetime import datetime
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

# 自作モジュール
from method.base.utils.logger import Logger
from method.base.spreadsheet.spreadsheetRead import GetDataGSSAPI
from method.base.decorators.decorators import Decorators
from method.base.utils.time_manager import TimeManager
from method.base.selenium.google_drive_download import GoogleDriveDownload
from method.base.spreadsheet.spreadsheetWrite import GssWrite
from method.base.spreadsheet.select_cell import GssSelectCell
from method.base.spreadsheet.err_checker_write import GssCheckerErrWrite
from method.base.utils.popup import Popup
from method.base.utils.logger import Logger
from method.base.selenium.chrome import ChromeManager
from method.base.selenium.loginWithId import SingleSiteIDLogin
from method.base.selenium.seleniumBase import SeleniumBasicOperations
from method.base.spreadsheet.spreadsheetRead import GetDataGSSAPI
from method.base.selenium.get_element import GetElement
from method.base.decorators.decorators import Decorators
from method.base.utils.time_manager import TimeManager
from method.base.selenium.google_drive_download import GoogleDriveDownload
from method.base.spreadsheet.spreadsheetWrite import GssWrite
from method.base.spreadsheet.select_cell import GssSelectCell
from method.base.spreadsheet.err_checker_write import GssCheckerErrWrite
from method.base.selenium.loginWithId import SingleSiteIDLogin
from method.base.utils.popup import Popup
from method.base.selenium.click_element import ClickElement
from method.base.utils.file_move import FileMove
from method.base.selenium.google_drive_upload import GoogleDriveUpload

# const
from method.const_element import GssInfo, LoginInfo, ErrCommentInfo, PopUpComment, Element

deco = Decorators()

# ----------------------------------------------------------------------------------
# **********************************************************************************
# 一連の流れ


class GetUserToInsta:
    def __init__(self, chrome: WebDriver):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.time_manager = TimeManager()
        self.gss_read = GetDataGSSAPI()
        self.gss_write = GssWrite()
        self.drive_download = GoogleDriveDownload()
        self.select_cell = GssSelectCell()
        self.gss_check_err_write = GssCheckerErrWrite()
        self.popup = Popup()


        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        # const
        self.const_gss_info = GssInfo.INSTA.value
        self.const_login_info = LoginInfo.INSTA.value
        self.const_err_cmt_dict = ErrCommentInfo.INSTA.value
        self.popup_cmt = PopUpComment.INSTA.value
        self.const_element = Element.INSTA.value

        self.login = SingleSiteIDLogin(chrome=chrome)
        self.random_sleep = SeleniumBasicOperations(chrome=chrome)
        self.get_element = GetElement(chrome=chrome)
        self.selenium = SeleniumBasicOperations(chrome=chrome)
        self.gss_read = GetDataGSSAPI()
        self.gss_write = GssWrite()
        self.drive_download = GoogleDriveDownload()
        self.drive_upload = GoogleDriveUpload()
        self.select_cell = GssSelectCell()
        self.gss_check_err_write = GssCheckerErrWrite()
        self.popup = Popup()
        self.click_element = ClickElement(chrome=chrome)
        self.file_move = FileMove()

    ####################################################################################
    # ----------------------------------------------------------------------------------
    # 各メソッドをまとめる

    def process(self):
        try:
            # いいねをクリック
            self.get_element.clickElement(by=self.const_element['by_5'], value=self.const_element['value_5'])

            # いいねのリストを取得
            modal_element = self.get_element.getElement(value=self.const_element['value_6'])

            # user_urlとnameを取得
            all_usernames, all_user_url = self._get_usernames_from_modal(modal_element=modal_element)

            return all_usernames, all_user_url

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)
            self.chrome.quit()
            self.popup.popupCommentOnly( popupTitle=self.const_err_cmt_dict["POPUP_TITLE_SHEET_INPUT_ERR"], comment=self.const_err_cmt_dict["POPUP_TITLE_SHEET_CHECK"], )


    # ----------------------------------------------------------------------------------

    def _get_usernames_from_modal(self, modal_element: WebElement, scroll_step: int =300, max_user_count: int = 10000) -> list:
        # set()は{}にどんどん入れ込む→同じものは入れない
        seen_users = set()
        all_usernames = []
        all_user_url = []

        # 初期位置
        scroll_position = 0
        # スクロール対象のモーダルエリア（適宜クラス指定などで調整）
        while len(all_usernames) < max_user_count:
            # a_tags = modal_element.find_elements(By.XPATH, './/a[starts-with(@href, "/") and string-length(@href) > 1]')
            a_tags = self.get_element.filterElement(parentElement=modal_element, value='.//a[starts-with(@href, "/") and string-length(@href) > 1]')

            for a in a_tags:
                href = a.get_attribute("href")
                if (
                    href and
                    href.startswith("https://www.instagram.com/") and
                    href not in seen_users
                ):
                    # 被らないようにするために追加
                    seen_users.add(href)
                    all_user_url.append(href)
                    username = href.replace("https://www.instagram.com/", "").strip("/")
                    all_usernames.append(username)

                    if len(all_usernames) >= max_user_count:
                        break

            # スクロールを小刻みに行う
            scroll_position += scroll_step
            self.logger.debug(f"スクロール位置: {scroll_position}")
            self.logger.debug(f"取得したユーザー名: {all_usernames} 合計: {len(set(all_usernames))}件")
            self.chrome.execute_script("arguments[0].scrollTop = arguments[1]", modal_element, scroll_position)
            time.sleep(1)

            # すでに全て読み込み終わっていた場合のブレーク条件
            current_height = self.chrome.execute_script("return arguments[0].scrollHeight", modal_element)
            if scroll_position >= current_height:
                break

        # スクロールが完了したら、全てのユーザー名を返す
        self.logger.debug(f"最終的に取得したユーザー名: {all_usernames} 合計: {len(set(all_usernames))}件")
        self.logger.debug(f"すべてのユーザーURL: {all_user_url} 合計: {len(all_user_url)}")
        return all_usernames, all_user_url

    # ----------------------------------------------------------------------------------
