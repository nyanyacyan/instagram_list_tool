#  coding: utf-8
# 文字列をすべてここに保管する
# ----------------------------------------------------------------------------------
# 2024/7/17 更新
# tree -I 'venv|resultOutput|__pycache__'
# ? Command + F10で大文字変換
# ----------------------------------------------------------------------------------
# import
import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()


# ----------------------------------------------------------------------------------
# GSS情報


class GssInfo(Enum):

    INSTA = {
        "JSON_KEY_NAME": "sns-auto-430920-08274ad68b41.json",
        "SHEET_URL": "https://docs.google.com/spreadsheets/d/1dghp-9A1vd9WZbybka-2MmrV2-rpm-7wwsI-tRp9jYM/edit?gid=675546558#gid=675546558",
        "WORKSHEET_NAME": "アカウント",

        # column名
        "URL": "URL",
        "CHECK": "チェック",
        "NAME": "ユーザー名",
        "ID": "ID",
        "PASSWORD": "Password",

        "POST_COMPLETE_DATE": "最新実施日時",
        "ERROR_DATETIME": "エラー日時",
        "ERROR_COMMENT": "エラー理由",

        # 選択する
        "CHOICE_COL": ["LINE友だちID", "LINE登録名"],
        "LINE_FRIEND_ID": "LINE友だちID",
        "LINE_NAME": "LINE登録名",
        "SIGN_UP_DATE": "登録日",

        "DRIVE_PARENTS_URL": "https://drive.google.com/drive/folders/17m3IFY35w-QWcwn39cM8BEAk7qWQwVts",
    }


# ----------------------------------------------------------------------------------
# ログイン情報


class LoginInfo(Enum):

    INSTA = {
        "LOGIN_URL": "https://www.instagram.com/",
        "HOME_URL": "",
        "EXPLORE_URL": "https://www.instagram.com/mon_guchi/p/DHipkplzBpR/",
        "ID_BY": "name",
        "ID_VALUE": "username",
        "PASS_BY": "name",
        "PASS_VALUE": "password",
        "BTN_BY": "xpath",
        "BTN_VALUE": "//button[.//div[text()='ログイン']]",
        "LOGIN_AFTER_ELEMENT_BY": "xpath",
        "LOGIN_AFTER_ELEMENT_VALUE": "//li[contains(@class, 'sidebar-item') and .//a[contains(text(), 'フォロワー分析')]]",

        # 入力
        "ID_INPUT_TEXT": os.getenv("INSTA_ID"),
        "PASS_INPUT_TEXT": os.getenv("INSTA_PASS"),

    }


# ----------------------------------------------------------------------------------


class ErrCommentInfo(Enum):

    INSTA = {

        # POPUP_TITLE
        "POPUP_TITLE_SHEET_INPUT_ERR": "スプレッドシートをご確認ください。",
        "POPUP_TITLE_FACEBOOK_LOGIN_ERR": "ログインが必要です",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
    }


# ----------------------------------------------------------------------------------


class PopUpComment(Enum):
    INSTA = {
        "": "",
        "": "",
        "": "",
    }


# ----------------------------------------------------------------------------------


class FollowerAnalysisElement(Enum):
    INSTA = {
        "ZIP_FILE_HEAD_NAME": "Instagramマイアカウント フォロワー分析",
        "ZIP_EXTENSION": ".zip",
        "CSV_FILE_HEAD_NAME": "フォロワーチャート",
        "CSV_EXTENSION": ".csv",
        "DOWNLOAD_DIR_NAME": "downloads",
        "UPLOAD_DIR_NAME": "uploads_to_google_drive",

        "ANALYSIS_BY": "",
        "ANALYSIS_VOL": "//a[contains(text(), 'フォロワー分析')]",
        "BULK_DOWNLOAD_BTN_BY": "",
        "BULK_DOWNLOAD_BTN_VOL": "//button[.//span[contains(text(), '一括DL')]]",
        "": "",
        "": "",
    }


# ----------------------------------------------------------------------------------


class EngagementAnalysisElement(Enum):
    INSTA = {
        "ZIP_FILE_HEAD_NAME": "Instagramマイアカウント エンゲージメント分析",

        "ZIP_EXTENSION": ".zip",
        "CSV_FILE_HEAD_FIRST_NAME": "エンゲージメントの推移",
        "CSV_FILE_HEAD_SECOND_NAME": "プロフィールインサイトチャート",

        "CSV_EXTENSION": ".csv",
        "DOWNLOAD_DIR_NAME": "downloads",
        "UPLOAD_DIR_NAME": "uploads_to_google_drive",

        "ANALYSIS_BY": "",
        "ANALYSIS_VOL": "//a[contains(text(), 'エンゲージメント分析')]",
        "BULK_DOWNLOAD_BTN_BY": "",
        "BULK_DOWNLOAD_BTN_VOL": "//button[.//span[contains(text(), '一括DL')]]",
        "": "",
        "": "",
    }


# ----------------------------------------------------------------------------------


class PostAnalysisElement(Enum):
    INSTA = {
        "ZIP_FILE_HEAD_NAME": "Instagramマイアカウント 投稿一覧",
        "ZIP_EXTENSION": ".zip",
        "CSV_FILE_HEAD_NAME": "インサイト投稿一覧",
        "CSV_EXTENSION": ".csv",
        "DOWNLOAD_DIR_NAME": "downloads",
        "UPLOAD_DIR_NAME": "uploads_to_google_drive",

        "ANALYSIS_BY": "",
        "ANALYSIS_VOL": "//a[contains(text(), '投稿一覧')]",
        "BULK_DOWNLOAD_BTN_BY": "",
        "BULK_DOWNLOAD_BTN_VOL": "//button[.//span[contains(text(), '一括DL')]]",
        "": "",
        "": "",
    }


# ----------------------------------------------------------------------------------


class StoriesAnalysisElement(Enum):
    INSTA = {
        "ZIP_FILE_HEAD_NAME": "Instagramマイアカウント ストーリーズ分析",
        "ZIP_EXTENSION": ".zip",
        "CSV_FILE_HEAD_NAME": "ストーリーズ投稿一覧",
        "CSV_EXTENSION": ".csv",
        "DOWNLOAD_DIR_NAME": "downloads",
        "UPLOAD_DIR_NAME": "uploads_to_google_drive",

        "ANALYSIS_BY": "",
        "ANALYSIS_VOL": "//a[contains(text(), 'ストーリーズ分析')]",
        "BULK_DOWNLOAD_BTN_BY": "",
        "BULK_DOWNLOAD_BTN_VOL": "//button[.//span[contains(text(), '一括DL')]]",
        "": "",
        "": "",
    }


# ----------------------------------------------------------------------------------

class Element(Enum):
    INSTA = {

        "by_1": 'xpath',
        "value_1": '//a[.//span[text()="検索"]]',
        "by_2": "xpath",
        "value_2": '//input[@aria-label="検索語句"]',
        "TEST_USERNAME": "mon_guchi",
        "by_3": "xpath",
        "value_3": '(//div[contains(@style, "flex-direction: column")]//a[@role="link"])[1]',
        "by_4": "xpath",
        "value_4": "//time",
        "by_5": "xpath",
        "value_5": '//span[contains(text(), "いいね！")]',
        "value_6": '//button//*[name()="svg"][@aria-label="次へ"]',
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",

    }

# ----------------------------------------------------------------------------------


