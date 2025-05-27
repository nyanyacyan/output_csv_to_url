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
        "WINDOW_WIDTH": 600,
        "WINDOW_HEIGHT": 240,
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
        "HOME_URL": "https://www.nna.jp/",
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

        # 詳細検索の要素
        "DETAIL_SEARCH_VALUE": '//span[text()="詳細検索"]',


        # 詳細検索部分
        "KEYWORD_VALUE": '//input[@placeholder="キーワードを入力"]',
        "TIME_LIMIT_VALUE_1": "",
        "COUNTRY_VALUE_1": "",
        "INDUSTRY_VALUE_1": "",
        "TARGET_SEARCH_VALUE_1": "",
        "SEARCH_BTN_VALUE": "",


        # モーダル選択
        "TIME_LIMIT_VALUE_2": "",
        "COUNTRY_VALUE_2": "",
        "INDUSTRY_VALUE_2": "",
        "TARGET_SEARCH_VALUE_2": "",


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
        "value_2": './/a[@class="tag--country"]',

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

# ----------------------------------------------------------------------------------


class KeyWordInfo(Enum):
    # 期間
    TIME_LIMIT = {
        "SELECT_WORD": "１日以内",
        "SELECT_VALUE": "today",
    }

    # アジア渡航・交通情報①
    ASIA_TRANSPORT = "ビザ"

    # 日系自動車メーカーの動向
    JA_AUTO = "トヨタ or ホンダ or スズキ or 日産 or 三菱自動車 or マツダ or ダイハツ or SUBARU or 日野自動車 or いすゞ or 三菱ふそう"

    # TRUMP関税で揺れるアジア
    TRUMP = "トランプ"

    # 中国EVの世界戦略
    CHINA_EV = "中国 EV"

    # 韓国の政局混迷
    KOREA = "尹"

    # アジアを支える鉄道輸送
    ASIA_TRAIN = "鉄道"


# ----------------------------------------------------------------------------------

class CountryInfo(Enum):
    # 日系自動車メーカーの動向
    JA_AUTO = {
        "タイ": "country_11",
        "ベトナム": "country_4",
        "ミャンマー": "country_69",
        "カンボジア": "country_71",
        "ラオス": "country_70",
        "マレーシア": "country_8",
        "シンガポール": "country_10",
        "インドネシア": "country_5",
        "フィリピン": "country_9",
        "ブルネイ": "country_77",
        "東ティモール": "country_103",
        "中国": "country_2",
        "香港": "country_3",
        "マカオ": "country_72",
        "台湾": "country_12",
        "韓国": "country_7",
        "北朝鮮": "country_73",
        "モンゴル": "country_102",
        "日本": "country_6",
        "インド": "country_68",
        "パキスタン": "country_78",
        "アフガニスタン": "country_79",
        "バングラデシュ": "country_80",
        "スリランカ": "country_81",
        "ネパール": "country_82",
        "ブータン": "country_83",
        "モルディブ": "country_84",
    }
    # 韓国の政局混迷
    KOREA = {
        "韓国": "country_7",
    }

    # アジアを支える鉄道輸送
    ASIA_TRAIN = {
        "中国": "country_2",
        "香港": "country_3",
        "マカオ": "country_4",
        "台湾": "country_5",
        "韓国": "country_6",
        "タイ": "country_7",
        "ベトナム": "country_8",
        "ミャンマー": "country_9",
        "カンボジア": "country_10",
        "ラオス": "country_11",
        "マレーシア": "country_12",
        "シンガポール": "country_13",
        "インドネシア": "country_14",
        "フィリピン": "country_15",
        "ブルネイ": "country_16",
        "東ティモール": "country_17",
        "インド": "country_18",
        "スリランカ": "country_19",
        "バングラデシュ": "country_20",
        "パキスタン": "country_21",
    }


# ----------------------------------------------------------------------------------

class CategoryDetailInfo(Enum):
    # アジア渡航・交通情報②
    ASIA_TRANSPORT = {
        "陸運": "category_detail.32",
        "海運": "category_detail.33",
        "空運": "category_detail.34",
        "観光": "category_detail.92",
    }

    # 中国EVの世界戦略
    CHINA_EV = {
        "自動車": "category_detail.6",
    }

    # 韓国の政局混迷
    KOREA = {
        "政治一般": "category_detail.69",
        "外交": "category_detail.75",
        "選挙": "category_detail.73",
        "軍事": "category_detail.72",
    }

    # アジアを支える鉄道輸送
    ASIA_TRAIN = {
        "陸運": "category_detail.32",
    }

    # 日系製造業のアジア進出
    JA_ASIA_ENTRY = {
        "自動車": "category_detail.6",
        "二輪車": "category_detail.7",
        "車部品": "category_detail.77",
        "電機": "category_detail.16",
        "保健医療": "category_detail.19",
        "医薬品": "category_detail.20",
        "化学一般": "category_detail.21",
        "バイオ": "category_detail.22",
        "繊維": "category_detail.23",
        "鉄鋼・金属": "category_detail.24",
        "宝石・宝飾品": "category_detail.25",
        "精密機器": "category_detail.27",
        "ゴム・皮革": "category_detail.28",
        "紙・パルプ": "category_detail.29",
        "機械": "category_detail.30",
        "ガラス・セメント": "category_detail.31",
        "その他製造": "category_detail.26",
        "石油・石炭・ガス": "category_detail.35",
        "鉱業": "category_detail.36",
    }

# ----------------------------------------------------------------------------------

class TargetSearchInfo(Enum):
    # 日系製造業のアジア進出
    JA_ASIA_ENTRY = {
        "日系企業進出": "tag_from_japan",
    }
