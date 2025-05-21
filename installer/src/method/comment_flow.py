# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/utage_csv_to_gss/installer/src"
# export PYTHONPATH="/Users/nyanyacyan/Desktop/Project_file/utage_csv_to_drive/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import pandas as pd
from typing import List
from datetime import datetime
from selenium.webdriver.chrome.webdriver import WebDriver

# 自作モジュール
from method.base.utils.logger import Logger
from method.base.decorators.decorators import Decorators
from method.base.spreadsheet.spreadsheetWrite import GssWrite
from method.base.spreadsheet.err_checker_write import GssCheckerErrWrite
from method.base.utils.logger import Logger
from method.base.selenium.seleniumBase import SeleniumBasicOperations
from method.base.selenium.get_element import GetElement
from method.base.decorators.decorators import Decorators
from method.base.spreadsheet.spreadsheetWrite import GssWrite
from method.base.spreadsheet.err_checker_write import GssCheckerErrWrite
from method.get_gss_df_flow import GetGssDfFlow

# const
from method.const_element import GssInfo, PopUpComment, Element, CommentFlowElement

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

        # タイムスタンプ
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        # const
        self.const_gss_info = GssInfo.INSTA.value
        self.popup_cmt = PopUpComment.INSTA.value
        self.const_element = Element.INSTA.value
        self.const_comment = CommentFlowElement.INSTA.value

        # インスタンス
        self.random_sleep = SeleniumBasicOperations(chrome=chrome)
        self.get_element = GetElement(chrome=chrome)
        self.gss_write = GssWrite()
        self.gss_check_err_write = GssCheckerErrWrite()
        self.get_gss_df_flow = GetGssDfFlow()

    ####################################################################################
    #! ----------------------------------------------------------------------------------
    # 書込データをスプシに書き込む

    def process(self, target_worksheet_name: str):
        try:
            # 書込データを取得
            filtered_write_data, target_df = self._get_filtered_write_data(target_worksheet_name=target_worksheet_name)

            # 書込データをDataFrameに変換
            filtered_write_data = pd.DataFrame(filtered_write_data)
            self.logger.debug(f"書込データ: {filtered_write_data}")

            # 書込データが空の場合
            if filtered_write_data.empty:
                self.logger.error("コメントの書込データが空です")
                return None

            # target_dfがある場合
            if target_df is None or target_df.empty:
                # もしtarget_dfがない場合
                self.logger.warning(f"既存データなし")
                None_row_num = 2
            else:
                self.logger.debug(f"既存データあり: {len(target_df)}")
                row_num = len(target_df)
                self.logger.debug(f"書込データの行数: {row_num}")
                None_row_num = row_num + 2

            end_row_num = None_row_num + len(filtered_write_data) + 1
            self.logger.debug(f"書込データの行数: {len(filtered_write_data)}")
            self.logger.debug(f"書込データの行数: {None_row_num} 行目から {end_row_num} 行目に書き込みます。")

            cell = f"A{None_row_num}:D{end_row_num}"
            self.logger.debug(f"書込データのセル: {cell}")
            self.logger.debug(f"書込データ: {target_worksheet_name} の {cell} 行目に書き込みます。")

            # 書込データのDataFrameをGSSへ書き込むためにリスト型に変換
            gss_write_list = filtered_write_data.values.tolist()
            self.logger.debug(f"書込データリスト: {gss_write_list}")

            # GSSへ書込
            self.gss_write.write_input_worksheet( gss_info=self.const_gss_info, worksheet_name=target_worksheet_name, cell=cell, input_data=gss_write_list )
            self.logger.debug(f"書込データ: {target_worksheet_name} の {cell} 行目に書き込みました。")

            self.logger.info(f"コメントユーザーをスプシに書込完了（全{len(filtered_write_data)}行）")
            return filtered_write_data

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)

    #! ----------------------------------------------------------------------------------
    # 既存のユーザー名を取得し、書込データをフィルタリングする

    def _get_filtered_write_data(self, target_worksheet_name: str):
        try:
            # 書込データを生成
            write_data = self._generate_write_data()

            # 既存のユーザー名リストを取得
            existing_username_list, target_df = self._get_written_username_list(target_worksheet_name=target_worksheet_name)
            self.logger.debug(f"既存のユーザー名リスト: {existing_username_list}")

            # 空の場合の処理
            if existing_username_list is None:
                self.logger.warning("スプレッドシートが初期状態です")
                return write_data, None

            # 既に書込済みのユーザー名を除外する
            filtered_write_data = []
            for data in write_data:
                # ユーザー名が既存のユーザー名リストに含まれていない場合
                if data['username'] not in existing_username_list:
                    filtered_write_data.append(data)
                    self.logger.info(f"フィルタリング対象: {data['username']}")
                else:
                    self.logger.warning(f"フィルタリング除外: {data['username']}")

            self.logger.debug(f"フィルタリング後の書込データ: {filtered_write_data}")
            return filtered_write_data, target_df

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)

    # ----------------------------------------------------------------------------------

    def _get_written_username_list(self, target_worksheet_name: str):
        try:
            # 対象のWorksheetの現在のDataFrameを取得
            target_df = self.get_gss_df_flow.no_filter_process(worksheet_name=target_worksheet_name)

            # DataFrameが空か確認（空ならNoneで返す）
            if target_df is None or target_df.empty:
                self.logger.warning(f"{target_worksheet_name} のスプシが初期状態です。")
                return None, None

            self.logger.debug(f"{target_worksheet_name}の入力前df: {target_df.head()}")

            username_series = target_df[self.const_gss_info['TARGET_INPUT_USERNAME']]
            self.logger.debug(f"ユーザー名のSeries: {username_series}")

            # シリーズの値をリストに変換
            existing_username_list = username_series.tolist()
            self.logger.debug(f"ユーザー名のリスト: {existing_username_list}")

            return existing_username_list, target_df

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)

    # ----------------------------------------------------------------------------------
    # 各メソッドをまとめる

    def _generate_write_data(self) -> List[dict]:
        try:
            # コメントユーザー要素のリストを取得
            user_urls =self._get_comment_user_url()

            if not user_urls:
                return []

            # 重複を除外する
            unique_checker = set()
            write_data = []
            for user_url in user_urls:
                self.logger.debug(f"ユーザーURL: {user_url}")

                # ユーザー名を取得
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
                    self.logger.warning(f"ユーザー名: {comment_username} を追加します。")
                    write_data.append(comment_dict_data)
                else:
                    # 重複している場合は、スキップする
                    self.logger.debug(f"重複ユーザー名: {comment_username} は既在するため、スキップします")

            self.logger.debug(f"書込データ: {write_data}")
            return write_data

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)

    # ----------------------------------------------------------------------------------
    # コメントユーザーurlを取得する

    def _get_comment_user_url(self):
        try:
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

                    # 週間前、時間前、日前のいずれかが含まれていて、返信が含まれている場合
                    li_text = li.text
                    if ("週間前" in li_text or "時間前" in li_text or "日前" in li_text or "分前" in li_text) and "返信" in li_text:
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

            if not filter_user_url:
                self.logger.warning("フィルタリング後のユーザーURLリストが空です。")
                return []

            for user_url in filter_user_url:
                self.logger.debug(f"ユーザーURL: {user_url}")
            self.logger.debug(f"フィルタリング後のユーザーURLリスト: {filter_user_url} {len(filter_user_url)}件")
            return filter_user_url

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} コメントがありません {e}" )
            self.logger.error(process_error_comment)


    # ----------------------------------------------------------------------------------
    # InstagramのユーザーURLからユーザー名を取得する

    def _get_comment_user_name(self, user_url: str):
        # URL部分を除去してユーザー名を取得
        username = user_url.replace("https://www.instagram.com/", "").strip("/")
        self.logger.debug(f"ユーザー名: {username}")
        return username

    # ----------------------------------------------------------------------------------

