# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/utage_csv_to_gss/installer/src"
# export PYTHONPATH="/Users/nyanyacyan/Desktop/Project_file/utage_csv_to_drive/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from datetime import datetime

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

# const
from method.const_element import GssInfo, LoginInfo, ErrCommentInfo, PopUpComment

deco = Decorators()

# ----------------------------------------------------------------------------------
# **********************************************************************************
# 一連の流れ


class GetGssDfFlow:
    def __init__(self):
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
        self.const_gss_info = GssInfo.UTAGE.value
        self.const_login_info = LoginInfo.UTAGE.value
        self.const_err_cmt_dict = ErrCommentInfo.UTAGE.value
        self.popup_cmt = PopUpComment.UTAGE.value


    ####################################################################################
    # ----------------------------------------------------------------------------------
    # 各メソッドをまとめる

    def process(self):
        try:
            # スプシにアクセス（Worksheet指定）
            df = self.gss_read._get_df_gss_url(gss_info=self.const_gss_info)
            df_filtered = df[df["チェック"] == "TRUE"]

            df_filtered.empty
            if df_filtered.empty:
                self.logger.error("チェック項目がある項目がありません")
                raise

            self.logger.debug(f'DataFrame: {df_filtered.head()}')

            # 上記URLからWorksheetを取得
            existing_titles = self.gss_read._get_all_worksheet(gss_info=self.const_gss_info)
            self.logger.debug(f'既存Worksheet一覧: {existing_titles}')

            return df_filtered

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)
            self.chrome.quit()
            self.popup.popupCommentOnly( popupTitle=self.const_err_cmt_dict["POPUP_TITLE_SHEET_INPUT_ERR"], comment=self.const_err_cmt_dict["POPUP_TITLE_SHEET_CHECK"], )


    # ----------------------------------------------------------------------------------
