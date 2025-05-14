# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/utage_csv_to_gss/installer/src"
# export PYTHONPATH="/Users/nyanyacyan/Desktop/Project_file/utage_csv_to_drive/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from typing import List
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
from method.get_gss_df_flow import GetGssDfFlow

# const
from method.const_element import GssInfo, LoginInfo, ErrCommentInfo, PopUpComment, Element, CommentFlowElement

deco = Decorators()

# ----------------------------------------------------------------------------------
# **********************************************************************************
# 一連の流れ


class CommentFlow:
    def __init__(self, chrome: WebDriver):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # chrome
        self.chrome = chrome

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
        self.const_comment = CommentFlowElement.INSTA.value


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
        self.get_gss_df_flow = GetGssDfFlow()

    ####################################################################################
    #! ----------------------------------------------------------------------------------
    # 書込データをスプシに書き込む

    def process(self, search_username: str, target_worksheet_name: str):
        try:
            # 書込データを取得
            filtered_write_data, target_df = self._get_filtered_write_data(search_username=search_username, target_worksheet_name=target_worksheet_name)

            if not filtered_write_data:
                return

            None_row_num = len(target_df) + 1
            self.logger.debug(f"\nユーザー名: {search_username}\nWS: {target_worksheet_name}\n書込データの行数: {None_row_num}")

            for data in filtered_write_data:
                self.logger.debug(f"書込データ: {data}")

                # 辞書データをリストに変換
                write_data_list = list(data.values())
                self.logger.debug(f"書込データリスト: {write_data_list}")

                cell = f"A{None_row_num}"
                self.logger.debug(f"書込データ: {data} を {target_worksheet_name} の {cell} 行目に書き込みます。")

                # 書込データのインデックスを取得
                self.gss_write.write_data_by_url( gss_info=self.const_gss_info, cell=cell, input_data=write_data_list )
                self.logger.debug(f"書込データ: {data} を {target_worksheet_name} の {cell} 行目に書き込みました。")

                None_row_num += 1
                self.logger.debug(f"次の書込データの行数: {None_row_num}")

            self.logger.info(f"コメントユーザーをスプシに書込完了（全{len(filtered_write_data)}行）")
            return

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)
            self.chrome.quit()
            self.popup.popupCommentOnly( popupTitle=self.const_err_cmt_dict["POPUP_TITLE_SHEET_INPUT_ERR"], comment=self.const_err_cmt_dict["POPUP_TITLE_SHEET_CHECK"], )

    #! ----------------------------------------------------------------------------------
    # 既存のユーザー名を取得し、書込データをフィルタリングする

    def _get_filtered_write_data(self, search_username: str, target_worksheet_name: str):
        try:
            write_data = self._generate_write_data(search_username)

            # 書込データがなかった場合にはNoneを返す
            if not write_data:
                return [], None

            existing_username_list, target_df = self._get_written_username_list(target_worksheet_name=target_worksheet_name)

            filtered_write_data = [
                data for data in write_data if data['username'] not in existing_username_list
            ]

            self.logger.debug(f"フィルタリング後の書込データ: {filtered_write_data}")
            return filtered_write_data, target_df

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)
            self.chrome.quit()
            self.popup.popupCommentOnly( popupTitle=self.const_err_cmt_dict["POPUP_TITLE_SHEET_INPUT_ERR"], comment=self.const_err_cmt_dict["POPUP_TITLE_SHEET_CHECK"], )


    # ----------------------------------------------------------------------------------

    def _get_written_username_list(self, target_worksheet_name: str):
        try:
            # 対象のWorksheetの現在のDataFrameを取得
            target_df = self.get_gss_df_flow.process(worksheet_name=target_worksheet_name)
            self.logger.debug(f"{target_worksheet_name}の入力前df: {target_df.head()}")

            # DataFrameが空か確認（空ならNoneで返す）
            if target_df is None or target_df.empty:
                self.logger.debug(f"{target_worksheet_name} のデータが空のため、処理をスキップします。")
                return None, None

            username_series = target_df[self.const_comment['TARGET_INPUT_USERNAME']]
            self.logger.debug(f"ユーザー名のSeries: {username_series}")

            # シリーズの値をリストに変換
            existing_username_list = username_series.tolist()
            self.logger.debug(f"ユーザー名のリスト: {existing_username_list}")

            return existing_username_list, target_df

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)
            self.chrome.quit()
            self.popup.popupCommentOnly( popupTitle=self.const_err_cmt_dict["POPUP_TITLE_SHEET_INPUT_ERR"], comment=self.const_err_cmt_dict["POPUP_TITLE_SHEET_CHECK"], )

    # ----------------------------------------------------------------------------------
    # 各メソッドをまとめる

    def _generate_write_data(self, search_username: str) -> List[dict]:
        try:
            # コメントユーザー要素のリストを取得
            comment_elements = self._get_comment_elements()

            if not comment_elements:
                return []

            # 重複を除外する
            unique_checker = set()
            write_data = []
            for i, element in enumerate(comment_elements):
                # ユーザーURLを取得
                user_url =self._get_comment_user_url(comment_element=element, element_num=i + 1)

                # InstagramのユーザーURLからユーザー名を取得
                comment_username = self._get_comment_user_name(user_url=user_url)

                comment_dict_data = {
                    "username": comment_username,
                    "user_url": user_url,
                    "like_or_comment": self.const_comment['INPUT_WORD_COMMENT'],
                    "timestamp": self.timestamp,
                }

                # 重複を除外する
                if comment_username not in unique_checker:
                    unique_checker.add(comment_username)

                    # コメントデータをリストに追加
                    write_data.append(comment_dict_data)
                else:
                    # 重複している場合は、スキップする
                    self.logger.debug(f"重複ユーザー名: {comment_username} はスキップされました。")

            self.logger.debug(f"書込データ: {write_data}")
            return write_data

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)
            self.chrome.quit()
            self.popup.popupCommentOnly( popupTitle=self.const_err_cmt_dict["POPUP_TITLE_SHEET_INPUT_ERR"], comment=self.const_err_cmt_dict["POPUP_TITLE_SHEET_CHECK"], )

    # ----------------------------------------------------------------------------------
    # コメントユーザー要素のリストを取得する
    #TODO 正しく取得できてない

    def _get_comment_elements(self):
        try:
            # self.logger.info(self.chrome.page_source)
            self.get_element.unlockDisplayNone()

            # コメント要素を取得
            ul_elements = self.get_element.getElements(by=self.const_element['by_12'], value=self.const_element['value_12'])
            self.logger.debug(f"ul要素の数: {len(ul_elements)}\n{ul_elements}")

            user_url_list = []
            for ul in ul_elements:
                self.logger.debug(f"ul要素: {ul}")
                self.logger.debug(f"ul要素のテキスト: {ul.text}")


                true_li_elements = []
                li_elements = self.get_element.filterElements(parentElement=ul,by=self.const_element['by_13'], value=self.const_element['value_13'])
                for li in li_elements:
                    self.logger.debug(f"li要素: {li}")
                    self.logger.debug(f"li要素のテキスト: {li.text}")

                    li_text = li.text
                    if ("週間前" in li_text or "時間前" in li_text) and "返信" in li_text:
                        true_li_elements.append(li)

                for l in true_li_elements:
                    a_elements = self.get_element.filterElements(parentElement=l,by=self.const_element['by_13'], value=self.const_element['value_15'])

                    for a in a_elements:
                        self.logger.debug(f"a要素: {a}")
                        self.logger.debug(f"a要素のテキスト: {a.text}")
                        user_url = a.get_attribute('href')
                        user_url_list.append(user_url)
                        self.logger.debug(f"ユーザーURL: {user_url}")

            for user_url in user_url_list:
                self.logger.debug(f"ユーザーURL: {user_url}")
            self.logger.debug(f"ユーザーURLリスト: {user_url_list}")

            filter_user_url = list({url for url in user_url_list if "/c/" not in url})

            for user_url in filter_user_url:
                self.logger.debug(f"ユーザーURL: {user_url}")
            self.logger.debug(f"フィルタリング後のユーザーURLリスト: {filter_user_url} {len(filter_user_url)}件")

            if not ul_elements:
                self.logger.warning("コメント要素が見つかりませんでした。")
                return []

            self.logger.debug(f"コメントユーザー要素の数: {len(comment_elements)}\n{comment_elements}")

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} コメントがありません {e}" )
            self.logger.error(process_error_comment)

        return filter_user_url

    # ----------------------------------------------------------------------------------
    # コメント要素からユーザー名を取得する

    def _get_comment_user_url(self, comment_element: WebElement, element_num: int):
        self.logger.debug(f"コメント要素: {comment_element}")
        self.logger.debug(f"コメント要素のインデックス: {element_num}")
        # ユーザー名を取得
        comment_a_tag = comment_element.find_element(By.XPATH, f'//a[contains(@href, "/") and @role="link"]')
        user_url = comment_a_tag.get_attribute('href')
        self.logger.debug(f"ユーザーURL: {user_url}")

        return user_url

    # ----------------------------------------------------------------------------------
    # InstagramのユーザーURLからユーザー名を取得する

    def _get_comment_user_name(self, user_url: str):
        # URL部分を除去してユーザー名を取得
        username = user_url.replace("https://www.instagram.com/", "").strip("/")
        self.logger.debug(f"ユーザー名: {username}")
        return username

    # ----------------------------------------------------------------------------------

