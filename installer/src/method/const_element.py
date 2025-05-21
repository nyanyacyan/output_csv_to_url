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

    OUTPUT_CSV = {
        "JSON_KEY_NAME": "sns-auto-430920-08274ad68b41.json",
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
