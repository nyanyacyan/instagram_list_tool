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
        "JSON_KEY_NAME": "western-well-396401-82d68890d8e2.json",
        "SHEET_URL": "https://docs.google.com/spreadsheets/d/1g7ycnDup8DYweQA7J1y7yT-ADrsvWSjw8ILQVdYcBEo/edit?gid=931453217#gid=931453217",
        "TARGET_WORKSHEET_NAME": "ターゲットリスト",
        "ACCOUNT_WORKSHEET_NAME": "アカウント",
        "WORKSHEET_NAME": "ターゲットリスト",

        # account
        "ACCOUNT_ID": "ID",
        "ACCOUNT_PASS": "Pass",
        "POST_COMPLETE_DATE": "最新実施日時",
        "ERROR_DATETIME": "エラー日時",
        "ERROR_COMMENT": "エラー理由",


        # column名
        "CHECK": "チェック",

        "NAME": "ユーザー名",
        "TARGET_USER_URL": "アカウントURL",
        "TARGET_WORKSHEET_URL": "出力先",
        "TARGET_COLUMN_WORKSHEET_NAME": "worksheet名",

        # target_worksheetのcolumn名
        "TARGET_INPUT_USERNAME": "ユーザー名",
        "TARGET_INPUT_USER_URL": "URL",
        "TARGET_INPUT_TYPE": "コメント or いいね",
        "TARGET_INPUT_DATE": "追加日",
        "START_DAYTIME": "取得開始日時",
        "END_DAYTIME": "取得終了日時",
        "RUNNING_DATE": "実施日時",
        "WRITE_ERROR": "エラー",

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
        "POPUP_TITLE_SHEET_CHECK": "スプレッドシートのチェックされている項目がありません",
        "POPUP_TITLE_SHEET_START_DATE": "対象の「取得開始日時」の欄が入力されてないです。",
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
        "POPUP_COMPLETE_TITLE": "処理完了",
        "POPUP_COMPLETE_MSG": "正常に処理が完了しました。",
        "": "",
    }


# ----------------------------------------------------------------------------------

class CommentFlowElement(Enum):
    INSTA = {
        "GSS_COLUMN_NAME": "コメント or いいね",
        "INPUT_WORD_COMMENT": "コメント",
        "INPUT_WORD_GOOD": "いいね",

    }


# ----------------------------------------------------------------------------------

class Element(Enum):
    INSTA = {

        "by_1": 'xpath',
        "value_1": '//a[.//span[text()="検索"]]',
        "TEST_USERNAME": "mon_guchi",

        # ピン留めされた要素の取得
        "by_2": "css",
        "value_2": 'svg[aria-label="ピン留めされた投稿のアイコン"]',

        # 最初の投稿の取得
        "value_3": '(//div[contains(@style, "flex-direction: column")]//a[@role="link"])[1]',

        # 日付要素
        "by_4": "xpath",
        "value_4": "//time",

        # いいねボタン
        "by_5": "xpath",
        "value_5": "//a[contains(@href, '/liked_by/') and @role='link']",

        # いいねのuserリストの取得
        "value_6": '//div[@role="dialog"]//div[contains(@style, "overflow")]',


        # 次への要素
        "value_7": '//button//*[name()="svg"][@aria-label="次へ"]',

        # コメントユーザー要素
        "by_12": "tag",
        "value_12": 'ul',
        "by_13": "tag",
        "value_13": 'li',
        "by_14": "tag",
        "value_14": 'h3',
        "by_15": "tag",
        "value_15": 'a',


        # いいねのmodal要素
        "value_9": '//div[@role="dialog"]//div[contains(@style, "overflow")]',
        "value_10": './/a[starts-with(@href, "/") and string-length(@href) > 1]',
        "value_11": './/a[starts-with(@href, "/") and string-length(@href) > 1]',

        # いいねのクリックがその他の場合の要素
        "value_16": '//a[span[text()="その他"] and contains(@href, "liked_by")]',
        "": "",
        "": "",

    }

# ----------------------------------------------------------------------------------


