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

class GUIInfo(Enum):
    OUTPUT_CSV = {
        "WINDOW_TITLE": "NNA_SITE_CSV_tool",
        "WINDOW_WIDTH": 445,
        "WINDOW_HEIGHT": 260,
        "WINDOW_PADDING": (10, 20, 0, 10),
        "WINDOW_POSITION_X": 0,
        "WINDOW_POSITION_Y": 0,
        "WINDOW_RESIZE": False,
    }

# ----------------------------------------------------------------------------------
# ログイン情報


class LoginInfo(Enum):

    OUTPUT_CSV = {
        "LOGIN_URL": "https://www.nna.jp/login?redirect_url=/",
        "HOME_URL": "",
        "EXPLORE_URL": "https://www.OUTPUT_CSVgram.com/mon_guchi/p/DHipkplzBpR/",
        "ID_BY": "id",
        "ID_VALUE": "user_code",
        "PASS_BY": "id",
        "PASS_VALUE": "password",
        "BTN_BY": "xpath",
        "BTN_VALUE": "//button[@label='ログイン']",
        "LOGIN_AFTER_ELEMENT_BY": "xpath",
        "LOGIN_AFTER_ELEMENT_VALUE": '//button[.//span[text()="はい"]]',

        # 入力
        "ID_INPUT_TEXT": os.getenv("SITE_ID"),
        "PASS_INPUT_TEXT": os.getenv("SITE_PASS"),

    }


# ----------------------------------------------------------------------------------


class ErrCommentInfo(Enum):

    OUTPUT_CSV = {

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
    OUTPUT_CSV = {
        "POPUP_COMPLETE_TITLE": "処理完了",
        "POPUP_COMPLETE_MSG": "正常に処理が完了しました。",
        "": "",
    }


# ----------------------------------------------------------------------------------

class CommentFlowElement(Enum):
    OUTPUT_CSV = {
        "GSS_COLUMN_NAME": "コメント or いいね",
        "INPUT_WORD_COMMENT": "コメント",
        "INPUT_WORD_GOOD": "いいね",

    }


# ----------------------------------------------------------------------------------

class Element(Enum):
    OUTPUT_CSV = {
        # ログイン移行画面の際にクリックする要素
        "LOGIN_TRANSFER_ID": "xpath",
        "LOGIN_TRANSFER_VALUE": '//button[.//span[text()="はい"]]',

        # main要素の取得
        "BY_MAIN": 'tag',
        "VALUE_MAIN": 'main',

        # li要素の取得
        "by_0": 'tag',
        "value_0": 'ul',

        # li要素の取得
        "by_1": 'tag',
        "value_1": 'li',

        # 国名の取得
        "value_2": '//a[@class="tag--country"]',

        # 記事名の取得
        "by_3": "tag",
        "value_3": 'h2',

        # URLの取得
        "by_4": "tag",
        "value_4": 'a',

    }

# ----------------------------------------------------------------------------------


class CsvInfo(Enum):
    OUTPUT_CSV = {
        "COL_NAME":  '["国名", "タイトル", "URL"]',
        "": "",


    }
