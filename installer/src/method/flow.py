# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/ccx_csv_to_drive/installer/src"
# export PYTHONPATH="/Users/nyanyacyan/Desktop/Project_file/instagram_list_tool/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os, time
import pandas as pd
import concurrent.futures
from typing import Dict
from datetime import datetime, date, timedelta

# 自作モジュール
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
from method.const_element import (
    GssInfo,
    LoginInfo,
    ErrCommentInfo,
    PopUpComment,
    Element,
)

deco = Decorators()

# ----------------------------------------------------------------------------------

# **********************************************************************************
# 一連の流れ


class SingleProcess:
    def __init__(self):
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()
        self.timestamp = datetime.now()
        self.timestamp_two = self.timestamp.strftime("%Y-%m-%d %H:%M")
        self.date_only_stamp = self.timestamp.date().strftime("%m月%d日")

        # const
        self.const_gss_info = GssInfo.INSTA.value
        self.const_login_info = LoginInfo.INSTA.value
        self.const_element = Element.INSTA.value
        self.const_err_cmt_dict = ErrCommentInfo.INSTA.value
        self.popup_cmt = PopUpComment.INSTA.value

        # Flow
        self.get_gss_df_flow = GetGssDfFlow()

    # **********************************************************************************
    # ----------------------------------------------------------------------------------

    def _single_process( self, gss_row_data: Dict, gss_info: Dict, complete_cell: str, err_datetime_cell: str, err_cmt_cell: str, login_info: Dict, ):
        """各プロセスを実行する"""

        # ✅ Chrome の起動をここで行う
        self.chromeManager = ChromeManager()
        self.chrome = self.chromeManager.flowSetupChrome()

        try:
            # インスタンスの作成 (chrome を引数に渡す)
            self.login = SingleSiteIDLogin(chrome=self.chrome)
            self.random_sleep = SeleniumBasicOperations(chrome=self.chrome)
            self.get_element = GetElement(chrome=self.chrome)
            self.selenium = SeleniumBasicOperations(chrome=self.chrome)
            self.gss_read = GetDataGSSAPI()
            self.gss_write = GssWrite()
            self.drive_download = GoogleDriveDownload()
            self.drive_upload = GoogleDriveUpload()
            self.select_cell = GssSelectCell()
            self.gss_check_err_write = GssCheckerErrWrite()
            self.popup = Popup()
            self.click_element = ClickElement(chrome=self.chrome)
            self.file_move = FileMove()



            #* 今回はログインあとのフロートする
            #TODO GSSよりデータ取得→dfを作成
            df = self.get_gss_df_flow.process()

            #TODO ログイン
            self.login.flowLoginID( login_info=self.const_login_info, )
            self.random_sleep._random_sleep(5, 10)

            #TODO 対象のページが開いているかどうかを確認

            #TODO ターゲットユーザーのURLリストを下に下記のフローを回す
            for index, row in df.iterrows():
                row_dict = row.to_dict()
                self.logger.debug(f"row_dict: {row_dict}")

                target_user_url = row_dict[self.const_gss_info["TARGET_USER_URL"]]
                start_daytime = row_dict[self.const_gss_info["START_DAYTIME"]]
                end_daytime = row_dict[self.const_gss_info["END_DAYTIME"]]
                running_date = row_dict[self.const_gss_info["RUNNING_DATE"]]
                write_error = row_dict[self.const_gss_info["WRITE_ERROR"]]

                self.logger.debug(f"\ntarget_user_url: {target_user_url}\nstart_daytime: {start_daytime}\nend_daytime: {end_daytime}\nrunning_date: {running_date}\nwrite_error: {write_error}")

                #TODO 新しいタブを開いてURLにアクセス
                self.chrome.execute_script("window.open('');")
                self.chrome.switch_to.window(self.chrome.window_handles[-1])
                self.chrome.get(target_user_url)
                self.random_sleep._random_sleep(5, 10)
                self.logger.debug(f"URLにアクセス: {target_user_url}")
                self.logger.debug(f"タブの数: {len(self.chrome.window_handles)}")

                #TODO ピン留めされた投稿数を取得
                pin_count = self.get_element.getElements(by=self.const_element['by_3'], value=self.const_element['value_3'])
                self.logger.debug(f"【{index}つ目】ピン留めされた投稿数: {pin_count}")

                #TODO 最初の投稿をクリック
                self.get_element.clickElement(by=self.const_element['by_3'], value=self.const_element['value_3'])
                self.random_sleep._random_sleep(5, 10)

                #TODO 日付を取得する
                post_date = self.get_element._get_attribute_to_element(by=self.const_element['by_4'], value=self.const_element['value_4'], attribute_value='datetime')
                self.logger.debug(f"投稿日時: {post_date}")
                self.logger.debug(f"投稿日時の型: {type(post_date)}")

                #TODO post_date投稿日時をdatetime型に変換
                post_date = datetime.strptime(post_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                self.logger.debug(f"投稿日時の型: {type(post_date)}")

                #TODO start_daytimeとend_daytimeの差分（取得したい日付リスト生成）
                start_daytime = datetime.strptime(start_daytime, "%Y-%m-%d %H:%M")
                end_daytime = datetime.strptime(end_daytime, "%Y-%m-%d %H:%M")
                self.logger.debug(f"start_daytime: {start_daytime}")
                self.logger.debug(f"end_daytime: {end_daytime}")

                #TODO 日付突合
                if start_daytime <= post_date <= end_daytime:
                    self.logger.debug(f"日付チェックOK: {post_date}")

                    

                    #TODO 日付チェックOKフローの実行→取得したデータをGSSに書き込む
                    self.gss_write.write_data_by_url( gss_info=gss_info, cell=complete_cell, input_data=self.timestamp_two )

                    #TODO 書き込みエラーのフラグを立てる
                    self.gss_write.write_data_by_url( gss_info=gss_info, cell=write_error, input_data="NG" )

                else:
                    self.logger.debug(f"日付チェックNG: {post_date}")


                #TODO 日付チェックOKフローの実行→取得したデータをGSSに書き込む

                #TODO 日付チェックNGフローの実行

                #TODO 対象のタブを閉じる（close）

            # コメントされている人のユーザー名を取得

        except TimeoutError:
            timeout_comment = "タイムエラー：ログインに失敗している可能性があります。"
            self.logger.error(f"{self.__class__.__name__} {timeout_comment}")
            # エラータイムスタンプ
            self.gss_write.write_data_by_url( gss_info=gss_info, cell=err_datetime_cell, input_data=self.timestamp )

            # エラーコメント
            self.gss_write.write_data_by_url( gss_info=gss_info, cell=err_cmt_cell, input_data=timeout_comment )

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)

            # エラータイムスタンプ
            self.logger.debug(f"self.timestamp: {self.timestamp}")
            self.gss_write.write_data_by_url( gss_info=gss_info, cell=err_datetime_cell, input_data=self.timestamp_two )

            # エラーコメント
            self.gss_write.write_data_by_url( gss_info=gss_info, cell=err_cmt_cell, input_data=process_error_comment )

        finally:
            delete_count = 0
            for upload_path in upload_path_list:
                self._delete_file(upload_path)  # CSVファイルを消去
                delete_count += 1
                self.logger.info(f"{delete_count} つ目のCSVファイルの削除を実施")

            # ✅ Chrome を終了
            self.chrome.quit()

    # ----------------------------------------------------------------------------------

    def _delete_file(self, file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
            self.logger.info(f"指定のファイルの削除を実施: {file_path}")

        else:
            self.logger.error( f"{self.__class__.__name__} ファイルが存在しません: {file_path}" )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# テスト実施

if __name__ == "__main__":

    test_flow = SingleProcess()
    # 引数入力
    test_flow._single_process()
