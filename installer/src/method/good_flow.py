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
from method.get_gss_df_flow import GetGssDfFlow

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
    # スプシに書き込む

    # ----------------------------------------------------------------------------------
    # 既存ユーザーと重複確認

    # ----------------------------------------------------------------------------------
    # DataFrameにあるユーザー名を取得する

    # ----------------------------------------------------------------------------------
    # DataFrameを取得する

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
    # 書込データをスプシに書き込む

    def process(self, target_worksheet_name: str):
        try:
            # 書込データを取得
            filtered_write_data, target_df = self._get_filtered_write_data(target_worksheet_name=target_worksheet_name)

            None_row_num = len(target_df) + 1

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
            return filtered_write_data

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)
            self.chrome.quit()
            self.popup.popupCommentOnly( popupTitle=self.const_err_cmt_dict["POPUP_TITLE_SHEET_INPUT_ERR"], comment=self.const_err_cmt_dict["POPUP_TITLE_SHEET_CHECK"], )

    #! ----------------------------------------------------------------------------------
    # 既存のユーザー名を取得し、書込データをフィルタリングする

    def _get_filtered_write_data(self, target_worksheet_name: str):
        try:
            write_data = self._generate_write_data()

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
    # いいねのユーザーデータを作成する

    def _generate_write_data(self):
        try:
            # モーダルを取得
            modal_element = self._get_modal_element()

            # いいねユーザー要素のリストを取得
            good_elements = self._get_good_elements(modal_element=modal_element)

            # 重複を除外する
            unique_checker = set()
            write_data = []
            for i, element in enumerate(good_elements):
                # ユーザーURLを取得
                user_url =self._get_good_user_url(good_element=element)

                # InstagramのユーザーURLからユーザー名を取得
                username = self._get_good_user_name(user_url=user_url)

                good_dict_data = {
                    "username": username,
                    "user_url": user_url,
                    "like_or_comment": self.self.const_comment['INPUT_WORD_GOOD'],
                    "timestamp": self.timestamp,
                }

                # 重複を除外する
                if username not in unique_checker:
                    unique_checker.add(username)

                    # コメントデータをリストに追加
                    write_data.append(good_dict_data)
                else:
                    # 重複している場合は、スキップする
                    self.logger.debug(f"重複ユーザー名: {username} はスキップされました。")

            self.logger.debug(f"書込データ: {write_data}")
            return write_data

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)
            self.chrome.quit()
            self.popup.popupCommentOnly( popupTitle=self.const_err_cmt_dict["POPUP_TITLE_SHEET_INPUT_ERR"], comment=self.const_err_cmt_dict["POPUP_TITLE_SHEET_CHECK"], )

    # ----------------------------------------------------------------------------------
    # コメント要素からユーザー名を取得する

    def _get_good_user_url(self, good_element: WebElement, element_num: int):
        self.logger.debug(f"コメント要素: {good_element}")
        self.logger.debug(f"コメント要素のインデックス: {element_num}")
        # ユーザー名を取得
        # comment_a_tag = good_element.find_element(By.XPATH, f'//a[contains(@href, "/") and @role="link"]')

        user_url = good_element.get_attribute('href')
        self.logger.debug(f"ユーザーURL: {user_url}")

        return user_url

    # ----------------------------------------------------------------------------------
    # InstagramのユーザーURLからユーザー名を取得する

    def _get_good_user_name(self, good_user_url: str):
        # URL部分を除去してユーザー名を取得
        username = good_user_url.replace("https://www.instagram.com/", "").strip("/")
        self.logger.debug(f"ユーザー名: {username}")
        return username

    # ----------------------------------------------------------------------------------
    # ユーザー要素を取得

    def _get_good_elements(self, modal_element: WebElement):
        good_elements = self.get_element.filterElements(parentElement=modal_element, value=self.const_element['value_11'])
        self.logger.debug(f"いいねのユーザー要素のリスト: {good_elements}")
        return good_elements


    # ----------------------------------------------------------------------------------
    # modalを取得

    def _get_modal_element(self) -> WebElement:
        # モーダルの要素を取得
        modal_element = self.get_element.getElement(value=self.const_element['value_9'])
        self.logger.debug(f"モーダル要素: {modal_element}")
        return modal_element

    # ----------------------------------------------------------------------------------
